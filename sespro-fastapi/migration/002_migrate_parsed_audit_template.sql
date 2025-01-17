-- INSERT INTO parsed_question
-- SELECT pq.id, uuid_generate_v4(), q.id, c.id, pq.audit, pq.worth, pq.passed, pq.notes
-- FROM parsedquestion pq
-- left outer join category c on c.uuid::text = pq.category::text
-- left outer join question q on q.uuid::text = pq.uuid::text;


-- DROP TABLE IF EXISTS parsedquestion CASCADE;
SELECT setval('parsed_question_id_seq', (SELECT MAX(id) FROM parsed_question)+1);