"""Miscellaneous utility functions and classes."""

# Copyright Algebraix Data Corporation 2015 - 2017
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
import textwrap as _textwrap
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


# noinspection PyIncorrectDocstring
def open_webpage_from_html_str(html: str):
    """Open the HTML content string ``html`` in the system default browser."""

    import tempfile
    import webbrowser
    webpage = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    webpage.write(bytes(html, 'utf-8'))
    webpage.close()
    webbrowser.open_new(webpage.name)


def print_var(variable_name, frames_up: int=0, skip: bool=False, short: bool=False,
              max_length: int=10000, append: str='', indent=None, indent_first=None):
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
    :param append: A string that is appended to the generated string.
    :param indent: Indent all lines with this string. Default is no indent.
    :param indent_first: Indent first line with this string. Default is the value of ``indent``.
    """
    if not skip:
        if indent is None:
            indent = ''
        if indent_first is None:
            indent_first = indent

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
        var_str = format_str.format(**format_vals)
        var_str_ind = _textwrap.indent(var_str, indent)
        if indent_first != indent:
            var_str_ind = indent_first + var_str_ind[len(indent):]
        print(var_str_ind)


def write_to_file_or_path(file_or_path, data_functor):
    """If ``file_or_path`` is a string, open a file and call ``data_functor`` on it. If it is not a
    string, assume it is a file-like object (with a ``.write()`` function) and call ``data_functor``
    on it.

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

    def __init__(self, is_function: bool=True, quiet: bool=False, args: []=None,
            notime: bool=False, walltime: bool=False):
        """Store time and caller's function name, increase indent, print caller's arguments."""
        FunctionTimer._indent += 1
        self._notime = notime
        self._quiet = quiet
        self._timer = _time.perf_counter if walltime else _time.process_time
        self._time_str = 'elapsed' if walltime else 'used'
        start_format = self.get_indent() + '...{0} START '
        if is_function:
            current_frame = _inspect.currentframe()
            outer_frames = _inspect.getouterframes(current_frame)
            (caller_frame, _, _, _, _, _) = outer_frames[1]
            _, _, _, values = _inspect.getargvalues(caller_frame)

            self.func_name = _inspect.getframeinfo(caller_frame)[2]
            if args is None:
                args = values.keys()
            if len(args) == 0:
                arguments = ''
                start_format += '{1}'
            else:
                arguments = '; '.join(
                    ['{0}: {1}'.format(k, v) for k, v in values.items() if k in args])
                start_format += '(args: {1})'
        else:
            self.func_name = '(main)'
            arguments = ''
            start_format += '{1}'

        if not self._quiet:
            print(start_format.format(self.func_name, arguments))

        self._ended = False
        self.start_time = self._timer()

    def __del__(self):
        self._final_outdent()

    def __enter__(self):
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._final_outdent()

    def _final_outdent(self):
        if not self._ended:
            FunctionTimer._indent -= 1
            self._ended = True

    def print(self, *texts):
        if not self._quiet:
            print(_textwrap.indent(' '.join(str(text) for text in texts),
                self.get_indent(additional=1)))

    def lap(self, variable_name: str=None, desc: str=None, skip: bool=False, short: bool=False,
            max_length: int=10000):
        """Print the currently elapsed time and optionally a variable value, properly indented.

        :param variable_name: The name of the variable to be printed. Defaults to ``None``.
        :param desc: A description for this lap. Only used if ``variable_name`` is ``None``.
        :param skip: Set to ``True`` to skip this lap. Defaults to ``False``.
        :param short: Print a short lap result without the full content of ``variable_name``.
        :param max_length: Maximal length of print. Defaults to 10000 characters.
        """
        if not skip and not self._quiet:
            self._print('LAP', variable_name, desc, short, frames_up=1, max_length=max_length)
        return self

    def end(self, variable_name: str=None, desc: str=None, short: bool=False,
            max_length: int=10000):
        """Decrease indent, print the elapsed time and optionally a variable value.

        :param variable_name: The name of the variable to be printed. Defaults to ``None``.
        :param desc: A description for this lap. Only used if ``variable_name`` is ``None``.
        :param short: Print a short lap result without the full content of ``variable_name``.
        :param max_length: Maximal length of print. Defaults to 10000 characters.
        """
        if not self._quiet:
            self._print('END', variable_name, desc, short, frames_up=1, max_length=max_length)
        self._final_outdent()

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
        frmt_str = '{indent}...{func_name} {label}'
        frmt_args = {'indent': self.get_indent(), 'func_name': self.func_name, 'label': label}
        if not self._notime:
            frmt_str += ' ({time_str} {elapsed_time:.3f} s)'
            frmt_args['elapsed_time'] = self.get_elapsed_time()
            frmt_args['time_str'] = self._time_str
        print(frmt_str.format(**frmt_args), end='')

        if variable_name is not None:
            assert desc is None
            print(': ', end='')
            print_var(variable_name, short=short, frames_up=frames_up + 1, max_length=max_length,
                indent=self.get_indent(1), indent_first='')
        elif desc is not None:
            print(': {0}'.format(desc))
        else:
            print('')

    def get_elapsed_time(self):
        """Return the time elapsed since construction in seconds (see ``__init__()``)."""
        elapsed = self._timer() - self.start_time
        return elapsed

    @staticmethod
    def get_indent(additional: int=0) -> str:
        """Return the current indent as string of spaces.
        :param additional: (Optional) Additional levels of indentation. Defaults to 0.
        """
        return ' ' * (FunctionTimer._indent_space_cnt * (FunctionTimer._indent + additional))


def core(string: str, begin_len: int=0, end_len: int=0) -> str:
    """Remove characters in the middle of a string by specifying the length of the beginning of
    the string and the length of the ending of the string. Ellipses are inserted in place of the
    core of the string that is being removed.

    :param string: The string to process.
    :param begin_len: The length, in characters, of the beginning part of the string.
    :param end_len: The length, in characters, of the ending part of the string.
    """

    if begin_len > 0 and end_len > 0 and begin_len - end_len < len(string):
        string = string[:begin_len] + '\n...\n' + string[-end_len:]
    return string


class PerformanceTimer:
    def __init__(self, quiet: bool=False):
        self._quiet = quiet
        self._start_time = _time.perf_counter()
        self._end_time = None

    def end(self, msg=''):
        if self._end_time is None:
            self._end_time = _time.perf_counter()
        if not self._quiet:
            print('{} elapsed time: {:.5f} seconds'.format(msg, self.get_elapsed_time()))

    def get_elapsed_time(self):
        return self._end_time - self._start_time

    @property
    def get_start_time(self) -> float:
        return self._start_time

    @property
    def get_end_time(self) -> float:
        return self._end_time
