
SELECT setval('audit_image_id_seq', (SELECT MAX(id) FROM audit_image)+1);

-- INSERT INTO audit_image
-- SELECT ROW_NUMBER() OVER (ORDER BY 1) AS id, uuid_generate_v4() as uuid, ai."user" as user, ai.premises as premises, ai.question as question, po.id as parsed_audit, pq.id as parsed_question, image_key, image_uri
-- FROM auditimage ai
-- LEFT OUTER JOIN parsed_audit po ON po.uuid = ai.parsed
-- LEFT OUTER JOIN parsed_question pq ON pq.parsed_audit = po.id
-- LEFT OUTER JOIN question q ON q.uuid = ai.question
-- WHERE pq.question = q.id;

