INSERT INTO audit_template
SELECT at.id, at.uuid, at.name, at.enabled, at.date_created FROM audittemplate at;

INSERT INTO audit_template_category (audit_template, category, "order")
SELECT at.id, cat.id, at.order_no::INTEGER
FROM (
SELECT id, json_object_keys(categories::json)::text as order_no,
       categories->>json_object_keys(categories::json)::text as cat_uuid
FROM audittemplate ) as at
left outer join category cat on cat.uuid::text = at.cat_uuid::text;


INSERT INTO audit_template_question (audit_template, question, "order")
SELECT at.id, q.id, at.order_no::INTEGER
FROM (
SELECT id, json_object_keys(questions::json)::text as order_no,
       questions->>json_object_keys(questions::json)::text as q_uuid
FROM audittemplate ) as at
left outer join question q on q.uuid::text = at.q_uuid::text;

DROP TABLE IF EXISTS audittemplate CASCADE;
