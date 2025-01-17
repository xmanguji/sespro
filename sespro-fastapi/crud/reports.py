from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pony.orm.core import desc
from pydantic import BaseModel
from pony.orm import select
from schema import GenericReport

from database import db
from model import ParsedQuestion, Premises, AuditTemplate, User, Role
from datetime import datetime, timedelta, timezone
import random
from uuid import UUID

ModelType = TypeVar("ModelType", bound=db.Entity)


class Report:

    def timezoneStr(date_str: str):
        # offset_minutes = int(date_str[-3:])        
        offset_minutes = 0     
        # offset_minutes = 330

        date_str_without_tz = date_str[:-4]
        dt = datetime.strptime(date_str_without_tz, "%Y-%m-%d %H:%M:%S.%f")
        tz_offset = timedelta(minutes=offset_minutes)

        datetime_with_timezone = dt.replace(tzinfo=timezone(tz_offset))
        return datetime_with_timezone

    def generic_report(locationUuid: Optional[str], templateUuid: Optional[str], fromDate: str, toDate: str, user: User) -> Optional[List[GenericReport]]:

        results = []
        
        user = User.get(uuid=user.uuid)
        role_name = Role[user.role.id]
                
        orgUUIDs = [t.uuid for t in user.premises_organization]
        orgUUIDs = list(set(orgUUIDs))
        print('-------------- orgUUIDs -----------------', orgUUIDs)
        
        if(role_name.name == 'ROLE_ROOT'): 
            query = select(
                (pa.uuid, pa.premises, pa.date_submitted, pq.uuid, q.uuid, q.text, pq.worth, pq.passed, pq.notes, pa.score, pa.score_percentage,
                    pa.final_comments, c.uuid, c.text, atemp.uuid, atemp.name)
                for pq in ParsedQuestion
                for pa in pq.parsed_audit
                for q in pq.question
                for c in q.category
                # for prem in pa.premises
                for atemp in pa.audit_template
                if (str(pa.premises) == locationUuid or locationUuid == '') and
                (str(atemp.uuid) == templateUuid or templateUuid == '') and
                (pa.date_submitted >= Report.timezoneStr(fromDate)) and
                (pa.date_submitted <= Report.timezoneStr(toDate))
            )
        else:
            query = select(
                (pa.uuid, pa.premises, pa.date_submitted, pq.uuid, q.uuid, q.text, pq.worth, pq.passed, pq.notes, pa.score, pa.score_percentage,
                    pa.final_comments, c.uuid, c.text, atemp.uuid, atemp.name)
                for pq in ParsedQuestion
                for pa in pq.parsed_audit
                for q in pq.question
                for c in q.category
                # for prem in pa.premises
                for atemp in pa.audit_template
                if (str(pa.premises) == locationUuid or locationUuid == '') and
                (str(atemp.uuid) == templateUuid or templateUuid == '') and
                (pa.date_submitted >= Report.timezoneStr(fromDate)) and
                (pa.date_submitted <= Report.timezoneStr(toDate)) and
                atemp.organization in orgUUIDs
            )
                    
        for row in query:
            uuid, location_uuid, date_submitted, pq_uuid, q_uuid, q_text, worth, is_passed, answer_notes, score, score_percentage, final_comments, c_uuid, c_text, at_uuid, at_name = row
            
            datetime_obj = datetime.strptime(str(date_submitted), "%Y-%m-%d %H:%M:%S.%f")
            formatted_date = datetime_obj.strftime("%m-%d-%Y")

            # start_date = datetime.strptime(fromDate[:-17], '%Y-%m-%d')
            # end_date = datetime.strptime(toDate[:-17], '%Y-%m-%d')
            # time_delta = end_date - start_date
            # random_days = random.randint(0, time_delta.days)
            # random_date = start_date + timedelta(days=random_days)
            # formatted_date = random_date.strftime('%m-%d-%Y')

            result_data = {
                'uuid': uuid,
                # 'location_uuid': uuids[random.randint(0, 15)],
                'location_uuid': location_uuid,
                'score': score,
                'score_percentage': score_percentage,
                'final_comments': final_comments,
                'parsed_question_uuid': pq_uuid,
                'question_text': q_text,
                'question_uuid': q_uuid,
                'category_text': c_text,
                'category_uuid': c_uuid,
                'worth': worth,
                'is_passed': is_passed,
                'answer_notes': answer_notes,
                'template_uuid': at_uuid,
                'template_name': at_name,
                'date_submitted': formatted_date,
            }

            results.append(result_data)

        return results


    def dashboard_audits_submitted(locationUuid: Optional[str], templateUuid: Optional[str], fromDate: str, toDate: str) -> int:

        data = db.execute(f"select * from fn_get_audits_submitted('{locationUuid}', '{templateUuid}', '{fromDate}', '{toDate}')")

        result = data.fetchone()

        db.commit()

        return result

    def dashboard_audits_average_score(locationUuid: Optional[str], templateUuid: Optional[str], fromDate: str, toDate: str) -> float:

        data = db.execute(f"select * from fn_average_score('{locationUuid}', '{templateUuid}', '{fromDate}', '{toDate}')")

        result = data.fetchone()

        db.commit()

        return result

reports = Report
    

