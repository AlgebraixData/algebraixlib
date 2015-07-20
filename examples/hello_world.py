"""A simple example with a 'Hello World' theme."""

# $Id: hello_world.py 22614 2015-07-15 18:14:53Z gfiedler $
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

# Data in an algebraixlib program is represented as MathObjects. MathObjects come in four types:
# Atoms, Couplets, Sets, and Multisets. Multisets will not be covered in this tutorial. Values that
# aren't themselves modeled by Data Algebra, such as strings and numbers, are represented by Atoms.
from algebraixlib.mathobjects import Atom
peanut_butter = Atom("peanut butter")
jelly = Atom("jelly")

# Every MathObject can be pretty-printed to the console using print().
print(peanut_butter)

# The non-MathObject value of the Atom can be accessed by its value property.
try:
    one = Atom(1)
    two = Atom(2)
    print("1 + 2 = {}".format(one.value + two.value))
    print("Will throw", one + two)
except TypeError as e:
    print("Error:", e)

# Couplets relate two pieces of information together. Those pieces of information must be
# represented as MathObjects; our two Atoms from earlier qualify.
from algebraixlib.mathobjects import Couplet
together = Couplet(peanut_butter, jelly)
print(together)

# MathObject initializers will coerce their arguments to be Atoms if non-MathObjects are passed.
coerced = Couplet("this", "that")
print(repr(coerced))

# The components of a Couplet are known as its left and right (abbreviated as 'right').
# Sometimes initializng a Couplet with named arguments can add clarity.
up_down = Couplet(left="up", right="down")
print("left is {}, right is {}".format(up_down.left, up_down.right))

# A Couplet's components can be swapped by evaluating the unary operation transpose.
import algebraixlib.algebras.couplets as couplets
one_two = Couplet(1, 2)
transpose_result = couplets.transpose(one_two)
print("A couplet {} and its transpose {}".format(one_two, transpose_result))

# When an expression is undefined in algebraixlib, it returns a special value, the singleton Undef.
# Undef cannot be used as a value in a MathObject and cannot be compared to any value (even itself).
# Use the is and is not operators to test if a value is undefined.
from algebraixlib.undef import Undef
print(Undef() is Undef())
print(Undef() is not Undef())
print(None is not Undef())

# The binary operation composition(a^b, c^d) evaluates to a^d when b == c, otherwise it is
# undefined.
a_to_b = Couplet('a', 'b')  # b^a
b_to_c = Couplet('b', 'c')  # c^b
print(couplets.compose(b_to_c, a_to_b))  # c^a
print(couplets.compose(a_to_b, b_to_c))  # undef, composition is not commutative

# Sets are used to create unordered collections of unique MathObjects. Non-MathObjects will be
# coerced into Atoms.
from algebraixlib.mathobjects import Set
many = Set(Atom("hello"), "world", Couplet("hola", "mundo"), "duplicate", "duplicate")
print(repr(many))

# Sets support for...in syntax for iteration and in and not in syntax for membership tests. Because
# sets are unordered, they do not support random access (no bracket operator).
nums = Set(1, 2, 3, 4, 5)
for elem in nums:
    print(elem, " ")
print(1 in nums)
print(7 in nums)

# Sets can be unioned, intersected, set-minused. Relations such as is_subset and is_superset are
# defined.
a = Set(1, 2)
b = Set(2, 3)

import algebraixlib.algebras.sets as sets

print("union(a, b) = {}".format(sets.union(a, b)))
print("intersect(a, b) = {}".format(sets.intersect(a, b)))
print("minus(a, b) = {}".format(sets.minus(a, b)))
print("is_subset(a, b) = {}".format(sets.is_subset_of(a, b)))
print("is_superset(a, {{1}}) = {}".format(sets.is_superset_of(a, Set(1))))

