"""Conversion utilities that present a `MathObject` as LaTeX markup.

The main entry point is the function `math_object_to_latex`; it delegates to the appropriate
conversion function according to the argument type.
"""

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
import itertools as _itertools

import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _undef
import algebraixlib.util.miscellaneous as _misc


# --------------------------------------------------------------------------------------------------

class Config:
    """A static class with module configuration values."""

    #: If ``True``, add colors to the output. If ``False``, print black only.
    colorize_output = True

    #: Number of characters to print for 'short' length of :class:`~.Atom` values. The remainder
    #: of the elements is represented by an ellipsis ('...').  See `math_object_to_latex` and
    #: `iprint_latex`.
    short_atom_len = 10

    #: Number of elements to print for 'short' length of :class:`~.Set`\s and
    #: :class:`~.Multiset`\s. The remainder of the elements is represented by an ellipsis,
    #: followed by the number of not shown elements in parentheses (for example '... (15)'). See
    #: `math_object_to_latex` and `iprint_latex`.
    short_set_len = 4


def math_object_to_latex(mobj, short: bool=False, _depth: int=0):
    """Return a `string` that represents a `MathObject` on `Undef()` in LaTeX markup.

    This function sorts the input ``mobj`` if it is a :class:`~.Set` or a :class:`~.Multiset` to
    make the output consistent, so be careful with big (multi)sets. (Such large (multi)sets
    where this is a problem may not be suitable to display in LaTeX anyway.)

    :param mobj: The instance that you want to translate into LaTeX. It must be a `MathObject`
        or `Undef()`.
    :param short: (Optional) When set to ``True``, a short version of the content is generated.
        Longer parts are abbreviated with ellipses ('...'). Defaults to ``False``. See also
        `Config.short_atom_len` and `Config.short_set_len`.
    :param _depth: (Optional) Internal use only. Indicate levels of nested (multi)sets. Is
        incremented for every nesting level. Default is 0.
    """
    if isinstance(mobj, _mo.MathObject):
        if mobj.is_set:
            return set_to_latex(mobj, short, _depth)
        elif mobj.is_multiset:
            return mset_to_latex(mobj, short, _depth)
        elif mobj.is_couplet:
            return couplet_to_latex(mobj, short)
        elif mobj.is_atom:
            return atom_to_latex(mobj, short)
        else:
            return '<application error>'
    elif mobj is _undef.Undef():
        return r"\mathit{undef}"
    else:
        return str(mobj)


# noinspection PyPackageRequirements
def iprint_latex(variable_name: str, variable_value=None, short: bool=False):
    """Display variables in IPython notebooks using LaTeX markup. Uses `math_object_to_latex`.

    This function sorts the input ``mobj`` if it is a :class:`~.Set` or a :class:`~.Multiset` to
    make the output consistent, so be careful with big (multi)sets. (Such large (multi)sets
    where this is a problem may not be suitable to display in LaTeX anyway.)

    :param variable_name: The name of the variable to display.
    :param variable_value: (Optional) The value of the variable. If it is missing, the variable
        value is fetched from the caller's frame; a variable with the name ``variable_name`` is
        assumed to exist in this case.
    :param short: (Optional) When set to ``True``, a short version of the content is generated.
        Longer parts are abbreviated with ellipses ('...'). Defaults to ``False``. See also
        `Config.short_atom_len` and `Config.short_set_len`.

    .. note:: This function imports from ``IPython`` and expects IPython to be installed. This is
        generally given when running in an IPython notebook.
    """
    from IPython.display import Math, display
    if variable_value is None:
        variable_value = _misc.get_variable(variable_name, frames_up=1)
    variable_latex = math_object_to_latex(variable_value, short=short)
    variable_name_latex = variable_name.replace('_', r'\_')
    latex = '{name} = {value}'.format(name=variable_name_latex, value=variable_latex)
    display(Math(latex))


# --------------------------------------------------------------------------------------------------

def atom_to_latex(atom: _mo.Atom, short: bool=False):
    """Return a `string` that represents the value of an Atom in LaTeX markup.

    :param atom: The :class:`~.Atom` to be represented in LaTeX markup.
    :param short: (Optional) When set to ``True``, a short version of the content is generated.
        Longer parts are abbreviated with ellipses ('...'). Defaults to ``False``. See also
        `Config.short_atom_len`.
    """
    assert atom.is_atom

    atom_str = str(atom)
    if short and len(atom_str) > Config.short_atom_len + 3:
        atom_str = atom_str[:Config.short_atom_len] + '...'

    # Wrap in mbox tag to enforce that it remains on one line.
    # Note: The str function on an Atom returns the value wrapped in single quotes.
    result_value = '{mbox}{{{atom}}}'.format(mbox=_Tokens.mbox, atom=atom_str)
    return result_value


