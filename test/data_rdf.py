"""RDF example data for tests."""

# $Id: data_rdf.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import os as _os
from rdflib import URIRef as _URIRef
from rdflib import BNode as _BNode

from algebraixlib.util.rdf import get_file_url as _get_file_url
from algebraixlib.mathobjects import Couplet, Set
from algebraixlib.util.test import get_test_file_path as _get_test_file_path

_print_examples = False
_cwd_url = _get_file_url(_os.getcwd()) + '/'


def _print_object_collection(name):
    if _print_examples:
        print('{name}:'.format(name=name))
        for key, val in sorted(globals()[name].items()):
            print('  "{key}": {val}'.format(key=key, val=val))


#: Basic RDF graphs.
basic_graphs = {
    '1': {
        'graph': lambda: """<absolute:b> <relative> "literal" .""",
        'mo': lambda: Set(Set([
            Couplet('s', _URIRef('absolute:b')),
            Couplet('p', _URIRef(_cwd_url + 'relative')),
            Couplet('o', 'literal')])
        )
    },
    '2': {
        'file': lambda: _get_test_file_path(__file__, '2.ttl'),
        'mo': lambda: Set({
            Set({
                Couplet('s', _URIRef('http://foo/a#b')),
                Couplet('p', _URIRef('http://foo/a#p1')),
                Couplet('o', '123')
            }),
            Set({
                Couplet('s', _URIRef('http://foo/a#b')),
                Couplet('p', _URIRef('http://foo/a#p1')),
                Couplet('o', '456')
            }),
            Set({
                Couplet('s', _URIRef('http://foo/b#b')),
                Couplet('p', _URIRef('http://foo/a#p2')),
                Couplet('o', _URIRef('http://foo/a#v1'))
            }),
            Set({
                Couplet('s', _URIRef('http://foo/b#b')),
                Couplet('p', _URIRef('http://foo/a#p3')),
                Couplet('o', _URIRef('http://foo/a#v2'))
            }),
        })
    },
    '3': {
        'graph': lambda: """
            <:claudius> <a:spouseOf> <:gertrude> .
            <:claudius> <a:uncleOf> <:hamlet> .
            <:gertrude> <a:motherOf> <:hamlet> .
            <:hamlet> <a:friendOf> <:horatio> .
            <:hamlet> <a:friendOf> <:rosencrantz> .
            <:hamlet> <a:friendOf> <:guildenstern> .
            <:ophelia> <a:girlfriendOf> <:hamlet> .
        """,
        'mo': lambda: Set({
            Set({
                Couplet('s', _URIRef(':claudius')),
                Couplet('p', _URIRef('a:spouseOf')),
                Couplet('o', _URIRef(':gertrude'))
            }),
            Set({
                Couplet('s', _URIRef(':claudius')),
                Couplet('p', _URIRef('a:uncleOf')),
                Couplet('o', _URIRef(':hamlet'))
            }),
            Set({
                Couplet('s', _URIRef(':gertrude')),
                Couplet('p', _URIRef('a:motherOf')),
                Couplet('o', _URIRef(':hamlet'))
            }),
            Set({
                Couplet('s', _URIRef(':hamlet')),
                Couplet('p', _URIRef('a:friendOf')),
                Couplet('o', _URIRef(':horatio'))
            }),
            Set({
                Couplet('s', _URIRef(':hamlet')),
                Couplet('p', _URIRef('a:friendOf')),
                Couplet('o', _URIRef(':rosencrantz'))
            }),
            Set({
                Couplet('s', _URIRef(':hamlet')),
                Couplet('p', _URIRef('a:friendOf')),
                Couplet('o', _URIRef(':guildenstern'))
            }),
            Set({
                Couplet('s', _URIRef(':ophelia')),
                Couplet('p', _URIRef('a:girlfriendOf')),
                Couplet('o', _URIRef(':hamlet'))
            })
        })
    },
}
_print_object_collection('basic_graphs')

#: RDF result tables
result_tables = {
    '1': Set([
        Set([
            Couplet(right=_URIRef('type:couplet'), left='?fav'),
            Couplet(right='james', left='?name'),
            Couplet(right=_URIRef('id:james'), left='?eng'),
            Couplet(right=6, left='?cnt'),
            Couplet(right=_BNode('blank node'), left='_:b0')
        ]),
    ]),
    '2': Set([
        Set([
            Couplet(right=_URIRef('type:couplet'), left='?fav'),
            Couplet(right='james', left='?name'),
            Couplet(right=_URIRef('id:james'), left='?eng'),
            Couplet(right=6, left='?cnt'),
            Couplet(right=_BNode('blank node0'), left='_:b0')
        ]),
        Set([
            Couplet(right='jeff', left='?name'),
            Couplet(right=_URIRef('id:jeff'), left='?eng'),
            Couplet(right=2.0, left='?cnt'),
            Couplet(right=_BNode('blank node1'), left='_:b1')
        ]),
    ]),
}
_print_object_collection('result_tables')
