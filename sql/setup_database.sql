-- Table: learn.math

DROP TABLE learn.card;

CREATE TABLE card
(
	id serial PRIMARY KEY,
	topic text COLLATE pg_catalog."default",
    question text COLLATE pg_catalog."default",
    answer text COLLATE pg_catalog."default",
    difficulty integer,
    last_date date,
    score integer

)

TABLESPACE pg_default;

ALTER TABLE card
    OWNER to postgres;

COMMENT ON TABLE card
    IS 'Holds questions and answers for various topics';


INSERT INTO card (topic, question, answer, difficulty, last_date, score)
VALUES ('Maths', 'This is a test Maths question', 'This is a test Maths answer', 5, '2021-04-20', 100),
('Maths', 'This is a second test Maths question', 'This is a second test Maths answer', 4, '2021-04-20', 10),
('Programming', 'This is a test Programming question', 'This is a test Programming answer', 5, '2021-04-20', 100),
('Programming', 'This is a second test Programming question', 'This is a second test Programming answer', 4, '2021-04-20', 10);

select * from card;
