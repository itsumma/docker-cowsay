#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# This script shows how to connect to a JIRA instance with a
# username and password over HTTP BASIC authentication.

from collections import Counter
from jira import JIRA
import re, subprocess
import commands

# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
# See
# https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK
# for details.
jira = JIRA('https://itsumma.atlassian.net/', basic_auth=('admin', 'feefeizoh1gaeF'))    # a username/password tuple

# # Get the mutable application properties for this server (requires
# # jira-system-administrators permission)
# props = jira.application_properties()

# # Find all issues reported by the admin
# issues = jira.search_issues('assignee=admin')

# # Find the top three projects containing issues reported by admin
# top_three = Counter(
#     [issue.fields.project.key for issue in issues]).most_common(3)

def get_last_ver(releases):
    last_ver = max([int(x.name.split(" v")[1]) for x in releases if "Release v" in x.name])
    return last_ver

def get_commit_number(line):
    issue_name = re.search("JIR-\d+", line).group(0)
    if issue_name:
        return issue_name.split("-")[1]
    else:
        return ''

def ver_to_dict(versions):
    new_list = []
    for i in versions:
        new_list.append({'name': i.name, 'id': i.id})

    return new_list


projects = jira.projects()
for i in projects:
    print "PROJECT NAME:", i.name
    versions = jira.project_versions(i)
    last_ver = get_last_ver(versions)
    new_ver = last_ver + 1
    print "PROJECT VERSIONS:"
    for ver in versions:
        print ver.id
        print ver.name
        # print ver.released

    # GETTING NEW COMMITS INFO
    # git_log = subprocess.check_output(['/usr/bin/git log master...dev --pretty=short | /usr/bin/grep JIR'])
    git_log = commands.getstatusoutput("/usr/bin/git log master...dev --pretty=short | /usr/bin/grep JIR")
    print git_log

    # CREATING NEW VERSION
    # jira.create_version(project=i.key,
    #                     name="Release v%d" % new_ver,
    #                     description="ololo")
    # issues = jira.issues()
    # for iss in issues:
    #     print iss

    # ADDING VERSION TO THE ISSUE
    print jira.issue('JIR-1').fields.versions
    new_versions = jira.issue('JIR-1').fields.versions
    new_versions.append(jira.version(id=10000))
    print new_versions
    # jira.issue('JIR-1').update(fields={'versions': ver_to_dict(new_versions)})

        # Parameters: 
        # name – name of the version to create
        # project – key of the project to create the version in
        # description – a description of the version
        # releaseDate – the release date assigned to the version
        # startDate – The start date for the version