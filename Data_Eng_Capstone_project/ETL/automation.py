import ibm_db
import mysql.connector

# Connect to MySQL
mysql_connection = mysql.connector.connect(user='root', password='MjA3ODktZGFuaWVs', host='127.0.0.1', $

# Define the connection string for DB2
dsn_hostname = "*"
dsn_uid = "lvq13846"
dsn_pwd = "BKiPKr2SUwwxfmFG"
dsn_port = "30875"
dsn_database = "bludb"

def get_last_rowid():
    # Connect to DB2 using your variables
    conn_str = f"DATABASE={dsn_database};" \
               f"HOSTNAME={dsn_hostname};" \
               f"PORT={dsn_port};" \
               f"PROTOCOL=TCPIP;" \
               f"UID={dsn_uid};" \
               f"PWD={dsn_pwd};" \
               f"SECURITY=SSL;"
    conn = ibm_db.connect(conn_str, "", "")

    if conn:
        # Prepare and execute the SQL query to retrieve the last rowid
        sql = "SELECT MAX(rowid) FROM sales_data"
        stmt = ibm_db.exec_immediate(conn, sql)

        # Fetch the result
        result = ibm_db.fetch_assoc(stmt)

        # Check if the result is not empty and contains the '1' key
        if result and '1' in result:
            last_rowid = result['1']
        else:
            last_rowid = None

        # Return the last rowid
        return last_rowid
    else:
        return None

# Get the last rowid from DB2
last_rowid = get_last_rowid()
print(f"The last rowid in the sales_data table is: {last_rowid}")

def get_latest_records(rowid):
    cursor = mysql_connection.cursor()
    query = f"SELECT * FROM sales_data WHERE rowid > {rowid}"
    cursor.execute(query)
    records = cursor.fetchall()
    return records
# Get the latest records from MySQL
latest_records = get_latest_records(last_rowid)
for record in latest_records:
    print(record)

def insert_records(records):
    if not records:
        print("No records to insert")
        return

    # Connect to DB2 using your variables
    conn_str = f"DATABASE={dsn_database};" \
               f"HOSTNAME={dsn_hostname};" \
               f"PORT={dsn_port};" \
               f"PROTOCOL=TCPIP;" \
               f"UID={dsn_uid};" \
               f"PWD={dsn_pwd};" \    
               f"SECURITY=SSL;"
    conn = ibm_db.connect(conn_str, "", "")

    if conn:
        # Prepare and execute the INSERT statement for DB2
        insert_sql = "INSERT INTO sales_data (column1, column2, ...) VALUES (?, ?, ...)"
        stmt = ibm_db.prepare(conn, insert_sql)

        # Insert each record into DB2
        for record in records:
            params = record  # This assumes that the order of values matches the order in your INSERT s$
            if ibm_db.execute(stmt, params):
                print(f"Record inserted into DB2: {record}")
            else:
                print(f"Failed to insert record into DB2: {record}")
    else:
        print("Failed to connect to DB2")
# Insert the additional records from MySQL into DB2
insert_records(latest_records)
print("New rows inserted into production data warehouse =", len(latest_records))

# Disconnect from MySQL
mysql_connection.close()

# Disconnect from DB2
ibm_db.close(conn)

# End of program


