# compile_contract.py - Contract compilation for ace.
# Copyright (C) 2014  Rob Myers <rob@robmyers.org>
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

import glob, os, re, subprocess, sys, yaml
import project_structure


def subproc(commands):
    """Pass array of strings to a subprocess and return result"""
    proc = subprocess.Popen(commands, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if err:
        print >>sys.stderr, err
    return out

def serpent_to_lll(filepath):
    """Load the Serpent file and compile to lll"""
    ast = subproc(["serpent", "parse", filepath])
    return subproc(["serpent", "rewrite", ast])

def serpent_to_hex(filepath):
    """Load the Serpent file and compile to hex"""
    return subproc(["serpent", "compile", filepath])

def lll_to_hex(lll):
    """Compile the lll to hex"""
    compiled = subproc(["serpent", "rewrite", lll])
    return subproc(["serpent", "compile", compiled])


class CompileContract(object):
    """Compile the contract(s)"""

    def __init__(self, contract):
        """Stash the contract filepath"""
        config = project_structure.load_config()
        self.contract_language = project_structure.contract_language(contract,
                                                                     config)
        self.contractdir = "contract"
        self.compile_command = config[self.contract_language]["compile_command"]
        contract = contract.strip()
        if contract:
            self.contract_files = [self.contract_filename(contract)]
        else:
            ext = project_structure.language_extension(self.contract_language)
            self.contract_files = project_structure.list_files(self.contractdir,
                                                               ext)

    def contract_filename(self, contract):
        """Format up the contract filename"""
        if contract.endswith(".py"):
            contract = re.sub("test_", "", contract)
        extension = project_structure.language_extension(self.contract_language)
        return project_structure.project_filepath(self.contractdir,
                                                  contract,
                                                  extension)

    def hex_filename(self, contract):
        """Make the hex filename from the contract name"""
        if contract.endswith(".py"):
            contract = re.sub("test_", "", contract)
        return project_structure.project_filepath("build",
                                                  contract,
                                                  ".hex")

    def serpent_lll_filename(self, contract):
        """Make the hex filename from the contract name"""
        if contract.endswith(".py"):
            contract = re.sub("test_", "", contract)
        return project_structure.project_filepath("build",
                                                  contract,
                                                  ".lll")

    def compile(self):
        """Compile the file"""
        for contract in self.contract_files:
            if os.path.exists(contract):
                if self.contract_language == "serpent":
                    lllfile = self.serpent_lll_filename(contract)
                    lll = serpent_to_lll(contract)
                    hexoutput = serpent_to_hex(contract)
                elif self.contract_language == "lll":
                    lll = open(contract).read()
                    hexoutput = lll_to_hex(lll)
                else:
                    raise "Unknown language: %s" % self.contract_language
                hexfile = self.hex_filename(contract)
                open(lllfile, 'w').write(lll)
                open(hexfile, 'w').write(hexoutput)
            else:
                print >>sys.stderr, "No such file: %s." % contract