def couplet_to_latex(couplet: _mo.Couplet, short: bool=False):
    r"""Return a `string` that represents a Couplet in LaTeX markup.

    :param couplet: The :class:`~.Couplet` to be represented in LaTeX markup.
    :param short: (Optional) When set to ``True``, a short version of the content is generated.
        Longer parts are abbreviated with ellipses ('...'). Defaults to ``False``. See also
        `Config.short_atom_len` and `Config.short_set_len`. (Even though this doesn't affect a
        ``Couplet`` directly, it may affect the :term:`left` and :term:`right component`\s of
        it.)
    """
    assert couplet.is_couplet

    left_color = _Colors().red if Config.colorize_output else None
    right_color = _Colors().blue if Config.colorize_output else None

    def make_component(comp, color=None):
        latex_str = math_object_to_latex(comp, short=short)
        if color:
            latex_str = ''.join((_Tokens.color, color, '{', latex_str, '}'))
        if comp.is_atom:
            return latex_str
        return '{}{}{}'.format(_Tokens.left_paren_dyn, latex_str, _Tokens.right_paren_dyn)

    result_value = '{left}{couplet_sym}{{{right}}}'.format(
        right=make_component(couplet.right, right_color),
        couplet_sym=_Tokens.mapsto,
        left=make_component(couplet.left, left_color))
    return result_value


def set_to_latex(set_: _mo.Set, short: bool=False, _depth: int=0):
    """Return a `string` that represents a Set in LaTeX markup.

    This function sorts the input ``set_`` to make the output consistent, so be careful with big
    sets. (Such large sets where this is a problem may not be suitable to display in LaTeX anyway.)

    :param set_: The :class:`~.Set` to be represented in LaTeX markup.
    :param short: (Optional) When set to ``True``, a short version of the content is generated.
        Longer parts are abbreviated with ellipses ('...'). Defaults to ``False``. See also
        `Config.short_set_len`.
    :param _depth: (Optional) Internal use only. Indicate levels of nested (multi)sets. Is
        incremented for every nesting level. Default is 0.
    """
    assert set_.is_set

    result = _Tokens.left_brace_dyn

    if _set_hasa_set(set_):
        # Use nesting delimiters for elements. Print on new lines.
        result += _Tokens.array_start

        # Add sorting to obtain predictable output.
        elem_itr = iter(sorted(set_.data))

        if short and set_.cardinality > Config.short_set_len + 1:
            result += (_Tokens.comma + _nested_set_helper(_depth)).join(
                [math_object_to_latex(element, short=short, _depth=_depth + 1)
                 for element in _itertools.islice(elem_itr, Config.short_set_len)])
            result += _Tokens.comma + _nested_set_helper(_depth) + _Tokens.ellipsis
            result += '({0})'.format(set_.cardinality - Config.short_set_len)
        else:
            result += (_Tokens.comma + _nested_set_helper(_depth)).join(
                [math_object_to_latex(element, short=short, _depth=_depth + 1)
                 for element in elem_itr])

        result += _Tokens.array_end

    else:
        # Use comma delimiters for elements. Print on single line.

        # Add sorting to obtain predictable output.
        elem_itr = iter(sorted(set_.data))

        if short and set_.cardinality > Config.short_set_len + 1:
            is_couplet_list = [elem.is_couplet
                for elem in _itertools.islice(set_, Config.short_set_len)]
        else:
            is_couplet_list = [elem.is_couplet for elem in set_]
        parenthesize_couplets = any(is_couplet_list) and not all(is_couplet_list)

        def optionally_parenthesize_couplet(element):
            def do_paren(e):
                return parenthesize_couplets and e.is_couplet

            left = _Tokens.left_paren if do_paren(element) else ''
            right = _Tokens.right_paren if do_paren(element) else ''
            elem_latex = math_object_to_latex(element, short=short, _depth=_depth + 1)
            return "{}{}{}".format(left, elem_latex, right)

        if short and set_.cardinality > Config.short_set_len + 1:
            result += (_Tokens.comma + _Tokens.space).join(
                optionally_parenthesize_couplet(element)
                for element in _itertools.islice(elem_itr, Config.short_set_len))
            result += _Tokens.comma + _Tokens.space + _Tokens.ellipsis
            result += '({0})'.format(set_.cardinality - Config.short_set_len)
        else:
            result += (_Tokens.comma + _Tokens.space).join(
                optionally_parenthesize_couplet(element) for element in elem_itr)

    result += _Tokens.right_brace_dyn
    return result


