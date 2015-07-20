"""Examples for using the Data Algebra library to solve RDF/SPARQL-style problems."""

# $Id: rdf_pattern_match.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import io
import rdflib
from time import time

from algebraixlib.io.rdf import export_table, import_graph
from algebraixlib.mathobjects import Set
from algebraixlib.util.html import DataAlgebraHtmlDescriptor as HtmlDesc, math_object_as_html
from algebraixlib.util.miscellaneous import open_webpage_from_html_str
from algebraixlib.util.rdf import triple_match, join

from examples.sampleRdfGraph import sample_graph


print_examples = True
show_results_as_webpage = True


# Print the input graph.
if print_examples:
    print('Input graph:', sample_graph)


# Data Algebra -------------------------------------------------------------------------------------

# Import the example graph as data algebra MathObject.
graph_algebra = import_graph(input_data=sample_graph, rdf_format='turtle')

if print_examples:
    print('Input graph (as MathObject):', graph_algebra)

# Query the MathObject graph, retrieving the id, name and favorite MathObject of all engineers who
# have all three.
start = time()
engineers_algebra = join(
    triple_match(graph_algebra, '?eng', rdflib.URIRef('rdf:name'), '?name'),
    triple_match(graph_algebra, '?eng', rdflib.URIRef('rdf:type'), rdflib.URIRef('cat:engineer')),
    triple_match(graph_algebra, '?eng', rdflib.URIRef('fav:mathobject'), '?fav')
)
elapsed_algebra = time() - start

engineers_algebra_json = io.StringIO()
export_table(
    file_or_path=engineers_algebra_json,
    lefts=Set(['?eng', '?name', '?fav']),
    table=engineers_algebra,
    out_format='json')

if print_examples:
    print('Engineers (data algebra API, took {time:.3f} s): {result}'.format(
        time=elapsed_algebra, result=engineers_algebra))
    print('The data in RDF JSON:\n{json}'.format(json=engineers_algebra_json.getvalue()))


# SPARQL (using rdflib) ----------------------------------------------------------------------------

# Import the example graph as rdflib Graph.
graph_rdflib = rdflib.Graph()
graph_rdflib.parse(data=sample_graph, format='turtle')

# Query the rdflib graph, retrieving the same data as with the previous data algebra query.
query_rdflib = """
    SELECT *
    WHERE {
        ?eng <rdf:name> ?name .
        ?eng <rdf:type> <cat:engineer> .
        ?eng <fav:mathobject> ?fav
    }
"""
start = time()
engineers_rdflib = graph_rdflib.query(query_rdflib)
elapsed_rdflib = time() - start

print(', '.join(engineers_rdflib.vars))
for solution in engineers_rdflib.bindings:
    print(', '.join([solution[var].n3() for var in engineers_rdflib.vars]))
print('(end)')


if print_examples:
    print('Engineers (SPARQL through rdflib, took {time:.3f} s): {result}'.format(
        time=elapsed_rdflib, result=engineers_rdflib.bindings))


# Present results ----------------------------------------------------------------------------------

if show_results_as_webpage:
    descriptors = [
        HtmlDesc(
            'Input Graph',
            graph_algebra,
            'The RDF graph source:' + sample_graph
        ),
        HtmlDesc(
            'Result',
            engineers_algebra,
            'Equivalent to the SPARQL query:' + query_rdflib + '\nWith the JSON result\n\n'
            + engineers_algebra_json.getvalue()
        )
    ]
    html = math_object_as_html('Example 1: Simple Query', descriptors)
    open_webpage_from_html_str(html)
