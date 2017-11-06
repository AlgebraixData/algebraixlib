"""Import data from XML."""

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
# noinspection PyProtectedMember
import algebraixlib.import_export._util as _util
import algebraixlib.mathobjects as _mo
import algebraixlib.util.miscellaneous as _misc


def import_xml(xml_file_or_filepath, convert_numerics: bool=False) -> 'P( A x M )':
    """Import the file ``xml_file_or_filepath`` as XML file and return nested relations.

    :param xml_file_or_filepath: A file path or a file object of the file to be imported.
    :param convert_numerics: If ``True``, numeric values (integers, floating-point numbers) are
        imported as number types. If ``False`` (default), everything is imported as string.
    :return: A nested :term:`relation` starting with a :term:`relation` that contains a single
        :term:`couplet` that represents the single XML root element.
    """
    def _get_atom_value_convert(atom_value: str):
        try:
            return int(atom_value)
        except ValueError:
            try:
                return float(atom_value)
            except ValueError:
                return atom_value

    def _get_atom_value_direct(atom_value: str) -> str:
        return atom_value

    _get_atom_value = _get_atom_value_convert if convert_numerics else _get_atom_value_direct

    def _process_attributes(node):
        for (name, value) in node.attributes.items():
            yield _mo.Couplet(
                left=_util.get_left_cached(name),
                right=_mo.Atom(_get_atom_value(value), True),
                direct_load=True)

    text_left = _mo.Atom('$')

    def _contains_text_node(set_: set) -> bool:
        # Return True if set_ (a set of Couplets) contains a couplet with the left component
        # text_left.
        for couplet in set_:
            if couplet.left == text_left:
                return True
        return False

    _util.get_left_cached.left_cache = {}

    def _process_nodes(nodes):
        for node in nodes:
            if node.nodeType == node.ELEMENT_NODE:
                # attributes and children are sets of Couplets.
                attributes = set(_process_attributes(node))
                children = set(_process_nodes(node.childNodes))  # May include text (text_left).
                children = children.union(attributes)
                if len(children) == 1 and _contains_text_node(children):
                    # We have a single child that is a text node. Remove one layer of couplets.
                    yield _mo.Couplet(
                        left=_util.get_left_cached(node.tagName),
                        right=_misc.get_single_iter_elem(children).right,
                        direct_load=True)
                else:
                    yield _mo.Couplet(
                        left=_util.get_left_cached(node.tagName),
                        right=_mo.Set(children, direct_load=True),
                        direct_load=True)
            elif node.nodeType == node.TEXT_NODE:
                text_node_text = node.data.strip()
                if len(text_node_text) > 0:
                    yield _mo.Couplet(
                        left=text_left,
                        right=_mo.Atom(_get_atom_value(text_node_text), direct_load=True),
                        direct_load=True)
            else:
                assert False  # Node type not supported.

    def _import_xml(xml_file):
        import xml.dom.minidom
        tree = xml.dom.minidom.parse(xml_file)
        return _mo.Set(_process_nodes(tree.childNodes), direct_load=True)

    if hasattr(xml_file_or_filepath, "readlines"):  # support StringIO
        return _import_xml(xml_file_or_filepath)
    else:
        with open(xml_file_or_filepath, encoding='utf-8') as file:
            return _import_xml(file)


def xml_to_str(xml_file_or_filepath, indent_text='   ', truncate=True, max_line_len=95,
        pre_len=0, post_len=0):
    """Return an XML file or string into a consistently formatted XML string.

    :param xml_file_or_filepath: A file path or a file object to be converted.
    :param indent_text: A string of characters used as indent.
    :param truncate: When ``True``, truncate converted text using ``max_line_len``.
    :param max_line_len: The maximum number of characters per line when truncation is used.
    :param pre_len: The maximum length, in characters, the first part of the converted string is
        allowed to be. (The part between ``pre_len`` and ``post_len`` is replaced with a line
        that contains an ellipsis.) Ignored if 0 or if ``post_len`` is 0.
    :param post_len: The maximum length, in characters, the last part of the converted string is
        allowed to be. (The part between ``pre_len`` and ``post_len`` is replaced with a line
        that contains an ellipsis.) Ignored if 0 or if ``pre_len`` is 0.
    """

    if not hasattr(xml_file_or_filepath, "readlines"):  # support StringIO
        xml_file_or_filepath = open(xml_file_or_filepath, encoding='utf-8')

    from xml.dom.minidom import parse
    xml_data = parse(xml_file_or_filepath)
    xml_str = xml_data.toprettyxml(indent_text)

    # Remove duplicate whitespace
    import re
    xml_str = re.sub(r"(?<=\n)[ \t\r]*\n", "", xml_str)
    if not truncate:
        return xml_str

    # Truncate
    def _truncator(matchobj):
        ellipses = '...<'
        len_foo = len(ellipses)
        if len(matchobj.group(0)) > max_line_len:
            return matchobj.group(0)[:max_line_len - len_foo] + ellipses
        return matchobj.group(0)

    xml_str = re.sub(r">.*<", _truncator, xml_str)

    if pre_len > 0 > post_len:
        return xml_str[:pre_len] + '\n...\n' + xml_str[post_len:]

    return xml_str

