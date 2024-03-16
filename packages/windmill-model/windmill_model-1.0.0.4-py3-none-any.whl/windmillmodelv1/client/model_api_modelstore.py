#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/25
# @Author  : yanxiaodong
# @File    : model_api_modelstore.py
"""
import re
from typing import Optional
modelstore_name_regex = re.compile("^workspaces/(?P<workspace_id>.+?)/modelstores/(?P<model_store_name>.+?)$")


class ModelStoreName:
    """
        The name of modelstore.
        """
    def __init__(self, workspace_id: str = None, local_name: str = None):
        self.workspace_id = workspace_id
        self.local_name = local_name


def get_name(workspace_id: str, model_store_name: str):
    """
    get name
    """
    return "workspaces/" + workspace_id + "/modelstores/" + model_store_name


def parse_modelstore_name(name: str) -> Optional[ModelStoreName]:
    """
    get local name
    """
    m = modelstore_name_regex.match(name)
    if m is None:
        return None
    return ModelStoreName(m.group("workspace_id"), m.group("model_store_name"))
