-- ALTER TABLE premises RENAME TO premises_old;

-- ALTER INDEX IF EXISTS idx_premises__premises_group RENAME TO idx_premises_old__premises_group;

-- INSERT INTO premises
-- SELECT po.id, po.uuid, po.name, pg.id, po.date_created
-- FROM premises_old po
-- LEFT OUTER JOIN premises_group pg ON pg.uuid = po.group;


SELECT setval('premises_group_id_seq', (SELECT MAX(id) FROM premises_group)+1);