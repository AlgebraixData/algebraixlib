"""Miscellaneous utility functions and classes."""

# $Id: miscellaneous.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import inspect as _inspect
import sys as _sys
import time as _time


def get_full_class_name(obj: object) -> str:
    """Get the fully qualified name of a class.

    :param obj: An object.
    :return: The class name of ``obj``, fully qualified with package and module name(s).
    """
    module_name = _inspect.getmodule(obj).__name__
    class_name = obj.__class__.__name__
    full_name = module_name + '.' + class_name
    return full_name


def get_hash(*args) -> int:
    """Create a hash of the arguments.

    :param args: Any number of arguments.
    :return: A hash of ``args``. The hash is an integer with the width of hashes on the system.
    """
    assert len(args) > 0
    hash_val = 0
    for arg in args:
        hash_val += hash(arg)
    hash_val &= ((1 << _sys.hash_info.width) - 1)
    return hash_val


def get_single_iter_elem(iterable):
    """Get the single element of ``iterable``.

    :param iterable: An iterable that is expected to have a single element.
    :return: The single element of ``iterable``. (Assert if there isn't exactly one element.)
    :raise: `StopIteration` if ``iterable`` doesn't contain at least one element; ``TypeError``
        if ``iterable`` isn't iterable.
    """
    assert len(iterable) == 1
    return next(iter(iterable))


def get_variable(variable_name: str, frames_up: int):
    """Return the variable with name ``variable_name``, from ``frames_up`` frames upwards.

    :param variable_name: The name of the variable to retrieve and return.
    :param frames_up: The number of call stack frames up (relative to the caller of this function).
    :return: The variable with the name ``variable_name``, ``frames_up`` frames up.
    """
    current_frame = _inspect.currentframe()
    outer_frames = _inspect.getouterframes(current_frame)
    (caller_frame, _, _, _, _, _) = outer_frames[frames_up + 1]
    variable_value = caller_frame.f_locals[variable_name]
    return variable_value


def open_webpage_from_html_str(html: str):
    """Open the HTML content string ``html`` in the system default browser."""

    import tempfile
    import webbrowser
    webpage = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    webpage.write(bytes(html, 'utf-8'))
    webpage.close()
    webbrowser.open_new(webpage.name)


def print_var(variable_name, frames_up: int=0, skip: bool=False, short: bool=False,
              max_length: int=10000, append: str=''):
    """Print a variable, given its name ``variable_name`` and its location in the call stack.

    :param variable_name: The name of the variable to print.
    :param frames_up: The number of call stacks up (relative to the caller of this function) where
        the variable is located. (If the caller wants to print a local variable, ``frames_up`` can
        be left at its default of 0.)
    :param skip: Set to ``True`` to skip printing the variable. Use to control a number of calls to
        `print_var` with a single variable.
    :param short: Set to ``True`` to print a short version (only name and len if applicable).
    :param max_length: The maximum length of the string to be printed. Set to ``None`` if you
        always want everything.
    """
    if not skip:
        variable_value = get_variable(variable_name, frames_up + 1)

        format_vals = {'variable_name': variable_name}
        if short:
            format_str_val = ''
        else:
            value_str = str(variable_value)
            if max_length is None:
                format_vals['variable_value'] = value_str
                format_str_val = '= {variable_value}'
            else:
                format_vals['variable_value'] = value_str[:max_length]
                format_str_val = '= {variable_value}'
                if len(value_str) > max_length:
                    format_str_val += '...'

        # noinspection PyBroadException
        try:
            format_vals['len'] = len(variable_value)
            format_str_len = '(len {len})'
        except Exception:
            format_str_len = ''

        format_str = '{{variable_name}}{format_str_len} {format_str_val}{append}'.format(
            format_str_len=format_str_len, format_str_val=format_str_val, append=append)
        print(format_str.format(**format_vals))


def write_to_file_or_path(file_or_path, data_functor):
    """If ``file_or_path`` is a string, open a file and call ``data_functor`` on it. If it is not a
    string, assume it is a file-like object (with a .write() function) and call ``data_functor`` on
    it.

    :param file_or_path: A string or a file-like object (with a .write() function).
    :param data_functor: A function-like object with one argument that is the writer.
    """
    if isinstance(file_or_path, str):
        # 'with' syntax handles close no matter what.
        with open(file_or_path, "w+", newline='') as out_file:
            data_functor(out_file)
    else:
        # Assume 'file_or_path' is a writer-type object.
        data_functor(file_or_path)


