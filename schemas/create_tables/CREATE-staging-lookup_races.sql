DROP TABLE IF EXISTS staging.lookup_races; 
CREATE UNLOGGED TABLE staging.lookup_races (
	code                                                                  int,                --
	value                                                                 varchar,            --
	description                                                           varchar             --
);
