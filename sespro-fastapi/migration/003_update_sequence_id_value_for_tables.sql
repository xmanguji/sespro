SELECT setval('auditimage_id_seq', (SELECT MAX(id) FROM auditimage)+1);
SELECT setval('parsed_question_id_seq', (SELECT MAX(id) FROM parsed_question)+1);