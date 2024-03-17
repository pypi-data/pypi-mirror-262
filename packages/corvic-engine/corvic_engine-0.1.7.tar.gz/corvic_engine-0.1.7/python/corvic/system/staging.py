"""Corvic system data staging protocol."""

from collections.abc import Iterable
from typing import Any

import sqlglot
from typing_extensions import Protocol


class StagingDB(Protocol):
    """A connection to some database where staging data can be found."""

    def count_ingested_rows(self, blob_name: str, *other_blob_names: str) -> int:
        ...

    def query_for_blobs(
        self, blob_names: list[str], column_names: list[str]
    ) -> sqlglot.exp.Query:
        ...

    def run_select_query(self, query: sqlglot.exp.Query) -> Iterable[dict[str, Any]]:
        ...
