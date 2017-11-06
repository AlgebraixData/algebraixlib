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


Algebra Reference
=================

.. glossary::
    :sorted:

    absolute
        Applied to :term:`couplet`\s, :term:`set`\s, constructs derived from them (like
        :term:`relation`\s) and :term:`algebra`\s. Such a construct is called **absolute** if its
        ground set is based on |set A|.

        See for example :term:`absolute set`.

        -   A :term:`relation` that has only members that are elements of the Cartesian product
            :math:`A \times A` is an 'absolute relation'. Example: :math:`\{a{\mapsto}1, b{\mapsto}2\}`.
            (However, an absolute :term:`relation` is *not* an absolute :term:`set`; the members of the
            relation are :term:`couplet`\s, not :term:`atom`\s.)
        -   The relation :math:`\{a{\mapsto}1, b{\mapsto}\{2\}\}` is not an absolute relation, as one
            of the right elements of the member :term:`couplet`\s is not an :term:`atom` (it is a
            :term:`set` :math:`\{2\}`).

    absolute clan
        An :term:`absolute` :term:`clan` is a clan that is an element of the second :term:`power
        set` of the :term:`Cartesian product` of |set A| (:math:`P^2(A \times A)`). Such a clan has
        only :term:`atom`\s as members of the :term:`couplet`\s in the :term:`relation`\s. Example:
        :math:`\{ \{2{\mapsto}1, 3{\mapsto}2\}, \{5{\mapsto}4, 9{\mapsto}7\} \}`.

    absolute couplet
        An :term:`absolute` :term:`couplet` is a couplet that is an element of the :term:`Cartesian
        product` of |set A| (:math:`A \times A`). Such a couplet has only :term:`atom`\s as members.
        Example: :math:`2{\mapsto}1`.

    absolute ground set
        Our :term:`algebra`\s normally have a :term:`ground set` and an **absolute ground set**. The
        absolute ground set is the ground set with the elements of the algebra being expressed in
        terms of |set A|.

        For example, the :term:`ground set` of the algebra of :term:`relation`\s is
        :math:`P(M \times M)`; this allows :term:`set`\s and :term:`couplet`\s as elements of the
        couplets that form the relations. The *absolute ground set* of the algebra of relations is
        :math:`P(A \times A)`; this requires :term:`atom`\s to form the couplets that form the
        relations.

    absolute multiclan
        An :term:`absolute` :term:`multiclan` is a multiclan that has only :term:`atom`\s as
        members of the :term:`couplet`\s in the :term:`relation`\s. See also :term:`absolute clan`.

    absolute multiset
        An :term:`absolute` :term:`multiset` is a multiset that is an element of the :term:`power
        set` of the :term:`Cartesian product` of |set A| with |set N| (:math:`P(A \times N)`.
        Such a multiset has only :term:`atom`\s as elements. Example: :math:`\{1{:}3, 'a'{:}5\}`.

    absolute relation
        An :term:`absolute` :term:`relation` is a set that is an element of the :term:`power set`
        of the :term:`Cartesian product` of |set A| (:math:`P(A \times A)`. Such a set has only
        :term:`couplet`\s as elements that consist only of :term:`atom`\s. Example:
        :math:`\{2{\mapsto}1, 5{\mapsto}2\}`.

    absolute set
        An :term:`absolute` :term:`set` is a set that is an element of the :term:`power set` of
        |set A| (:math:`P(A)`. Such a set has only :term:`atom`\s as elements. Example:
        :math:`\{1, 2\}`.

    algebra
        An **algebra** is a set together with one or more operations defined on it. For a more
        detailed definition see :ref:`algebras`.

    algebra of clans
        The **algebra of clans** is the algebra on :term:`set`\s of :term:`relation`\s.  As a
        result its ground set is the second power set of :term:`couplet`\s, which allows us to
        use more operations in addition to those on an :term:`algebra of sets`.  See
        :ref:`algebraofclans` for a more detailed explanation.

    algebra of couplets
        Given a collection of couplets we define an algebra on it by including the operations of
        :term:`composition` and :term:`transposition`.  See :ref:`algebraofcouplets` for a more
        detailed definition.

    algebra of multiclans
        An algebra defined on :term:`multiset`\s of :term:`relation`\s.  This algebra is
        similar to the :term:`algebra of clans`, but takes into account multiplicities of
        relations.  See :ref:`algebraofmultclan` for more information.

    algebra of multisets
        An algebra on the set of all :term:`multiset`\s of |set M| with the operations of
        :term:`multiset union`, :term:`multiset intersection`, :term:`multiset addition`,
        :term:`multiset difference`, and :term:`submultiset`.  See
        :ref:`algebraofmultisets` for more detailed information.

    algebra of relations
        The algebra of relations is an algebra on a set of couplets under the operations of
        :term:`composition` and :term:`transposition`.  See :ref:`algebraofrelns` for a more
        detailed definition.

    algebra of sets
        Also called **set algebra**, is the algebra formed by taking the :term:`power set` of
        a set and applying the operations of :term:`union` and :term:`intersection`.
        See :ref:`algebraofsets` for a more detailed definition.

    atom
        An atom is a datum that is not a :term:`set` or a :term:`couplet`. The set of all atoms is
        |set A|.

    bijective
        A :term:`relation` is **bijective** if it is both :term:`left-functional` and
        :term:`right-functional`.

    binary intersection
        A **binary intersection** is an :term:`intersection` of two :term:`set`\s. See
        :term:`intersection` for a complete definition.

    binary extension
        A **binary extension** is an :term:`extension` of a :term:`binary operation` from a given
        :term:`algebra` to an extension of the algebra that consists of :term:`set`\s of
        the elements of the original algebra:

        .. math:: binaryExtn(op, S1, S2) := \{op(s1, s2)\ :\ s1 \in S1 \text{ and } s2 \in S2
                \text{ where } op(s1, s2) \text{ is defined}\}

    binary multi-extension
        A **binary multi-extension** is an :term:`extension` of a :term:`binary operation` from a
        given :term:`algebra` to an extension of the algebra that consists of :term:`multiset`\s of
        the elements of the original algebra:

        .. math:: binMultiExtn(op, S1, S2) :=
                \{op(s1, s2){:}(\dot{S1}(s1) \cdot \dot{S2}(s2))\
                :\ s1 \in S1 \text{ and } s2 \in S2
                \text{ where } op(s1, s2) \text{ is defined}\}

    binary operation
        A **binary operation** is an operation with two arguments, typically with a result that
        belongs to the same :term:`ground set` as the arguments (when the operation is a member of
        an :term:`algebra`).

    binary relation
        We represent a `binary relation`_ as a :term:`set` where every member is a :term:`couplet`.
        We also call this simply a :term:`relation`.

    binary union
        A **binary union** is a :term:`union` of two sets.  See :term:`union` for more information.

    Cartesian product
        The **Cartesian product** of two :term:`set`\s :math:`X \times Y` is the set of all
        :term:`couplet`\s where the first member of the couplet is a member of :math:`X` and the
        second member of the couplet is a member of :math:`Y`.

    clan
        A **clan** is a :term:`set` of :term:`relation`\s.

    clan diagonal
        A **clan diagonal** is a :term:`clan` with a single :term:`relation` that is a
        :term:`diagonal`.

    complement
        The **complement** of a given set is the collection of elements not in the given set.  This
        definition depends on a choice of a larger set in which context every other set is a subset
        of.  In particular, given an :term:`algebra of sets` whose ground set is the
        :term:`power set` :math:`P(U)` and :math:`X\in P(U)`, then the complement of :math:`X` is:

        .. math::
                X' := \{x \in U: x \not\in X\} = U - X

    composition
        The **composition** of the :term:`couplet`\s :math:`a{\mapsto}b` and :math:`c{\mapsto}d` is
        defined as:

        .. math:: c{\mapsto}d \circ a{\mapsto}b :=
                \begin{cases}
                    a{\mapsto}d & \text{if } b = c \\
                    \text{undefined} & \text{if } b \ne c
                \end{cases}

        The operation may be extended to extended :term:`algebra`\s using the
        :term:`binary extension` and -- if there is no danger of ambiguities -- is then also called
        simply 'composition'.

        Specific extensions:

        -   :term:`Algebra of relations`:
            :math:`R_2 \circ R_1 := \{c_2 \circ c_1\ :\ c_1 \in R_1,\ c_2 \in R_2\}`

            (:math:`R_1` and :math:`R_2` are :term:`relation`\s; :math:`c_1` and :math:`c_2` are
            :term:`couplet`\s.)

        -   :term:`Algebra of clans`:
            :math:`C_2 \circ C_1 := \{R_2 \circ R_1\ :\ R_1 \in C_1,\ R_2 \in C_2\}`

            (:math:`C_1` and :math:`C_2` are :term:`clan`\s; :math:`R_1` and :math:`R_2` are
            :term:`relation`\s.)

        -   :term:`Algebra of multiclans`:
            :math:`\dot{C}_2 \circ \dot{C}_1 := \{(R_2 \circ R_1){:}(\dot{C}_2(R_2) \cdot \dot{C}_1(R_1))\ :\ R_1 \in \dot{C}_1,\ R_2 \in \dot{C}_2\}`

            (:math:`\dot{C}_1` and :math:`\dot{C}_2` are :term:`multiclan`\s; :math:`R_1` and
            :math:`R_2` are :term:`relation`\s.)

    couplet
        A **couplet** is an ordered pair, following the `Kuratowski definition of an ordered pair`_
        defined as :math:`\{\{l\}, \{l, r\}\}`. It is the mathematical object used to represent
        a datum or data point.  We denote it by :math:`l{\mapsto}r`, with :math:`l` called the
        :term:`left component`, and :math:`r` the :term:`right component`.

    cross-functional union
        A short name for :term:`cross-left-functional union` in cases where no ambiguities are
        expected.

    cross-intersection
        The **cross-intersection** is an :term:`extension` of :term:`intersection` (or
        :term:`multiset intersection`). Depending on the specific form of extension, it may be a
        :term:`binary extension` (when extending to an :term:`algebra of sets`) or a
        :term:`binary multi-extension` (when extending to an :term:`algebra of multisets`).

        In the specific context, **cross-intersection** is the :term:`binary extension` of
        :term:`intersection` from an :term:`algebra of sets` to an algebra of sets of sets (for
        example, from the :term:`algebra of relations` to the :term:`algebra of clans`). The
        cross-intersection of the sets (of sets) :math:`\mathbb{S}` and :math:`\mathbb{T}` is
        defined as:

        .. math:: \mathbb{S} \blacktriangle \mathbb{T}
            = \{X \cap Y\ : X \in \mathbb{S} \text{ and } Y \in \mathbb{T}\}

        For the version of cross-intersection on the :term:`algebra of multiclans` and on an
        :term:`algebra of multisets` in general see :term:`multi-cross-intersection`.

    cross-left-functional union
        The **cross-left-functional union**, (or :term:`cross-functional union`), of two
        :term:`clan`\s :math:`\mathbb{C}` and :math:`\mathbb{D}` is a
        :term:`binary extension` of the :term:`left-functional union` from the
        :term:`algebra of relations` to the :term:`algebra of clans`:

        .. math:: \mathbb{C} \underset{f}{\blacktriangledown} \mathbb{D}
            = \{R \underset{f}{\cup} Q\ : R \in \mathbb{C} \text{ and } Q \in \mathbb{D}\}

    cross-right-functional union
        The **cross-right-functional union** of two :term:`clan`\s :math:`\mathbb{C}` and
        :math:`\mathbb{D}` is a :term:`binary extension` of the :term:`right-functional
        union` from the :term:`algebra of relations` to the :term:`algebra of clans`:

        .. math:: \mathbb{C} \underset{rf}{\blacktriangledown} \mathbb{D}
            = \{R \underset{rf}{\cup} Q\ : R \in \mathbb{C} \text{ and } Q \in \mathbb{D}\}

    cross-substriction
        The **cross-substriction** is a :term:`binary extension` of :term:`substriction` from an
        :term:`algebra of sets` to an algebra of sets of sets (for example, from the
        :term:`algebra of relations` to the :term:`algebra of clans`). The cross-substriction of
        the sets (of sets) :math:`\mathbb{S}` and :math:`\mathbb{T}` is defined as:

        .. math:: \mathbb{S} \blacktriangleleft \mathbb{T}
            = \{X \vartriangleleft Y\ : X \in \mathbb{S} \text{ and } Y \in \mathbb{T}\}
            = \{X : X \in \mathbb{S} \text{ and } X \subset Y \text{ for some } Y \in \mathbb{T} \}

        We also have a :term:`binary multi-extension` of cross-substriction called the
        :term:`multi-cross-substriction`.

    cross-superstriction
        The **cross-superstriction** is a :term:`binary extension` of :term:`superstriction` from an
        :term:`algebra of sets` to an algebra of sets of sets (for example, from the
        :term:`algebra of relations` to the :term:`algebra of clans`). The cross-superstriction of
        the sets (of sets) :math:`\mathbb{S}` and :math:`\mathbb{T}` is defined as:

        .. math:: \mathbb{S} \blacktriangleright \mathbb{T}
            = \{X \vartriangleright Y\ : X \in \mathbb{S} \text{ and } Y \in \mathbb{T}\}
            = \{X : X \in \mathbb{S} \text{ and } X \supset Y \text{ for some } Y \in \mathbb{T} \}

        We also have a :term:`binary multi-extension` of cross-superstriction called the
        :term:`multi-cross-superstriction`.

    cross-union
        The **cross-union** is a :term:`binary extension` of :term:`union` from an :term:`algebra of
        sets` to an algebra of sets of sets (for example, from the :term:`algebra of relations` to
        the :term:`algebra of clans`). The cross-union of the sets (of sets) :math:`\mathbb{S}` and
        :math:`\mathbb{T}` is defined as:

        .. math:: \mathbb{S} \blacktriangledown \mathbb{T}
            = \{X \cup Y\ : X \in \mathbb{S} \text{ and } Y \in \mathbb{T}\}

        We also have a :term:`binary multi-extension` of cross-union called the
        :term:`multi-cross-union`.

    diagonal
        The **diagonal** is an :term:`equivalence relation`. The diagonal of a :term:`set` :math:`S`
        is defined as:

        .. math:: D_S = \{x{\mapsto}x \in S \times S\ : x \in S\}

    difference
        The **difference** of two :term:`set`\s :math:`S` and :math:`T` is the set of elements in
        :math:`S` but not in :math:`T` (see also `Wikipedia: Relative complement`_). The definition
        is:

        .. math:: S \setminus T = \{x: x \in S\ \&\ x \notin T\}

    equivalence relation
        A :term:`relation` is said to be an **equivalence relation** if it is
        :term:`reflexive`, :term:`symmetric` and :term:`transitive`.

    extension
        An **extension** of a given set or algebra, is an extension of the set or algebra either by
        expanding the ground set, the set of operations on the set or both.  For a more detailed
        definition, see :ref:`extension`.

    finite intersection
        A **finite intersection** is the intersection of a finite collection of :term:`set`\s. See
        :term:`intersection` for a complete definition.

    finite union
        A **finite union** is the :term:`union` of a finite collection of :term:`set`\s.  See
        :term:`union` for a more detailed explanation.

    function
        A **function** is a :term:`left-functional` :term:`relation`.

    functional
        A short name for :term:`left-functional` in cases where no ambiguities are expected.

    functional union
        A short name for :term:`left-functional union` in cases where no ambiguities are
        expected.

    ground set
        The :term:`set` that contains all the elements of an :term:`algebra`.

    identity element
        The element of the :term:`ground set` of an :term:`algebra` that, when used as one of the
        arguments of a :term:`binary operation` produces the other argument of the operation as
        result of the operation.

    intersection
        An operation on sets that creates a set by collecting the elements in common to
        two or more individual sets into a new set.  In mathematical terms, if
        :math:`\mathbb{S}` is a collection of sets, then the **intersection** of all of the sets
        in :math:`\mathbb{S}` is denoted:

        .. math::  \bigcap \mathbb{S} = \bigcap_{T\in\mathbb{S}}T,

        and is the set :math:`\{x\ : \forall T \in \mathbb{S},\ x \in T\}`.  If
        :math:`\mathbb{S}` consists of only two sets, the intersection is called a **binary
        intersection**.  If :math:`\mathbb{S}` consists of a finite collection of sets, the
        intersection is called a **finite intersection**.  See also `Wikipedia: Intersection`_.

    left
        A short name for :term:`left component` where no ambiguity is expected.

    left component
        Given a :term:`couplet` represented by :math:`l{\mapsto}r`, the component :math:`l` is
        called the **left component**.

    left set
        The **left set** of a :term:`relation` :math:`R` is the :term:`set` of all
        :term:`left component`\s of its members:

        .. math:: left(R) = \{ l\ : l{\mapsto}r \in R \}

        The left set of a :term:`clan` :math:`\mathbb{C}` is the :term:`union` of all
        left sets of its member relations:

        .. math:: left(\mathbb{C}) = \underset{R\ \in\ \mathbb{C}}{\bigcup} left(R)

    left-functional
        A :term:`relation` :math:`R` is said to be **left-functional**, or simply
        **functional**, if:

        .. math:: x{\mapsto}y \in R\ \& \ x{\mapsto}z \in R \implies y = z

        A :term:`clan` :math:`\mathbb{C}` is said to be (left-)functional if all its relations are
        functional:

        .. math:: \forall R \in \mathbb{C}: R \text{ is left-functional}

    left-functional union
        The **left-functional union** (or :term:`functional union`) of two :term:`function`\s
        :math:`R` and :math:`Q` is the :term:`union` of the two relations if the result is
        :term:`left-functional`, otherwise the result is not defined:

        .. math:: R \underset{f}{\cup} Q =
            \begin{cases}
                R \cup Q & \text{if }R \cup Q \text{ is left-functional} \\
                \text{undefined} & \text{if it is not left-functional}
            \end{cases}

    left-regular
        A :term:`clan` :math:`\mathbb{C}` is said to be **left-regular** (or short :term:`regular`)
        if it is :term:`left-functional` and the :term:`left set`\s of all its :term:`relation`\s
        are the same:

        .. math:: \begin{align*}
                \forall R \in \mathbb{C}&: R \text{ is left-functional} \text{ and } \\
                \forall R, Q \in \mathbb{C}&: left(R) = left(Q)
            \end{align*}

    lhs-cross-functional union
        A short name for :term:`lhs-cross-left-functional union` in cases where no ambiguities
        are expected.

    lhs-cross-left-functional union
        Given two :term:`clan`\s the **lhs-cross-left-functional union** (or
        :term:`lhs-cross-functional union`) takes the :term:`cross-left-functional union`, then
        any relations in the clan on the left side of the operation that resulted in the empty set
        are collected by taking their :term:`union` and combined with the result of the
        cross-left-functional union.   Mathematically, if :math:`\mathbb{C}` and :math:`\mathbb{D}`
        are the two clans in question, then their lhs-cross-left-functional union is:

        .. math:: \mathbb{C} \overrightarrow{\underset{f}\blacktriangledown} \mathbb{D} =
            \mathbb{C} \underset{f}{\blacktriangledown} \mathbb{D}
            \bigcup\{T : T\in\mathbb{C}\ \& \
                T \underset{f}{\blacktriangledown} \mathbb{D} = \varnothing \}

    multiclan
        A **multiclan** is a :term:`multiset` of :term:`relation`\s.

    multi-cross-intersection
        Let :math:`\dot{\mathbb{S}}` and :math:`\dot{\mathbb{T}}` be :term:`multiset`\s of
        :term:`set`\s with :math:`X \in \dot{\mathbb{S}}` and :math:`Y \in \dot{\mathbb{T}}`, then
        their **multi-cross-intersection** is defined in the same way as the
        :term:`cross-intersection` with the multiplicities satisfying:

        .. math:: \dot{\mathbb{S}} \blacktriangle \dot{\mathbb{T}}(X \cap Y) =
            \dot{\mathbb{S}}(X) \cdot \dot{\mathbb{T}}(Y)

        Where there is no ambiguity we will refer to the multi-cross-intersection simply as the
        cross-intersection.

    multi-cross-substriction
        Let :math:`\dot{\mathbb{S}}` and :math:`\dot{\mathbb{T}}` be :term:`multiset`\s of
        :term:`set`\s with :math:`X \in \dot{\mathbb{S}}` and :math:`Y \in \dot{\mathbb{T}}`, then
        their **multi-cross-substriction** is defined in the same way as the
        :term:`cross-substriction` with the multiplicities satisfying:

        .. math:: \dot{\mathbb{S}} \blacktriangleleft \dot{\mathbb{T}}(X \vartriangleleft Y) =
            \dot{\mathbb{S}}(X)

        Where there is no ambiguity we will refer to the multi-cross-substriction simply as the
        cross-substriction.

    multi-cross-superstriction
        Let :math:`\dot{\mathbb{S}}` and :math:`\dot{\mathbb{T}}` be :term:`multiset`\s of
        :term:`set`\s with :math:`X \in \dot{\mathbb{S}}` and :math:`Y \in \dot{\mathbb{T}}`, then
        their **multi-cross-superstriction** is defined in the same way as the
        :term:`cross-superstriction` with the multiplicities satisfying:

        .. math:: \dot{\mathbb{S}} \blacktriangleright \dot{\mathbb{T}}(X \vartriangleright Y) =
            \dot{\mathbb{S}}(X)

        Where there is no ambiguity we will refer to the multi-cross-superstriction simply as the
        cross-superstriction.

    multi-cross-union
        Let :math:`\dot{\mathbb{S}}` and :math:`\dot{\mathbb{T}}` be :term:`multiset`\s of
        :term:`set`\s with :math:`X \in \dot{\mathbb{S}}` and :math:`Y \in \dot{\mathbb{T}}`, then
        their **multi-cross-union** is defined in the same way as the :term:`cross-union` with the
        multiplicities satisfying:

        .. math:: \dot{\mathbb{S}} \blacktriangledown \dot{\mathbb{T}}(X \cup Y) =
            \dot{\mathbb{S}}(X) \cdot \dot{\mathbb{T}}(Y)

        Where there is no ambiguity we will refer to the multi-cross-union simply as the
        cross-union.

    multiplicity
        Given an element of a :term:`multiset`, the **multiplicity** of that element is the number
        of times the element appears in the multiset.  See :ref:`multiset` for more information.

    multiset
        A **multiset**, also sometimes called a **bag**, is a generalization of the idea of
        a set where multiple instances of the same element are allowed.  See :ref:`multiset`
        for more information.

    multiset addition
        The **multiset addition** of two :term:`multiset`\s :math:`\dot{S}` and :math:`\dot{T}`
        is defined as follows:

        .. math:: \big(\dot{S} + \dot{T}\big)(x) = \dot{S}(x) + \dot{T}(x)

        for any :math:`x`, where here we take :math:`\dot{S}(x)=0` for :math:`x \not\in \dot{S}`,
        and :math:`\dot{T}(x)=0` for :math:`x \not\in \dot{T}`.

    multiset difference
        The **multiset difference** of two :term:`multiset`\s :math:`\dot{S}` and :math:`\dot{T}`
        is defined as follows:

        .. math:: \big(\dot{S} \setminus \dot{T}\big)(x) =
            \begin{cases}
                \dot{S}(x) - \dot{T}(x) & \text{if } \dot{S}(x) - \dot{T}(x)>0 \\
                \text{undefined} & \text{if } \dot{S}(x) - \dot{T}(x) \leq 0
            \end{cases}

        for any :math:`x`, where here we take :math:`\dot{S}(x)=0` for :math:`x \not\in \dot{S}`,
        and :math:`\dot{T}(x)=0` for :math:`x \not\in \dot{T}`.

    multiset intersection
        We define the **multiset intersection** of two :term:`multiset`\s :math:`\dot{S}` and
        :math:`\dot{T}` to be:

        .. math:: \big(\dot{S} \cap \dot{T}\big)(x) = min \big(\dot{S}(x), \dot{T}(x)\big)

        for any :math:`x`, where here we take :math:`\dot{S}(x)=0` for :math:`x \not\in \dot{S}`,
        and :math:`\dot{T}(x)=0` for :math:`x \not\in \dot{T}`.

    multiset union
        We define the **multiset union** of two :term:`multiset`\s :math:`\dot{S}` and
        :math:`\dot{T}` to be:

        .. math:: \big(\dot{S} \cup \dot{T}\big)(x) = max \big(\dot{S}(x), \dot{T}(x)\big)

        for any :math:`x`, where here we take :math:`\dot{S}(x)=0` for :math:`x \not\in \dot{S}`,
        and :math:`\dot{T}(x)=0` for :math:`x \not\in \dot{T}`.

    partition
        A **partition** of a :term:`set` is the splitting of a set into a collection of smaller
        :term:`subset`\s. Mathematically, given a set :math:`S`, we create a set of subsets of
        :math:`S` such that the :term:`union` of those sets is :math:`S`, and whose pairwise
        :term:`intersection` is the empty set (another term for this is that any two sets are
        **disjoint**).

    power set
        The **power set** of any set :math:`S`, written :math:`P(S)`, is the set of all subsets of
        :math:`S`, including the empty set and :math:`S` itself. We also use the expressions 'second
        power set', 'third power set' and so on to mean successive application of the power set
        operation for the indicated number of times: 'power set of the power set of the ... of
        :math:`S`. (Adapted from `Wikipedia: Power set`_.)

    projection
        Given a :term:`clan`, call it :math:`C`, and a collection of elements, call it
        :math:`lefts`, the **projection** of :math:`C` onto :math:`lefts` is a new clan
        where all of the :term:`left component`\s of all of the :term:`couplet`\s of the
        :term:`relation`\s of :math:`C` are in the set :math:`lefts`.

        To obtain the projection of :math:`C` onto :math:`lefts` mathematically we can do this as
        follows:

        .. math:: D_{lefts} := \{l{\mapsto}l\ : l\in lefts \} \\
            project(C,lefts) = \{ R \circ D_{lefts}\ : R\in C\}

    reflexive
        A :term:`relation` :math:`R` is said to be **reflexive** if:

        .. math:: \forall x \in left(R) \cup right(R): x{\mapsto}x \in R

        A :term:`couplet` can also be **reflexive** if it is of the form :math:`x{\mapsto}x`.

        See also :term:`left set`, :term:`right set`.

    regular
        A short name for :term:`left-regular` in cases where no ambiguities are expected.

    relation
        A **relation** is a :term:`set` of :term:`couplet`\s.  See also :term:`binary relation`.

    right
        A short name for :term:`right component` where no ambiguity is expected.

    right component
        Given a :term:`couplet` represented by :math:`l{\mapsto}r` the component
        :math:`r` is the **right component**.

    right-functional
        A :term:`relation` :math:`R` is said to be **right-functional** if:

        .. math:: y{\mapsto}x \in R\ \&\ z{\mapsto}x \in R \implies y = z

    right-functional union
        The **right-functional union** of two :term:`right-functional` :term:`relation`\s
        :math:`R` and :math:`Q` is the :term:`union` of the two relations if the result is
        :term:`right-functional`, otherwise the result is not defined:

        .. math:: R \underset{rf}{\cup} Q =
                \begin{cases}
                    R \cup Q & \text{if }R \cup Q \text{ is right-functional} \\
                    \text{undefined} & \text{if it is not right-functional}
                \end{cases}

    right-regular
        A :term:`clan` :math:`\mathbb{C}` is said to be **right-regular** if the
        :term:`right set`\s of all its :term:`relation`\s are the same:

        .. math:: \forall R, Q \in \mathbb{C}: right(R) = right(Q)

    right multiset
        The **right multiset** of a :term:`multiclan` :math:`\mathbb{C}` is the
        :term:`multiset addition` of all :term:`right set`\s of its member relations:

        .. math:: right(\mathbb{C}) = \underset{R\ \in\ \mathbb{C}}{+} right(R)

    right set
        The **right set** of a :term:`relation` :math:`R` is the :term:`set` of all
        :term:`right component`\s of its members:

        .. math:: right(R) = \{ r\ : l{\mapsto}r \in R \}

        The right set of a :term:`clan` :math:`\mathbb{C}` is the :term:`union` of all
        right sets of its member relations:

        .. math:: right(\mathbb{C}) = \underset{R\ \in\ \mathbb{C}}{\bigcup} right(R)

    set
        A **set** is a collection of distinct objects.  Each object of a set is called an
        **element** of the set.  In particular, if :math:`X` is a set, then we denote the fact
        that :math:`x` is an element of :math:`X` by writing :math:`x\in X`.  We will apply the
        axioms of :term:`Zermelo-Fraenkel set theory with choice (ZFC)` to the sets.  See also
        :ref:`sets` for more information about set notation

    set A
        The :term:`set` :math:`A` is the set of all :term:`atom`\s. It is a subset of the
        |set M|.

    set M
        The :term:`set` :math:`M` is the set of all elements that can be represented in a given
        system, including :term:`atom`\s, :term:`couplet`\s and :term:`set`\s. (A consequence of
        this is that the :term:`power set` of :math:`M` :math:`P(M)` cannot be represented in a
        given system, and therefore is not an element of :math:`M`.)

    set N
        The :term:`set` :math:`N` is the set of all positive integers.

    submultiset
        The **submultiset** relation is a :term:`binary relation` of :term:`multiset`\s. A multiset
        :math:`\dot{S}` is a submultiset of a multiset :math:`\dot{T}` if the following holds:

        .. math:: \dot{S} \subset \dot{T} \iff \forall x \in \dot{S}, \: \dot{S}(x) \leq \dot{T}(x).

    subset
        The **subset** relation is a :term:`binary relation` of :term:`set`\s. A set :math:`S` is
        a subset of a set :math:`T` if every element of :math:`S` is also an element of :math:`T`:

        .. math:: S \subset T \implies \forall x\ [\ x \in S\ \implies\ x \in T\ ]

    substriction
        **Substriction** is a partial binary operation on :term:`set`\s and :term:`multiset`\s. The
        substriction of two sets or multisets :math:`S` and :math:`T` is defined as:

        .. math:: S \vartriangleleft T = S\ \ \text{if}\ \ S \subset T

        (When extended to an algebra of sets of sets (for example, the :term:`algebra of clans`),
        we obtain the :term:`cross-substriction`, which is also sometimes called
        'substriction'.)

    supermultiset
        The **supermultiset** relation is a :term:`binary relation` of :term:`multiset`\s. A
        multiset :math:`\dot{S}` is a supermultiset of a multiset :math:`\dot{T}` if the following
        holds:

        .. math:: \dot{S} \supset \dot{T} \iff \forall x \in \dot{T},  \: \dot{S}(x) \geq \dot{T}(x).

    superset
        The **superset** relation is a binary relation of :term:`set`\s. A set :math:`S` is a
        superset of a set :math:`T` if every element of :math:`T` is also an element of :math:`S`:

        .. math:: S \supset T \implies \forall x\ [\ x \in T\ \implies\ x \in S\ ]

    superstriction
        **Superstriction** is a partial binary operation on :term:`set`\s and :term:`multiset`\s.
        The superstriction of two sets or multisets :math:`S` and :math:`T` is defined as:

        .. math:: S \vartriangleright T := S\ \ \text{if}\ \ S \supset T

        (When extended to an algebra of sets of sets (for example, the :term:`algebra of clans`),
        we obtain the :term:`cross-superstriction`, which is also sometimes called
        'superstriction'.)

    symmetric
        A :term:`relation` :math:`R` is said to be **symmetric** if:

        .. math:: \forall x, y \in left(R) \cup right(R): x{\mapsto}y \in R \implies y{\mapsto}x \in R

        See also :term:`left set`, :term:`right set`.

    symmetric difference
        The **symmetric difference** of two :term:`set`\s :math:`S` and :math:`T` is the set of
        elements that are only in one of the sets. The definition is:

        .. math:: S \vartriangle T = (S \cup T) \setminus (S \cap T)

    transitive
        A :term:`relation` :math:`R` is said to be **transitive** if:

        .. math:: \forall x, y, z \in left(R) \cup right(R):
            (x{\mapsto}y \in R \ \& \ y{\mapsto}z \in R) \implies x{\mapsto}z \in R

        See also :term:`left set`, :term:`right set`.

    transposition
        **Transposition** is a unary operation on :term:`couplet`\s. The transposition of a couplet
        :math:`a{\mapsto}b` is defined as:

        .. math:: \overleftrightarrow{a{\mapsto}b} = b{\mapsto}a

        The operation may be extended to extended :term:`algebra`\s (like the :term:`algebra
        of relations`) using the :term:`unary extension` and -- if there is no danger of ambiguities
        -- is then also called simply 'transposition'.

        In :term:`multiset`\s and :term:`multiclan`\s the operation is the same and the
        multiplicities do not change.

    unary extension
        The unary :term:`extension` is the operation that extends a :term:`unary operation` from
        its :term:`algebra` to an extended algebra (which is an :term:`algebra of sets`):

        .. math:: unaryExtn(op, S) := \{op(s)\ :\ s \in S
                \text{ where } op(s) \text{ is defined}\}

    unary multi-extension
        The unary multi-:term:`extension` is the operation that extends a :term:`unary operation`
        from its :term:`algebra` to an extended algebra (which is an :term:`algebra of multisets`).
        For this extension, the multiplicities do not change:

        .. math:: unaryExtn(op, \dot{S}) := \{op(s){:}\dot{S}(s)\ :\ s \in S
                \text{ where } op(s) \text{ is defined}\}

    unary operation
        An operation with only one argument, typically with a result that belongs to the same
        ground set as the argument (when the operation is a member of an :term:`algebra`).

    union
        An operation on sets that creates a set by collecting the elements of two or more
        individual sets into a new set.  In mathematical terms, if :math:`\mathbb{S}` is a
        collection of sets, then the **union** of all of the sets in :math:`\mathbb{S}` is
        denoted:

        .. math::  \bigcup \mathbb{S} = \bigcup_{T\in\mathbb{S}}T,

        and is the set :math:`\{x\ : \exists T \in \mathbb{S},\ x \in T\}`.  If
        :math:`\mathbb{S}` consists of only two sets, the union is called a **binary union**.
        If :math:`\mathbb{S}` consists of a finite collection of sets, the union is called a
        **finite union**.  See also `Wikipedia: Union`_.

    Zermelo-Fraenkel set theory with choice (ZFC)
        A system of axioms on sets that is the standard form of set theory and the foundation
        of much of modern mathematics. See also
        `Wikipedia: Zermelo-Fraenkel set theory with choice (ZFC)`_.


.. |set A| replace:: :term:`set A` (:math:`A`)
.. |set M| replace:: :term:`set M` (:math:`M`)
.. |set N| replace:: :term:`set N` (:math:`N`)

.. _binary relation:
    http://en.wikipedia.org/wiki/Binary_relation
.. _Kuratowski definition of an ordered pair:
    http://en.wikipedia.org/wiki/Ordered_pair#Kuratowski_definition
.. _Wikipedia\: Intersection:
    http://en.wikipedia.org/wiki/Intersection_%28set_theory%29
.. _Wikipedia\: Power set:
    http://en.wikipedia.org/wiki/Power_set
.. _Wikipedia\: Relative complement:
    http://en.wikipedia.org/wiki/Complement_%28set_theory%29#Relative_complement
.. _Wikipedia\: Union:
    http://en.wikipedia.org/wiki/Union_%28set_theory%29
.. _Wikipedia\: Zermelo-Fraenkel set theory with choice (ZFC):
    http://en.wikipedia.org/wiki/Zermelo%E2%80%93Fraenkel_set_theory
