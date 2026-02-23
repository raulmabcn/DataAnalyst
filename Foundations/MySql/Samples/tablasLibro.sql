
CREATE TABLE actuaciones_destacadas (
  ID_ALUMNO int  NOT NULL,
  ID_CURSO int  NOT NULL,
  ACTUACION varchar(120)  NOT NULL
);

INSERT INTO actuaciones_destacadas VALUES(3, 1, '10 en examen parcial ');
INSERT INTO actuaciones_destacadas VALUES(3, 1, 'Práctica PHP muy bien desarrollada');
INSERT INTO actuaciones_destacadas VALUES(5, 3, 'Práctica de subconsultas en where perfecta');
INSERT INTO actuaciones_destacadas VALUES(2, 4, 'Diseño muy creativo');

CREATE TABLE alumnos (
  ID_ALUMNO int  NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  APELLIDOS varchar(50)  NOT NULL,
  F_NACIMIENTO date NOT NULL,
  PRIMARY KEY (ID_ALUMNO)
);

INSERT INTO alumnos VALUES(1, 'Pablo', 'Hernandaz Mata', '1995-03-14');
INSERT INTO alumnos VALUES(2, 'Jeremias', 'Santo Lote', '1993-07-12');
INSERT INTO alumnos VALUES(3, 'Teresa', 'Lomas Trillo', '1989-06-19');
INSERT INTO alumnos VALUES(4, 'Marta', 'Fuego García', '1992-11-23');
INSERT INTO alumnos VALUES(5, 'Sergio', 'Ot Dirmet', '1991-04-21');
INSERT INTO alumnos VALUES(6, 'Carmen', 'Dilma Perna', '1987-12-04');

CREATE TABLE alumnos_cursos (
  ID_ALUMNO int  NOT NULL,
  ID_CURSO int  NOT NULL,
  PRIMARY KEY (ID_ALUMNO,ID_CURSO)
);

INSERT INTO alumnos_cursos VALUES(1, 1);
INSERT INTO alumnos_cursos VALUES(3, 1);
INSERT INTO alumnos_cursos VALUES(5, 1);
INSERT INTO alumnos_cursos VALUES(4, 2);
INSERT INTO alumnos_cursos VALUES(1, 3);
INSERT INTO alumnos_cursos VALUES(5, 3);
INSERT INTO alumnos_cursos VALUES(2, 4);
INSERT INTO alumnos_cursos VALUES(6, 4);

CREATE TABLE alumnos_cursos_hist (
  TEMPORADA varchar(9) NOT NULL,
  ID_ALUMNO int  NOT NULL,
  ID_CURSO int  NOT NULL
);

INSERT INTO alumnos_cursos_hist VALUES('2012-2013', 6, 4);
INSERT INTO alumnos_cursos_hist VALUES('2012-2013', 2, 4);
INSERT INTO alumnos_cursos_hist VALUES('2012-2013', 5, 3);
INSERT INTO alumnos_cursos_hist VALUES('2012-2013', 1, 3);
INSERT INTO alumnos_cursos_hist VALUES('2012-2013', 4, 2);
INSERT INTO alumnos_cursos_hist VALUES('2012-2013', 5, 1);
INSERT INTO alumnos_cursos_hist VALUES('2012-2013', 3, 1);
INSERT INTO alumnos_cursos_hist VALUES('2012-2013', 1, 1);

CREATE TABLE alumnos_cursos_tmp (
  ID_CURSO int  NOT NULL,
  TITULO varchar(50)  NOT NULL,
  ID_ALUMNO int  NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  APELLIDOS varchar(50)  NOT NULL
);

INSERT INTO alumnos_cursos_tmp VALUES(1, 'Programación PHP', 1, 'Pablo', 'Hernandaz Mata');
INSERT INTO alumnos_cursos_tmp VALUES(1, 'Programación PHP', 3, 'Teresa', 'Lomas Trillo');
INSERT INTO alumnos_cursos_tmp VALUES(1, 'Programación PHP', 5, 'Sergio', 'Ot Dirmet');
INSERT INTO alumnos_cursos_tmp VALUES(2, 'Modelos abstracto de datos', 4, 'Marta', 'Fuego García');
INSERT INTO alumnos_cursos_tmp VALUES(3, 'SQL desde cero', 1, 'Pablo', 'Hernandaz Mata');
INSERT INTO alumnos_cursos_tmp VALUES(3, 'SQL desde cero', 5, 'Sergio', 'Ot Dirmet');
INSERT INTO alumnos_cursos_tmp VALUES(4, 'Dibujo técnico', 2, 'Jeremias', 'Santo Lote');
INSERT INTO alumnos_cursos_tmp VALUES(4, 'Dibujo técnico', 6, 'Carmen', 'Dilma Perna');


