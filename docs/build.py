"""Build the API documentation and open it in the default browser.

The output is generated in the directory :file:`_build` (see ``_build_output_dir``).

Sphinx must be installed for this script to work (:program:`pip install sphinx`).

The recommended way to run this script is from within PyCharm. Running it from the command line
requires that the directory of this script is the current directory. (This is automatically set
by default by PyCharm when it runs a script.)
"""

# $Id: build.py 22614 2015-07-15 18:14:53Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-15 13:14:53 -0500 (Wed, 15 Jul 2015) $
#
# This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.
#
# algebraixlib is free software: you can redistribute it and/or modify it under the terms of version
# 3 of the GNU Lesser General Public License as published by the Free Software Foundation.
#
# algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
# If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------
import filecmp
import os
import shutil
import sphinx
import sphinx.apidoc
import webbrowser


# Configurations used during debugging -------------------------------------------------------------
_skip_apidoc = False
_skip_load_in_browser = False


# Project setup ------------------------------------------------------------------------------------

# Packages (top-level directories) to be parsed by sphinx-apidoc.
_source_packages = ['algebraixlib']

# Sphinx builders to be run. Determine output formats and other features (like running doctests).
_builders = ['html', 'doctest', 'coverage']

# The base directory for the parsed sources (relative to this file's directory).
_rst_base_dir = '_source'
_rst_temp_dir = _rst_base_dir + '.temp'

# The base directory for the output in target formats (relative to this file's directory).
_build_output_dir = '_build'

# Formatting options for sphinx-apidoc.
_apidoc_format = ['--no-toc', '--separate', '--module-first']


# Utilities ----------------------------------------------------------------------------------------

def _get_files_in_dir(directory):
    """Return a list of the file names in the given directory."""
    return [file_name
        for file_name in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, file_name))]


def _sync_dir(temp_dir, file_names):
    """Sync the in ``temp_dir`` with the corresponding files under ``_rst_base_dir``. The list of
    files should match ``file_names``."""
    rel_dir = os.path.relpath(temp_dir, _rst_temp_dir)
    source_dir = os.path.join(_rst_temp_dir, rel_dir)
    target_dir = os.path.join(_rst_base_dir, rel_dir)
    assert os.path.isdir(source_dir)
    if os.path.isdir(target_dir):
        source_files = _get_files_in_dir(source_dir)
        target_files = _get_files_in_dir(target_dir)
        for file in source_files:
            source_file_path = os.path.join(source_dir, file)
            target_file_path = os.path.join(target_dir, file)
            if not os.path.isfile(target_file_path):
                # Copy missing files.
                shutil.copy2(source_file_path, target_file_path)
                # Copy mismatched files.
            elif not filecmp.cmp(source_file_path, target_file_path, shallow=False):
                shutil.copy2(source_file_path, target_file_path)
        for file in target_files:
            source_file_path = os.path.join(source_dir, file)
            target_file_path = os.path.join(target_dir, file)
            if not os.path.isfile(source_file_path):
                # Delete files in target that shouldn't be there.
                os.remove(target_file_path)
    else:
        shutil.copytree(source_dir, target_dir)
    # Make sure everything matches now.
    match, mismatch, error = filecmp.cmpfiles(source_dir, target_dir, file_names, shallow=False)
    assert len(match) == len(file_names) and len(mismatch) == 0 and len(error) == 0


# Sphinx build execution ---------------------------------------------------------------------------

# Run sphinx-apidoc. Create the API .rst files in _rst_temp_dir, then sync to _rst_base_dir.
if not _skip_apidoc:
    # Clean out the apidoc temp tree. Leftovers here may create problems.
    if os.path.isdir(_rst_temp_dir):
        shutil.rmtree(_rst_temp_dir)
    # Create .rst files in _rst_temp_dir.
    for package in _source_packages:
        rst_dir = os.path.join(_rst_temp_dir, package)
        code_dir = os.path.join('..', package)
        cmd_opts = ['--force', '-o' + rst_dir, code_dir]
        sphinx.apidoc.main(['sphinx-apidoc'] + _apidoc_format + cmd_opts)
    # Sync from _rst_temp_dir to _rst_base_dir.
    if not os.path.isdir(_rst_base_dir):
        os.mkdir(_rst_base_dir)
    for dir_path, subdir_list, file_list in os.walk(_rst_temp_dir):
        _sync_dir(dir_path, file_list)
    # Get rid of _rst_temp_dir.
    shutil.rmtree(_rst_temp_dir)

# Run sphinx. Convert all .rst files to target formats (_builders) into _build_output_dir.
for builder in _builders:
    cmd_opts = ['-b', builder, '.', _build_output_dir]
    res = sphinx.build_main(['sphinx-build'] + cmd_opts)
    if res != 0:
        raise RuntimeError('sphinx-build call failed for builder ' + builder)

# Open the documentation in browser.
if not _skip_load_in_browser:
    # Open file in new tab (`new=2`) in browser.
    html_file = os.path.join(_build_output_dir, 'index.html')
    webbrowser.open(html_file, new=2)
