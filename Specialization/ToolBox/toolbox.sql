-- Generate drop's for all the tables of the schema:
SELECT CONCAT('DROP TABLE IF EXISTS `', table_name, '`;')
FROM information_schema.tables
WHERE table_schema = 'testing';
-- #######################################################

-- Show time consult:
SET profiling = 1; -- Activa el perfilado
-- Ejecuta tu consulta
SHOW PROFILES;
-- ########################################################

-- Check the infile restriction
-- Get the route for put/get files from mySQL

SHOW global variables like 'local_infile';
SHOW variables like 'secure_file_priv';
-- ########################################################




