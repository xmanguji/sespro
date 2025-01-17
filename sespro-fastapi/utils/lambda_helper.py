import json
import logging

import boto3
from botocore.config import Config

from core.config import settings

logger = logging.getLogger(__name__)

client = boto3.client("lambda",
                      config=Config(signature_version='s3v4'),
                      region_name=settings.AWS_REGION)


def invoke_emailer(*, url: str, uuid: str, report_id: int, auditor: str, template_name, site: str, score: str, to_emails: list, bcc_emails: list) -> dict:
    payload = {
        'url': url,
        'uuid': str(uuid),
        'report_id': report_id,
        'auditor': auditor,
        'template_name': template_name,
        'site': site,
        'score': score,
        'to_emails': to_emails,
        'bcc_emails': bcc_emails
    }
    payload = json.dumps(payload)
    logger.info(payload)
    result = client.invoke(
        FunctionName=settings.EMAILER_LAMBDA,
        InvocationType='Event',  # Async call
        Payload=bytes(payload, encoding='utf8')
    )

    return result['StatusCode'] == 202  # async calls return 202 ACCEPTED if queued

# def call_emailer():
#     lambda_result = invoke_emailer(
#         url="https://8xqnzbdtv6.execute-api.us-east-1.amazonaws.com/prod/v2_0/audit/render/dcf1fa16-6acc-4d00-9897-0fe692eb7e8c?user=c099dfe7-ff5f-4f04-80a6-b41d66c15cec",
#         uuid="dcf1fa16-6acc-4d00-9897-0fe692eb7e8c",
#         report_id="dcf1fa16-6acc-4d00-9897-0fe692eb7e8c",
#         auditor="Canarcy Blues Brevard",
#         site="Canarcy Blues Brevard",
#         template_name="Canarcy  QA Full Audit",
#         score=f"{(0.93 * 100):.0f}%",
#         to_emails=['beau.tarek@gmail.com', 'dylan@juicedapps.com'],
#         bcc_emails=['zberhanu@gmail.com'])
#     print(lambda_result)

# call_emailer()