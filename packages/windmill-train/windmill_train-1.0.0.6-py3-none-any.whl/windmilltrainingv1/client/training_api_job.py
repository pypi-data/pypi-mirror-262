#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/14
# @Author  : yanxiaodong
# @File    : training_api_job.py
"""
import re

job_name_regex = re.compile("^workspaces/(?P<workspace_id>.+?)/projects/(?P<project_name>.+?)/jobs/(?P<job_name>.+?)$")


def parse_job_name(name: str):
    """
    Get workspace id, project name and job local name from job name.
    """
    m = job_name_regex.match(name)
    if m is None:
        return None, None, None
    return m[job_name_regex.groupindex["workspace_id"]], \
        m[job_name_regex.groupindex["project_name"]], \
        m[job_name_regex.groupindex["job_name"]]