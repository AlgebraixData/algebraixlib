"""Import and export facilities for RDF data."""

# $Id: rdf.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import abc
import rdflib as _rdflib

import algebraixlib.algebras.clans as _clans
import algebraixlib.algebras.relations as _relations
import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _ud
import algebraixlib.util.miscellaneous as _misc
import algebraixlib.util.rdf as _rdf


def import_graph(input_file=None, input_data: str=None, rdf_format: str=None) -> 'PP(A x A)':
    """Return an :term:`absolute` :term:`graph` into which the RDF graph ``input_file`` has been
    imported.

    -   The left components are 's' (subject), 'p' (predicate) and 'o' (object) (see `triple`).
    -   Blank nodes are converted to IRIs (skolemization).
    -   URI references are represented as rdflib.URIRef instances (embedded in an :class:`~.Atom`).
    -   Literals are converted to intuitive native Python types (embedded in an :class:`~.Atom`).

    :param input_file: A string that is a path (relative or absolute) to the file to be imported,
        or a `StringIO` instance. Exactly one of ``input_file`` and ``input_data`` must be given.
    :param input_data: The input data as string. Exactly one of ``input_file`` and ``input_data``
        must be given.
    :param rdf_format: The format of the RDF graph that is being imported. See `<Plugin parsers>`_
        for a list of supported formats and their corresponding strings. If none is given, the file
        name's extension is used to guess a format. If that fails, Turtle is used as default.
    :return: An :term:`absolute` :term:`graph` with the data from the RDF graph that has been
        imported.

    .. _Plugin parsers: http://rdflib.readthedocs.org/en/latest/plugin_parsers.html
    """
    if input_file is None and input_data is None:
        raise AssertionError("Exactly one of 'input_file' and 'input_data' must be given")
    if input_file is not None and input_data is not None:
        raise AssertionError("Exactly one of 'input_file' and 'input_data' must be given")

    if rdf_format is None:
        try:
            rdf_format = _rdflib.util.guess_format(input_file) or 'turtle'
        except AttributeError:
            rdf_format = 'turtle'

    graph = _rdflib.Graph()
    graph.parse(source=input_file, data=input_data, format=rdf_format)
    graph.skolemize()
    return _convert_graph_to_mathobjects(graph)


