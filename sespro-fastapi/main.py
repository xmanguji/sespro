from core.factory import create_app
from mangum import Mangum
from database import db, db_instance
from pony.orm import commit, db_session
from migration.initalization_script import initScript
import os
import hashlib as hs

app = create_app(create_tables=True, check_tables=False)


@app.on_event("startup")
@db_session
def startup_event():

    initScript()


app = Mangum(app)