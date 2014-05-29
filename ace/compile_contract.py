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

# We call Serpent from the command line
# rather than importing it and compiling directly.
# This is so Serpent isn't a dependency
# for when we support compiling more languages.

class CompileContract(object):
    """Compile the contract(s)"""
    
    def __init__(self, contract):
        """Stash the contract filepath"""
        config = project_structure.load_config()
        self.contract_language = config["ace"]["default_language"]
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
        """Format up the contract filename"""
        if contract.endswith(".py"):
            contract = re.sub("test_", "", contract)
        return project_structure.project_filepath("hex",
                                                  contract,
                                                  ".hex")
    
    def compile(self):
        """Compile the file"""
        for contract in self.contract_files:
            if os.path.exists(contract):
                hexfile = self.hex_filename(contract)
                command = self.compile_command % (contract, hexfile)
                subprocess.call(command, shell=True)
            else:
                print >>sys.stderr, "No such file: %s." % contract