# We can use a Couplet to model a single truth, such as 'blue'^'sky' or 'jeff'^'name'. By collecting
# multiple Couplets together in a set, we form a mathematical model of a data record. This data
# structure, called a binary relation (abbreviated from hereon as simply 'relation'), is the
# fundamental data type in a Data Algebra program.
record_relation = Set(Couplet('id', 123), Couplet('name', 'jeff'), Couplet('loves', 'math'),
                      Couplet('loves', 'code'))
print(record_relation)

# Some relations, specify a function from left to right. This is the case when every left
# value maps to exactly one right value. Such a relation is called "left functional".
# Likewise, a relation can be said to be "right functional" when every right value maps
# to exactly one left value.
import algebraixlib.algebras.relations as relations

functional_relation = Set(Couplet('subject', 123), Couplet('name', 'james'), Couplet('level', 10))
print(relations.get_right(functional_relation, 'subject'))
print(relations.get_left(functional_relation, 123))
print(relations.get_right(record_relation,
                                'loves'))  # See non-functional record_relation above.

# Function evaluation syntax makes this more concise.
print("functional_relation('subject') =", functional_relation('subject'))
print("functional_relation(123) =", functional_relation(123))

# The power set of a set S, which we'll denote as P(S), is the set of all subsets of S. Note how in
# the example below, the elements of set_s are numbers, and the elements of powerset_s are sets of
# numbers.
set_s = Set(1, 2, 3)
powerset_s = sets.power_set(set_s)
print("S := ", set_s)
print("P(S) = ", powerset_s)

# Consider that if C is the set of all Couplets, then the set of all relations R can be defined as
# P(C), that is, every relation is a subset of the set of all Couplets. It turns out that we can
# exploit this relationship by "extending" operations on Couplets up to relations to make them useful
# there. To extend a unary operation such as couplets.transpose, we apply it to every Couplet in a
# relation, which results in another relation.
import algebraixlib.extension as extension

first_relation = Set(Couplet('a', 1), Couplet('b', 2), Couplet('c', 3))
transposed_relation = extension.unary_extend(first_relation, couplets.transpose)
print("transposed_relation:", transposed_relation)

# Similarly, a binary operation like couplets.composition can be extended by applying to every element
# of the cross product of two relations. Notice that couplets.composition is a partial binary
# operation (given two legitimate Couplets, it may be undefined). When couplets.compose(a, b) is
# not defined, it simply isn't included in the membership of the resulting relation. By extending,
# we have turned composition into a full binary operation in the power set algebra.
second_relation = Set(Couplet('one', 'a'), Couplet('won', 'a'), Couplet('four', 'd'))
composed_relation = extension.binary_extend(first_relation, second_relation, couplets.compose)
empty_relation = extension.binary_extend(second_relation, first_relation,
                                 couplets.compose)  # empty relation; still not commutative
print("composed_relation:", composed_relation)
print("empty_relation:", empty_relation)

# These extended operations are defined as functions in the relations module.
transpose_is_same = transposed_relation == relations.transpose(first_relation)
compose_is_same = composed_relation == relations.compose(first_relation, second_relation)
print("transpose_is_same:", transpose_is_same)
print("compose_is_same:", compose_is_same)

# The following docstring specifies a CSV table of words in various languages, with their meaning
# normalized to English.
vocab_csv = """word,language,meaning
hello,English,salutation
what's up,English,salutation
hola,Spanish,salutation
world,English,earth
mundo,Spanish,earth
gallo,Spanish,rooster
Duniy?,Hindi,earth
Kon'nichiwa,Japanese,salutation
hallo,German,salutation
nuqneH,Klingon,salutation
sekai,Japanese,earth
schmetterling,German,butterfly
mariposa,Spanish,butterfly
"""

# Tables can be modeled as sets of binary relations, which we call clans.
from io import StringIO
from algebraixlib.io.csv import import_csv

file = StringIO(vocab_csv)
vocab_clan = import_csv(file)
print("vocab_clan:", vocab_clan)

# Superstriction(A, B) is a partial binary operation on sets. It is defined as A if A is a superset
# of B, otherwise it is undefined.
hello_relation = Set(Couplet('word', 'hello'), Couplet('language', 'English'),
                     Couplet('meaning', 'salutation'))
