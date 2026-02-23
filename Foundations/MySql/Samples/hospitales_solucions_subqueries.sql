-- 1) Mostra el nom del hospital amb més pressupost de cada comunitat autònoma.

	-- Subquery al WHERE (filtre)
		-- Opció amb 2 camps al where
		select comunidad_autonoma, nombre
		from hospitales
		where
			(comunidad_autonoma, presupuesto_anual_millones) in
			(	select comunidad_autonoma, max(presupuesto_anual_millones)
				from hospitales
				group by comunidad_autonoma);
			
		-- Opció amb 1 camp al where
		select comunidad_autonoma, nombre
		from hospitales
		where
			presupuesto_anual_millones in
			(	select max(presupuesto_anual_millones)
				from hospitales
				group by comunidad_autonoma);
			
	-- Subquery al FROM
	select h.comunidad_autonoma, h.nombre
	from hospitales h left join 
		(select comunidad_autonoma, max(presupuesto_anual_millones) as pres
				from hospitales
				group by comunidad_autonoma) max_presupuesto_ca
		on (h.comunidad_autonoma = max_presupuesto_ca.comunidad_autonoma)
	where presupuesto_anual_millones = pres;
    
	-- Subquery correlacionada
    SELECT comunidad_autonoma, nombre
	FROM hospitales T1
	WHERE presupuesto_anual_millones = (SELECT MAX(presupuesto_anual_millones)
										FROM hospitales T2
										WHERE T1.comunidad_autonoma = T2.comunidad_autonoma)
	ORDER BY comunidad_autonoma;

-- 2) Mostra el nom de l'hospital i el nom del pacient que te menys edat de cada hospital.

	-- Subquery al WHERE (filtre)
		-- Opció amb 2 camps al where
		select h.nombre, p.nombre , p.edad
		from hospitales h join pacientes p on h.hospital_id = p.hospital_id
		where (p.hospital_id, p.edad) in
		(select hospital_id, min(edad)
		from pacientes
		group by hospital_id)
        order by 1;
    
		-- ERROR! En aquest cas no es pot fer amb un únic camps al filtre ja que surten més hospitals
		select h.nombre, p.nombre , p.edad
		from hospitales h join pacientes p on h.hospital_id = p.hospital_id
		where p.edad in
		(select min(edad)
		from pacientes
		group by hospital_id)
        order by 1;

	-- Subquery al FROM
	select h.nombre, p.nombre , p.edad
	from 	pacientes p	join hospitales h on h.hospital_id = p.hospital_id
					join (select hospital_id, min(edad) min_edad
						from pacientes
						group by hospital_id) min_edad_hosp on h.hospital_id = min_edad_hosp.hospital_id
	where p.edad = min_edad
	order by 1;
    
    -- Subquery correlacionada (triga molt més que les altres opcions)
    SELECT h.nombre, p1.nombre , p1.edad
	FROM pacientes p1 JOIN hospitales h ON p1.hospital_id = h.hospital_id
	WHERE p1.edad = (SELECT MIN(edad)
						FROM pacientes p2
                        WHERE p2.hospital_id = p1.hospital_id);

-- 3) Mostra els hospitals que estàn per sobre de la mitja de "indice_satisfaccion" de cada comunidad autònoma

	-- En aquest cas no és possible fer-la al WHERE (filtre)

    -- Subquery al FROM
	select nombre, indice_satisfaccion 'is_hospital', avg_is 'is_medio_ccaa'
	from hospitales left join 
		(select comunidad_autonoma, avg(indice_satisfaccion) avg_is
		from hospitales
		group by comunidad_autonoma) sub_tabla
		on (hospitales.comunidad_autonoma=sub_tabla.comunidad_autonoma)
	where indice_satisfaccion > avg_is
	order by 2;

	-- Subquery correlacionada
	SELECT h1.nombre, h1.indice_satisfaccion 'is_hospital'
	FROM
		hospitales h1
	WHERE
		h1.indice_satisfaccion > (SELECT AVG(indice_satisfaccion)
							FROM
								hospitales h2
							WHERE h1.comunidad_autonoma = h2.comunidad_autonoma)
							-- no hace falta group by porque ya se está igualando por la comunidad autonoma
	order by 2;
