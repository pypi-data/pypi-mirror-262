# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import importlib
import sys
from os import PathLike
from pathlib import Path


def get_project_root_path(
        module_file_path_name: PathLike,
        module_name: str,
        source_depth: int = 0
) -> PathLike:
    """
    Return the root path of the Python project.


    :note: The function detects whether the module has been installed as a
        3rd party library (i.e., within the directory ``site-packages``).
        In this case, any source directory would have been removed from
        the path to the module file.  Therefore, the argument
        ``source_depth`` is automatically set to ``0``.


    :param module_file_path_name: The path to the module from which this
        function is called.  This SHOULD be the Python built-in variable
        ``__file__``, which evaluates to the pathname of the current
        module.

    :param module_name: The name of the module from which this function is
        called.  This SHOULD be the Python built-in variable ``__name__``,
        which evaluates to the name of the current module.

    :param source_depth: The depth of the Python project's source directory
        from the Python project's root directory.

        Python developers usually create a ``src`` directory at the root of
        their Python project where they organize their project's modules,
        rather than putting their sources file directly in the root
        directory.  For example::

        ```text
        .
        ├── CHANGELOG.md
        ├── LICENSE.md
        ├── README.md
        ├── data
        │   ├── ...
        │   .
        │   └── ...
        ├── poetry.lock
        ├── pyproject.toml
        ├── run.py
        └── src
            └── ...
                ├── __init__.py
                ├── ...
                .
                └── ...
                .   ├── __init__.py
                .   .
                .   └── ...
                └── ...
        ```

        In this case, the depth of the Python project's source directory
        is ``1``.

        This argument is automatically sets to ``0`` if the module has
        been installed as 3rd party library, in which case Python project's
        source directory has been removed from the path to this module file.


    :return: The root path of the Python project.


    :raise ValueError: If the module name doesn't refer to a Python
        package but to a not packaged script (i.e., ``__main__``).
    """
    if module_name == '__main__':
        raise ValueError("A Python packaged module is required")

    if source_depth < 0:
        raise ValueError("The source depth must be a positive integer")

    # :patch: Check whether the Python module has been installed as a 3rd
    #     party libray, i.e., inside the directory ``site-packages``.  This
    #     directory is where user installed packages are dropped.
    #
    #
    if 'site-packages' in str(module_file_path_name):
        source_depth = 0

    # Determine the number of folders that composed the module namespace.
    #
    # module_file_path_name = '/lib/perseus-core-python-library/src/majormode/perseus/utils/logging.py'
    # module_name = 'majormode.perseus.utils.logging'
    #
    # The module namespace has a length of 4 folder.
    module_namespace_depth = len(module_name.split('.'))

    # module_file_path_name = '/lib/perseus-core-python-library/src/majormode/perseus/utils/__init__.py'
    # module_name = 'majormode.perseus.utils'
    if Path(module_file_path_name).name == '__init__.py':
        module_namespace_depth += 1

# Determine the project root path from the module file path name,
# removing the relative path to this module, i.e., the number of folders
# that composed the module's path.
#
# module_file_path_name = '/lib/perseus-core-python-library/src/majormode/perseus/utils/logging.py'
# module_file_path_name.parents = ['lib', 'perseus-core-python-library', 'src', 'majormode', 'perseus', 'utils']
# module_name = 'majormode.perseus.utils.logging'
# module_namespace_depth = 4
# module_package_file_name.parents[module_namespace_depth - 1] = '/lib/perseus-core-python-library/src'
#
# module_file_path_name = '/lib/perseus-core-python-library/src/majormode/perseus/utils/__init__.py'
# module_file_path_name.parents = ['lib', 'perseus-core-python-library', 'src', 'majormode', 'perseus', 'utils']
# module_name = 'majormode.perseus.utils'
# module_namespace_depth = 3
#
# module_package_file_name.parents[module_namespace_depth - 1] = '/lib/perseus-core-python-library/src/'

    module_package_file_name = Path(module_file_path_name)
    project_path = module_package_file_name.parents[module_namespace_depth - 1 + source_depth]

    return project_path


def load_module(module_package_name):
    """
    Load the specified Python module specified by a string representation.


    @note: The function prevents from circular import.


    :param module_package_name: A string representation of the Python
        packaged module (module namespace) using "dotted module names",
        e.g., `foo.bar`.


    :return: An object of the specified module.
    """
    return sys.modules.get(module_package_name) or importlib.import_module(module_package_name)


def load_class(class_module_package_name):
    """
    Dynamically load a Python class specified by the string representation
    of this class in a Python packaged module (module namespace).


    @note: The function prevents from circular import.


    :param class_module_package_name: A string representation of the class
        to load using "dotted module names", e.g., `foo.bar.MyClass`.


    :return: The specified class.
    """
    module_package_name, class_name = class_module_package_name.rsplit('.', 1)

    return getattr(load_module(module_package_name), class_name)