CREATE TABLE articulos (
  ID_ARTICULO int NOT NULL,
  DESCRIPCION varchar(30)  NOT NULL,
  PRECIO float  NULL,
  AUDITORIA datetime NOT NULL,
  PRIMARY KEY (ID_ARTICULO)
);

INSERT INTO articulos VALUES(1, 'Leche 1L.', 0.95, '2013-09-23 12:23:14');
INSERT INTO articulos VALUES(2, 'Café 250 gr.', 9.98, '2013-10-22 18:33:51');
INSERT INTO articulos VALUES(3, 'Agua 5L.', 1.65, '2013-10-01 20:16:36');
INSERT INTO articulos VALUES(4, 'Galletas 200 gr.', 1, '2013-08-11 10:03:54');
INSERT INTO articulos VALUES(32, 'Fregasuelos', 1.25, '2013-11-02 12:59:56');

CREATE TABLE calzados (
  ID_CALZADO int NOT NULL,
  CALZADO varchar(40)  NOT NULL,
  PESO_GR int NOT NULL,
  PRIMARY KEY (ID_CALZADO)
);

INSERT INTO calzados VALUES(1, 'deportivas', 675);
INSERT INTO calzados VALUES(2, 'mocasines', 800);
INSERT INTO calzados VALUES(3, 'botas', 1050);

CREATE TABLE camisas (
  ID_CAMISA int NOT NULL,
  CAMISA varchar(40)  NOT NULL,
  PESO_GR int NOT NULL,
  PRIMARY KEY (ID_CAMISA)
);

INSERT INTO camisas VALUES(1, 'lino blanca', 210);
INSERT INTO camisas VALUES(2, 'algodon naranja', 290);
INSERT INTO camisas VALUES(3, 'seda negra', 260);

CREATE TABLE cursos (
  ID_CURSO int  NOT NULL,
  TITULO varchar(50)  NOT NULL,
  ID_PROFE int  DEFAULT NULL,
  PRIMARY KEY (ID_CURSO)
);

INSERT INTO cursos VALUES(1, 'Programación PHP', 3);
INSERT INTO cursos VALUES(2, 'Modelos abstracto de datos', 3);
INSERT INTO cursos VALUES(3, 'SQL desde cero', 1);
INSERT INTO cursos VALUES(4, 'Dibujo técnico', 2);
INSERT INTO cursos VALUES(5, 'SQL avanzado', NULL);

CREATE TABLE emplea2 (
  ID_EMPLEADO int  NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  APELLIDOS varchar(50)  NOT NULL,
  F_NACIMIENTO date NOT NULL,
  SEXO varchar(1)  NOT NULL,
  CARGO varchar(30)  NOT NULL,
  SALARIO float  NOT NULL,
  PRECIO_HORA float NOT NULL,
  PRIMARY KEY (ID_EMPLEADO)
);

INSERT INTO emplea2 VALUES(1, 'Carlos', 'Jiménez Clarín', '1985-05-03', 'H', 'Mozo', 1530, 20.2);
INSERT INTO emplea2 VALUES(2, 'Elena', 'Rubio Cuestas', '1978-09-25', 'M', 'Secretaria', 1326, 18.18);
INSERT INTO emplea2 VALUES(3, 'José', 'Calvo Sisman', '1990-11-12', 'H', 'Mozo', 1428, 19.19);
INSERT INTO emplea2 VALUES(4, 'Margarita', 'Ródriguez Garcés', '1992-05-16', 'M', 'Secretaria', 1352.01, 18.18);

CREATE TABLE empleados (
  ID_EMPLEADO int  NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  APELLIDOS varchar(50)  NOT NULL,
  F_NACIMIENTO date NOT NULL,
  SEXO varchar(1)  NOT NULL,
  CARGO varchar(30)  NOT NULL,
  SALARIO float  NOT NULL,
  PRIMARY KEY (ID_EMPLEADO)
);

