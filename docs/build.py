"""Build the API documentation and open it in the default browser.

The output is generated in the directory :file:`_build` (see ``_build_output_dir``).

Sphinx must be installed for this script to work (:program:`pip install sphinx`).

The recommended way to run this script is from within PyCharm. Running it from the command line
requires that the directory of this script is the current directory. (This is automatically set
by default by PyCharm when it runs a script.)
<<<<<<< HEAD

Keyword arguments:

-   --rebuild, -r: Rebuild the documentation. (Normally, intermediate files from the previous
    build are cached.)
-   --skipload, -s: Skip the loading of the index file in the system default browser.
"""

# $Id: build.py 22812 2015-08-19 21:50:49Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-19 16:50:49 -0500 (Wed, 19 Aug 2015) $
=======
"""

# $Id: build.py 22698 2015-07-28 17:09:23Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-28 12:09:23 -0500 (Tue, 28 Jul 2015) $
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
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
# noinspection PyPackageRequirements
import sphinx
# noinspection PyPackageRequirements
import sphinx.apidoc
import webbrowser


# Configurations used during debugging -------------------------------------------------------------
_skip_apidoc = False
<<<<<<< HEAD
=======
_skip_load_in_browser = False
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272


# Project setup ------------------------------------------------------------------------------------

# Packages (top-level directories) to be parsed by sphinx-apidoc.
_source_packages = ['algebraixlib']

# Sphinx builders to be run. Determine output formats and other features (like running doctests).
_builders = ['html', 'doctest', 'coverage']

<<<<<<< HEAD

# Default values -----------------------------------------------------------------------------------

# Formatting options for sphinx-apidoc.
_apidoc_format = ['--no-toc', '--separate', '--module-first']

=======
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
# The base directory for the parsed sources (relative to this file's directory).
_rst_base_dir = '_source'
_rst_temp_dir = _rst_base_dir + '.temp'

# The base directory for the output in target formats (relative to this file's directory).
_build_output_dir = '_build'

<<<<<<< HEAD

# Sphinx build -------------------------------------------------------------------------------------

def build_documentation(working_dir,
        source_packages, builders, apidoc_format=_apidoc_format,
        rst_base_dir=_rst_base_dir, rst_temp_dir=_rst_temp_dir, build_output_dir=_build_output_dir,
        skip_apidoc=_skip_apidoc, skip_load_in_browser=False, load_file=None,
        rebuild=False):

    def get_files_in_dir(directory):
        """Return a list of the file names in the given directory."""
        return [file_name
            for file_name in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, file_name))]

    def get_dirs_in_dir(directory):
        """Return a list of the directory names in the given directory."""
        return [dir_name
            for dir_name in os.listdir(directory)
                if os.path.isdir(os.path.join(directory, dir_name))]

    def sync_dir(temp_dir, file_names, rst_base_dir, rst_temp_dir):
        """Sync the in ``temp_dir`` with the corresponding files under ``_rst_base_dir``. The
        list of files should match ``file_names``."""
        rel_dir = os.path.relpath(temp_dir, rst_temp_dir)
        source_dir = os.path.join(rst_temp_dir, rel_dir)
        target_dir = os.path.join(rst_base_dir, rel_dir)

        if os.path.isdir(target_dir):
            target_subdirs = get_dirs_in_dir(target_dir)
            for subdir in target_subdirs:
                source_subdir = os.path.join(source_dir, subdir)
                target_subdir = os.path.join(target_dir, subdir)
                if not os.path.isdir(source_subdir):
                    shutil.rmtree(target_subdir)

        assert os.path.isdir(source_dir)
        if not os.path.isdir(source_dir):
            if os.path.isdir(target_dir):
                shutil.rmtree(target_dir)
        else:
            if os.path.isdir(target_dir):
                source_files = get_files_in_dir(source_dir)
                target_files = get_files_in_dir(target_dir)
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

    current_dir = os.getcwd()
    os.chdir(working_dir)

    build_output_dir = os.path.abspath(build_output_dir)
    rst_base_dir = os.path.abspath(rst_base_dir)
    rst_temp_dir = os.path.abspath(rst_temp_dir)

    try:
        if rebuild:
            print('...rebuilding (with clean build directories)...')
            for dir_to_clean in [rst_base_dir, build_output_dir]:
                if os.path.isdir(dir_to_clean):
                    import time
                    shutil.rmtree(dir_to_clean)
                    time.sleep(1)
                    os.mkdir(dir_to_clean)

        # Run sphinx-apidoc. Create the API .rst files in _rst_temp_dir, then sync to _rst_base_dir.
        if not skip_apidoc:
            # Clean out the apidoc temp tree. Leftovers here may create problems.
            if os.path.isdir(rst_temp_dir):
                shutil.rmtree(rst_temp_dir)
            # Create .rst files in rst_temp_dir.
            for package in source_packages:
                rst_dir = os.path.join(rst_temp_dir, package)
                code_dir = os.path.join('..', package)
                cmd_opts = ['--force', '-o' + rst_dir, code_dir]
                sphinx.apidoc.main(['sphinx-apidoc'] + apidoc_format + cmd_opts)
            # Sync from _rst_temp_dir to _rst_base_dir.
            if not os.path.isdir(rst_base_dir):
                os.mkdir(rst_base_dir)
            if not os.path.isdir(rst_temp_dir):
                os.mkdir(rst_temp_dir)
            for dir_path, subdir_list, file_list in os.walk(rst_temp_dir):
                sync_dir(dir_path, file_list, rst_base_dir, rst_temp_dir)
            # Get rid of _rst_temp_dir.
            if os.path.isdir(rst_temp_dir):
                shutil.rmtree(rst_temp_dir)

        # Run sphinx. Convert all .rst files to target formats (_builders) into _build_output_dir.
        for builder in builders:
            cmd_opts = ['-b', builder, '.', build_output_dir]
            res = sphinx.build_main(['sphinx-build'] + cmd_opts)
            if res != 0:
                raise RuntimeError('sphinx-build call failed for builder ' + builder)

        # Open the documentation in browser.
        if not skip_load_in_browser:
            # Open file in new tab (`new=2`) in browser.
            html_file = os.path.join(build_output_dir, load_file + '.html')
            print('...opening {index} in default browser...'.format(index=html_file))
            webbrowser.open(html_file, new=2)
    finally:
        os.chdir(current_dir)


def get_arg_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Build (public) documentation.')
    parser.add_argument('-r', '--rebuild', help='rebuild documentation', action='store_true')
    parser.add_argument('-s', '--skipload', help='skip loading in browser', action='store_true')
    return parser


# Running as script --------------------------------------------------------------------------------

if __name__ == '__main__':
    args = get_arg_parser().parse_args()

    build_documentation(working_dir='.',
        source_packages=_source_packages, builders=_builders,
        rebuild=args.rebuild, load_file='index', skip_load_in_browser=args.skipload)
=======
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
>>>>>>> 8314b2bc25b1d2d8cfaef682762ca91234bc9272
