-- ALTER TABLE parsed_question RENAME COLUMN "audit" TO "parsed_audit";


SELECT setval('parsed_question_id_seq', (SELECT MAX(id) FROM parsed_question)+1);