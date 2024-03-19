#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/6
# @Author  : yanxiaodong
# @File    : training_api_dataset.py.py
"""
import re
from typing import Optional
dataset_name_regex = \
    re.compile("^workspaces/(?P<workspace_id>.+?)/projects/(?P<project_name>.+?)/datasets/(?P<dataset_name>.+?)$")


class DatasetName:
    """
    Dataset name.
    """
    def __init__(self, workspace_id: str = None, project_name: str = None, local_name: str = None):
        self.workspace_id = workspace_id
        self.project_name = project_name
        self.local_name = local_name


def parse_dataset_name(name: str) -> Optional[DatasetName]:
    """
    Get workspace id, project name and dataset name from dataset name.
    """
    m = dataset_name_regex.match(name)
    if m is None:
        return None
    return DatasetName(m.group("workspace_id"), m.group("project_name"), m.group("dataset_name"))
