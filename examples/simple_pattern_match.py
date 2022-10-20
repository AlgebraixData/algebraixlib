"""Examples for Data Algebra library."""

# Copyright Permission.io, Inc. (formerly known as Algebraix Data Corporation), Copyright (c) 2022.
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

import algebraixlib.algebras.clans as clans
from algebraixlib.import_export.rdf import import_graph
from algebraixlib.util.html import DataAlgebraHtmlDescriptor as HtmlDesc, math_object_as_html
from algebraixlib.util.miscellaneous import open_webpage_from_html_str
from algebraixlib.util.rdf import match_and_project

from examples.sample_rdf_graph import sample_graph


print_examples = True
show_results_as_webpage = True


# Import and print the input graph.
graph_algebra = import_graph(io.StringIO(sample_graph), rdf_format='turtle')
if print_examples:
    print('Input graph:', sample_graph)
    print('Input graph (as MathObject):', graph_algebra)


# Query the imported graph using general pattern matching APIs.
names = match_and_project(
    graph_algebra,
    {'p': rdflib.URIRef('rdf:name')},
    {'s': '?eng', 'o': '?name'}
)
engineers = match_and_project(
    graph_algebra,
    {'p': rdflib.URIRef('rdf:type'), 'o': rdflib.URIRef('cat:engineer')},
    {'s': '?eng'}
)
engs_and_names = clans.cross_functional_union(names, engineers)

if print_examples:
    print('Engineers and their names:', engs_and_names)


# Present results.
if show_results_as_webpage:
    descriptors = [
        HtmlDesc('Input Graph', graph_algebra, 'The RDF graph source:' + sample_graph),
        HtmlDesc('Result', engs_and_names, 'Only engineers with names.')
    ]
    html = math_object_as_html('Simple Pattern Match Example', descriptors)
    open_webpage_from_html_str(html)
