r"""Pretty-printing of `MathObject`\s."""

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
import algebraixlib.mathobjects as _mo


# --------------------------------------------------------------------------------------------------

def mo_to_str(math_object: _mo.MathObject, abbreviated=False, indent_text='   ', indent='',
        max_line_len=95):
    """Return the contents of the `MathObject` ``math_object`` as a readable string.

    :type math_object: _mo.MathObject|_mo.Atom|_mo.Couplet|_mo.Set
    :param abbreviated: If ``False`` spell out `MathObject` names; if ``True`` use shorter symbols.
    :param indent_text: The string used when indenting.
    :param indent: The accumulated indent that is increased using ``indent_text`` during recursive
        calls.
    :param max_line_len: The maximum number of characters per line. Longer lines are truncated.
    """

    def _couplet_pre_text():
        if abbreviated:
            return '('
        return 'Couplet('

    def _couplet_left_text():
        if abbreviated:
            return ''
        return 'left='

    def _couplet_seperator_text():
        if abbreviated:
            return '->'
        return ', '

    def _couplet_right_text():
        if abbreviated:
            return ''
        return 'right='

    def _couplet_post_text():
        if abbreviated:
            return ')'
        return ')'

    def _set_pre_text(type_):
        if abbreviated:
            return '{'
        return type_ + '({'

    def _set_post_text():
        if abbreviated:
            return '}'
        return '})'

    mo_str = ''

    if math_object.is_atom:
        if abbreviated:
            mo_str = str(math_object)
        else:
            mo_str = repr(math_object)

    elif math_object.is_couplet:
        mo_str += indent + _couplet_pre_text() + _couplet_left_text()
        mo_str += mo_to_str(
            math_object.left, abbreviated, indent_text, indent + indent_text, max_line_len)
        mo_str += _couplet_seperator_text() + _couplet_right_text()
        if math_object.right.is_set:
            mo_str += '\n'
        right = mo_to_str(
            math_object.right, abbreviated, indent_text, indent + indent_text, max_line_len)

        if math_object.right.is_atom:
            if len(mo_str) + len(right) > max_line_len:
                pos = max_line_len - len('...') - len(mo_str) - len(right) \
                    - len(_couplet_post_text() + '\n')
                right = right[:pos]
                right += '...'

        mo_str += right

        if math_object.right.is_set:
            mo_str += indent
        mo_str += _couplet_post_text() + '\n'

    elif math_object.is_set or math_object.is_multiset:
        mo_str += indent + _set_pre_text('Set' if math_object.is_set else 'Multiset')

        for sub in math_object:
            if sub.is_set or sub.is_couplet:
                mo_str += '\n'
            break

        i = len(math_object) - 1
        for sub in math_object:
            mo_str += mo_to_str(sub, abbreviated, indent_text, indent + indent_text, max_line_len)
            if sub.is_atom and i > 0:
                mo_str += ', '
                i -= 1
        mo_str += indent + _set_post_text() + '\n'

    else:
        raise AssertionError('Type {type} not yet implemented'.format(type=type(math_object)))

    return mo_str

