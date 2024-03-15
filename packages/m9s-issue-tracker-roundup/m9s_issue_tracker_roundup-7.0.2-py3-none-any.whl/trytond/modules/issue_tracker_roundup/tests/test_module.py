# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class IssueTrackerRoundupTestCase(ModuleTestCase):
    "Test Issue Tracker Roundup module"
    module = 'issue_tracker_roundup'


del ModuleTestCase
