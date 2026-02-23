DELIMITER //

CREATE FUNCTION MAYOR(P_VALOR_1 int, 
                      P_VALOR_2 int) RETURNS int(11)
begin
   declare V_RETORNO int;

   if P_VALOR_1 > P_VALOR_2 then
      set V_RETORNO = P_VALOR_1;
   else
      set V_RETORNO = P_VALOR_2;
   end if;

   return V_RETORNO;
end;
//

CREATE PROCEDURE ACTUALIZA_NOVEDADES()
begin
   declare V_ID_ARTICULO int;
   declare V_PRECIO float;
   declare V_HAY_REGISTROS boolean default true;
   declare C_NOVEDADES cursor for 
           select ID_ARTICULO, PRECIO
             from NOVEDADES;
   declare continue handler for not found
           set V_HAY_REGISTROS = false;

   open C_NOVEDADES;   
   fetch C_NOVEDADES into V_ID_ARTICULO, V_PRECIO;


   while V_HAY_REGISTROS do

      update ARTICULOS
         set PRECIO = V_PRECIO
       where ID_ARTICULO = V_ID_ARTICULO;

       fetch C_NOVEDADES into V_ID_ARTICULO, V_PRECIO;

   end while;
   close C_NOVEDADES;
end;
//

CREATE PROCEDURE ACTUALIZA_PRECIOS()
begin
   update ARTICULOS as ART
      set PRECIO = ( select PRECIO
                       from NOVEDADES as NOV
                      where NOV.ID_ARTICULO = ART.ID_ARTICULO
                   )
    where exists (select 1 
                    from NOVEDADES as NVD
                   where NVD.ID_ARTICULO = ART.ID_ARTICULO);
end;
//

CREATE FUNCTION ES_PAR(P_VALOR int) RETURNS char(2)
begin
   declare V_RETORNO char(2);
 
   if mod(P_VALOR, 2) = 0 then
      set V_RETORNO = 'SI';
   else
      set V_RETORNO = 'NO';
   end if;
 
   return V_RETORNO;
end;
//

CREATE FUNCTION SUMA_SALARIOS(P_SEXO char(1)) RETURNS float
begin
   declare V_SUMA float;
 
   select sum(SALARIO)
     into V_SUMA
     from EMPLEADOS
    where SEXO = P_SEXO
       or P_SEXO is null;
 
   return V_SUMA;
end;
//

-- videojuego

CREATE PROCEDURE FINALIZAR_JUEGO(P_JUEGO int)
begin
   update JUEGO
      set FINALIZADO = 'S'
    where ID_JUEGO = P_JUEGO;
end;
//

CREATE FUNCTION INCREMENTAR_INTENTOS(P_JUEGO int) RETURNS int(11)
begin
   declare V_INTENTOS int;

   update JUEGO
      set INTENTOS = INTENTOS + 1
    where ID_JUEGO = P_JUEGO;

   select INTENTOS
     into V_INTENTOS
     from JUEGO
    where ID_JUEGO = P_JUEGO;

   return V_INTENTOS;
end;
//

CREATE FUNCTION OBTENER_JUEGO(P_JUGADOR char(30)) RETURNS int(11)
begin
   declare V_JUEGO int;

   select ID_JUEGO
     into V_JUEGO
     from JUEGO
    where JUGADOR = P_JUGADOR
      and FINALIZADO = 'N';

   if V_JUEGO is null then
      insert into JUEGO(JUGADOR, NUMERO) 
      values (P_JUGADOR, round ( rand() * 999 ));
      
      select last_insert_id()
        into V_JUEGO;
   end if;
      return V_JUEGO;
end;
//

CREATE FUNCTION OBTENER_NUMERO(P_JUEGO int) RETURNS int(11)
begin
   declare V_NUMERO int;

   select NUMERO
     into V_NUMERO
     from JUEGO
    where ID_JUEGO = P_JUEGO;

   return V_NUMERO;
end;
//

CREATE FUNCTION NUMERO_SECRETO(P_JUGADOR char(30),
                               P_NUMERO int) returns char(200)
begin
   declare V_JUEGO int;
   declare V_NUMERO int;
   declare V_INTENTOS int;
   declare V_RETORNO char(200);
 
   -- control de parametros de entrada
   if P_JUGADOR is null then
      return 'Debe indicar un nombre de jugador';
   elseif not (P_NUMERO >= 0 and P_NUMERO < 1000) 
               or P_NUMERO is null then
      return 'Debe indicar un numero entre 0 y 999';
   end if;
 
   set V_JUEGO = OBTENER_JUEGO(P_JUGADOR);
   set V_NUMERO = OBTENER_NUMERO(V_JUEGO);
   set V_INTENTOS = INCREMENTAR_INTENTOS(V_JUEGO);
 
   if V_NUMERO = P_NUMERO then
      call FINALIZAR_JUEGO(V_JUEGO);
      set V_RETORNO = concat('Correcto, ha necesitado ', 
                             V_INTENTOS, ' intentos');
   else
      if V_NUMERO < P_NUMERO then
         set V_RETORNO = 'El número secreto es menor que';
      elseif V_NUMERO > P_NUMERO then
         set V_RETORNO = 'El número secreto es mayor que';
      end if;
 
      set V_RETORNO = concat(V_RETORNO, ' ', P_NUMERO,
                             '. Intentos: ', V_INTENTOS);     
   end if;   
   return V_RETORNO;
end; 
//

-- TRIGGERS

create TRIGGER ARTICULOS_TRG 
before update on ARTICULOS for each row
begin
   if NEW.PRECIO is null then
      set NEW.PRECIO = OLD.PRECIO;
   end if;

   set NEW.AUDITORIA = localtime;
end;
//

create TRIGGER LINEAS_FACTURA_INS_TRG 
before insert on LINEAS_FACTURA for each row
begin
   set NEW.TOTAL_LINEA =  NEW.PRECIO * NEW.CANTIDAD;
   update FACTURAS
      set TOTAL_FACTURA = TOTAL_FACTURA + NEW.TOTAL_LINEA
    where ID_FACTURA = NEW.ID_FACTURA;
end;
//

create TRIGGER LINEAS_FACTURA_DEL_TRG 
after delete on LINEAS_FACTURA for each row
begin
   update FACTURAS
      set TOTAL_FACTURA = TOTAL_FACTURA - OLD.TOTAL_LINEA
    where ID_FACTURA = OLD.ID_FACTURA;
end;
//

create TRIGGER LINEAS_FACTURA_UPD_TRG 
before update on LINEAS_FACTURA for each row
begin
   -- declaración de variables
   declare V_VARIACION float; 
 
   -- calculos
   set NEW.TOTAL_LINEA = NEW.PRECIO *  NEW.CANTIDAD;
   set V_VARIACION = NEW.TOTAL_LINEA - OLD.TOTAL_LINEA;
 
   -- actualizacion del total factura
   update FACTURAS
      set TOTAL_FACTURA = TOTAL_FACTURA + V_VARIACION
    where ID_FACTURA = NEW.ID_FACTURA;
end;
//

DELIMITER ;

ALTER TABLE juego
CHANGE COLUMN ID_JUEGO ID_JUEGO INT(11) NOT NULL AUTO_INCREMENT;

