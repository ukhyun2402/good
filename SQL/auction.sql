
CREATE TABLE public.auction(
    id integer NOT NULL DEFAULT nextval('auction_list_id_seq'::regclass),
    auction_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    mulgeon_number integer DEFAULT 1,
    law character varying(50) COLLATE pg_catalog."default" NOT NULL,
    last_check timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    auction_done boolean DEFAULT false,
    CONSTRAINT auction_list_pkey PRIMARY KEY (id)
)