def mset_to_latex(mset: _mo.Multiset, short: bool=False, _depth: int=0):
    """Return a `string` that represents a Multiset in LaTeX markup.

    This function sorts the input ``mset`` to make the output consistent, so be careful with big
    sets. (Such large multisets where this is a problem may not be suitable to display in LaTeX
    anyway.)

    :param mset: The :class:`~.Multiset` to be represented in LaTeX markup.
    :param short: (Optional) When set to ``True``, a short version of the content is generated.
        Longer parts are abbreviated with ellipses ('...'). Defaults to ``False``. See also
        `Config.short_set_len`.
    :param _depth: (Optional) Internal use only. Indicate levels of nested (multi)sets. Is
        incremented for every nesting level. Default is 0.
    """
    assert mset.is_multiset

    def latex_mset(value, multiple):
        return '{value}{separator}{multiple}'.format(
            value=math_object_to_latex(value, short=short, _depth=_depth + 1),
            separator=_Tokens.colon + _Tokens.space,
            multiple=multiple)

    if _set_hasa_set(mset):
        # Use nesting delimiters for elements. Print on new lines.
        start = _Tokens.array_start
        separator = _Tokens.comma + _nested_set_helper(_depth)
        end = _Tokens.array_end
    else:
        # Use comma delimiters for elements. Print on single line.
        start = ''
        separator = _Tokens.comma + _Tokens.space
        end = ''

    result = _Tokens.left_bracket_dyn + start

    if short and mset.cardinality > Config.short_set_len + 1:
        result += separator.join(
            [latex_mset(elem_key, multiple) for elem_key, multiple in _itertools.islice(
                sorted(mset.data.items()), Config.short_set_len)])
        result += separator + _Tokens.ellipsis
    else:
        result += separator.join([latex_mset(elem_key, multiple)
                                  for elem_key, multiple in sorted(mset.data.items())])

    result += end + _Tokens.right_bracket_dyn
    return result


# --------------------------------------------------------------------------------------------------

# noinspection PyUnusedLocal
def _nested_set_helper(depth):
    """Insert markup for nested indentation. (Currently only insert newlines.)

    Meant to insert markup and indendation for printing nested sets and multisets. This
    functionality is currently deactivated.

    :param depth: The nesting level.
    :return: LaTeX markup representing a new line and the associated indentation.
    """
    return ''.join([_Tokens.newline, "\n"])  # newline added for markup readability
    # Print additional indentation (presently undesired)
    # return ''.join([_Tokens.newline, _Tokens.quad, _Tokens.quad * depth])


def _set_hasa_set(a_set):
    """Determe whether a (multi)set has elements that are also (multi)sets."""
    for element in a_set:
        if element.is_set or element.is_multiset:
            return True
    return False


class _Tokens:
    """A static class that contains all the LaTeX tokens that we need."""
    newline = r"\\"
    space = r"\ "
    medium_space = r"\>"
    big_space = r"\;"
    comma = r","
    colon = r":"
    right_brace = r"\}"
    right_bracket = r"]"
    right_paren = r")"
    left_brace = r"\{"
    left_bracket = r"["
    left_paren = r"("
    left_brace_dyn = r"\left\{"
    right_brace_dyn = r"\right\}"
    left_bracket_dyn = r"\left["
    right_bracket_dyn = r"\right]"
    left_paren_dyn = r"\left("
    right_paren_dyn = r"\right)"
    array_start = r"\begin{array}{l}"
    array_end = r"\end{array}"
    expon = r"^"
    quad = r"\quad"
    dquad = r"\qquad"
    mbox = r"\mbox"
    color = r"\color"
    ellipsis = r'\text{...}'
    mapsto = r"{\mapsto}"


class _Colors:
    r"""A static class that contains the strings that can be used as arguments to LaTeX \color."""
    gray = "{gray}"
    silver = "{silver}"
    black = "{black}"
    white = "{white}"
    red = "{red}"
    yellow = "{yellow}"
    maroon = "{maroon}"
    lime = "{lime}"
    olive = "{olive}"
    green = "{green}"
    teal = "{teal}"
    aqua = "{aqua}"
    blue = "{blue}"
    navy = "{navy}"
    purple = "{purple}"
    fuchsia = "{fuchsia}"
