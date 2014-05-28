# project_structure.py - Shared support code for ace.
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

import inspect, glob, os, yaml
from pkg_resources import resource_stream

LANGUAGE_EXTENSION = {"serpent":"se"}
ACE_CONFIG_PATH = "config/ace.yaml"

def source_file_root():
    """Get the path to ace's file resources"""
    abspath = os.path.abspath(inspect.getfile(inspect.currentframe()))
    return os.path.join(os.path.dirname(abspath), "files")

def source_file(filepath):
    """Open the file in ace/files"""
    return resource_stream(__name__, os.path.join("files", filepath))

def is_project_dir(path=False):
    """Check whether the path is a project directory"""
    if not path:
        path = os.path.abspath(os.getcwd())
    maybe_exists = os.path.join(path, ACE_CONFIG_PATH)
    return os.path.exists(maybe_exists)

def project_root(path):
    """Get the directory that is the project root,
       or False if not a project"""
    root = False
    path = os.path.abspath(path)
    if is_project_dir(path):
        root = path
    else:
        while(not path == "/") and not is_project_dir(path):
            path = os.path.dirname(path)
            if is_project_dir(path):
                root = path
                break
    return root

def project_root_from_cwd():
    """Get the project root, starting the search at cwd"""
    return project_root(os.getcwd())

def is_in_project():
    """Check whether the command is being called in the project"""
    return project_root_from_cwd() != False

def project_filepath(dirname, filename, kind, projectdir=False):
    """Strip filename and build a file path of:
       projectdir/dirname/filename-sans-path-and-extension.kind"""
    if not projectdir:
        projectdir = project_root_from_cwd()
    kind = kind.strip(".")
    filename = os.path.splitext(filename)[0]
    filename = os.path.basename(filename)
    return os.path.join(projectdir, dirname, "%s.%s" % (filename, kind))
    
def load_config(config_filename="ace"):
    """Load the given config file"""
    filebase = os.path.basename(os.path.splitext(config_filename)[0])
    filepath = project_filepath("config", filebase, "yaml")
    return yaml.load(open(filepath))

def language_extension(language):
    """Get the extension (sans dot) for the language"""
    return LANGUAGE_EXTENSION[language]

def list_files(directory, extension):
    """Return a list of files with the given extension in the given directory"""
    wildcard = "*.%s" % extension
    path = project_filepath(directory, "*", extension)
    return glob.glob(path)
