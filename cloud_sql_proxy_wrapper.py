import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import subprocess

# ---------- H E L P E R ----------
# ------- F U N C T I O N S -------

def credentials_json():
    return os.path.join(os.getenv('APPDATA'), 'gcloud', 'application_default_credentials.json')
    
def check_credentials_file():
    file_does_not_exist = "Credentials file does not exist.\n"
    gcloud_auth_message = "Make sure to run `gcloud auth application-default login` on Google Cloud SDK to create/update the credentials file.\n"
    
    try:
        __GOOGLE_APPLICATION_CREDENTIALS = Path(credentials_json())
        date_modified = datetime.fromtimestamp(
            Path(__GOOGLE_APPLICATION_CREDENTIALS).stat().st_mtime)
        print("".join([f"Latest credentials file was downloaded on {date_modified}.\n", gcloud_auth_message]))
    except FileNotFoundError:
        print("".join([file_does_not_exist, gcloud_auth_message]))

def check_cloud_sql_proxy():
        __error_msg = f"Download Cloud SQL Proxy on https://dl.google.com/cloudsql/cloud_sql_proxy_x64.exe."
        assert Path("cloud_sql_proxy.exe").exists(), __error_msg

def chdir_gcloud_sdk():
    file_path = Path(f"C:\Program Files (x86)\Google\Cloud SDK")
    os.chdir(file_path)

def instance_name(file_name: str):
    file = pd.read_json(file_name)
    return ":".join([value for value in file.iloc[0]]) + "=tcp:5432"


# ------------ M A I N ------------
if __name__ == '__main__':
    
    print("\nWelcome to Cloud SQL Proxy wrapper.\n\n")
    instances_arg = instance_name('instances.json')

    check_credentials_file()
    chdir_gcloud_sdk()
    check_cloud_sql_proxy()
    print("\nStarting cloud_sql_proxy\n")

    subprocess.run([f"./cloud_sql_proxy",
                    "".join(["-instances=", instances_arg]),
                    "".join(["-credential_file=", credentials_json()])])
