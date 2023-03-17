--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Ubuntu 14.4-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.5

-- Started on 2022-08-28 23:30:48

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

DROP DATABASE d2vvds8i9hqjdi;
--
-- TOC entry 4323 (class 1262 OID 339631166)
-- Name: d2vvds8i9hqjdi; Type: DATABASE; Schema: -; Owner: uhysseybzvygpe
--

CREATE DATABASE d2vvds8i9hqjdi WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.UTF-8';


ALTER DATABASE d2vvds8i9hqjdi OWNER TO uhysseybzvygpe;

\connect d2vvds8i9hqjdi

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

--
-- TOC entry 4325 (class 0 OID 0)
-- Name: d2vvds8i9hqjdi; Type: DATABASE PROPERTIES; Schema: -; Owner: uhysseybzvygpe
--

ALTER DATABASE d2vvds8i9hqjdi SET search_path TO '$user', 'public', 'heroku_ext';


\connect d2vvds8i9hqjdi

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

--
-- TOC entry 6 (class 2615 OID 404319393)
-- Name: heroku_ext; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA heroku_ext;


ALTER SCHEMA heroku_ext OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 339697646)
-- Name: parts; Type: TABLE; Schema: public; Owner: uhysseybzvygpe
--

CREATE TABLE public.parts (
    part_id integer NOT NULL,
    part_name character varying(255) NOT NULL
);


ALTER TABLE public.parts OWNER TO uhysseybzvygpe;

--
-- TOC entry 211 (class 1259 OID 339697670)
-- Name: parts_part_id_seq; Type: SEQUENCE; Schema: public; Owner: uhysseybzvygpe
--

CREATE SEQUENCE public.parts_part_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.parts_part_id_seq OWNER TO uhysseybzvygpe;

--
-- TOC entry 4329 (class 0 OID 0)
-- Dependencies: 211
-- Name: parts_part_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: uhysseybzvygpe
--

ALTER SEQUENCE public.parts_part_id_seq OWNED BY public.parts.part_id;


--
-- TOC entry 212 (class 1259 OID 339697727)
-- Name: users; Type: TABLE; Schema: public; Owner: uhysseybzvygpe
--

CREATE TABLE public.users (
    id SERIAL NOT NULL,
    user_id integer,
    balance real DEFAULT 100,
    is_game boolean,
    bet real,
    player_score integer,
    dealer_score integer,
    player_cards character varying,
    dealer_cards character varying,
    deck character varying DEFAULT false,
    user_name character varying(20),
    user_lastname character varying(20),
    lang character varying(2) DEFAULT 'ru'::character varying,
    games_played integer DEFAULT 0,
    games_won integer DEFAULT 0,
    games_lost integer DEFAULT 0,
    games_tied integer DEFAULT 0,
    last_played timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    user_nickname character varying(32),
    all_in_games_count smallint DEFAULT 0,
    max_win real DEFAULT 0,
    max_loss real DEFAULT 0,
    all_in_win smallint DEFAULT 0,
    all_in_loss smallint DEFAULT 0,
    is_all_in boolean DEFAULT false,
    all_in_tie smallint DEFAULT 0,
    blackjack_count integer DEFAULT 0
);


ALTER TABLE public.users OWNER TO uhysseybzvygpe;

--
-- TOC entry 213 (class 1259 OID 339697786)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: uhysseybzvygpe
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO uhysseybzvygpe;

--
-- TOC entry 4330 (class 0 OID 0)
-- Dependencies: 213
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: uhysseybzvygpe
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4157 (class 2604 OID 339697842)
-- Name: parts part_id; Type: DEFAULT; Schema: public; Owner: uhysseybzvygpe
--

ALTER TABLE ONLY public.parts ALTER COLUMN part_id SET DEFAULT nextval('public.parts_part_id_seq'::regclass);


--
-- TOC entry 4170 (class 2604 OID 339697865)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: uhysseybzvygpe
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4176 (class 2606 OID 339698125)
-- Name: parts parts_pkey; Type: CONSTRAINT; Schema: public; Owner: uhysseybzvygpe
--

ALTER TABLE ONLY public.parts
    ADD CONSTRAINT parts_pkey PRIMARY KEY (part_id);


--
-- TOC entry 4178 (class 2606 OID 339698157)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: uhysseybzvygpe
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4324 (class 0 OID 0)
-- Dependencies: 4323
-- Name: DATABASE d2vvds8i9hqjdi; Type: ACL; Schema: -; Owner: uhysseybzvygpe
--

REVOKE CONNECT,TEMPORARY ON DATABASE d2vvds8i9hqjdi FROM PUBLIC;


--
-- TOC entry 4326 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA heroku_ext; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA heroku_ext TO uhysseybzvygpe WITH GRANT OPTION;


--
-- TOC entry 4327 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: uhysseybzvygpe
--

REVOKE ALL ON SCHEMA public FROM postgres;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO uhysseybzvygpe;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- TOC entry 4328 (class 0 OID 0)
-- Dependencies: 832
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO uhysseybzvygpe;


-- Completed on 2022-08-28 23:30:55

--
-- PostgreSQL database dump complete
--

