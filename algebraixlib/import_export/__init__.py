r"""This package contains modules with facilities for importing and exporting data.

Supported formats are:

-   :mod:`~.csv`: Export :term:`regular` :term:`clan`\s as CSV data and import CSV data into clans.
-   :mod:`~.json`: Import hierarchical JSON data into nested :term:`relation`\s.
-   :mod:`~.mojson`: Export constructs that contain `MathObject`\s to JSON and import that data.
    This format is guaranteed to round-trip.
-   :mod:`~.rdf`: Import RDF graphs in the formats N-Triples and Turtle. Export tabular results as
    RDF-CSV and RDF-JSON.
-   :mod:`~.xml`: Import hierarchical XML data into nested :term:`relation`\s.

All these import/export facilities are not meant to be full, standard-compliant implementations.
They are rather examples for how these formats can be represented in and converted to data algebra,
missing details and features notwithstanding.
"""

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
