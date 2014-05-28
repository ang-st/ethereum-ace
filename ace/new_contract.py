# new_contract.py - Contract creation for ace.
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

import inspect, os, re, sys, yaml
import project_structure

class NewContract(object):
    """Create a new ethereum contract"""
    
    def __init__(self, contract_name):
        """Stash the contract details and generate various filepaths"""
        self.contract_name = os.path.splitext(contract_name)[0]
        intercaps = "".join([x.capitalize() for x in contract_name.split("_")])
        self.contract_classname = "Test" + intercaps
        test_dir = "test"
        config = project_structure.load_config()
        contract_language = config["ace"]["default_language"]
        contract_ext = project_structure.language_extension(contract_language)
        contract_dir = contract_language
        contract_filename = "%s.%s" % (self.contract_name, contract_ext)
        test_filename = config["ace"]["test_framework"] + ".py.template"
        self.test_template_filepath = os.path.join(test_dir, test_filename)
        contract_source_filename = "contract." + contract_ext
        self.contract_template_filepath = os.path.join(contract_dir,
                                                       contract_source_filename)
        # If we swap the project_structure code in, keep this as well
        self.contract_filepath = os.path.join(contract_dir, contract_filename)
        self.test_filepath = os.path.join(test_dir,
                                          "test_" + contract_name + ".py")
    
    def should_create_files(self):
        """Check whether the contract already exists"""
        return (not os.path.exists(self.contract_filepath)) \
            and (not os.path.exists(self.test_filepath))

    def create_file(self, infile, outfilepath):
        """Create the contract file"""
        template = infile.read()
        substitutions = {"%CLASSNAME%":self.contract_classname,
                         "%SOURCEFILE%":self.contract_filepath}
        content = template
        for key, value in substitutions.items():
            content = re.sub(key, value, content)
        open(outfilepath, "w").write(content)
    
    def create_files(self):
        """Create the directory structure for the project"""
        contemp = project_structure.source_file(self.contract_template_filepath)
        testtemp = project_structure.source_file(self.test_template_filepath)
        self.create_file(contemp, self.contract_filepath)
        self.create_file(testtemp, self.test_filepath)
    
    def create_contract(self):
        """Create the project as specified"""
        if self.should_create_files():
            self.create_files()
        else:
            print >> sys.stderr, "Contract file(s) already exist, not creating."