INSERT INTO empleados VALUES(1, 'Carlos', 'Jiménez Clarín', '1985-05-03', 'H', 'Mozo', 1500);
INSERT INTO empleados VALUES(2, 'Elena', 'Rubio Cuestas', '1978-09-25', 'M', 'Secretaria', 1300);
INSERT INTO empleados VALUES(3, 'José', 'Calvo Sisman', '1990-11-12', 'H', 'Mozo', 1400);
INSERT INTO empleados VALUES(4, 'Margarita', 'Ródriguez Garcés', '1992-05-16', 'M', 'Secretaria', 1325.5);

CREATE TABLE empleados_tmp (
  ID_EMPLEADO int  NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  APELLIDOS varchar(50)  NOT NULL,
  F_NACIMIENTO date NOT NULL,
  SEXO varchar(1)  NOT NULL,
  CARGO varchar(30)  NOT NULL,
  SALARIO float  NOT NULL
);

INSERT INTO empleados_tmp VALUES(1, 'Carlos', 'Jiménez Clarín', '1985-05-03', 'H', 'Mozo', 1500);
INSERT INTO empleados_tmp VALUES(2, 'Elena', 'Rubio Cuestas', '1978-09-25', 'M', 'Secretaria', 1300);
INSERT INTO empleados_tmp VALUES(3, 'José', 'Calvo Sisman', '1990-11-12', 'H', 'Mozo', 1400);
INSERT INTO empleados_tmp VALUES(4, 'Margarita', 'Ródriguez Garcés', '1992-05-16', 'M', 'Secretaria', 1325.5);

CREATE TABLE equipos (
  ID_EQUIPO int  NOT NULL,
  EQUIPO varchar(30)  NOT NULL,
  PRIMARY KEY (ID_EQUIPO)
);

INSERT INTO equipos VALUES(1, 'Las Palmas');
INSERT INTO equipos VALUES(2, 'Xerez');
INSERT INTO equipos VALUES(3, 'Getafe');
INSERT INTO equipos VALUES(4, 'Nastic');
INSERT INTO equipos VALUES(5, 'Celta');
INSERT INTO equipos VALUES(6, 'Alcorcón');

CREATE TABLE eventos (
  ID_JORNADA int  NOT NULL,
  ID_EVENTO int  NOT NULL,
  LOCAL int  NOT NULL,
  VISITANTE int  NOT NULL,
  RESULTADO varchar(1)  DEFAULT NULL,
  PRIMARY KEY (ID_JORNADA,ID_EVENTO)
);

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

CREATE TABLE facturas (
  ID_FACTURA int NOT NULL,
  TOTAL_FACTURA float NOT NULL,
  FECHA_FACTURA date NOT NULL,
  PRIMARY KEY (ID_FACTURA)
);

INSERT INTO facturas VALUES(1, 36.38, '2013-11-02');

CREATE TABLE fechas (
  fecha date DEFAULT NULL
);

INSERT INTO fechas VALUES('2008-12-01');
INSERT INTO fechas VALUES(NULL);

CREATE TABLE jornadas (
  ID_JORNADA int  NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  FECHA date NOT NULL,
  DISPUTADA varchar(1)  NOT NULL DEFAULT 'N',
  PRIMARY KEY (ID_JORNADA)
);

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

CREATE TABLE juego (
  ID_JUEGO int  NOT NULL,
  JUGADOR varchar(30)  NOT NULL,
  NUMERO int NOT NULL,
  INTENTOS int NOT NULL DEFAULT '0',
  FINALIZADO varchar(11)  NOT NULL DEFAULT 'N',
  PRIMARY KEY (ID_JUEGO)
);

CREATE TABLE lineas_factura (
  ID_FACTURA int NOT NULL,
  ID_LINEA int NOT NULL,
  ID_ARTICULO int NOT NULL,
  CANTIDAD int NOT NULL,
  PRECIO float NOT NULL,
  TOTAL_LINEA float NOT NULL,
  PRIMARY KEY (ID_FACTURA,ID_LINEA)  
);

INSERT INTO lineas_factura VALUES(1, 1, 2, 3, 9.26, 27.78);
INSERT INTO lineas_factura VALUES(1, 2, 4, 2, 1, 2);
INSERT INTO lineas_factura VALUES(1, 3, 3, 4, 1.65, 6.6);

CREATE TABLE mascotas (
  ID_MASCOTA int NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  ESPECIE varchar(1)  NOT NULL,
  SEXO varchar(1)  NOT NULL,
  UBICACION varchar(6)  NOT NULL,
  ESTADO varchar(1)  NOT NULL,
  PRIMARY KEY (ID_MASCOTA)
);

