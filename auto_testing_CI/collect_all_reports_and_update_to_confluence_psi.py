import glob
import sys
import generate_rc_report_content_for_each_testing_type_psi
import generate_rc_report_content_for_all_testings_psi
import confluence_client
import ci3_error

class CollectAllReportsAndUpdateToConfluence():

  def __init__(self, username, password, confluence_username, confluence_password, et_rc_version, title, space, parent_page):
    self.username = username
    self.password = password
    self.confluence_username = confluence_username
    self.confluence_password = confluence_password
    self.et_rc_version = et_rc_version
    self.each_rc_report = ""
    self.file = file
    self.build_name_list = ['errata-qe-test/errata-qe-test-e2e-post-merge-pipeline', 'errata-qe-test/errata-qe-test-baseline-performance-pipeline',
                            'errata-qe-test/errata-qe-test-bug-regression-pipeline', 'errata-qe-test/errata-qe-test-ts2-post-merge-pipeline']
    self.all_rc_report = generate_rc_report_content_for_all_testings_psi.GenerateAllReports()
    self.final_report = ""
    self.title = title
    self.space = space
    self.parent_page = parent_page

  def generate_report_for_each_test_type(self):
    for build_name in self.build_name_list:
      print "==== Generate report for the build: ", build_name
      self.each_rc_report = generate_rc_report_content_for_each_testing_type_psi.GenerateRCReportContent(
          self.username, self.password, self.confluence_username, self.confluence_password, build_name, self.et_rc_version)
      self.each_rc_report.generate_rc_report_for_current_rc_version()

  def collect_report_for_all_testings(self):
    self.all_rc_report.generate_all_reports()

  def run_generate(self):
    self.generate_report_for_each_test_type()
    self.collect_report_for_all_testings()
    self.final_report = self.all_rc_report.general_reports_content

  def add_page_to_confluence(self):
    confulence_api_client = confluence_client.ConfluenceClient(
        self.confluence_username, self.confluence_password, self.title, self.space, self.final_report, self.parent_page)
    confulence_api_client.create_update_page()

  def collect_reports_and_update_to_confluence(self):
    self.run_generate()
    self.add_page_to_confluence()

if __name__ == "__main__":
  if len(sys.argv) < 8:
    raise ci3_error.CollectAllReportsAndAddToConfluenceInputError
  else:
    username = sys.argv[1]
    password = sys.argv[2]
    confluence_username = sys.argv[3]
    confluence_password = sys.argv[4]
    et_rc_version = sys.argv[5]
    title = sys.argv[6]
    space = sys.argv[7]
    parent_page = sys.argv[8]
  regenerate_reports = CollectAllReportsAndUpdateToConfluence(
      username, password, confluence_username, confluence_password, et_rc_version, title, space, parent_page)
  regenerate_reports.collect_reports_and_update_to_confluence()
