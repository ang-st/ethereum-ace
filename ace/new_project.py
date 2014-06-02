# new_contract.py - Project creation for ace.
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

import inspect, os, shutil, sys
import project_structure

class NewProject(object):
    """Create a new ace project"""
    
    # TODO: unified manifest-based copy & template system
    #       to share with contract creation.
    
    DIRS = ["config", "build", "log", "contract", "test"]
    FILES = ["config/ace.yaml", "config/development.yaml"]
    
    def __init__(self, project_name):
        """Stash the project details"""
        self.project_name = project_name
        self.project_dir = self.project_name
        self.recreate_directory = False
    
    def should_create_project(self):
        """Check whether the directory already exists unless recreating"""
        if self.recreate_directory:
            return True
        else:
            return not os.path.exists(self.project_dir)
    
    def create_dirs(self):
        """Create the directory structure for the project"""
        for dirname in self.DIRS:
            newdir = os.path.join(self.project_dir, dirname)
            try:
                os.makedirs(newdir)
            except:
                print >> sys.stderr, "Directory already exists: %s" % newdir
    
    def create_files(self):
        """Copy the files needed by the project into their directories"""
        for filepath in self.FILES:
            sourcefile = project_structure.source_file(filepath)
            destfilepath = os.path.join(self.project_dir, filepath)
            if not os.path.exists(filepath):
                open(destfilepath, 'w').write(sourcefile.read())
            else:
                print >> sys.stderr, "File already exists: %s" % filepath
    
    def create_project(self):
        """Create the project as specified"""
        if self.should_create_project():
            self.create_dirs()
            self.create_files()
        else:
            print >> sys.stderr, "Project directory already exists. Stopping."