super_pos = sets.superstrict(hello_relation, Set(Couplet('language', 'English')))
super_neg = sets.superstrict(hello_relation, Set(Couplet('language', 'Mandarin')))
print(super_pos)
print(super_neg)

# By extending superstriction to clans, which are sets of sets (of Couplets), we can define a helpful
# mechanism to restrict vocab_clan to only those relations that contain particular values.
import algebraixlib.algebras.clans as clans
salutation_records_clan = clans.superstrict(vocab_clan, Set(Set(Couplet('meaning', 'salutation'))))
earth_records_clan = clans.superstrict(vocab_clan, Set(Set(Couplet('meaning', 'earth'))))
print("salutation_records_clan:", salutation_records_clan)
print("earth_records_clan:", earth_records_clan)

# By choosing an appropriate right-hand argument, our extended composition operation from earlier can
# model projection.
words_langs_clan = Set(Set(Couplet('word', 'word'), Couplet('language', 'language')))
print("words_langs_clan:", words_langs_clan)

# The relations.diag and clans.diag utility functions create a "diagonal" relation or clan,
# respectively, with simpler syntax.
assert words_langs_clan == clans.diag('word', 'language')

# Since the meaning of each set of records ('salutation') is invariant among the relations in
# salutation_records_clan, we can drop those Couplets. Note that the cardinality of the resulting
# clan is the same, but each relation now contains only two Couplets.
salutation_words_n_langs_clan = clans.compose(salutation_records_clan, words_langs_clan)
print("salutation_words_n_langs_clan:", salutation_words_n_langs_clan)

# However, we can take this one step further and "rename" the 'word' attribute to something more
# specific by replacing the value 'word' with 'salutation' everywhere we find it as the left of a
# Couplet. By doing this, we both compress the information in each relation and also set our data up
# for later processing.
salutations_n_langs_clan = clans.compose(salutation_words_n_langs_clan,
                                         Set(Set(Couplet("salutation", "word"),
                                                 Couplet("language", "language"))))
print("salutations_n_langs_clan:", salutations_n_langs_clan)

# We'll do the same for earth_records_clan, but do the projection and "rename" all in one
# composition operation.
earths_n_langs_clan = clans.compose(earth_records_clan,
                                    Set(Set(Couplet("earth", "word"),
                                            Couplet("language", "language"))))
print("earths_n_langs_clan:", earths_n_langs_clan)

# Our next task will be to relate these clans to each other in a way that preserves the functional
# characteristic of every relation. We can define a partial binary operation
# functional_union(A, B) on relations to be union(A, B) if union(A, B) is left functional else
# undefined.
func_union_pos = relations.functional_union(hello_relation,
                                                  Set(Couplet('language', 'English'),
                                                      Couplet('more', 'info')))
func_union_neg = relations.functional_union(hello_relation,
                                                  Set(Couplet('language', 'Spanish'),
                                                      Couplet('more', 'info')))
print(func_union_pos)
print(func_union_neg)

# Lifting this operation to clans models natural join-like behavior.
salutations_words_langs_clan = clans.functional_cross_union(salutations_n_langs_clan,
                                                                  earths_n_langs_clan)
print("salutations_words_langs_clan:", salutations_words_langs_clan)

# Now that the clans have been related to each other through their language attributes, we can
# do another projection. Notice how the "renaming" of 'word' to 'salutation' and 'earth' allows us
# to distinguish each of the words' meaning after joining the clans.
salutations_n_words_clan = clans.compose(salutations_words_langs_clan,
                                         clans.diag('salutation', 'earth'))
print("result")
print("salutations_n_words_clan:", salutations_n_words_clan)

# Finally, we will distill this data down to a single relation describing "Hello, World" phrases.
greeting_relation = Set(Couplet(rel('earth'), rel('salutation'))
                        for rel in salutations_n_words_clan)
print("Greetings:", greeting_relation)
