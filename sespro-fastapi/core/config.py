import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl, Field
from pydantic.networks import EmailStr

path = Path.cwd()

env_path = path / ".env"

load_dotenv(dotenv_path=env_path)

ENVIRONMENT = os.environ.get("ENVIRONMENT", "LOCAL")

if ENVIRONMENT == "PRODUCTION":
    database_dict = {
        "provider": "postgres",
        "host": os.getenv("PROD_DB_HOST"),
        "user": os.getenv("PROD_DB_USER"),
        "password": os.getenv("PROD_DB_PASS"),
        "database": os.getenv("PROD_DB_NAME"),
    }

elif ENVIRONMENT == "DEVELOPMENT" or ENVIRONMENT == "LOCAL":
    database_dict = {
        "provider": "postgres",
        "host": os.getenv("DEV_DB_HOST"),
        "user": os.getenv("DEV_DB_USER"),
        "password": os.getenv("DEV_DB_PASS"),
        "database": os.getenv("DEV_DB_NAME"),
    }

elif ENVIRONMENT == "TEST":
    database_dict = {
        "provider": "postgres",
        "host": os.getenv("TEST_DB_HOST"),
        "user": os.getenv("TEST_DB_USER"),
        "password": os.getenv("TEST_DB_PASS"),
        "database": os.getenv("TEST_DB_NAME"),
    }
else:
    database_dict = {"provider": "sqlite", "filename": "db.sqlite", "create_db": True}

include_pass = os.environ.get("INCLUDE_PASS", False)
if include_pass == "True":
    INCLUDE_PASS = True
elif include_pass == "False":
    INCLUDE_PASS = False
else:
    INCLUDE_PASS = False

include_na = os.environ.get("INCLUDE_NA", False)
if include_na == "True":
    INCLUDE_NA = True
elif include_na == "False":
    INCLUDE_NA = False
else:
    INCLUDE_NA = False

include_no = os.environ.get("INCLUDE_NO", False)
if include_no == "True":
    INCLUDE_NO = True
elif include_no == "False":
    INCLUDE_NO = False
else:
    INCLUDE_NO = False


class Settings(BaseSettings):
    # API settings
    API_TITLE: str = Field('Report API', env='API_TITLE')
    API_ROOT_PATH: str = Field('', env='API_ROOT_PATH')  # /path
    API_TIMEZONE: str = Field(..., env='API_TIMEZONE')  # America/Phoenix
    API_CORS_ORIGINS: List[AnyHttpUrl] = Field([], env='API_CORS_ORIGINS')  # unused

    # Application settings
    SECRET: str = Field(..., env='SECRET')
    # URLs
    CLIENT_BASE_URL: str = Field(..., env='CLIENT_BASE_URL')
    RENDER_BASE_URL: str = Field(..., env='RENDER_BASE_URL')
    # Audit options
    INCLUDE_PASS: bool = Field(False, env='INCLUDE_PASS')
    INCLUDE_NA: bool = Field(False, env='INCLUDE_NA')
    INCLUDE_NO: bool = Field(False, env='INCLUDE_NO')
    SEND_TO_AUDITOR: bool = Field(True, env='SEND_TO_AUDITOR')
    REVIEW_EDITOR: bool = Field(False, env='REVIEW_EDITOR')
    # Render/PDF options
    RENDER_TEMPLATE: str = Field(..., env='RENDER_TEMPLATE')
    EMAILER_LAMBDA: str = Field(..., env='EMAILER_LAMBDA')
    BADGE: bool = Field(False, env='BADGE')
    THUMBNAIL_HEIGHT: int = Field(512, env='THUMBNAIL_HEIGHT')
    THUMBNAIL_WIDTH: int = Field(512, env='THUMBNAIL_WIDTH')
    # Date format (US vs UK)
    UK_DATE: bool = Field(False, env='UK_DATE')
    # Blind emails for reports - debugging/monitoring
    EXTRA_BCC_EMAILS: List[str] = Field([], env='EXTRA_BCC_EMAILS')
    # Error emails
    ERROR_EMAILS: List[str] = Field([], env='ERROR_EMAILS')

    # AWS settings
    AWS_REGION: str = Field('us-east-1', env='AWS_REGION')
    # AWS S3
    AWS_S3_BUCKET: str = Field(..., env='AWS_S3_BUCKET')
    AWS_S3_IMAGE_FOLDER: str = Field(..., env='AWS_S3_IMAGE_FOLDER')
    AWS_S3_DATA_FOLDER: str = Field(..., env='AWS_S3_DATA_FOLDER')
    AWS_S3_REMAP_FOLDER: str = Field(..., env='AWS_S3_REMAP_FOLDER')
    # AWS SES
    AWS_SES_SENDER: EmailStr = Field(..., env='AWS_SES_SENDER')

    DB_DICT: dict = {}

    # Extra defaults
    API_V1_0STR: str = "/v1_0"
    API_V2_0STR: str = "/v2_0"


settings = Settings()
settings.DB_DICT = database_dict
