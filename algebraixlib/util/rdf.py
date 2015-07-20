r"""This module contains RDF-specific data manipulation facilities. The code is RDF/SPARQL-inspired
but does not officially implement any RDF standards.

Glossary
========

.. glossary::

    triple
        A :term:`relation` with three members, with the :term:`left component`\s ``'s'``, ``'p'``,
        ``'o'``. A generic triple is an element of :math:`P(A \times M)`; an RDF triple is an
        element of :math:`P(A \times A)`. (See also :term:`set A` and :term:`set M`.)

    graph
        A :term:`clan` where every :term:`relation` it contains is a :term:`triple`. A generic
        graph is an element of :math:`P^2(A \times M)`; an RDF graph is an element of
        :math:`P^2(A \times A)`. (See also :term:`set A` and :term:`set M`.)

API
===

"""

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
import os as _os
import urllib.parse as _urlparse
import urllib.request as _urlreq
import algebraixlib.algebras.clans as _clans
import algebraixlib.algebras.relations as _relations
import algebraixlib.mathobjects as _mo


def is_file_url(path_or_url: str) -> bool:
    """Return ``True`` if ``path_or_url`` is a file URL (that is, starts with ``'file://'``)."""
    return path_or_url.startswith('file://')


def get_file_url(path: str) -> str:
    """Return the file URL that corresponds to the file path ``path``. If ``path`` is relative, it
    is converted into an absolute path before being converted into a file URL."""
    return _urlparse.urljoin('file:', _urlreq.pathname2url(_os.path.abspath(path)))


def is_triple(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is a `triple`."""
    return _relations.is_member(obj) and _check_triple(obj)


def is_absolute_triple(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is an :term:`absolute` :term:`triple`."""
    return _relations.is_absolute_member(obj) and _check_triple(obj)


def make_triple(subject: '( M )', predicate: '( M )', object_: '( M )') -> 'P(A x M)':
    """Return an RDF `triple`, created from ``subject``, ``predicate`` and ``object_``.

    Each of the arguments must be an instance of `MathObject` or a Python type that automatically
    converts to an :class:`~.Atom` in the :class:`~.Couplet` constructor.
    """
    return _mo.Set([
        _mo.Couplet(left='s', right=subject),
        _mo.Couplet(left='p', right=predicate),
        _mo.Couplet(left='o', right=object_),
    ])


def is_graph(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is a `graph`."""
    return _clans.is_member(obj) and _check_graph(obj)


def is_absolute_graph(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is an :term:`absolute` `graph`."""
    return _clans.is_absolute_member(obj) and _check_graph(obj)


def triple_match(rdf_graph: 'PP(A x M)', subject=None, predicate=None, object_=None) -> 'PP(A x M)':
    """Evaluate SPARQL-like triple pattern matches.

    Treat string values for subject, predicate, object that begin with ``'?'`` or ``'$'`` similarly
    to SPARQL variables; they define the projection (output) lefts. Other values are used for
    matching.

    :param rdf_graph: The `graph` on which to operate.
    :param subject: Handle the subjects in ``rdf_graph``: a variable name (create output), a value
        that's not a variable name (match) or ``None`` (ignore).
    :param predicate: Handle the predicates in ``rdf_graph``: a variable name (create output), a
        value that's not a variable name (match) or ``None`` (ignore).
    :param object_: Handle the objects in ``rdf_graph``: a variable name (create output), a value
        that's not a variable name (match) or ``None`` (ignore).
    :return: A :term:`clan` with the matches.
    """
    assert(is_graph(rdf_graph))
    pattern = {}
    projection = {}

    def add(rdf_left, value):
        if value is not None:
            if isinstance(value, str) and value[0] in '?$':
                projection[rdf_left] = value
            else:
                pattern[rdf_left] = value

    add('s', subject)
    add('p', predicate)
    add('o', object_)

    return match_and_project(rdf_graph, pattern, projection)


def join(rdf_solution1, rdf_solution2, *rdf_solutions):
    """Return the functional cross union (:func:`.multiclans.functional_cross_union`) of all
    arguments.
    """
    result = _clans.functional_cross_union(rdf_solution1, rdf_solution2)
    for sln in rdf_solutions:
        result = _clans.functional_cross_union(result, sln)
    return result


def _check_triple(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is (almost) a :term:`triple`. Perform all checks except for the
    membership in the :term:`algebra of relations`."""
    # noinspection PyUnresolvedReferences
    return isinstance(obj, _mo.Set) and obj.cardinality == 3 \
        and obj.get_left_set() == _mo.Set('s', 'p', 'o')


def _check_graph(obj: _mo.MathObject) -> bool:
    """Return ``True`` if ``obj`` is (almost) a :term:`graph`. Perform all checks except for the
    membership in the :term:`algebra of clans`."""
    return isinstance(obj, _mo.Set) and obj.get_left_set() == _mo.Set('s', 'p', 'o') \
        and obj.is_left_regular()


def match_and_project(graph: 'PP( AxA )', pattern: dict=None, projection: dict=None):
    """Return all relations in ``graph`` that contain all members of ``pattern``. Rename their lefts
    according to the members of ``projection``.

    :param graph: An absolute clan.
    :param pattern: A dictionary where the keys are the lefts and the values the rights that
        will be matched.
    :param projection: A dictionary where the values are the new names and the keys the existing
        names of the lefts to be renamed.
    """
    assert(_clans.is_member(graph))
    if pattern is None:
        pattern = {}
    if projection is None:
        projection = {}

    matches = pattern_match(graph, pattern)
    compose_ctrl_set = _clans.transpose(_clans.from_dict(projection))
    return _clans.compose(matches, compose_ctrl_set, _checked=False)


def pattern_match(graph: 'PP( AxA )', pattern: dict):
    """Return all relations in ``graph`` that contain all members of ``pattern``.

    :param graph: An absolute clan.
    :param pattern: A dictionary where the keys are the lefts and the values the rights that
        will be matched.
    """
    assert(_clans.is_member(graph))
    match_predicate = _clans.from_dict(pattern)
    return _clans.superstrict(graph, match_predicate, _checked=False)
