from model import DatabaseScript
import os
import hashlib as hs
from database import db, db_instance
from pony.orm import commit, db_session
from core.security import logger


def initScript():

    db = db_instance()

    migration_script_path = "./migration"

    logger.info("Entered initscript")

    try:
        os.chdir(migration_script_path)
    except:
        logger.info("All script has been completed")
        print("All script has been complete")

    for script_file in os.listdir():

        logger.info("Found the script file %s", str(script_file))
        # Check whether file is in text format or not
        if script_file.endswith(".sql"):
            file_path = f"{script_file}"
            # call read text file function
            database_script = DatabaseScript.get(scriptName=str(script_file))

            script = read_text_file(script_file)

            if database_script is None or database_script.hash != str(hash_script_file(script_file)):

                print(f"Started executing the script file %s", str(script_file))

                db.execute(script)

                DatabaseScript(scriptName=script_file, hash=str(hash_script_file(script_file)))

                db.commit()

                logger.info("Completed executing the script file %s", str(script_file))

            else:
                logger.info("The script has been already executed %s", str(script_file))

        else:
            logger.info("Found the script file %s is not a db script", str(script_file))

def read_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def hash_script_file(file_path):
    hash_sha1 = hs.sha1()
    with open(file_path, 'rb') as file:
        buffer = file.read()
        hash_sha1.update(buffer)
    return hash_sha1.hexdigest()