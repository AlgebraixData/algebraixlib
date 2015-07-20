"""A conversion utility that manipulates a `MathObject` into a LaTeX representation.

The main entry point is the `math_object_to_latex` function; it delegates to the appropriate
conversion function according to the argument type.
"""

# $Id: latexprinter.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import itertools as _itertools

import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _undef
import algebraixlib.util.miscellaneous as _misc


class Config:
    """Module configuration values."""
    colorize_output = True
    short_atom_len = 10
    short_set_len = 4


class _Tokens:
    """Contains all the LaTeX tokens that we need."""
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
    """Contains the strings that can be used as arguments to LaTeX \color."""
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


def nested_set_helper(depth):
    """
    This function inserts the appropriate number of spaces for indentation, based on how many nests
    sets of sets that are currently being printed.
    :param depth: Indicates the current number of nests of sets
    :return: A snippet of LaTeX representing the correct amount of space when starting a new line
    of printing.
    """
    return ''.join([_Tokens.newline, "\n"])  # newline added for markup readability

# Print additional indentation (presently undesired
#    return ''.join([token_tool.newline,
#                    token_tool.quad,
#                    token_tool.quad * depth])


def set_hasa_set(a_set):
    """A interim function for determining the structure of a set.

    :param a_set: The set to test.
    :return: True if the set provided contains elements which are also sets.
    """
    for element in a_set:
        if isinstance(element, _mo.Set) or isinstance(element, _mo.Multiset):
            return True
    return False


def math_object_to_latex(mobj, short: bool=False, _depth: int=0):
    """Prints a math object formatted in LaTeX.
    If it is not provided with a specific math object, returns an error string.

    :param mobj: The object that you want to translate into LaTeX. It must be a :class:`~.Set`, :class:`~.Atom`,
        :class:`~.Couplet` or `Undef()`.
    :param short: When set to ``True``, a short version of the content is generated. Longer parts
        are abbreviated with ellipses ('...'). Defaults to ``False``.
    :param _depth: Defaults to 0, to not be exposed to a caller.  Is incremented when the provided
        math object is a set that contains a set.
    :return: string of LaTeX markup representing the provided math object.
    """
    if isinstance(mobj, _mo.Set):
        return set_to_latex(mobj, short, _depth)
    if isinstance(mobj, _mo.Multiset):
        return mset_to_latex(mobj, short, _depth)
    if isinstance(mobj, _mo.Couplet):
        return couplet_to_latex(mobj, short)
    if isinstance(mobj, _mo.Atom):
        return atom_to_latex(mobj, short)
    if mobj is _undef.Undef():
        return "\mathit{undef}"

    return str(mobj)

def iprint_latex(variable_name: str, variable_value=None, short: bool=False):
    """A utility to display variables in IPython notebooks.

    :param variable_name: The name of the variable to display.
    :param variable_value: The optional value of the variable. If it is missing, the variable
        value is fetched from the caller's frame; a variable with the name ``variable_name`` is
        assumed to exist in this case.
    :param short: When set to ``True``, a short version of the content is generated. Longer parts
        are abbreviated with ellipses ('...'). Defaults to ``False``.
    """
    from IPython.display import Math, display
    if variable_value is None:
        variable_value = _misc.get_variable(variable_name, frames_up=1)
    variable_latex = math_object_to_latex(variable_value, short=short)
    variable_name_latex = variable_name.replace('_', r'\_')
    latex = '{name} = {value}'.format(name=variable_name_latex, value=variable_latex)
    display(Math(latex))

def atom_to_latex(atom, short: bool=False):
    """
    Prints an atom formatted in LaTeX.
    For example the "atom("scooby")" will be represented in LaTeX as "\mbox{scooby}"

    The atom is wrapped in mbox tag to enforce that it remains on one line. Note, currently the str
    function on a atom returns the value wrapped in single quotes.

    Returns an error string if the atom is not of type Atom.

    :param atom: The atom to be turned into LaTeX.
    :param short: When set to ``True``, a short version of the content is generated. Longer parts
        are abbreviated with ellipses ('...'). Defaults to ``False``.
    :return: The LaTeX markup of the atom."""
    assert isinstance(atom, _mo.Atom)
    atom_str = str(atom)
    if short and len(atom_str) > Config.short_atom_len + 3:
        atom_str = atom_str[:Config.short_atom_len] + '...'
    result_value = '{mbox}{{{atom}}}'.format(mbox=_Tokens.mbox, atom=atom_str)

    # result_value = '{l_lime}{{{l_mbox}{{{l_atom!s}}}}}'.format(l_mbox=_Tokens.mbox,
    #     l_lime=token_tool.color_lime_token, l_atom=atom)

    return result_value


def couplet_to_latex(couplet, short: bool=False):
    """
    Prints a couplet formatted in LaTeX.

    Note, currently this implementation only supports couplets which contain atoms.  The LaTeX of a
    couplet which contains non atom math objects might look malformed.

    For example the "Couplet(left=atom("scooby"), right=atom("doo")" will be represented in LaTeX as
    "(\mbox{scooby}{\mapsto}{\mbox{doo}})"

    Returns an error string if the couplet is not of type Couplet.

    :param couplet: The couplet to be turned into LaTeX.
    :param short: When set to ``True``, a short version of the content is generated. Longer parts
        are abbreviated with ellipses ('...'). Defaults to ``False``.
    :return: The LaTeX markup of the couplet."""
    assert isinstance(couplet, _mo.Couplet)

    left_color = _Colors().red if Config.colorize_output else None
    right_color = _Colors().blue if Config.colorize_output else None

    def make_component(comp, color=None):
        latex_str = math_object_to_latex(comp, short=short)
        if color:
            latex_str = ''.join((_Tokens.color, color, '{', latex_str, '}'))
        if isinstance(comp, _mo.Atom):
            return latex_str
        return '{}{}{}'.format(_Tokens.left_paren_dyn, latex_str, _Tokens.right_paren_dyn)

    result_value = '{left}{couplet_sym}{{{right}}}'.format(
        right=make_component(couplet.right, right_color),
        couplet_sym=_Tokens.mapsto,
        left=make_component(couplet.left, left_color))
    return result_value