INSERT INTO mascotas VALUES(1, 'Budy', 'P', 'M', 'E05', 'B');
INSERT INTO mascotas VALUES(2, 'Pipo', 'P', 'M', 'E02', 'B');
INSERT INTO mascotas VALUES(3, 'Nuna', 'P', 'H', 'E02', 'A');
INSERT INTO mascotas VALUES(4, 'Bruts', 'P', 'M', 'E03', 'A');
INSERT INTO mascotas VALUES(5, 'Americo ', 'G', 'M', 'E04', 'A');
INSERT INTO mascotas VALUES(6, 'Sombra', 'P', 'H', 'E05', 'A');
INSERT INTO mascotas VALUES(7, 'Amaya', 'G', 'H', 'E04', 'A');
INSERT INTO mascotas VALUES(8, 'Talia ', 'G', 'H', 'E01', 'B');
INSERT INTO mascotas VALUES(9, 'Trabis', 'P', 'M', 'E02', 'A');
INSERT INTO mascotas VALUES(10, 'Tesa', 'G', 'H', 'E01', 'A');
INSERT INTO mascotas VALUES(11, 'Titito ', 'G', 'M', 'E04', 'B');
INSERT INTO mascotas VALUES(12, 'Truca', 'P', 'H', 'E02', 'A');
INSERT INTO mascotas VALUES(13, 'Zulay', 'P', 'H', 'E05', 'A');
INSERT INTO mascotas VALUES(14, 'Dandi ', 'G', 'M', 'E04', 'A');
INSERT INTO mascotas VALUES(15, 'Ras ', 'G', 'M', 'E01', 'A');
INSERT INTO mascotas VALUES(16, 'Canela', 'P', 'H', 'E02', 'A');


CREATE TABLE novedades (
  ID_ARTICULO int NOT NULL,
  DESCRIPCION varchar(30)  NOT NULL,
  PRECIO float DEFAULT NULL
);

INSERT INTO novedades VALUES(2, 'Café 250 gr.', 9.92);
INSERT INTO novedades VALUES(3, 'Agua 5L.', 1.59);

CREATE TABLE pantalones (
  ID_PANTALON int NOT NULL,
  PANTALON varchar(40)  NOT NULL,
  PESO_GR int NOT NULL,
  PRIMARY KEY (ID_PANTALON)
);

INSERT INTO pantalones VALUES(1, 'tela azul marino', 470);
INSERT INTO pantalones VALUES(2, 'pana marron claro', 730);

CREATE TABLE personas (
  ID_PERSONA int NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  RUBIA varchar(1)  NOT NULL,
  ALTA varchar(1)  NOT NULL,
  GAFAS varchar(1)  NOT NULL,
  PRIMARY KEY (ID_PERSONA)
);

INSERT INTO personas VALUES(1, 'Manuel', 'S', 'S', 'N');
INSERT INTO personas VALUES(2, 'Maria', 'N', 'N', 'S');
INSERT INTO personas VALUES(3, 'Carmen', 'S', 'N', 'S');
INSERT INTO personas VALUES(4, 'José', 'S', 'S', 'S');
INSERT INTO personas VALUES(5, 'Pedro', 'N', 'S', 'N');

CREATE TABLE poker (
  ID_SESION int NOT NULL,
  F_SESION date NOT NULL,
  GANANCIA int NOT NULL,
  PRIMARY KEY (ID_SESION)
);

INSERT INTO poker VALUES(1, '2008-12-18', 23);
INSERT INTO poker VALUES(2, '2008-12-25', -34);
INSERT INTO poker VALUES(3, '2009-01-06', 46);
INSERT INTO poker VALUES(4, '2009-01-25', -37);
INSERT INTO poker VALUES(5, '2009-02-08', 16);
INSERT INTO poker VALUES(6, '2009-02-16', -28);
INSERT INTO poker VALUES(7, '2009-02-27', 15);
INSERT INTO poker VALUES(8, '2009-03-05', -57);
INSERT INTO poker VALUES(9, '2009-03-12', 49);
INSERT INTO poker VALUES(10, '2009-03-19', 9);
INSERT INTO poker VALUES(11, '2009-03-24', 21);
INSERT INTO poker VALUES(12, '2009-04-06', -27);

CREATE TABLE productos (
  ID_ARTICULO int NOT NULL,
  DESCRIPCION varchar(30)  NOT NULL,
  PRECIO float DEFAULT NULL,
  RECALCULAR varchar(1)  NOT NULL DEFAULT 'N',
  PRIMARY KEY (ID_ARTICULO)
);

