USE m4_t2;

-- 2) Fes una "union" de les dues taules.

	SELECT * 
	FROM nenes
	UNION
	SELECT *
	FROM nens;

-- 3) Fes una "union all" de les mateixes taules i explica les diferències.    
    
	SELECT * 
	FROM nenes
	UNION ALL
	SELECT *
	FROM nens;

