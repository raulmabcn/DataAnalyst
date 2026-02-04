
-- TABLAS. La definición de clave primaria esta integrada en la instrucción de creación de tabla. 

CREATE TABLE equipos (
  ID_EQUIPO int  NOT NULL,
  EQUIPO varchar(30)  NOT NULL,
  PRIMARY KEY (ID_EQUIPO)
);

CREATE TABLE eventos (
  ID_JORNADA int  NOT NULL,
  ID_EVENTO int  NOT NULL,
  LOCAL int  NOT NULL,
  VISITANTE int  NOT NULL,
  RESULTADO varchar(1)  DEFAULT NULL,
  PRIMARY KEY (ID_JORNADA,ID_EVENTO)
);

CREATE TABLE jornadas (
  ID_JORNADA int  NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  FECHA date NOT NULL,
  DISPUTADA varchar(1)  NOT NULL DEFAULT 'N',
  PRIMARY KEY (ID_JORNADA)
);

CREATE TABLE quinielas (
  ID_QUINIELA int  NOT NULL,
  ID_JORNADA int  NOT NULL,
  NOMBRE varchar(30)  DEFAULT NULL,
  ESCRUTADA varchar(1)  NOT NULL DEFAULT 'N',
  ACIERTOS int DEFAULT NULL,
  PRIMARY KEY (ID_QUINIELA)  
);

CREATE TABLE pronosticos (
  ID_QUINIELA int  NOT NULL,
  ID_PRO int  NOT NULL,
  ID_JORNADA int  NOT NULL,
  ID_EVENTO int  NOT NULL,
  PRONOSTICO varchar(1)  NOT NULL,
  PRIMARY KEY (ID_QUINIELA,ID_PRO)  
);

-- DATOS

INSERT INTO equipos VALUES(1, 'Las Palmas');
INSERT INTO equipos VALUES(2, 'Xerez');
INSERT INTO equipos VALUES(3, 'Getafe');
INSERT INTO equipos VALUES(4, 'Nastic');
INSERT INTO equipos VALUES(5, 'Celta');
INSERT INTO equipos VALUES(6, 'Alcorcón');


INSERT INTO eventos VALUES(1, 1, 5, 1, '1');
INSERT INTO eventos VALUES(1, 2, 2, 3, '1');
INSERT INTO eventos VALUES(1, 3, 4, 6, '1');
INSERT INTO eventos VALUES(2, 1, 1, 2, '2');
INSERT INTO eventos VALUES(2, 2, 3, 4, '1');
INSERT INTO eventos VALUES(2, 3, 6, 5, '2');
INSERT INTO eventos VALUES(3, 1, 1, 4, 'X');
INSERT INTO eventos VALUES(3, 2, 3, 5, '2');
INSERT INTO eventos VALUES(3, 3, 6, 2, '1');
INSERT INTO eventos VALUES(4, 1, 3, 6, '2');
INSERT INTO eventos VALUES(4, 2, 2, 4, '2');
INSERT INTO eventos VALUES(4, 3, 1, 5, '1');
INSERT INTO eventos VALUES(5, 1, 1, 3, '1');
INSERT INTO eventos VALUES(5, 2, 5, 2, '2');
INSERT INTO eventos VALUES(5, 3, 6, 4, '1');
INSERT INTO eventos VALUES(6, 1, 2, 1, 'X');
INSERT INTO eventos VALUES(6, 2, 4, 3, '1');
INSERT INTO eventos VALUES(6, 3, 5, 6, '2');
INSERT INTO eventos VALUES(7, 1, 3, 2, 'X');
INSERT INTO eventos VALUES(7, 2, 4, 5, '1');
INSERT INTO eventos VALUES(7, 3, 6, 1, 'X');
INSERT INTO eventos VALUES(8, 1, 3, 1, NULL);
INSERT INTO eventos VALUES(8, 2, 2, 6, NULL);
INSERT INTO eventos VALUES(8, 3, 5, 4, NULL);
INSERT INTO eventos VALUES(9, 1, 1, 6, NULL);
INSERT INTO eventos VALUES(9, 2, 5, 3, NULL);
INSERT INTO eventos VALUES(9, 3, 4, 2, NULL);
INSERT INTO eventos VALUES(10, 1, 6, 3, NULL);
INSERT INTO eventos VALUES(10, 2, 4, 1, NULL);
INSERT INTO eventos VALUES(10, 3, 2, 5, NULL);


