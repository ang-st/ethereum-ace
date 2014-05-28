# acetest.py - Local test support code for ace.
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
import serpent

import project_structure

# processblock.debug = 1


def load_serpent(filename):
    return serpent.compile(open(filename).read())


class Key(object):

    def __init__(self, secret):
        self.key = utils.sha3(secret)
        self.address = utils.privtoaddr(self.key)


class Simulator(object):

    GASPRICE = 10**12
    STARTGAS = 10000

    def __init__(self, founders):
        self.founders = founders
        self.reset()

    def reset(self):
        self.genesis = blocks.genesis(self.founders)
        self.nonce = Counter()

    def load_contract(self, frm, code, endowment=0):
        _tx = transactions.contract(nonce=self.nonce[frm],
                                    gasprice=self.GASPRICE,
                                    startgas=self.STARTGAS,
                                    endowment=endowment,
                                    code=code).sign(frm.key)
        result, contract = processblock.apply_tx(self.genesis, _tx)
        assert result

        self.nonce[frm] += 1
        return contract

    def tx(self, frm, to, value, data):
        encoded_data = serpent.encode_datalist(data)
        _tx = transactions.Transaction(nonce=self.nonce[frm],
                                       gasprice=self.GASPRICE,
                                       startgas=self.STARTGAS,
                                       to=to, value=value,
                                       data=encoded_data).sign(frm.key)
        result, ans = processblock.apply_tx(self.genesis, _tx)
        assert result

        self.nonce[frm] += 1
        return serpent.decode_datalist(ans)

    def get_storage_data(self, contract, index):
        return self.genesis.get_storage_data(contract, index)

    def get_storage_dict(self, contract):
        return self.genesis.get_storage(contract).to_dict()

    
def get_development_accounts():
    config = project_structure.load_config("development")
    accounts = {}
    accounts_section = config["accounts"]
    for account in accounts_section.keys():
        accounts[account] = Key(accounts_section[account])
    return accounts
