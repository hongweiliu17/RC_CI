# /bin/env python
# -*- coding: utf-8 -*-
import jenkins
import os
import sys

RC_Jenkins = os.environ.get(
    'RC_Jenkins_URL') or 'https://errata-jenkins.rhev-ci-vms.eng.rdu2.redhat.com'
Build_Job = 'deployment-packages'


class TalkToRCCIForLatestDevBuild():
    def __init__(self, username, password, build_name=Build_Job):
        self.username = username
        self.password = password
        self.build_name = build_name
        self.server = jenkins.Jenkins(RC_Jenkins, self.username, self.password)
        self.et_build_version = ""

    def get_lastest_build_number(self):
        return self.server.get_job_info(self.build_name)['lastBuild']['number']

    def get_latest_successful_build_number(self):
        return self.server.get_job_info(self.build_name)['lastSuccessfulBuild']['number']

    def get_dev_build(self):
        ready_build = self.get_latest_successful_build_number()
        latest_build = self.get_lastest_build_number()
        if ready_build == latest_build:
            print ready_build
        else:
            print "Error, the latest job to build rpm is failed. No build!"


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    if len(sys.argv) == 4:
        build_name = sys.argv[3]
        talk_to_rc_jenkins = TalkToRCCIForLatestDevBuild(
            username, password, build_name)
    else:
        talk_to_rc_jenkins = TalkToRCCIForLatestDevBuild(username, password)
    talk_to_rc_jenkins.get_dev_build()