INSERT INTO jornadas VALUES(1, 'Jornada 1', '2010-01-10', 'S');
INSERT INTO jornadas VALUES(2, 'Jornada 2', '2010-01-17', 'S');
INSERT INTO jornadas VALUES(3, 'Jornada 3', '2010-01-24', 'S');
INSERT INTO jornadas VALUES(4, 'Jornada 4', '2010-02-07', 'S');
INSERT INTO jornadas VALUES(5, 'Jornada 5', '2010-02-14', 'S');
INSERT INTO jornadas VALUES(6, 'Jornada 6', '2010-02-21', 'S');
INSERT INTO jornadas VALUES(7, 'Jornada 7', '2010-03-07', 'S');
INSERT INTO jornadas VALUES(8, 'Jornada 8', '2010-03-21', 'N');
INSERT INTO jornadas VALUES(9, 'Jornada 9', '2010-04-04', 'N');
INSERT INTO jornadas VALUES(10, 'Jornada 10', '2010-04-18', 'N');


INSERT INTO quinielas VALUES(1, 1, 'Quini 1.1', 'S', 0);
INSERT INTO quinielas VALUES(2, 1, 'Quini 1.2', 'S', 1);
INSERT INTO quinielas VALUES(3, 1, 'Quini 1.3', 'S', 0);
INSERT INTO quinielas VALUES(4, 2, 'Quini 2.1', 'S', 1);
INSERT INTO quinielas VALUES(5, 2, 'Quini 2.2', 'S', 1);
INSERT INTO quinielas VALUES(6, 3, 'Quini 3.1', 'S', 1);
INSERT INTO quinielas VALUES(7, 3, 'Quini 3.2', 'S', 1);
INSERT INTO quinielas VALUES(8, 3, 'Quini 3.3', 'S', 3);
INSERT INTO quinielas VALUES(9, 3, 'Quini 3.4', 'S', 2);
INSERT INTO quinielas VALUES(10, 4, 'Quini 4.1', 'S', 2);
INSERT INTO quinielas VALUES(11, 4, 'Quini 4.2', 'S', 0);
INSERT INTO quinielas VALUES(12, 4, 'Quini 4.3', 'S', 0);
INSERT INTO quinielas VALUES(13, 5, 'Quini 5.1', 'S', 2);
INSERT INTO quinielas VALUES(14, 5, 'Quini 5.2', 'S', 2);
INSERT INTO quinielas VALUES(15, 6, 'Quini 6.1', 'S', 0);
INSERT INTO quinielas VALUES(16, 6, 'Quini 6.2', 'S', 1);
INSERT INTO quinielas VALUES(17, 6, 'Quini 6.3', 'S', 0);
INSERT INTO quinielas VALUES(18, 7, 'Quini 7.1', 'S', 1);
INSERT INTO quinielas VALUES(19, 7, 'Quini 7.2', 'S', 1);
INSERT INTO quinielas VALUES(20, 8, 'Quini 8.1', 'N', NULL);
INSERT INTO quinielas VALUES(21, 8, 'Quini 8.2', 'N', NULL);


