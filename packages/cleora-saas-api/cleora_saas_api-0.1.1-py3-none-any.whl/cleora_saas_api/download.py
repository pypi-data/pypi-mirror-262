import os
from cleora_saas_api.token.access_token import get_access_token
import pyrebase

from cleora_saas_api.config import FIREBASE_CONFIG, STORAGE_ROOT


def download_file(external_path: str, local_path: str, id_token):
    print("-- Result download started --")
    firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
    storage = firebase.storage()
    external_path = external_path.replace(STORAGE_ROOT, "")

    access_tk = get_access_token()

    filename = os.path.basename(local_path)
    path = os.path.dirname(local_path)
    storage.child(external_path).download(filename=filename, path=path, token=access_tk)

    print("-- Result download finished --")
