CREATE DATABASE dummy;

USE dummy;

CREATE TABLE dummy (
	id			INT,
    foreign_id	VARCHAR(10),
    name		VARCHAR(50),
    price		DECIMAL(5,2),
    place		CHAR(25),
    log_time	TIMESTAMP,
    event_time	DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY (foreign_id) REFERENCES foreign_table(id)
);

ALTER TABLE dummy
	DROP	COLUMN price,
    ADD		COLUMN price DECIMAL(6,2) NOT NULL,
    MODIFY	COLUMN place VARCHAR(25),
    RENAME	COLUMN place TO here,
    CHANGE	COLUMN here place CHAR(20),
    
    ADD		FOREIGN KEY (place) REFERENCES foreign_table(id),
    ADD		CONSTRAINT fk_constrain_name FOREIGN KEY (place) REFERENCES foreign_table(id),
    DROP	CONSTRAINT fk_constrain_name,
    DROP	PRIMARY KEY,
    ADD		PRIMARY KEY (id);
    
    
LOAD DATA INFILE 'C:\\path_dir\\file_name.csv' 
INTO TABLE dummy
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
( t_column1, t_column3, @val1 ) -- Se mapean las columnas del fichero en estos valores.
SET t_column2 = "dummy", t_column4 = SUBSTRING( @val1, 2);  


UPDATE dummy SET d_column = 'dummy' WHERE d_column = 3;
DELETE FROM dymmy WHERE d_column = '4';
INSERT INTO dummy (t_column, t_column1, t_column2) VALUES( 'dumy1','dumy2','dym3' );


SELECT 
	CASE 
		WHEN id = 1 THEN 'one'
		WHEN id = 2 THEN 'two'
		ELSE 'noOnenoTwo'
	END AS case_sentence
FROM JSON_TABLE(
	CONCAT('["', REPLACE( '3,4,2,1', ',', '","'), '"]'),
	'$[*]' COLUMNS (id INT PATH '$')
) temp;

SELECT ROW_NUMBER() OVER ( PARTITION BY t_colum_group   ORDER BY t_colum_order DESC ) AS rn; -- No funcional



    
    