INSERT INTO productos VALUES(1, 'Leche 1L.', 0.95, 'N');
INSERT INTO productos VALUES(2, 'Café 250 gr.', 9.98, 'N');
INSERT INTO productos VALUES(3, 'Agua 5L.', 1.65, 'N');
INSERT INTO productos VALUES(4, 'Galletas 200 gr.', 1, 'N');
INSERT INTO productos VALUES(32, 'Fregasuelos', 1.25, 'N');

CREATE TABLE profesores (
  ID_PROFE int  NOT NULL,
  NOMBRE varchar(30)  NOT NULL,
  APELLIDOS varchar(50)  NOT NULL,
  F_NACIMIENTO date NOT NULL,
  PRIMARY KEY (ID_PROFE)
);

INSERT INTO profesores VALUES(1, 'Federico', 'Gasco Daza', '1975-04-23');
INSERT INTO profesores VALUES(2, 'Ana', 'Saura Trenzo', '1969-08-02');
INSERT INTO profesores VALUES(3, 'Rosa', 'Honrosa Pérez', '1980-09-05');
INSERT INTO profesores VALUES(4, 'Carlos', 'García Martínez', '1985-05-24');

CREATE TABLE pronosticos (
  ID_QUINIELA int  NOT NULL,
  ID_PRO int  NOT NULL,
  ID_JORNADA int  NOT NULL,
  ID_EVENTO int  NOT NULL,
  PRONOSTICO varchar(1)  NOT NULL,
  PRIMARY KEY (ID_QUINIELA,ID_PRO)  
);

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

CREATE TABLE quinielas (
  ID_QUINIELA int  NOT NULL,
  ID_JORNADA int  NOT NULL,
  NOMBRE varchar(30)  DEFAULT NULL,
  ESCRUTADA varchar(1)  NOT NULL DEFAULT 'N',
  ACIERTOS int DEFAULT NULL,
  PRIMARY KEY (ID_QUINIELA)  
);

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


CREATE TABLE table_constraints_academia (
  CONSTRAINT_CATALOG	varchar(512) NOT NULL,
  CONSTRAINT_SCHEMA	varchar(64) NOT NULL,
  CONSTRAINT_NAME	varchar(64) NOT NULL,
  TABLE_SCHEMA varchar(64)  NOT NULL ,
  TABLE_NAME varchar(64)  NOT NULL ,
  CONSTRAINT_TYPE varchar(64)  NOT NULL 
);

INSERT INTO table_constraints_academia VALUES('def', 'academia', 'PRIMARY', 'academia', 'alumnos', 'PRIMARY KEY');
INSERT INTO table_constraints_academia VALUES('def', 'academia', 'PRIMARY', 'academia', 'alumnos_cursos', 'PRIMARY KEY');
INSERT INTO table_constraints_academia VALUES('def', 'academia', 'ALUMNOS_CURSOS_ID_CURSO_FK', 'academia', 'alumnos_cursos', 'FOREIGN KEY');
INSERT INTO table_constraints_academia VALUES('def', 'academia', 'ALUMNOS_CURSOS_ID_ALUMNO_FK', 'academia', 'alumnos_cursos', 'FOREIGN KEY');
INSERT INTO table_constraints_academia VALUES('def', 'academia', 'PRIMARY', 'academia', 'cursos', 'PRIMARY KEY');
INSERT INTO table_constraints_academia VALUES('def', 'academia', 'CURSOS_ID_PROFE_INX', 'academia', 'cursos', 'UNIQUE');
INSERT INTO table_constraints_academia VALUES('def', 'academia', 'CURSOS_ID_PROFE_FK', 'academia', 'cursos', 'FOREIGN KEY');
INSERT INTO table_constraints_academia VALUES('def', 'academia', 'PRIMARY', 'academia', 'profesores', 'PRIMARY KEY');


CREATE TABLE vehiculos (
  ID_VEHICULO int NOT NULL,
  MARCA varchar(30)  NOT NULL,
  MODELO varchar(30)  NOT NULL,
  PROX_ITV date NOT NULL,
  ULTI_ITV date  NULL,
  PRIMARY KEY (ID_VEHICULO)
);

