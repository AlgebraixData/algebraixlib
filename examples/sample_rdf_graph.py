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
