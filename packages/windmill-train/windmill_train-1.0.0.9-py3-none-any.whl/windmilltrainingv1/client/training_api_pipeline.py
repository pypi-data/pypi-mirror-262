#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/3/15 12:17
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : training_api_pipeline.py
# @Software: PyCharm
"""
import re
from typing import Optional

pipeline_name_regex = \
    re.compile("^workspaces/(?P<workspace_id>.+?)/projects/(?P<project_name>.+?)/pipelines/(?P<pipeline_name>.+?)$")


class PipelineName:
    """
    The name of pipeline.
    """
    def __init__(self, workspace_id: str = None, project_name: str = None, local_name: str = None):
        self.workspace_id = workspace_id
        self.project_name = project_name
        self.local_name = local_name


def parse_pipeline_name(name: str) -> Optional[PipelineName]:
    """
    Get workspace id, project name and dataset pipeline from pipeline name.
    """
    m = pipeline_name_regex.match(name)
    if m is None:
        return None
    return PipelineName(m.group("workspace_id"), m.group("project_name"), m.group("pipeline_name"))