INSERT INTO vehiculos VALUES(1, 'Alfa Romeo', 'Brera', '2011-10-20', NULL);
INSERT INTO vehiculos VALUES(2, 'Seat', 'Panda', '2009-12-01', '2008-12-01');
INSERT INTO vehiculos VALUES(3, 'BMW', 'X3', '2010-07-18', NULL);
INSERT INTO vehiculos VALUES(4, 'Citroën', 'C2', '2010-08-24', '2009-08-24');
INSERT INTO vehiculos VALUES(5, 'Ford', 'Fiesta', '2011-04-22', NULL);

ALTER TABLE actuaciones_destacadas
  ADD CONSTRAINT actuaciones_destacadas_ID_ALUMNO_FK FOREIGN KEY (ID_ALUMNO) REFERENCES alumnos (ID_ALUMNO),
  ADD CONSTRAINT actuaciones_destacadas_ID_CURSO_FK FOREIGN KEY (ID_CURSO) REFERENCES cursos (ID_CURSO);

ALTER TABLE alumnos_cursos
  ADD CONSTRAINT alumnos_cursos_id_alumno_fk FOREIGN KEY (ID_ALUMNO) REFERENCES alumnos (ID_ALUMNO),
  ADD CONSTRAINT alumnos_cursos_id_curso_fk FOREIGN KEY (ID_CURSO) REFERENCES cursos (ID_CURSO);

ALTER TABLE cursos
  ADD CONSTRAINT cursos_id_profe_fk FOREIGN KEY (ID_PROFE) REFERENCES profesores (ID_PROFE);

ALTER TABLE eventos
  ADD CONSTRAINT EVENTOS_ID_JORNADA_FK FOREIGN KEY (ID_JORNADA) REFERENCES jornadas (ID_JORNADA),
  ADD CONSTRAINT EVENTOS_ID_LOCAL_FK FOREIGN KEY (LOCAL) REFERENCES equipos (ID_EQUIPO),
  ADD CONSTRAINT EVENTOS_ID_VISITANTE_FK FOREIGN KEY (VISITANTE) REFERENCES equipos (ID_EQUIPO);

ALTER TABLE lineas_factura
  ADD CONSTRAINT lineas_factura_id_articulo_fk FOREIGN KEY (ID_ARTICULO) REFERENCES articulos (ID_ARTICULO),
  ADD CONSTRAINT lineas_factura_id_factura_fk FOREIGN KEY (ID_FACTURA) REFERENCES facturas (ID_FACTURA);

ALTER TABLE pronosticos
  ADD CONSTRAINT PRONOSTICOS_ID_JOR_ID_EVEN_FK FOREIGN KEY (ID_JORNADA, ID_EVENTO) REFERENCES eventos (ID_JORNADA, ID_EVENTO),
  ADD CONSTRAINT PRONOSTICOS_ID_QUINIELA_FK FOREIGN KEY (ID_QUINIELA) REFERENCES quinielas (ID_QUINIELA);

ALTER TABLE quinielas
  ADD CONSTRAINT QUINIELAS_ID_JORNADA_FK FOREIGN KEY (ID_JORNADA) REFERENCES jornadas (ID_JORNADA);

create view TOTALES_SALARIO_V as
select SEXO, sum(SALARIO) as TOTAL
  from EMPLEADOS 
 group by SEXO;
 
create view ALUMNOS_CURSOS_V as
select C.ID_CURSO,
       C.TITULO CURSO,
       A.ID_ALUMNO, 
       A.APELLIDOS,
       A.NOMBRE
  from ALUMNOS_CURSOS AC, ALUMNOS A, CURSOS C
 where AC.ID_ALUMNO = A.ID_ALUMNO
   and AC.ID_CURSO = C.ID_CURSO
 order by C.TITULO , A.NOMBRE , A.APELLIDOS;
 
create view EMPLEADOS_V as
select ID_EMPLEADO,
       NOMBRE,
       APELLIDOS,       
       date_format(F_NACIMIENTO,'%d/%m/%Y') as F_NACIMIENTO,
       if(SEXO = 'M', 'Mujer', 'Hombre') as DESC_SEXO,
       SEXO,  CARGO, SALARIO
  from EMPLEADOS;
  
create view MASCOTAS_V as
select ID_MASCOTA,
       NOMBRE,
       if(ESPECIE = 'P', 'Perro', 'Gato' ) ESPECIE,
       if(SEXO = 'M', 'Macho', 'Hembra') SEXO,
       UBICACION,
       if (ESTADO = 'A', 'Alta', 'Baja') ESTADO       
  from MASCOTAS;
 