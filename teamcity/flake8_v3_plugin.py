import re

from flake8.formatting import base

from teamcity.messages import TeamcityServiceMessages
from teamcity import __version__


class TeamcityReport(base.BaseFormatter):
    name = 'teamcity-messages'
    version = __version__
    messages = TeamcityServiceMessages()
    messages.message(
        'message',
        text='%s %s enabled; __file__ = %s' % (name, version, __file__))

    def format(self, error):
        position = '%s:%d:%d' % (
            error.filename, error.line_number, error.column_number)
        error_message = '%s %s' % (error.code, error.text)
        test_name = 'flake8: %s: %s' % (position, error_message)

        line = error.physical_line
        offset = error.column_number
        details = [
            line.rstrip(),
            re.sub(r'\S', ' ', line[:offset]) + '^',
        ]
        details = '\n'.join(details)

        self.messages.testFailed(test_name, error_message, details)
