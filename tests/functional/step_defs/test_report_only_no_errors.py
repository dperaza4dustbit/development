# -*- coding: utf-8 -*-
"""Report only submission

Partners, redhat and community users can publish their chart by submitting
error-free report that was generated by chart-verifier.
"""
import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)

from functional.utils.chart_certification import ChartCertificationE2ETestSingle

@pytest.fixture
def workflow_test():
    test_name = 'Test Chart Report Only'
    test_report = 'tests/data/report.yaml'
    workflow_test = ChartCertificationE2ETestSingle(test_name=test_name, test_report=test_report)
    yield workflow_test
    workflow_test.cleanup()


@scenario('../features/report_without_chart.feature', "A partner or redhat associate submits an error-free report")
def test_partner_or_redhat_user_submits_report():
    """A partner or redhat associate submits an error-free report."""

@scenario('../features/report_without_chart.feature', "A community user submits an error-free report")
def test_community_user_submits_report():
    """A community user submits an error-free report"""

@given(parsers.parse("the vendor <vendor> has a valid identity as <vendor_type>"))
def user_has_valid_identity(workflow_test, vendor, vendor_type):
    """the vendor <vendor> has a valid identity as <vendor_type>."""
    workflow_test.set_vendor(vendor, vendor_type)


@given(parsers.parse("an error-free report is used in <report_path>"))
def user_has_created_error_free_report(workflow_test, report_path):
    """an error-free report is used in <report_path>."""
    workflow_test.update_test_report(report_path)
    workflow_test.setup_git_context()
    workflow_test.setup_gh_pages_branch()
    workflow_test.setup_temp_dir()
    workflow_test.process_owners_file()
    workflow_test.process_report()


@when("the user sends a pull request with the report")
def user_sends_pull_request_with_report(workflow_test):
    """the user sends a pull request with the report."""
    workflow_test.send_pull_request()


@then("the user sees the pull request is merged")
def user_should_see_pull_request_getting_merged(workflow_test):
    """the user sees the pull request is merged."""
    workflow_test.check_workflow_conclusion(expect_result='success')
    workflow_test.check_pull_request_result(expect_merged=True)


@then("the index.yaml file is updated with an entry for the submitted chart")
def index_yaml_is_updated_with_new_entry(workflow_test):
    """The index.yaml file is updated with a new entry."""
    workflow_test.check_index_yaml()

@then("the pull request is not merged")
def the_pull_request_is_not_getting_merged(workflow_test):
    """the pull request is not merged"""
    workflow_test.check_workflow_conclusion(expect_result='failure')
    workflow_test.check_pull_request_result(expect_merged=False)

@then(parsers.parse("user gets the <message> in the pull request comment"))
def user_gets_the_message_in_the_pull_request_comment(workflow_test, message):
    """user gets the message in the pull request comment"""
    workflow_test.check_pull_request_comments(expect_message=message)