
DROP FUNCTION IF EXISTS fn_generic_report(CHARACTER, CHARACTER, timestamp with time zone, timestamp with time zone);

CREATE OR REPLACE FUNCTION fn_generic_report(
	_locationUuid CHARACTER(36),
	_templateUuid CHARACTER(36),
  _fromDate TIMESTAMP WITH TIME ZONE,
  _toDate TIMESTAMP WITH TIME ZONE
)
  RETURNS TABLE(
    uuid CHARACTER VARYING,
    location_name CHARACTER VARYING,
	  location_uuid CHARACTER VARYING,
    score BIGINT,
	  score_percentage BIGINT,
    final_comments CHARACTER VARYING,
    parsed_question_uuid CHARACTER VARYING,
    question_text CHARACTER VARYING,
	  question_uuid CHARACTER VARYING,
    category_text CHARACTER VARYING,
    category_uuid CHARACTER VARYING,
    worth INT,
    is_passed BOOLEAN,
    answer_notes CHARACTER VARYING,
	  template_uuid CHARACTER VARYING,
	  template_name CHARACTER VARYING,
    date_submitted TIMESTAMP WITH TIME ZONE
  )
LANGUAGE 'plpgsql'
COST 100
VOLATILE
ROWS 1000

AS $BODY$

DECLARE _row record;
  
BEGIN

  FOR _row IN(
          SELECT pa.uuid as uuid, pa.date_submitted as date_submitted, pq.uuid as pq_uuid, q.uuid as q_uuid, q.text as q_text, 
	  			  pq.worth as worth, pq.passed as is_passed, pq.notes as answer_notes,
                  pa.score as score, pa.score_percentage as score_percentage, pa.final_comments as final_comments,
	  			  prem.name as prem_name, prem.uuid as prem_uuid, c.uuid as c_uuid, c.text as c_text, atemp.uuid as at_uuid, atemp.name as at_name
          FROM parsed_question pq
	  	  	JOIN parsed_audit pa on pa.id = pq.parsed_audit
	  		JOIN question q on q.id = pq.question
	  		JOIN category c on c.id = q.category
	  		JOIN premises prem on pa.premises = prem.uuid
	  		JOIN audit_template atemp on atemp.id = pa.audit_template
	  	WHERE
		  (pa.premises::text = _locationUuid OR _locationUuid = '')
		  AND (atemp.uuid::text = _templateUuid OR _templateUuid = '')
         AND (
		    pa.date_submitted >= _fromDate
            AND pa.date_submitted <=  _toDate
          )
  )

  LOOP	
    uuid := _row.uuid;
    location_name := _row.prem_name;
	  location_uuid := _row.prem_uuid;
    score := _row.score;
	  score_percentage := _row.score_percentage;
    final_comments := _row.final_comments;
    parsed_question_uuid := _row.pq_uuid;
    question_text := _row.q_text;
	  question_uuid := _row.q_uuid;
    category_text := _row.c_text;
    category_uuid := _row.c_uuid;
    worth := _row.worth;
    is_passed := _row.is_passed;
    answer_notes := _row.answer_notes;
	  template_uuid := _row.at_uuid;
	  template_name := _row.at_name;
    date_submitted := _row.date_submitted;
    RETURN NEXT;
  END LOOP;

END;


$BODY$;


-- select * from fn_generic_report('6e79e424-1c86-4534-86f6-dcd9a37b3ca9', '6decc7d5-adcf-49bd-83bc-7bc8cc9d64a5', '2022-02-01 00:00:00.000+300', '2022-02-03 00:00:00.000+300');
