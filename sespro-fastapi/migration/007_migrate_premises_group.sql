-- INSERT INTO premises_group
-- SELECT pg.id, pg.uuid, pg.name, pg.render_enabled
-- FROM premisesgroup pg;


SELECT setval('premises_group_id_seq', (SELECT MAX(id) FROM premises_group)+1);