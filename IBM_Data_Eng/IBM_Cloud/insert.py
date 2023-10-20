import pymongo
import json

# Connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Modify the connection string as needed
db = client["entertainment"]  # Specify your database name
collection = db["movies"]  # Specify your collection name

# Read the JSON file
with open("/home/erodesk/Git/briefcase/IBM_Cloud/movies2222.json", "r") as file:  # Replace "movies.json" with your file path
    movies_data = json.load(file)

# Insert documents from the JSON data
collection.insert_many(movies_data)

# Close the MongoDB connection
client.close()