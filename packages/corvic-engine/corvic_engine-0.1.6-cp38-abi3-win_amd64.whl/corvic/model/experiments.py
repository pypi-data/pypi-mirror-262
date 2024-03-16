"""Experiments."""

from collections.abc import Iterable, Iterator
from typing import Any, TypeAlias

import polars as pl

from corvic import embed, orm
from corvic.model.spaces import Space, SpaceEdgeTableMetadata
from corvic.model.wrapped_orm import WrappedOrmObject
from corvic.result import BadArgumentError

ExperimentID: TypeAlias = orm.ExperimentID


class Experiment(WrappedOrmObject[ExperimentID, orm.Experiment]):
    """Experiments are the results produced by applying embedding methods to Spaces.

    Example:
    >>> experiment = Experiment.node2vec(space, dim=10, walk_length=10, window=10)
    """

    def _sub_orm_objects(self, orm_object: orm.Experiment) -> Iterable[orm.Base]:
        return []

    @classmethod
    def node2vec(
        cls, space: Space, *, dim: int, walk_length: int, window: int
    ) -> embed.Node2Vec[str]:
        """Run Node2Vec on the graph described by the space.

        Args:
            space: The space to run Node2Vec on
            dim: The dimensionality of the embedding
            walk_length: Length of the random walk to be computed
            window: Size of the window. This is half of the context,
                as the context is all nodes before `window` and
                after `window`.

        Returns:
            An Experiment
        """
        if not space.relationships:
            raise BadArgumentError("Node2Vec requires some relationships")

        directed = space.relationships[0].directional
        if any(rel.directional != directed for rel in space.relationships):
            raise NotImplementedError(
                "node2vec with mixed directionality not yet implemented"
            )

        def normalize(id_val: Any, source_name: str):
            return f"{source_name}-{id_val}"

        edge_tables = space.output_edge_tables()
        if not edge_tables:
            raise BadArgumentError("Node2Vec requires some sources to be output")

        def edge_generator():
            for table in space.output_edge_tables():
                edge_table_info = table.get_typed_metadata(SpaceEdgeTableMetadata)
                for row in table.to_dicts().unwrap_or_raise():
                    yield (
                        normalize(
                            row[edge_table_info.start_source_column_name],
                            edge_table_info.start_source_name,
                        ),
                        normalize(
                            row[edge_table_info.end_source_column_name],
                            edge_table_info.end_source_name,
                        ),
                    )

        n2v_space = embed.Space(list(edge_generator()), directed=directed)
        return embed.Node2Vec(
            space=n2v_space, dim=dim, walk_length=walk_length, window=window
        )

    def to_polars(self) -> Iterator[pl.DataFrame]:
        raise NotImplementedError()
