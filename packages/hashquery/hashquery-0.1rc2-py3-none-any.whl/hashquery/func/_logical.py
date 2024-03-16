from typing import *

from ..model.column_expression import ColumnExpression, SqlFunctionColumnExpression
from ..utils.keypath.resolve import defer_keypath_args


@defer_keypath_args
def and_(*clauses: List[ColumnExpression]) -> ColumnExpression:
    """
    an `AND` expression in SQL
    """
    return SqlFunctionColumnExpression("and", clauses)


@defer_keypath_args
def or_(*clauses: List[ColumnExpression]) -> ColumnExpression:
    """
    an `OR` expression in SQL
    """
    return SqlFunctionColumnExpression("or", clauses)
