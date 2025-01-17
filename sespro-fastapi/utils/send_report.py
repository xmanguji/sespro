import logging
import typing
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import time

import boto3
from botocore.config import Config

from core.config import settings
from utils.s3_helper import get_raw_data

logger = logging.getLogger(__name__)
client = boto3.client("ses",
                      config=Config(signature_version='s3v4'),
                      region_name=settings.AWS_REGION)


def _send_debug_report(subject: str = 'MQMv2 Report Exception',
                       msg: str = 'Debug Test',
                       fr: str = 'claire@methodmill.com',
                       to: typing.List[str] = None):
    logger.info(subject, msg, fr, to)


def generate_report_subject(premises_name: str, auditor_name: str, score: str, uk: bool = True) -> str:
    today = date.today().strftime('%d-%m-%Y') if uk else date.today().strftime('%m-%d-%Y')
    return f'Audit Report {today} by {auditor_name} - {premises_name} - {score}'


def generate_report_body(auditor_name: str, app_name: str) -> str:
    lines = [
        f'{auditor_name.strip()},',
        '\n\n',
        'Here is the audit report you have generated',
        '\n\n',
        'Sincerely,',
        '\n',
        app_name
    ]

    return ''.join(lines)


def generate_email_filename(auditor_name: str) -> str:
    today = date.today().strftime('%Y-%m-%d')
    unixt: int = int(time())
    today = f'{today}-{unixt}'
    return f'{auditor_name}-{today}.pdf'


def send_error_report(traceback: str, from_email: str, to_emails: list, subject: str = 'Report API Error'):
    to_emails = list(set(to_emails))
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ','.join(to_emails)
    msg.preamble = 'Multipart message\n'
    body_part = MIMEText(traceback, 'plain')
    msg.attach(body_part)
    client.send_raw_email(Source=from_email, Destinations=to_emails, RawMessage={'Data': msg.as_string()})


def send_audit_report(from_email: str, subject: str, body: str,
                      s3_pdf: str, email_attachment_name: str,
                      to_emails: typing.List[str],
                      bcc_emails: typing.List[str]):
    to_emails = list(set(to_emails))
    bcc_emails = list(set(bcc_emails))

    all_emails = list({*to_emails, *bcc_emails})

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ','.join(to_emails)
    msg['Bcc'] = ','.join(bcc_emails)

    msg.preamble = 'Multipart message\n'

    # fetch file s3
    res = get_raw_data(f'pdfs/{s3_pdf}', settings.AWS_S3_BUCKET)
    if not res["success"]:
        raise RuntimeError(f'PDF key given does not exist: {s3_pdf}')

    # no decoding, must be bytes
    pdf_data = res["obj_json"].read()

    part = MIMEApplication(pdf_data)
    part.add_header('Content-Disposition',
                    'attachment',
                    filename=email_attachment_name)
    part.add_header('Content-Type', 'application/pdf')

    body_part = MIMEText(body, 'plain')
    msg.attach(body_part)

    msg.attach(part)

    client.send_raw_email(Source=from_email, Destinations=all_emails, RawMessage={'Data': msg.as_string()})
