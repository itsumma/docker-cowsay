#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.

from collections import Counter
from jira import JIRA
import re, subprocess
import commands

jira = JIRA('https://itsumma.atlassian.net/', basic_auth=('admin', 'feefeizoh1gaeF'))    # a username/password tuple

def get_last_ver(releases):
    last_ver = max([int(x.name.split(" v")[1]) for x in releases if "Release v" in x.name])
    return last_ver

def get_version_object_by_num(project, number):
    project_versions = jira.project_versions(project)
    for ver in project_versions:
        if ver.name.endswith(" v%d" % number):
            return ver

def get_commit_issue_number(line):
    issue_name = re.search("JIR-\d+", line).group(0)
    if issue_name:
        return issue_name
    else:
        return ''

def ver_to_dict(versions):
    new_list = []
    for i in versions:
        new_list.append({'name': i.name, 'id': i.id})

    return new_list


projects = jira.projects()

jira_project_tag = "JIR"

project = jira.project(jira_project_tag)

# GETTING PROJECT INFO
print "PROJECT NAME:", project.name
# print project
# versions = jira.project_versions(project)
# last_ver = get_last_ver(versions)
# new_ver = last_ver + 1
# print "PROJECT VERSIONS:"
# for ver in versions:
#     print ver.id
#     print ver.name
    # print ver.released

# GETTING NEW COMMITS INFO
issues_to_update = []
git_log = commands.getstatusoutput(
        "/usr/bin/git log master...dev --pretty=short | /usr/bin/grep %s" % jira_project_tag
    )[1]
for i in git_log.split("\n"):
    issue_number = get_commit_issue_number(i)
    if not issue_number in issues_to_update:
        issues_to_update.append(issue_number)
print issues_to_update

# CHECKING UNREALISED VERSIONS OR CREATING NEW ONE
unreleased_versions = []
for ver in jira.project_versions(project):
    if not ver.released:
        unreleased_versions.append(ver)
if unreleased_versions:
    last_num = get_last_ver(unreleased_versions)
    version_to_release = get_version_object_by_num(project, last_num)
else:
    last_ver = get_last_ver(jira.project_versions(project))
    new_ver = last_ver + 1
    version_to_release = jira.create_version(project=project.key,
                    name="Release v%d" % new_ver,
                    description="ololo")
print version_to_release

# issues = jira.issues()
# for iss in issues:
#     print iss

# ADDING VERSION TO THE ISSUE
for iss in issues_to_update:
    version = []
    version.append(version_to_release)
    jira.issue(iss).update(fields={'versions': ver_to_dict(version)})
# print jira.issue('JIR-1').fields.versions
# new_versions = jira.issue('JIR-1').fields.versions
# new_versions.append(version_to_release)
# print new_versions
# jira.issue('JIR-1').update(fields={'versions': ver_to_dict(new_versions)})

    # Parameters: 
    # name – name of the version to create
    # project – key of the project to create the version in
    # description – a description of the version
    # releaseDate – the release date assigned to the version
    # startDate – The start date for the version