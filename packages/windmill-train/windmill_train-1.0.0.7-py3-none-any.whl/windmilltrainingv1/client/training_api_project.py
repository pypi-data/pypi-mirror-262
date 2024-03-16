#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/6
# @Author  : yanxiaodong
# @File    : training_api_project.py
"""
import re

project_name_regex = re.compile("^workspaces/(?P<workspace_id>.+?)/projects/(?P<project_name>.+?)$")


def parse_project_name(name: str):
    """
    Get workspace id, project local name from project name.
    """
    m = project_name_regex.match(name)
    if m is None:
        return None, None
    return m[project_name_regex.groupindex["workspace_id"]], \
        m[project_name_regex.groupindex["project_name"]]


def get_project_name(workspace_id: str, project_name: str):
    """
    Get project name.
    """
    return "workspaces/" + workspace_id + "/projects/" + project_name