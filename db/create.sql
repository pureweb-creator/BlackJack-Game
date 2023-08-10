CREATE TABLE users (
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