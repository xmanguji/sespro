from typing import Union
from http import HTTPStatus
from uuid import UUID
from webbrowser import get

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from pony.orm import db_session
from core.security import get_current_active_user
from crud import reports as crud_reports
from model import User

router = APIRouter(prefix='/reports')


@router.get('/generic')
@version(1, 0)
@db_session
def reports(fromDate: str, toDate: str, locationUuid: Union[str, 'None'] = None, templateUuid: Union[str, None] = None, user: User = Depends(get_current_active_user)):
    """
    Gets the full data of a parsed audit by UUID

    Args:
        uuid: The parsed audit UUID to fetch

    Returns: The raw submitted content of the requested audit from a client application
    """
    report_data = crud_reports.generic_report(locationUuid, templateUuid, fromDate, toDate, user)

    
    return report_data


@router.get('/dashboard/totalaudits')
@version(1, 0)
@db_session
def number_of_audits_submitted(fromDate: str, toDate: str, locationUuid: Union[str, 'None'] = None, templateUuid: Union[str, None] = None, _: User = Depends(get_current_active_user)):

    audits_submitted = crud_reports.dashboard_audits_submitted(locationUuid, templateUuid, fromDate, toDate)

    return audits_submitted

@router.get('/dashboard/averagescore')
@version(1, 0)
@db_session
def audits_average_score(fromDate: str, toDate: str, locationUuid: Union[str, 'None'] = None, templateUuid: Union[str, None] = None, _: User = Depends(get_current_active_user)):

    average_score = crud_reports.dashboard_audits_average_score(locationUuid, templateUuid, fromDate, toDate)

    return average_score
