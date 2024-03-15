#!/usr/bin/python3

import os.path
import requests
from tqdm import tqdm


def download_url(url: str, path: str = None, *, fname: str = None):
    if fname is None or not fname:
        fname = url.split("/")[-1].strip()

    path = os.path.expanduser(os.path.join(path, fname)) if path is not None else fname

    if os.path.exists(path):
        raise FileExistsError(f"'{path}' already exists.")

    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))

    # Can also replace 'file' with a io.BytesIO object
    with open(path, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)