# test_contract.py - Contract testing for ace.
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

import os, re, subprocess, sys, yaml
import project_structure

class TestContract(object):
    """Run the test(s)"""
    
    def __init__(self, test):
        """Stash the test filepath"""
        config = project_structure.load_config()
        self.test_command = config["ace"]["development_test_command"]
        test = test.strip()
        if test:
            self.test_files = [self.test_filename(test)]
        else:
            self.test_files = project_structure.list_files("test", "py")
    
    def test_filename(self, test):
        """Format up the test filename"""
        if test.endswith(".py"):
            contract = re.sub("test_", "", contract)
        basename = "test_" + os.path.splitext(os.path.basename(test))[0]
        return project_structure.project_filepath("test", basename, "py")
    
    def run_tests(self):
        """Run the tests"""
        for test in self.test_files:
            if os.path.exists(test):
                command = self.test_command % test
                subprocess.call(command,
                                stdout=sys.stdout,
                                stderr=sys.stderr,
                                shell=True)
            else:
                print >> sys.stderr, "No such file: %s." % test
