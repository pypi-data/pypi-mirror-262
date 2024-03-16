# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/9/5 17:14
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : __init__.py.py
# @Software: PyCharm
"""
from typing import Dict, Optional
import os

from .s3 import S3BlobStore
from .blobstore import KIND_S3, blobstore_config


def blobstore(kind: str, endpoint: str, config: Optional[Dict]):
    """
    Initialize a blobstore.

    Args:
        kind: blobstore kind
        endpoint: blobstore endpoint
        config: blobstore config
    """
    if kind == KIND_S3:
        return S3BlobStore(endpoint=endpoint, config=config)
    else:
        raise ValueError("Unsupported filesystem kind: {}".format(kind))


def download_by_filesystem(filesystem, file_path: str, dest_path: str):
    """
    Download a file by filesystem.
    """
    client = blobstore(*blobstore_config(filesystem=filesystem))

    meta_list = client.list_meta(path=file_path)
    for meta in meta_list:
        dest_file = os.path.join(dest_path, meta.name)
        if not os.path.exists(os.path.dirname(dest_file)):
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
        client.download_file(path=meta.url_path, file_name=dest_file)