class FunctionTimer:
    """Time a function (and parts of it), with provisions for call hierarchies of functions.

    Example code:

    .. code::

        from algebraixlib.util.miscellaneous import FunctionTimer

        def foo():
            skip_laps = False  # Set to True to skip lap prints.
            timer1 = FunctionTimer()

            var1 = 'something' # Do some work.
            timer1.lap('var1', skip=skip_laps)

            var2 = 'something else' # Do some more work.
            timer1.lap('var2', skip=skip_laps)

            result = 'laboriously calculated' # Do still more work.
            timer1.end('result')

            return result

        timer = FunctionTimer(is_function=False)

        foo()
        timer.lap(desc='after first call')

        foo()
        timer.lap(desc='after second call')
    """

    #: The current indent level. Is incremented at the beginning of a function (creation of a new
    #: instance) and decremented at the end (`end`).
    _indent = -1

    #: The number of spaces for a single indent. Is constant.
    _indent_space_cnt = 3

    def __init__(self, is_function: bool=True):
        """Store time and caller's function name, increase indent, print caller's arguments."""
        FunctionTimer._indent += 1
        start_format = self.get_indent() + '...{0} START '
        if is_function:
            current_frame = _inspect.currentframe()
            outer_frames = _inspect.getouterframes(current_frame)
            (caller_frame, _, _, _, _, _) = outer_frames[1]
            _, _, _, values = _inspect.getargvalues(caller_frame)

            self.func_name = _inspect.getframeinfo(caller_frame)[2]
            arguments = '; '.join(['{0}: {1}'.format(key, val) for key, val in values.items()])
            start_format += '(args: {1})'
        else:
            self.func_name = '(main)'
            arguments = ''
            start_format += '{1}'

        print(start_format.format(self.func_name, arguments))
        self.start_time = _time.process_time()

    def lap(self, variable_name: str=None, desc: str=None, skip: bool=False, short: bool=False,
            max_length: int=10000):
        """Print the currently elapsed time and optionally a variable value, properly indented.

        :param variable_name: The name of the variable to be printed. Defaults to ``None``.
        :param desc: A description for this lap. Only used if ``variable_name`` is ``None``.
        :param skip: Set to ``True`` to skip this lap. Defaults to ``False``.
        :param short: Print a short lap result without the full content of ``variable_name``.
        :param max_length: Maximal length of print. Defaults to 10000 characters.
        """
        if not skip:
            self._print('LAP', variable_name, desc, short, frames_up=1, max_length=max_length)

    def end(self, variable_name: str=None, desc: str=None, short: bool=False,
            max_length: int=10000):
        """Decrease indent, print the elapsed time and optionally a variable value.

        :param variable_name: The name of the variable to be printed. Defaults to ``None``.
        :param desc: A description for this lap. Only used if ``variable_name`` is ``None``.
        :param short: Print a short lap result without the full content of ``variable_name``.
        :param max_length: Maximal length of print. Defaults to 10000 characters.
        """
        self._print('END', variable_name, desc, short, frames_up=1, max_length=max_length)
        FunctionTimer._indent -= 1

    def _print(self, label: str, variable_name: str, desc: str, short: bool, frames_up: int,
               max_length: int):
        """Print the elapsed time and an optional variable value.

        :param label: A label to print after the function name. Indicate the occasion; set to
            ``'LAP'`` by `lap` and ``'END'`` by `end`.
        :param variable_name: The name of the variable to print after the elapsed time. Skip if
            the name is empty or ``None``.
        :param frames_up: The number of call stack frames upwards (relative to the caller) where
            the variable is located.
        """
        print(self.get_indent() + '...{func_name} {label} (elapsed {elapsed_time:.3f} s)'.format(
            func_name=self.func_name, label=label, elapsed_time=self.get_elapsed_time()),
            end='')
        if variable_name is not None:
            assert desc is None
            print(': ', end='')
            print_var(variable_name, short=short, frames_up=frames_up + 1, max_length=max_length)
        elif desc is not None:
            print(': {0}'.format(desc))
        else:
            print('')

    def get_elapsed_time(self):
        """Return the time elapsed since construction in seconds (see ``__init__()``)."""
        elapsed = _time.process_time() - self.start_time
        return elapsed

    @staticmethod
    def get_indent():
        """Return the current indent as string of spaces."""
        return ' ' * (FunctionTimer._indent_space_cnt * FunctionTimer._indent)
