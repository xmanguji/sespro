
DROP FUNCTION IF EXISTS fn_average_score(CHARACTER, CHARACTER, timestamp with time zone, timestamp with time zone);

CREATE OR REPLACE FUNCTION fn_average_score(
	_locationUuid CHARACTER(36),
	_templateUuid CHARACTER(36),
  	_fromDate TIMESTAMP WITH TIME ZONE,
 	_toDate TIMESTAMP WITH TIME ZONE
)
    RETURNS DOUBLE PRECISION
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE
	
	AS $BODY$
	
		DECLARE _numberOfAudits INTEGER;

		BEGIN
		
		_numberOfAudits = fn_get_audits_submitted(_locationUuid, _templateUuid, _fromDate, _toDate);

      RETURN (

        SELECT SUM(pa.score_percentage)/_numberOfAudits AS average_score
        FROM parsed_audit pa
		JOIN audit_template ot on ot.id = pa.audit_template
        WHERE
		  (pa.premises::text = _locationUuid OR _locationUuid = '')
		  AND (ot.uuid::text = _templateUuid OR _templateUuid = '')
         AND (
		    pa.date_submitted >= _fromDate
            AND pa.date_submitted <=  _toDate
          )

      );

		END;


	$BODY$;


-- select * from fn_average_score('6e79e424-1c86-4534-86f6-dcd9a37b3ca9', '6decc7d5-adcf-49bd-83bc-7bc8cc9d64a5', '2022-02-01 00:00:00.000+300', '2022-02-03 00:00:00.000+300');