def export_table(file_or_path, lefts: 'P( A )', table: 'PP(A x A)', out_format: str='csv'):
    """Return a serialized table as string in a supported RDF format for table serialization.

    **Limitations**:
    -   Leading '?' and '$' are not stripped from lefts (variable names).
    -   Non-printable characters are backslash-escaped.
    -   ``table`` must be an :term:`absolute` :term:`graph`.

    :param file_or_path: Either a file path (in this case the data is written to a file at this
        location) or a file object (in this case the data is written to its ``.write()`` function).
    :param lefts: The set of the left components in ``table`` that is exported.
    :param table: A :term:`clan` that contains the data to be exported.
    :param out_format: A supported RDF table format. Supported are ``'csv'`` (`<SPARQL 1.1 Query
        Results CSV and TSV Formats>`_) and ``'json'`` (`<SPARQL 1.1 Query Results JSON Format>`_).

    .. _SPARQL 1.1 Query Results CSV and TSV Formats:
        http://www.w3.org/TR/2013/REC-sparql11-results-csv-tsv-20130321/
    .. _SPARQL 1.1 Query Results JSON Format:
        http://www.w3.org/TR/2013/REC-sparql11-results-json-20130321/
    """

    # noinspection PyPep8
    class Csv(_ExportTable):
        """Specialize _ExportTable for RDF CSV."""
        def __init__(self, clan, ordered_lefts):
            _ExportTable.__init__(self, clan=clan, ordered_lefts=ordered_lefts)
        def _doc_start(self):
            pass
        def _doc_end(self):
            pass
        def _header_start(self):
            pass
        def _header_between_lefts(self):
            self._file.write(', ')
        def _header_end(self):
            self._file.write('\n')
        def _body_start(self):
            pass
        def _body_end(self):
            pass
        def _row_start(self):
            pass
        def _row_between_relations(self):
            pass
        def _row_end(self):
            self._file.write('\n')
        def _item_between_couplets(self):
            self._file.write(', ')
        def _write_item(self, left, right, prefix_separator):
            if right is not _ud.Undef():
                self._write_atom(right)
        def _write_atom(self, atom: _mo.Atom):
            data = str(atom.value).replace('"', '""')
            self._file.write('"' + data + '"')

    # noinspection PyPep8
    class Json(_ExportTable):
        """Specialize _ExportTable for RDF JSON."""
        def __init__(self, clan, ordered_lefts):
            _ExportTable.__init__(self, clan=clan, ordered_lefts=ordered_lefts)
        def _doc_start(self):
            self._file.write('{')
        def _doc_end(self):
            self._file.write('}')
        def _header_start(self):
            self._file.write('"head":{"vars":[')
        def _header_between_lefts(self):
            self._file.write(', ')
        def _header_end(self):
            self._file.write(']},\n')
        def _body_start(self):
            self._file.write('"results":{"bindings":[\n')
        def _body_end(self):
            self._file.write(']}')
        def _row_start(self):
            self._file.write('{')
        def _row_between_relations(self):
            self._file.write(',')
        def _row_end(self):
            self._file.write('}\n')
        def _item_between_couplets(self):
            pass
        def _write_item(self, left, right, prefix_separator):
            if right is not _ud.Undef():
                if prefix_separator:
                    self._file.write(', ')
                self._write_atom(left)
                self._file.write(': {"type":')
                if isinstance(right.value, _rdflib.URIRef):
                    self._file.write('"uri"')
                elif isinstance(right.value, _rdflib.BNode):
                    self._file.write('"bnode"')
                else:
                    self._file.write('"literal"')
                    lit = _rdflib.Literal(right.value)
                    if isinstance(lit.datatype, str):
                        self._file.write(', "datatype":"')
                        self._file.write(lit.datatype)
                        self._file.write('"')
                self._file.write(', "value":')
                self._write_atom(right)
                self._file.write('}\n')
        def _write_atom(self, atom: _mo.Atom):
            self._file.write('"' + str(atom.value) + '"')

    assert(_clans.is_absolute_member(table))
    sorted_lefts = sorted(lefts)
    if out_format == 'csv':
        writer = Csv(clan=table, ordered_lefts=sorted_lefts)
    elif out_format == 'json':
        writer = Json(clan=table, ordered_lefts=sorted_lefts)
    else:
        raise AssertionError("'out_format' must be 'csv' or 'json'")
    writer.export(file_or_path)


def _convert_graph_to_mathobjects(rdflib_graph: _rdflib.Graph) -> 'PP(A x A)':
    """Return a `graph` from the data in the `~_rdflib.Graph` `rdflib_graph`."""
    return _mo.Set(_make_triple_from_graph(triple_tuple) for triple_tuple in rdflib_graph)


def _make_triple_from_graph(triple_tuple) -> 'P(A x A)':
    """Return a `triple` created from the rdflib triple tuple ``triple_tuple``."""
    return _rdf.make_triple(
        subject=_convert_identifier_to_mathobject(triple_tuple[0]),
        predicate=_convert_identifier_to_mathobject(triple_tuple[1]),
        object_=_convert_identifier_to_mathobject(triple_tuple[2])
    )


def _convert_identifier_to_mathobject(term) -> '( A )':
    """Return an :class:`~.Atom` with the rdflib identifier ``term`` converted into the atom's
    value.

    :param term: Must be an `rdflib.URIRef`, `rdflib.BNode` or an `rdflib.Literal`.
    :return: An :class:`~.Atom` with a value derived from ``term``:
        -   `URIRef` and `BNode` instances are inserted into the atom as their type.
        -   `Literal` instances are inserted as the intuitive native Python type (using
            `Literal.toPython` -- see the documentation for `Literal`).
    """
    if isinstance(term, _rdflib.URIRef) or isinstance(term, _rdflib.BNode):
        return _mo.Atom(term)
    elif isinstance(term, _rdflib.Literal):
        return _mo.Atom(term.toPython())
    else:
        raise TypeError("'term' must be 'URIRef', 'BNode' or 'Literal'")