INSERT INTO pronosticos VALUES(1, 1, 1, 1, 'X');
INSERT INTO pronosticos VALUES(1, 2, 1, 2, 'X');
INSERT INTO pronosticos VALUES(1, 3, 1, 3, 'X');
INSERT INTO pronosticos VALUES(2, 1, 1, 1, 'X');
INSERT INTO pronosticos VALUES(2, 2, 1, 2, '1');
INSERT INTO pronosticos VALUES(2, 3, 1, 3, '2');
INSERT INTO pronosticos VALUES(3, 1, 1, 1, 'X');
INSERT INTO pronosticos VALUES(3, 2, 1, 2, 'X');
INSERT INTO pronosticos VALUES(3, 3, 1, 3, '2');
INSERT INTO pronosticos VALUES(4, 1, 2, 1, '1');
INSERT INTO pronosticos VALUES(4, 2, 2, 2, '2');
INSERT INTO pronosticos VALUES(4, 3, 2, 3, '2');
INSERT INTO pronosticos VALUES(5, 1, 2, 1, 'X');
INSERT INTO pronosticos VALUES(5, 2, 2, 2, 'X');
INSERT INTO pronosticos VALUES(5, 3, 2, 3, '2');
INSERT INTO pronosticos VALUES(6, 1, 3, 1, 'X');
INSERT INTO pronosticos VALUES(6, 2, 3, 2, '1');
INSERT INTO pronosticos VALUES(6, 3, 3, 3, 'X');
INSERT INTO pronosticos VALUES(7, 1, 3, 1, '2');
INSERT INTO pronosticos VALUES(7, 2, 3, 2, '2');
INSERT INTO pronosticos VALUES(7, 3, 3, 3, '2');
INSERT INTO pronosticos VALUES(8, 1, 3, 1, 'X');
INSERT INTO pronosticos VALUES(8, 2, 3, 2, '2');
INSERT INTO pronosticos VALUES(8, 3, 3, 3, '1');
INSERT INTO pronosticos VALUES(9, 1, 3, 1, 'X');
INSERT INTO pronosticos VALUES(9, 2, 3, 2, '2');
INSERT INTO pronosticos VALUES(9, 3, 3, 3, 'X');
INSERT INTO pronosticos VALUES(10, 1, 4, 1, '2');
INSERT INTO pronosticos VALUES(10, 2, 4, 2, '1');
INSERT INTO pronosticos VALUES(10, 3, 4, 3, '1');
INSERT INTO pronosticos VALUES(11, 1, 4, 1, '1');
INSERT INTO pronosticos VALUES(11, 2, 4, 2, 'X');
INSERT INTO pronosticos VALUES(11, 3, 4, 3, '2');
INSERT INTO pronosticos VALUES(12, 1, 4, 1, 'X');
INSERT INTO pronosticos VALUES(12, 2, 4, 2, '1');
INSERT INTO pronosticos VALUES(12, 3, 4, 3, 'X');
INSERT INTO pronosticos VALUES(13, 1, 5, 1, '1');
INSERT INTO pronosticos VALUES(13, 2, 5, 2, 'X');
INSERT INTO pronosticos VALUES(13, 3, 5, 3, '1');
INSERT INTO pronosticos VALUES(14, 1, 5, 1, '1');
INSERT INTO pronosticos VALUES(14, 2, 5, 2, '2');
INSERT INTO pronosticos VALUES(14, 3, 5, 3, '2');
INSERT INTO pronosticos VALUES(15, 1, 6, 1, '1');
INSERT INTO pronosticos VALUES(15, 2, 6, 2, 'X');
INSERT INTO pronosticos VALUES(15, 3, 6, 3, '1');
INSERT INTO pronosticos VALUES(16, 1, 6, 1, '2');
INSERT INTO pronosticos VALUES(16, 2, 6, 2, '1');
INSERT INTO pronosticos VALUES(16, 3, 6, 3, 'X');
INSERT INTO pronosticos VALUES(17, 1, 6, 1, '1');
INSERT INTO pronosticos VALUES(17, 2, 6, 2, '2');
INSERT INTO pronosticos VALUES(17, 3, 6, 3, '1');
INSERT INTO pronosticos VALUES(18, 1, 7, 1, 'X');
INSERT INTO pronosticos VALUES(18, 2, 7, 2, '2');
INSERT INTO pronosticos VALUES(18, 3, 7, 3, '2');
INSERT INTO pronosticos VALUES(19, 1, 7, 1, '2');
INSERT INTO pronosticos VALUES(19, 2, 7, 2, '1');
INSERT INTO pronosticos VALUES(19, 3, 7, 3, '1');
INSERT INTO pronosticos VALUES(20, 1, 8, 1, '1');
INSERT INTO pronosticos VALUES(20, 2, 8, 2, '2');
INSERT INTO pronosticos VALUES(20, 3, 8, 3, '2');
INSERT INTO pronosticos VALUES(21, 1, 8, 1, 'X');
INSERT INTO pronosticos VALUES(21, 2, 8, 2, '1');
INSERT INTO pronosticos VALUES(21, 3, 8, 3, '2');

-- CLAVES FORANEAS

ALTER TABLE eventos
  ADD CONSTRAINT EVENTOS_ID_JORNADA_FK FOREIGN KEY (ID_JORNADA) REFERENCES jornadas (ID_JORNADA),
  ADD CONSTRAINT EVENTOS_ID_LOCAL_FK FOREIGN KEY (LOCAL) REFERENCES equipos (ID_EQUIPO),
  ADD CONSTRAINT EVENTOS_ID_VISITANTE_FK FOREIGN KEY (VISITANTE) REFERENCES equipos (ID_EQUIPO);


ALTER TABLE pronosticos
  ADD CONSTRAINT PRONOSTICOS_ID_JOR_ID_EVEN_FK FOREIGN KEY (ID_JORNADA, ID_EVENTO) REFERENCES eventos (ID_JORNADA, ID_EVENTO),
  ADD CONSTRAINT PRONOSTICOS_ID_QUINIELA_FK FOREIGN KEY (ID_QUINIELA) REFERENCES quinielas (ID_QUINIELA);

ALTER TABLE quinielas
  ADD CONSTRAINT QUINIELAS_ID_JORNADA_FK FOREIGN KEY (ID_JORNADA) REFERENCES jornadas (ID_JORNADA);

