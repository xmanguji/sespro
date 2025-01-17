-- FUNCTION: fn_get_user_premises()

DROP FUNCTION IF EXISTS fn_get_user_premises(CHARACTER);

CREATE OR REPLACE FUNCTION fn_get_user_premises(
	_userUuid CHARACTER(36)
)
    RETURNS CHARACTER VARYING[]
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE
	
	AS $BODY$
											   
		BEGIN

				RETURN ARRAY(
						SELECT prem.uuid
						FROM users AS u,  premises_user pu, premises prem
						WHERE u.uuid::text = _userUuid 
							AND (pu.user = u.id AND prem.id = pu.premises)
					
						union 
					
						select prem.uuid
						from users as u, premises_group_user pgu, premises_group pg
						join premises prem on prem.group = pg.id
						where u.uuid::text = _userUuid 
							AND (pgu.user = u.id AND pg.id = pgu.group_id)
				);
			
		END;

	$BODY$;

--  select * from fn_get_user_premises('9d7e0748-00e2-4189-8885-78c13b39a61f');
