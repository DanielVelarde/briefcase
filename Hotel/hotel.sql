-- Crear la base de datos
CREATE DATABASE hotel_management;

-- Conectar a la base de datos
\c hotel_management;

-- Tablas principales
CREATE TABLE pais (
    idpais SERIAL PRIMARY KEY,
    nomepais VARCHAR(100) NOT NULL
);

CREATE TABLE estado (
    idestado SERIAL PRIMARY KEY,
    nomeestado VARCHAR(100) NOT NULL,
    idpais INT REFERENCES pais(idpais)
);

CREATE TABLE cidades (
    idcidades SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idestado INT REFERENCES estado(idestado)
);

CREATE TABLE endpess (
    idendereco SERIAL PRIMARY KEY,
    logradouro VARCHAR(200),
    numero VARCHAR(20),
    bairro VARCHAR(100),
    cep VARCHAR(10),
    idcidades INT REFERENCES cidades(idcidades)
);

CREATE TABLE pessoa (
    idpessoa SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    razaosocial VARCHAR(200),
    numdocumento VARCHAR(20),
    email VARCHAR(100),
    idendresidencial INT REFERENCES endpess(idendereco),
    idendcomercial INT REFERENCES endpess(idendereco)
);

CREATE TABLE tipohospede (
    idtipohospede SERIAL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE hotel (
    idhotel SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL
);

CREATE TABLE reservasfront (
    idreservasfront SERIAL PRIMARY KEY,
    idhotel INT REFERENCES hotel(idhotel),
    numreserva VARCHAR(50) NOT NULL,
    datareserva DATE NOT NULL,
    datachegadareal DATE,
    datachegprevista DATE,
    datapartidareal DATE,
    datapartprevista DATE,
    statusreserva INT,
    garantenoshow CHAR(1),
    observacoes TEXT,
    coduh VARCHAR(50),
    codsegmento VARCHAR(50),
    idtarifa INT,
    moecodigomanual VARCHAR(10),
    tipouhestadia INT,
    tipouhtarifa INT,
    idroomlist INT,
    idorigem INT,
    clientereservante INT REFERENCES pessoa(idpessoa),
    clientehospede INT REFERENCES pessoa(idpessoa),
    adultos INT,
    criancas1 INT,
    criancas2 INT,
    percdescontodiaria NUMERIC(5, 2),
    valordesconto NUMERIC(10, 2),
    vlrdiaria NUMERIC(10, 2),
    vlrdiariamanual NUMERIC(10, 2)
);

CREATE TABLE movimentohospedes (
    idmovimentohospedes SERIAL PRIMARY KEY,
    idreservasfront INT REFERENCES reservasfront(idreservasfront),
    idhospede INT REFERENCES pessoa(idpessoa),
    idtipohospede INT REFERENCES tipohospede(idtipohospede),
    principal CHAR(1)
);

CREATE TABLE tipouh (
    idtipouh SERIAL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    idgrupouh INT
);

CREATE TABLE grupouh (
    idgrupouh SERIAL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE uh (
    coduh VARCHAR(50) PRIMARY KEY,
    idhotel INT REFERENCES hotel(idhotel),
    idtipouh INT REFERENCES tipouh(idtipouh)
);

CREATE TABLE roomlistvhf (
    idroomlist SERIAL PRIMARY KEY,
    idreservagrupo INT,
    codacomodacao VARCHAR(50)
);

CREATE TABLE reservagrupo (
    idreservagrupo SERIAL PRIMARY KEY,
    idhotel INT REFERENCES hotel(idhotel),
    nomegrupo VARCHAR(200),
    codsegmento VARCHAR(50),
    idorigem INT,
    dataconfirmacao DATE,
    datacancelamento DATE,
    statusreserva INT
);

CREATE TABLE segmento (
    codsegmento VARCHAR(50) PRIMARY KEY,
    descricao VARCHAR(200) NOT NULL
);

CREATE TABLE origemreserva (
    idorigem SERIAL PRIMARY KEY,
    descricao VARCHAR(200) NOT NULL
);

CREATE TABLE tarifahotel (
    idtarifa SERIAL PRIMARY KEY,
    idhotel INT REFERENCES hotel(idhotel),
    descricao VARCHAR(200) NOT NULL,
    idgrupotarifa INT,
    moecodigo VARCHAR(10),
    codcategoria VARCHAR(50),
    datainicio DATE,
    datafinal DATE
);

CREATE TABLE moeda (
    moecodigo VARCHAR(10) PRIMARY KEY,
    moesigla VARCHAR(10) NOT NULL
);

CREATE TABLE lancamentosfront (
    idlancamento SERIAL PRIMARY KEY,
    idconta INT,
    datalancamento DATE NOT NULL,
    vlrlancamento NUMERIC(10, 2) NOT NULL,
    idtipodebcred INT
);

CREATE TABLE contasfront (
    idconta SERIAL PRIMARY KEY,
    idreservasfront INT REFERENCES reservasfront(idreservasfront)
);

CREATE TABLE tipodebcredhotel (
    idtipodebcred SERIAL PRIMARY KEY,
    descricao VARCHAR(200) NOT NULL,
    idhotel INT REFERENCES hotel(idhotel),
    idprincipal INT
);

CREATE TABLE paramhotel (
    idhotel INT REFERENCES hotel(idhotel),
    codcategtarbalcao VARCHAR(50),
    idtipodcdiaria INT,
    PRIMARY KEY (idhotel)
);

CREATE TABLE datasis (
    data DATE NOT NULL,
    idhotel INT REFERENCES hotel(idhotel),
    PRIMARY KEY (data, idhotel)
);

CREATE TABLE cotacaomoeda (
    idcotacaomoeda SERIAL PRIMARY KEY,
    moecodigo VARCHAR(10) REFERENCES moeda(moecodigo),
    cotdata DATE NOT NULL,
    cotvalor NUMERIC(10, 2) NOT NULL
);

-- Índices para optimización
CREATE INDEX idx_reservasfront_idhotel ON reservasfront(idhotel);
CREATE INDEX idx_movimentohospedes_idreservasfront ON movimentohospedes(idreservasfront);
CREATE INDEX idx_lancamentosfront_idconta ON lancamentosfront(idconta);
CREATE INDEX idx_tarifahotel_idhotel ON tarifahotel(idhotel);
CREATE INDEX idx_datasis_idhotel ON datasis(idhotel);