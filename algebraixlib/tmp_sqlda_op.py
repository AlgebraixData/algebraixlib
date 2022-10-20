# Copyright Permission.io, Inc. (formerly known as Algebraix Data Corporation), Copyright (c) 2022.
#
# Confidential and proprietary. For internal use only.
# --------------------------------------------------------------------------------------------------


def tmp_sqlda_op(is_pure):
    def decorator(f):
        f.is_pure = is_pure
        return f

    return decorator
