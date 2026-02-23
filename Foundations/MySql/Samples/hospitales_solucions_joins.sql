-- 1) Mostra el nom dels hospitals i los pacients extranjers que hi ha a la localitat de Toledo.

	-- En aquest cas, fer-ho amb inner join o left join és el mateix ja que tots els hospitals estan a la taula de "pacientes" i "hospitales" 
	select h.nombre, p.nombre
	from hospitales h inner join pacientes p on h.hospital_id = p.hospital_id
	where localidad = "Toledo" and nacionalidad = "extranjera";

	select h.nombre, p.nombre
	from hospitales h left join pacientes p on h.hospital_id = p.hospital_id
	where localidad = "Toledo" and nacionalidad = "extranjera";

-- 2) Mostra el nom dels hospitals i la quantitat d'especialitats que hi ha als hospitals de la consulta anterior.

	-- En aquest cas, fer-ho amb inner join o left join és el mateix ja que tots els hospitals estan a la taula de "especialidades" i "hospitales" 
	select h.nombre, count(especialidad) as num_especialidades
	from hospitales h inner join especialidades e on h.hospital_id = e.hospital_id
	where localidad = "Toledo"
    group by h.nombre;
    
    select h.nombre, count(especialidad) as num_especialidades
	from hospitales h left join especialidades e on h.hospital_id = e.hospital_id
	where localidad = "Toledo"
    group by h.nombre;

-- 3) Mostra el nom del hospital i les especialitats que té l'hospital amb identificador 105.

	-- En aquest cas, fer-ho amb inner join o left join és el mateix ja que tots els hospitals estan a la taula de "especialidades" i "hospitales" 
	select h.nombre, especialidad
	from hospitales h inner join especialidades e on h.hospital_id = e.hospital_id
	where h.hospital_id = 105;

	select h.nombre, especialidad
	from hospitales h left join especialidades e on h.hospital_id = e.hospital_id
	where h.hospital_id = 105;

-- 4) Digues quants hospitals tenen dades a la taula "hospitales" però no tenen dades a la taula de "pacientes".
	select count(*) 
	from hospitales h left join pacientes p on h.hospital_id = p.hospital_id
	where p.nombre is null;

-- 5) Mostra el nom de l'hospital que té menys especialitats fixes.

	-- Si ho fem només amb JOINs aconseguim un resultat estàtic. En aquest cas hi ha 2 hospitals empatats. Perquè surtin tots de forma dinàmica caldria fer servir subqueries (veure següent solució).
	select h.nombre, count(*)
	from hospitales h left join especialidades e on h.hospital_id = e.hospital_id
    where e.fija = "S"
    group by h.nombre
    order by count(*)
	limit 1;
	
    -- Solució dinàmica usant subqueries
	SELECT h.nombre, COUNT(*) AS num_especialidades
	FROM hospitales h INNER JOIN especialidades e ON h.hospital_id = e.hospital_id
    where e.fija = "S"
	GROUP BY h.nombre
	HAVING COUNT(*)
	= (
			select count(*)
			from especialidades e 
			where e.fija = "S"
			group by e.hospital_id
			order by count(*)
			limit 1
			);

-- 6) Mostra el nom i el nombre total de visites de l'hospital amb identificador 45.
	select h.hospital_id , h.nombre, sum(p.numero_visitas) 
	from hospitales h left join pacientes p on h.hospital_id = p.hospital_id
	where h.hospital_id=45
	group by 1,2;

-- 7) Mostra el nom de l'hospital, el nom dels seus pacients estrangers i el nombre de visites, així com les especialitats que NO són fixes. Totes aquestes dades de l'hospital amb identificador 45.
	select h.hospital_id , h.nombre, p.nombre, numero_visitas, especialidad 
	from hospitales h left join pacientes p on h.hospital_id = p.hospital_id
						left join especialidades e on h.hospital_id = e.hospital_id
	where h.hospital_id=45 and e.fija = "N" and p.nacionalidad = "extranjera";

-- 8) Suma el "numero_visitas" de la consulta anterior (a mà) i compara-la amb el "numero_visitas" de la consulta núm. 6. Són iguals? Què està passant?
	
    -- Les dades dels pacients i les especialitats no es poden analitzar junts ja que estan a nivell de hospital.
    -- És a dir, no podem saber amb les taules que tenim les especialitats per pacient.
    -- Això provoca duplicats si intentem treure en la mateixa consulta camps de les dues taules.

