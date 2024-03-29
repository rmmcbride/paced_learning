-- Table: public.card

--DROP TABLE public.card;
--
--CREATE TABLE public.card (
--	id serial4 NOT NULL,
--	topic text NULL,
--	question text NULL,
--	answer text NULL,
--	difficulty int4 NULL,
--	last_date date NULL,
--	score int4 NULL,
--	CONSTRAINT card_pkey PRIMARY KEY (id),
--	CONSTRAINT card_un UNIQUE (id)
--);
--
--TABLESPACE pg_default;
--
--ALTER TABLE card
--    OWNER to postgres;
--
--COMMENT ON TABLE card
--    IS 'Holds questions and answers for various topics';
--
--
--INSERT INTO card (topic, question, answer, difficulty, last_date, score)
--VALUES ('Maths', 'This is a test Maths question', 'This is a test Maths answer', 5, '2021-04-20', 100),
--('Maths', 'This is a second test Maths question', 'This is a second test Maths answer', 4, '2021-04-20', 10),
--('Programming', 'This is a test Programming question', 'This is a test Programming answer', 5, '2021-04-20', 100),
--('Programming', 'This is a second test Programming question', 'This is a second test Programming answer', 4, '2021-04-20', 10);
--
--select * from card;
