DROP TABLE IF EXISTS staging.lookup_origination_types;
CREATE UNLOGGED TABLE staging.lookup_origination_types (
	code                                                                  int,                --
	value                                                                 varchar,            --
	description                                                           varchar             --
);
