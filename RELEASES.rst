.. Algebraix Technology Core Library documentation.
    Copyright Algebraix Data Corporation 2015 - 2017

    This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.

    algebraixlib is free software: you can redistribute it and/or modify it under the terms of
    version 3 of the GNU Lesser General Public License as published by the Free Software Foundation.

    algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
    If not, see <http://www.gnu.org/licenses/>.

    This file is not included via toctree. Mark it as orphan to suppress the warning that it isn't
    included in any toctree.

:orphan:

Release Notes for algebraixlib
==============================

1.4
---

-   Moved ``CacheStatus`` into its own module and removed ``utils.py`` in ``mathobjects``.
-   Moved all of the modules in ``io`` into ``import_export``.
-   Allow ``import_json`` to take in floats.
-   Better handling of less than functionality for couplets, multisets, and sets.
-   Added a ``tmp_sqlda_op``  to handle nodes that are not "SQL-DA" operations.

1.3
---

-   ``Atom``:

    -   Bug fix to not compare differently typed values as equal.
    -   Updated to have pickle support.

-   mojson.py extended to support ``Multiset``.
-   ``import_csv`` function:

    -   Updated to have new argument for column names.
    -   Updated to propagate multiclan properties.

-   ``Undef``:

    -   Updated to have a factory function.
    -   ``Undef`` propagation added to all algebras to support correct answers for chaining
        data algebra expressions.

-   ``Multiset``:

    -   Iteration performance improved.
    -   Updated to support ``[]`` notation.

-   ``Mathobject`` updated to have ``__deepcopy__`` method.
-   ``unary_multi_extend`` updated to support either ``Set`` or ``Multiset``.
-   ``Couplet`` updated to have factory function.
-   ``Set`` updated to have factory function.
-   Partition functions extended to operate on ``Multiset``\s.
-   ``Multiclan`` bug fix for multiplicities in substrict/superstrict operations.
-   Minor quality of life improvements to ``mo_to_str`` function.
-   ``Multiclan`` algebra updated to have new operations:

    -   ``get_rights``
    -   ``get_rights_for_left``
    -   ``project``
    -   ``from_dict``
    -   ``diag``
    -   ``defined_at``
    -   ``order_slice_to_listgen``
    -   ``order_slice``
    -   ``multiclan_to_listgen``

-   ``Multiset`` algebra updated to have new operations:

    -   ``get_left_set``
    -   ``get_right_set``
    -   ``single``
    -   ``some``

-   Minor quality of life changes to miscellaneous.py.

1.2
---

-   Major improvements to how ``MathObject`` properties are handled.
-   Corrections to propagations of ``MathObject`` properties.
-   Additions to math documentation.
-   Added an example IPython notebooks about XML representation.
-   Minor corrections to example code in IPython notebooks.
-   Minor improvements to layout of documentation.

1.1
---

-   Initial release.
