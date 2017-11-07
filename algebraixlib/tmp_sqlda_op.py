# Copyright Algebraix Data Corporation 2015 - 2017
#
# Confidential and proprietary. For internal use only.
# --------------------------------------------------------------------------------------------------


def tmp_sqlda_op(is_pure):
    def decorator(f):
        f.is_pure = is_pure
        return f

    return decorator
