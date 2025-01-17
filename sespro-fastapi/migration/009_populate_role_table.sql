-- INSERT INTO role (name, displayname, "order")
-- VALUES
--     ('ROLE_ROOT', 'Root', 1),
--     ( 'ROLE_MANAGER', 'Manager', 2),
--     ('ROLE_AUDITOR', 'Auditor', 3);


SELECT setval('role_id_seq', (SELECT MAX(id) FROM role)+1);