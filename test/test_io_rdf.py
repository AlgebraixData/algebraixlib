"""Testing the io.rdf module."""

# $Id: test_io_rdf.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import inspect
import io
import os
from rdflib import BNode, Literal, URIRef, XSD
import sys
import unittest

import algebraixlib.algebras.clans as clans
from algebraixlib.mathobjects import Atom, Couplet, Set
# noinspection PyUnresolvedReferences
from data_rdf import basic_graphs as bg, result_tables as rt

# noinspection PyProtectedMember
from algebraixlib.io.rdf import _convert_identifier_to_mathobject, import_graph, export_table
from algebraixlib.util.rdf import is_file_url, get_file_url, is_triple, is_absolute_triple, \
    is_graph, is_absolute_graph, triple_match, join, make_triple

# This graph is extracted from examples.sampleRdfGraph.py
sample_graph = """
    <id:jeff> <rdf:name> 'jeff' .
    <id:jeff> <rdf:type> <cat:engineer> .
    <id:james> <rdf:name> 'james' .
    <id:james> <rdf:type> <cat:engineer> .
    <id:james> <fav:mathobject> <type:couplet> .
    <id:donald> <rdf:type> <cat:duck> .
    <id:donald> <rdf:name> 'donald duck' .
    <id:donald> <fav:mathobject> <type:atom> .
"""


