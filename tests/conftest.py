import os
import sys
import urllib3


app_root_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..', 'async_requests'
    )
)
sys.path.append(app_root_path)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)