class _ExportTable(abc.ABC):
    """A base class for data export writers for tabular data (absolute clans)."""

    def __init__(self, clan: 'PP(A x A)', ordered_lefts=None, leftset: 'P( A )'=None):
        """Constructor. Call in the derived class's constructor.

        :param clan: The tabular data to be exported.
        :param ordered_lefts: An optional (ordered) list of left atoms that determines the
            columns to be exported from ``clan`` and their order.
        :param leftset: An optional (unordered) set of left atoms that determines the the columns
            to be exported from ``clan``. If neither ordered_lefts nor lefts is given, all left
            components from ``clan`` are exported.
        """
        # Is set in .export()
        self._file = None

        if not _clans.is_member(clan):
            raise TypeError("'clan' must be a clan")
        self._clan = clan

        if ordered_lefts is not None:
            if leftset is not None:
                raise AssertionError("Only one of 'ordered_lefts' and 'lefts' may be given")
            if len(ordered_lefts) == 0:
                raise AssertionError("'ordered_lefts' must contain at least one left component")
            for left in ordered_lefts:
                if not isinstance(left, _mo.Atom):
                    raise TypeError("'ordered_lefts' must consist of Atom instances")
            self._ordered_lefts = ordered_lefts
        elif leftset is not None:
            self._ordered_lefts = []
            for left in leftset:
                if not isinstance(left, _mo.Atom):
                    raise TypeError("'lefts' must consist of Atom instances")
                self._ordered_lefts.append(left)
            if len(self._ordered_lefts) == 0:
                raise AssertionError("'lefts' must contain at least one left component")
        else:
            lefts = _clans.get_lefts(clan, _checked=False)
            self._ordered_lefts = [left for left in lefts]

    def export(self, file_or_path):
        """Export the data of this instance to ``file_or_path``.

        :param file_or_path: Either a file path (in this case the data is written to a file at this
            location) or a file object (in this case the data is written to its .write() function).
        """
        def write_data(out_file):
            self._file = out_file
            self._doc_start()
            self._write_header()
            self._write_body()
            self._doc_end()
        _misc.write_to_file_or_path(file_or_path, write_data)

    # ----------------------------------------------------------------------------------------------

    @abc.abstractmethod
    def _doc_start(self):
        """Document start sequence."""
        pass

    @abc.abstractmethod
    def _doc_end(self):
        """Document end sequence."""
        pass

    @abc.abstractmethod
    def _header_start(self):
        """Header start sequence."""
        pass

    @abc.abstractmethod
    def _header_between_lefts(self):
        """Sequence between the lefts in the header (that's not in start or end)."""
        pass

    @abc.abstractmethod
    def _header_end(self):
        """Header end sequence."""
        pass

    @abc.abstractmethod
    def _body_start(self):
        """Body (data) start sequence."""
        pass

    @abc.abstractmethod
    def _body_end(self):
        """Body (data) end sequence."""
        pass

    @abc.abstractmethod
    def _row_start(self):
        """Row (relation) start sequence."""
        pass

    @abc.abstractmethod
    def _row_between_relations(self):
        """Sequence between the rows/relations (that's not in start or end)."""
        pass

    @abc.abstractmethod
    def _row_end(self):
        """Row (relation) end sequence."""
        pass

    @abc.abstractmethod
    def _write_item(self, left, right, prefix_separator):
        """Write an item. Prefix a separator (if this is not handled by _item_between_couplets())
        if prefix_separator is True."""
        pass

    @abc.abstractmethod
    def _item_between_couplets(self):
        """Sequence between the items/couplets (that's not in _write_item())."""
        pass

    @abc.abstractmethod
    def _write_atom(self, atom: _mo.Atom):
        """Write a data item. Handle escaping, quoting etc. -- everything to convert an atom into an
        output string."""
        pass

    # ----------------------------------------------------------------------------------------------

    def _write_header(self):
        self._header_start()
        itr = iter(self._ordered_lefts)
        self._write_atom(next(itr))
        for left in itr:
            self._header_between_lefts()
            self._write_atom(left)
        self._header_end()

    def _write_body(self):
        self._body_start()
        relation_itr = iter(self._clan)
        self._write_row(next(relation_itr))
        for relation in relation_itr:
            self._row_between_relations()
            self._write_row(relation)
        self._body_end()

    def _write_row(self, relation: 'P(A x A)'):
        self._row_start()
        lefts_itr = iter(self._ordered_lefts)
        left = next(lefts_itr)
        self._write_item_wrapper(relation, left, False)
        for left in lefts_itr:
            self._item_between_couplets()
            self._write_item_wrapper(relation, left, True)
        self._row_end()

    def _write_item_wrapper(self, relation: 'P(A x A)', left: '( A )', prefix_separator: bool):
        right = _relations.get_right(relation, left)
        self._write_item(left, right, prefix_separator)
        pass