class RdfTest(unittest.TestCase):
    """Test the io.rdf module."""

    print_examples = False

    def test_is_file_url(self):
        """Test determining if a string is an URL"""
        self.assertFalse(is_file_url("file:"))
        self.assertTrue(is_file_url("file://"))

    def test_get_file_url(self):
        cwd_url = get_file_url(os.getcwd()) + '/'
        if sys.platform == 'win32':
            cwd_drive = os.getcwd()[:2]
            self.assertEqual(get_file_url('/abc/de'), 'file:///{dr}/abc/de'.format(dr=cwd_drive))
            self.assertEqual(get_file_url(r'\bbc\de'), 'file:///{dr}/bbc/de'.format(dr=cwd_drive))
            self.assertEqual(get_file_url('//cbc/de'), 'file://cbc/de')
            self.assertEqual(get_file_url(r'C:\dbc\de'), 'file:///C:/dbc/de')
            self.assertEqual(get_file_url('C:/ebc/de'), 'file:///C:/ebc/de')
            self.assertEqual(get_file_url(r'fbc\de'), cwd_url + 'fbc/de')
        else:
            self.assertEqual(get_file_url('/abc/de'), 'file:///abc/de')
            self.assertEqual(get_file_url('//cbc/de'), 'file://cbc/de')
            self.assertEqual(get_file_url('fbc/de'), cwd_url + 'fbc/de')

    def test_is_graph(self):
        """Test identifying a graph."""
        graph = Set({make_triple(1, 2, 3)})
        self.assertTrue(is_graph(graph))
        # not a clan
        not_graph = Atom('a')
        self.assertFalse(is_graph(not_graph))
        # not left regular
        not_graph = Set({Couplet('a', 1), Couplet('a', 2), Couplet('a', 3)})
        self.assertFalse(is_graph(not_graph))
        # left set is not spo
        not_graph = Set({Couplet('a', 1), Couplet('b', 2), Couplet('c', 3)})
        self.assertFalse(is_graph(not_graph))

    def test_is_absolute_graph(self):
        """Test identifying an absolute graph."""
        graph = Set({make_triple(1, 2, 3)})
        self.assertTrue(is_absolute_graph(graph))
        # not a clan
        not_graph = Atom('a')
        self.assertFalse(is_absolute_graph(not_graph))
        # not left regular
        not_graph = Set({Couplet('a', 1), Couplet('a', 2), Couplet('a', 3)})
        self.assertFalse(is_absolute_graph(not_graph))
        # left set is not spo
        not_graph = Set({Couplet('a', 1), Couplet('b', 2), Couplet('c', 3)})
        self.assertFalse(is_absolute_graph(not_graph))

    def test_is_triple(self):
        """Test identifying a triple."""
        # a relation with left set 'spo' and cardinality 3
        triple = Set({Couplet('s', 1), Couplet('p', 2), Couplet('o', 3)})
        self.assertTrue(is_triple(triple))
        # a relation with left set 'abc'
        not_triple = Set({Couplet('a', 1), Couplet('b', 2), Couplet('c', 3)})
        self.assertFalse(is_triple(not_triple))
        # a relation with cardinality 4
        not_triple = Set({Couplet('s', 1), Couplet('p', 2), Couplet('o', 3), Couplet('a', 1)})
        self.assertFalse(is_triple(not_triple))
        # not a relation
        not_triple = Set({Atom('s'), Atom('p'), Atom('o')})
        self.assertFalse(is_triple(not_triple))

    def test_is_absolute_triple(self):
        """Test identifying an absolute triple."""
        # a relation with left set 'spo' and cardinality 3
        absolute_triple = Set({Couplet('s', 1), Couplet('p', 2), Couplet('o', 3)})
        self.assertTrue(is_absolute_triple(absolute_triple))
        # a relation with left set 'abc'
        not_absolute_triple = Set({Couplet('a', 1), Couplet('b', 2), Couplet('c', 3)})
        self.assertFalse(is_absolute_triple(not_absolute_triple))
        # a relation with cardinality 4
        not_absolute_triple = Set(Couplet('s', 1), Couplet('p', 2), Couplet('o', 3),
            Couplet('a', 1))
        self.assertFalse(is_absolute_triple(not_absolute_triple))
        # not a relation
        not_absolute_triple = Set({Atom('s'), Atom('p'), Atom('o')})
        self.assertFalse(is_absolute_triple(not_absolute_triple))

    def test_make_triple(self):
        self.assertEqual(
            make_triple(1, 2, 3),
            Set([Couplet('s', 1), Couplet('p', 2), Couplet('o', 3)])
        )

    def test_import_graph(self):
        """Test importing clans from files and strings (function import_graph())."""
        self.assertRaises(AssertionError, lambda: import_graph())
        self.assertRaises(AssertionError, lambda: import_graph(input_file='1', input_data='2'))

        def check_graph(graph_mo, graph_ref):
            self.assertEqual(graph_mo.get_ground_set(), clans.get_absolute_ground_set())
            self.assertEqual(graph_mo.get_left_set(), Set('s', 'p', 'o'))
            self.assertEqual(graph_mo, graph_ref)

        for graph_id in bg.keys():
            graph_data = bg[graph_id]
            if 'file' in graph_data:
                graph = import_graph(input_file=graph_data['file']())
                check_graph(graph, graph_data['mo']())
            else:
                assert 'graph' in graph_data
                graph1 = import_graph(input_file=io.StringIO(graph_data['graph']()))
                check_graph(graph1, graph_data['mo']())
                graph2 = import_graph(input_data=graph_data['graph']())
                check_graph(graph2, graph_data['mo']())

    def test_convert_identifier_to_mathobject(self):
        """Test the function _convert_identifier_to_mathobject()."""
        self.assertRaises(TypeError, lambda: _convert_identifier_to_mathobject(5))
        self.assertEqual(
            Atom(URIRef('http://server/path')),
            _convert_identifier_to_mathobject(URIRef('http://server/path')))
        self.assertEqual(
            Atom(BNode('http://server/path')),
            _convert_identifier_to_mathobject(BNode('http://server/path')))
        self.assertNotEqual(
            Atom(BNode('http://server/path')),
            _convert_identifier_to_mathobject(URIRef('http://server/path')))
        self.assertEqual(
            Atom(1),
            _convert_identifier_to_mathobject(Literal('1', datatype=XSD.integer)))
        self.assertEqual(
            Atom(1.0),
            _convert_identifier_to_mathobject(Literal('1', datatype=XSD.double)))
        self.assertNotEqual(
            Atom(1),
            _convert_identifier_to_mathobject(Literal('1', datatype=XSD.double)))
        self.assertEqual(
            Atom('1'),
            _convert_identifier_to_mathobject(Literal('1', datatype=XSD.string)))
        self.assertNotEqual(
            Atom(1),
            _convert_identifier_to_mathobject(Literal('1', datatype=XSD.string)))

    def test_export_table(self):
        table = rt['1']
        lefts = table.get_left_set()
        self.assertRaises(TypeError, lambda: export_table(lefts, table, '1'))

        csv = io.StringIO(newline='')
        self.assertRaises(AssertionError, lambda: export_table(csv, lefts, table, '1'))

        csv = io.StringIO(newline='')
        export_table(file_or_path=csv, lefts=lefts, table=table, out_format='csv')
        csv_str = csv.getvalue()
        if self.print_examples:
            print('csv:', csv_str)
        self.assertEqual(csv_str, """\
"?cnt", "?eng", "?fav", "?name", "_:b0"
"6", "id:james", "type:couplet", "james", "blank node"
""")

        json = io.StringIO(newline='')
        export_table(file_or_path=json, lefts=lefts, table=table, out_format='json')
        json_str = json.getvalue()
        if self.print_examples:
            print('json:', json_str)
        self.assertEqual(json_str, """\
{"head":{"vars":["?cnt", "?eng", "?fav", "?name", "_:b0"]},
"results":{"bindings":[
{"?cnt": {"type":"literal", "datatype":"http://www.w3.org/2001/XMLSchema#integer", "value":"6"}
, "?eng": {"type":"uri", "value":"id:james"}
, "?fav": {"type":"uri", "value":"type:couplet"}
, "?name": {"type":"literal", "value":"james"}
, "_:b0": {"type":"bnode", "value":"blank node"}
}
]}}""")

        table = rt['2']
        lefts = table.get_left_set()

        csv = io.StringIO(newline='')
        export_table(file_or_path=csv, lefts=lefts, table=table, out_format='csv')
        csv_str = csv.getvalue()
        if self.print_examples:
            print('csv:', csv_str)

        json = io.StringIO(newline='')
        export_table(file_or_path=json, lefts=lefts, table=table, out_format='json')
        json_str = json.getvalue()
        if self.print_examples:
            print('json:', json_str)

    def test_triple_match_assert(self):
        self.assertRaises(AssertionError, lambda: triple_match(Atom(1)))

    def test_triple_match(self):
        # Determine the number of types in the graph data
        graph_type_cnt = sample_graph.count('rdf:type')

        # Import the example graph as data algebra MathObject.
        graph = import_graph(input_data=sample_graph, rdf_format='turtle')
        
        # Extract the triples that have a type and include their id
        triples_matched = triple_match(graph, '?id', URIRef('rdf:type'), '?type')

        # Verify that the number of sets matched equals the number of types in the graph
        self.assertEqual(len(triples_matched), graph_type_cnt)

    def test_join_binary(self):
        clan1 = Set(Set([Couplet(1, 'one')]))
        clan2 = Set(Set([Couplet(2, 'two')]))
        answer = Set(Set([Couplet(1, 'one'), Couplet(2, 'two')]))
        joined = join(clan1, clan2)
        # data is unordered so don't use equality, use symmetric difference
        self.assertEqual(0, len(answer.data ^ joined.data))

    def test_join_ternary(self):
        clan1 = Set(Set([Couplet(1, 'one')]))
        clan2 = Set(Set([Couplet(2, 'two')]))
        clan3 = Set(Set([Couplet(3, 'three')]))
        answer = Set(Set([Couplet(1, 'one'), Couplet(2, 'two'), Couplet(3, 'three')]))
        joined = join(clan1, clan2, clan3)
        # data is unordered so don't use equality, use symmetric difference
        self.assertEqual(0, len(answer.data ^ joined.data))

    def test_join_quaternary(self):
        clan1 = Set(Set([Couplet(1, 'one')]))
        clan2 = Set(Set([Couplet(2, 'two')]))
        clan3 = Set(Set([Couplet(3, 'three')]))
        clan4 = Set(Set([Couplet(4, 'four')]))
        answer = Set(Set(Couplet(1, 'one'), Couplet(2, 'two'), Couplet(3, 'three'),
            Couplet(4, 'four')))
        joined = join(clan1, clan2, clan3, clan4)
        # data is unordered so don't use equality, use symmetric difference
        self.assertEqual(0, len(answer.data ^ joined.data))


# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
