# development_test_class.py - Local test base class for ace.
# Adapted from:
# https://github.com/EtherCasts/evm-sim/blob/master/tests/sim.py
# Which was released under the MIT License.
# New code Copyright (C) 2014  Rob Myers <rob@robmyers.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import Counter

from pyethereum import transactions, blocks, processblock, utils
import sim

import compile_contract, project_structure

# processblock.debug = 1


def load_source(filename):
    if filename.endswith(".lll"):
        return sim.compile_lll(filename)
    else:
        return sim.compile_serpent(filename)

def get_development_accounts():
    config = project_structure.load_config("development")
    accounts = {}
    accounts_section = config["accounts"]
    for account in accounts_section.keys():
        accounts[account] = sim.Key(accounts_section[account])
    return accounts


class LocalTestBaseClass(object):
    """Local test version of AceTest"""

    CONTRACT = ""
    CREATOR = ""
    GAS_AMOUNT = 10**18

    @classmethod
    def setup_class(cls):
        # Get keys from config
        cls.code = load_source(cls.CONTRACT)
        endowments = {}
        cls.accounts = get_development_accounts()
        for account in cls.accounts.keys():
            endowments[cls.accounts[account].address] = cls.GAS_AMOUNT
        cls.sim = sim.Simulator(endowments)

    def setup_method(self, method):
        self.sim.reset()
        self.contract = self.sim.load_contract(self.accounts[self.CREATOR],
                                               self.code)
