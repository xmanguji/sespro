import json
import os
import subprocess
import sys
import tempfile

mqm_reporting_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'mqm-reporting',
                 'src'))


def get_actual_python_interpreter() -> str:
    # our friend uWSGI loves to change sys.executable, for some reason- also violating the guarantees set out in
    # the Python documentation.
    if 'uwsgi' not in sys.executable.lower():
        return sys.executable

    data = subprocess.check_output(f'which python3',
                                   shell=True,
                                   env=os.environ).strip().decode('utf8')
    return data


python_interpreter: str = get_actual_python_interpreter()


class PDFGenError(Exception):
    def __init__(self, traceback_message: str):
        self.traceback_message = traceback_message


def create_pdf_report(json_data) -> str:
    # race condition with file handle write exclusivity here but i'm too lazy to pass a file handle to a subprocess
    # so whatever
    # also the caller of this has to take care to delete the file.
    of, filename = tempfile.mkstemp()
    os.close(of)

    p = subprocess.Popen([python_interpreter, 'generate_pdf.py', filename],
                         cwd=mqm_reporting_folder,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    out_data, _ = p.communicate(json_data.encode('utf8'))

    js = json.loads(out_data)

    if 'error' in js:
        raise PDFGenError(js['error'])

    return js['pdf']
