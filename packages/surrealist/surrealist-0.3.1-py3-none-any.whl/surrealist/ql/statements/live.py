from typing import List, Callable

from surrealist.connections import Connection
from surrealist.ql.statements.live_statements import LiveUseWhere
from surrealist.ql.statements.statement import Statement
from surrealist.result import SurrealResult
from surrealist.utils import OK


class Live(Statement, LiveUseWhere):
    """
    Represents LIVE SELECT statement, it should be able to use any statements from documentation

    Refer to: https://docs.surrealdb.com/docs/surrealql/statements/live-select

    Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_live_examples.py
    """

    def __init__(self, connection: Connection, table_name: str, callback: Callable, use_diff: bool = False):
        super().__init__(connection)
        self._table_name = table_name
        self._alias = None
        self._diff = use_diff
        self._callback = callback

    def alias(self, value_name: str, alias: str) -> "Live":
        """

        :param value_name:
        :param alias:
        :return:
        """
        self._alias = (value_name, alias)
        self._diff = False
        return self

    def validate(self) -> List[str]:
        return [OK]

    def run(self) -> SurrealResult:
        return self._drill(self.to_str())

    def _drill(self, query):
        return self._connection.custom_live(query, self._callback)

    def _clean_str(self):
        if self._diff:
            what = "DIFF"
        elif self._alias:
            what = f"{self._alias[0]} AS {self._alias[1]}"
        else:
            what = "*"
        return f"LIVE SELECT {what} FROM {self._table_name}"
