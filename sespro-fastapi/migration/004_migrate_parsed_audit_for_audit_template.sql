-- drop table if exists parsedaudit

-- INSERT INTO parsed_audit
-- SELECT pa.id as id, pa.uuid as uuid, at.id as audit_template, premises, "user", raw_data_key, raw_data_uri, score, max_score,
--                          score_percentage, final_comments, extra, start_time, end_time, date_submitted
-- FROM parsedaudit pa
-- LEFT OUTER JOIN audit_template at ON at.uuid = pa.template;


SELECT setval('parsed_audit_id_seq', (SELECT MAX(id) FROM parsed_audit)+1);
