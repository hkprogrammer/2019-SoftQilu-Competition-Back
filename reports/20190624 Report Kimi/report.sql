PRAGMA foreign_keys = '1';
PRAGMA database_list;
SELECT type,name,sql,tbl_name FROM "main".sqlite_master;
PRAGMA encoding
SELECT COUNT(*) FROM (SELECT "_rowid_",* FROM "main"."post" ORDER BY "_rowid_" ASC);
SELECT "_rowid_",* FROM "main"."post" ORDER BY "_rowid_" ASC LIMIT 0, 49999;
SELECT COUNT(*) FROM (SELECT "_rowid_",* FROM "main"."user" ORDER BY "_rowid_" ASC);
SELECT "_rowid_",* FROM "main"."user" ORDER BY "_rowid_" ASC LIMIT 0, 49999;
UPDATE "main"."user" SET "level"=? WHERE "_rowid_"='2';
UPDATE "main"."user" SET "level"=? WHERE "_rowid_"='2';
UPDATE "main"."user" SET "level"=? WHERE "_rowid_"='1';
PRAGMA auto_vacuum
PRAGMA automatic_index
PRAGMA checkpoint_fullfsync
PRAGMA foreign_keys
PRAGMA fullfsync
PRAGMA ignore_check_constraints
PRAGMA journal_mode
PRAGMA journal_size_limit
PRAGMA locking_mode
PRAGMA max_page_count
PRAGMA page_size
PRAGMA recursive_triggers
PRAGMA secure_delete
PRAGMA synchronous
PRAGMA temp_store
PRAGMA user_version
PRAGMA wal_autocheckpoint
SELECT 'x' NOT LIKE 'X'
SELECT COUNT(*) FROM (SELECT "_rowid_",* FROM "main"."user" ORDER BY "_rowid_" ASC);
SELECT "_rowid_",* FROM "main"."user" ORDER BY "_rowid_" ASC LIMIT 0, 49999;
SELECT COUNT(*) FROM (SELECT "_rowid_",* FROM "main"."post" ORDER BY "_rowid_" ASC);
SELECT "_rowid_",* FROM "main"."post" ORDER BY "_rowid_" ASC LIMIT 0, 49999;
SELECT COUNT(*) FROM (SELECT "_rowid_",* FROM "main"."user" ORDER BY "_rowid_" ASC);
SELECT "_rowid_",* FROM "main"."user" ORDER BY "_rowid_" ASC LIMIT 0, 49999;
SELECT COUNT(*) FROM (SELECT "_rowid_",* FROM "main"."post" ORDER BY "_rowid_" ASC);
SELECT "_rowid_",* FROM "main"."post" ORDER BY "_rowid_" ASC LIMIT 0, 49999;
SELECT COUNT(*) FROM (SELECT "_rowid_",* FROM "main"."user" ORDER BY "_rowid_" ASC);
SELECT "_rowid_",* FROM "main"."user" ORDER BY "_rowid_" ASC LIMIT 0, 49999;
