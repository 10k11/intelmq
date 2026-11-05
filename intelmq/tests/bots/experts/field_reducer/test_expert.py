# SPDX-FileCopyrightText: 2017 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.field_reducer.expert import FieldReducerExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "classification.type": "unauthorised-information-modification",
                 "time.observation": "2015-09-12T00:00:00+00:00",
                 "feed.name": "test-feed",
                 }
WHITELIST_OUTPUT = {"__type": "Event",
                    "time.observation": "2015-09-12T00:00:00+00:00",
                    }
BLACKLIST_OUTPUT = {"__type": "Event",
                    "classification.type": "unauthorised-information-modification",
                    "feed.name": "test-feed",
                    }


class TestFieldReducerExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FieldReducerExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FieldReducerExpertBot
        cls.input_message = EXAMPLE_INPUT
        cls.sysconfig = {'type': 'whitelist', 'keys': ['time.source', 'time.observation']}

    def test_whitelist(self):
        self.run_bot()
        self.assertMessageEqual(0, WHITELIST_OUTPUT)

    def test_blacklist(self):
        self.sysconfig = {'type': 'blacklist', 'keys': 'time.source, time.observation'}
        self.run_bot()
        self.assertMessageEqual(0, BLACKLIST_OUTPUT)
    def test_blacklist_extra_subfields(self):
        self.input_message = {**EXAMPLE_INPUT,
                              "extra.source.naics": 1,
                              "extra.source.sic": 2,
                              "extra.sourcefoo": 3,
                              "extra.other": 4,
                              }
        self.sysconfig = {'type': 'blacklist', 'keys': ['extra.source']}
        self.run_bot()
        self.assertMessageEqual(0, {**EXAMPLE_INPUT,
                                    "extra.sourcefoo": 3,
                                    "extra.other": 4,
                                    })

    def test_blacklist_extra_all(self):
        self.input_message = {**EXAMPLE_INPUT, "extra.a": 1, "extra.b.c": 2}
        self.sysconfig = {'type': 'blacklist', 'keys': ['extra']}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_INPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
