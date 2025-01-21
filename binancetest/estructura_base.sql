--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: btc_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.btc_data (
    id integer NOT NULL,
    pair_id integer,
    "timestamp" timestamp without time zone NOT NULL,
    open numeric(30,8),
    high numeric(30,8),
    low numeric(30,8),
    close numeric(30,8),
    volume numeric(30,8),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    symbol character varying(50)
);


--
-- Name: btc_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.btc_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: btc_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.btc_data_id_seq OWNED BY public.btc_data.id;


--
-- Name: btc_pairs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.btc_pairs (
    id integer NOT NULL,
    base_currency_id integer,
    quote_currency_id integer,
    symbol character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: btc_pairs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.btc_pairs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: btc_pairs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.btc_pairs_id_seq OWNED BY public.btc_pairs.id;


--
-- Name: cryptocurrencies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cryptocurrencies (
    id integer NOT NULL,
    symbol character varying(20) NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: cryptocurrencies_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cryptocurrencies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cryptocurrencies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cryptocurrencies_id_seq OWNED BY public.cryptocurrencies.id;


--
-- Name: eth_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.eth_data (
    id integer NOT NULL,
    pair_id integer,
    "timestamp" timestamp without time zone NOT NULL,
    open numeric(30,8),
    high numeric(30,8),
    low numeric(30,8),
    close numeric(30,8),
    volume numeric(30,8),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    symbol character varying(50)
);


--
-- Name: eth_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.eth_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: eth_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.eth_data_id_seq OWNED BY public.eth_data.id;


--
-- Name: eth_pairs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.eth_pairs (
    id integer NOT NULL,
    base_currency_id integer,
    quote_currency_id integer,
    symbol character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: eth_pairs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.eth_pairs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: eth_pairs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.eth_pairs_id_seq OWNED BY public.eth_pairs.id;


--
-- Name: usdt_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usdt_data (
    id integer NOT NULL,
    pair_id integer,
    "timestamp" timestamp without time zone NOT NULL,
    open numeric(30,8),
    high numeric(30,8),
    low numeric(30,8),
    close numeric(30,8),
    volume numeric(30,8),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    symbol character varying(50)
);


--
-- Name: usdt_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usdt_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usdt_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usdt_data_id_seq OWNED BY public.usdt_data.id;


--
-- Name: usdt_pairs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usdt_pairs (
    id integer NOT NULL,
    base_currency_id integer,
    quote_currency_id integer,
    symbol character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: usdt_pairs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usdt_pairs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usdt_pairs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usdt_pairs_id_seq OWNED BY public.usdt_pairs.id;


--
-- Name: btc_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_data ALTER COLUMN id SET DEFAULT nextval('public.btc_data_id_seq'::regclass);


--
-- Name: btc_pairs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_pairs ALTER COLUMN id SET DEFAULT nextval('public.btc_pairs_id_seq'::regclass);


--
-- Name: cryptocurrencies id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cryptocurrencies ALTER COLUMN id SET DEFAULT nextval('public.cryptocurrencies_id_seq'::regclass);


--
-- Name: eth_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eth_data ALTER COLUMN id SET DEFAULT nextval('public.eth_data_id_seq'::regclass);


--
-- Name: eth_pairs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eth_pairs ALTER COLUMN id SET DEFAULT nextval('public.eth_pairs_id_seq'::regclass);


--
-- Name: usdt_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usdt_data ALTER COLUMN id SET DEFAULT nextval('public.usdt_data_id_seq'::regclass);


--
-- Name: usdt_pairs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usdt_pairs ALTER COLUMN id SET DEFAULT nextval('public.usdt_pairs_id_seq'::regclass);


--
-- Name: btc_data btc_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_data
    ADD CONSTRAINT btc_data_pkey PRIMARY KEY (id);


--
-- Name: btc_pairs btc_pairs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_pairs
    ADD CONSTRAINT btc_pairs_pkey PRIMARY KEY (id);


--
-- Name: btc_pairs btc_pairs_symbol_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_pairs
    ADD CONSTRAINT btc_pairs_symbol_key UNIQUE (symbol);


--
-- Name: cryptocurrencies cryptocurrencies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cryptocurrencies
    ADD CONSTRAINT cryptocurrencies_pkey PRIMARY KEY (id);


--
-- Name: cryptocurrencies cryptocurrencies_symbol_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cryptocurrencies
    ADD CONSTRAINT cryptocurrencies_symbol_key UNIQUE (symbol);


--
-- Name: eth_data eth_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eth_data
    ADD CONSTRAINT eth_data_pkey PRIMARY KEY (id);


--
-- Name: eth_pairs eth_pairs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eth_pairs
    ADD CONSTRAINT eth_pairs_pkey PRIMARY KEY (id);


--
-- Name: eth_pairs eth_pairs_symbol_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eth_pairs
    ADD CONSTRAINT eth_pairs_symbol_key UNIQUE (symbol);


--
-- Name: btc_data unique_pair_timestamp; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_data
    ADD CONSTRAINT unique_pair_timestamp UNIQUE (pair_id, "timestamp");


--
-- Name: btc_data unique_symbol_timestamp_btc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_data
    ADD CONSTRAINT unique_symbol_timestamp_btc UNIQUE (pair_id, "timestamp");


--
-- Name: eth_data unique_symbol_timestamp_eth; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eth_data
    ADD CONSTRAINT unique_symbol_timestamp_eth UNIQUE (pair_id, "timestamp");


--
-- Name: usdt_data unique_symbol_timestamp_usdt; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usdt_data
    ADD CONSTRAINT unique_symbol_timestamp_usdt UNIQUE (pair_id, "timestamp");


--
-- Name: usdt_data usdt_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usdt_data
    ADD CONSTRAINT usdt_data_pkey PRIMARY KEY (id);


--
-- Name: usdt_pairs usdt_pairs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usdt_pairs
    ADD CONSTRAINT usdt_pairs_pkey PRIMARY KEY (id);


--
-- Name: usdt_pairs usdt_pairs_symbol_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usdt_pairs
    ADD CONSTRAINT usdt_pairs_symbol_key UNIQUE (symbol);


--
-- Name: idx_btc_data_pair_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_btc_data_pair_id ON public.btc_data USING btree (pair_id);


--
-- Name: idx_btc_data_timestamp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_btc_data_timestamp ON public.btc_data USING btree ("timestamp");


--
-- Name: idx_eth_data_pair_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_eth_data_pair_id ON public.eth_data USING btree (pair_id);


--
-- Name: idx_eth_data_timestamp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_eth_data_timestamp ON public.eth_data USING btree ("timestamp");


--
-- Name: idx_usdt_data_pair_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_usdt_data_pair_id ON public.usdt_data USING btree (pair_id);


--
-- Name: idx_usdt_data_timestamp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_usdt_data_timestamp ON public.usdt_data USING btree ("timestamp");


--
-- Name: btc_pairs btc_pairs_base_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_pairs
    ADD CONSTRAINT btc_pairs_base_currency_id_fkey FOREIGN KEY (base_currency_id) REFERENCES public.cryptocurrencies(id);


--
-- Name: btc_pairs btc_pairs_quote_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.btc_pairs
    ADD CONSTRAINT btc_pairs_quote_currency_id_fkey FOREIGN KEY (quote_currency_id) REFERENCES public.cryptocurrencies(id);


--
-- Name: eth_pairs eth_pairs_base_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eth_pairs
    ADD CONSTRAINT eth_pairs_base_currency_id_fkey FOREIGN KEY (base_currency_id) REFERENCES public.cryptocurrencies(id);


--
-- Name: eth_pairs eth_pairs_quote_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eth_pairs
    ADD CONSTRAINT eth_pairs_quote_currency_id_fkey FOREIGN KEY (quote_currency_id) REFERENCES public.cryptocurrencies(id);


--
-- Name: usdt_pairs usdt_pairs_base_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usdt_pairs
    ADD CONSTRAINT usdt_pairs_base_currency_id_fkey FOREIGN KEY (base_currency_id) REFERENCES public.cryptocurrencies(id);


--
-- Name: usdt_pairs usdt_pairs_quote_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usdt_pairs
    ADD CONSTRAINT usdt_pairs_quote_currency_id_fkey FOREIGN KEY (quote_currency_id) REFERENCES public.cryptocurrencies(id);


--
-- PostgreSQL database dump complete
--

