"""
    We like to think of a sqlda expression graph as a bunch nodes that are sqlda operations.  But in
    reality that is not true.  For example here are some nodes that are not sqlda ops,
    `make_undef`, `get_right`, `unary_multi_extend`, and `make_set`.  In this case we need all
    the nodes that are actually in a sqlda graph to have certain properties.  But we can
    not leverage a sqlda_op decorator, since it requires thinks that are specific to the actual
    operations (not nodes).  This module was created to cover some of the other nodes (not
    operations) creating a feeling like everything was designed consistently in a sqlda graph.
    It had to be put in algebraixlib for dependencies reasons, in reality this is an awful spot
    for it.
"""

# Copyright Algebraix Data Corporation 2017
#
# Confidential and proprietary. For internal use only.
# --------------------------------------------------------------------------------------------------


# todo: review above header comment.  A quick solution could be to forward these operations by
# adding a sqlda wrapper.
def tmp_sqlda_op(is_pure):
    def decorator(f):
        f.is_pure = is_pure
        return f

    return decorator