def set_to_latex(mobj_set, short: bool=False, depth=0):
    r"""Prints a set formatted in LaTeX.

    The function checks to see if a set contains another set, if it does, then the elements are
    printed by row on new lines, instead of horizontally.  The elements are also indented under the
    outer brackets. This indentation is continued until the nesting stops.

    Returns an error string if the couplet is not an :class:`algebraixlib.mathobjects.couplet.Couplet`.

    :param mobj_set: The set to be turned into LaTeX.
    :param short: When set to ``True``, a short version of the content is generated. Longer parts
        are abbreviated with ellipses ('...'). Defaults to ``False``.
    :param depth: A counter of how many tabs to insert when printing the elements; default is 0.
    :return: The LaTeX markup of the set or an error message.
    """

    assert isinstance(mobj_set, _mo.Set)

    result = _Tokens.left_brace_dyn

    if set_hasa_set(mobj_set):  # Use nesting delimiters for elements.  Print on new lines.
        result += _Tokens.array_start
        #result += nested_set_helper(depth, _Tokens)

        # Add sorting to obtain predictable output.
        elem_itr = iter(sorted(mobj_set.data))

        if short and mobj_set.cardinality > Config.short_set_len + 1:
            result += (_Tokens.comma + nested_set_helper(depth)).join(
                [math_object_to_latex(element, short=short, _depth=depth + 1)
                    for element in _itertools.islice(elem_itr, Config.short_set_len)])
            result += _Tokens.comma + nested_set_helper(depth) + _Tokens.ellipsis
            result += '({0})'.format(mobj_set.cardinality - Config.short_set_len)
        else:
            result += (_Tokens.comma + nested_set_helper(depth)).join(
                [math_object_to_latex(element, short=short, _depth=depth + 1)
                    for element in elem_itr])

        result += _Tokens.array_end

    else:  # Use comma delimiters for elements. Print on single line.
        # Add sorting to obtain predictable output.
        elem_itr = iter(sorted(mobj_set.data))

        if short and mobj_set.cardinality > Config.short_set_len + 1:
            is_couplet_list = [isinstance(elem, _mo.Couplet)
                for elem in _itertools.islice(mobj_set, Config.short_set_len)]
        else:
            is_couplet_list = [isinstance(elem, _mo.Couplet) for elem in mobj_set]
        parenthesize_couplets = any(is_couplet_list) and not all(is_couplet_list)

        def optionally_parenthesize_couplet(element):
            def do_paren(e):
                return parenthesize_couplets and isinstance(e, _mo.Couplet)

            left = _Tokens.left_paren if do_paren(element) else ''
            right = _Tokens.right_paren if do_paren(element) else ''
            elem_latex = math_object_to_latex(element, short=short, _depth=depth + 1)
            return "{}{}{}".format(left, elem_latex, right)

        if short and mobj_set.cardinality > Config.short_set_len + 1:
            result += (_Tokens.comma + _Tokens.space).join(
                optionally_parenthesize_couplet(element)
                    for element in _itertools.islice(elem_itr, Config.short_set_len))
            result += _Tokens.comma + _Tokens.space + _Tokens.ellipsis
            result += '({0})'.format(mobj_set.cardinality - Config.short_set_len)
        else:
            result += (_Tokens.comma + _Tokens.space).join(
                optionally_parenthesize_couplet(element) for element in elem_itr)

    result += _Tokens.right_brace_dyn
    return result


def mset_to_latex(mobj_mset, short: bool=False, depth=0):

    assert isinstance(mobj_mset, _mo.Multiset)

    def latex_mset(value, multiple):
        return '{value}{separator}{multiple}'.format(
            value=math_object_to_latex(value, short=short, _depth=depth + 1),
            separator=_Tokens.colon + _Tokens.space,
            multiple=multiple)

    if set_hasa_set(mobj_mset):  # Use nesting delimiters for elements.  Print on new lines.
        start = _Tokens.array_start
        separator = _Tokens.comma + nested_set_helper(depth)
        end = _Tokens.array_end
    else:  # Use comma delimiters for elements. Print on single line.
        start = ''
        separator = _Tokens.comma + _Tokens.space
        end = ''

    result = _Tokens.left_bracket_dyn + start

    if short and mobj_mset.cardinality > Config.short_set_len + 1:
        result += separator.join([latex_mset(elem_key, multiple)
            for elem_key, multiple in _itertools.islice(
                sorted(mobj_mset.data.items()), Config.short_set_len)])
        result += separator + _Tokens.ellipsis
    else:
        result += separator.join([latex_mset(elem_key, multiple)
            for elem_key, multiple in sorted(mobj_mset.data.items())])

    result += end + _Tokens.right_bracket_dyn
    return result
