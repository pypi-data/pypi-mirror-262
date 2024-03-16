from buf.validate import validate_pb2 as _validate_pb2
from corvic_generated.algorithm.graph.v1 import graph_pb2 as _graph_pb2
from corvic_generated.embedding.v1 import models_pb2 as _models_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Parameters(_message.Message):
    __slots__ = ("space_id", "column_embedding_parameters", "node2vec_parameters")
    SPACE_ID_FIELD_NUMBER: _ClassVar[int]
    COLUMN_EMBEDDING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    NODE2VEC_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    space_id: str
    column_embedding_parameters: _models_pb2.ColumnEmbeddingParameters
    node2vec_parameters: _graph_pb2.Node2VecParameters
    def __init__(self, space_id: _Optional[str] = ..., column_embedding_parameters: _Optional[_Union[_models_pb2.ColumnEmbeddingParameters, _Mapping]] = ..., node2vec_parameters: _Optional[_Union[_graph_pb2.Node2VecParameters, _Mapping]] = ...) -> None: ...

class Experiment(_message.Message):
    __slots__ = ("name", "description", "params")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    params: _containers.RepeatedCompositeFieldContainer[Parameters]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., params: _Optional[_Iterable[_Union[Parameters, _Mapping]]] = ...) -> None: ...

class ExperimentEntry(_message.Message):
    __slots__ = ("room_id", "experiment_id", "created_at", "experiment")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    experiment_id: str
    created_at: _timestamp_pb2.Timestamp
    experiment: Experiment
    def __init__(self, room_id: _Optional[str] = ..., experiment_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., experiment: _Optional[_Union[Experiment, _Mapping]] = ...) -> None: ...

class GetExperimentRequest(_message.Message):
    __slots__ = ("experiment_id",)
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    experiment_id: str
    def __init__(self, experiment_id: _Optional[str] = ...) -> None: ...

class GetExperimentResponse(_message.Message):
    __slots__ = ("experiment_entry",)
    EXPERIMENT_ENTRY_FIELD_NUMBER: _ClassVar[int]
    experiment_entry: ExperimentEntry
    def __init__(self, experiment_entry: _Optional[_Union[ExperimentEntry, _Mapping]] = ...) -> None: ...

class ListExperimentsRequest(_message.Message):
    __slots__ = ("room_id",)
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    def __init__(self, room_id: _Optional[str] = ...) -> None: ...

class ListExperimentsResponse(_message.Message):
    __slots__ = ("experiment_entries",)
    EXPERIMENT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    experiment_entries: _containers.RepeatedCompositeFieldContainer[ExperimentEntry]
    def __init__(self, experiment_entries: _Optional[_Iterable[_Union[ExperimentEntry, _Mapping]]] = ...) -> None: ...

class CreateExperimentRequest(_message.Message):
    __slots__ = ("room_id", "experiment", "description", "params")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    experiment: Experiment
    description: str
    params: _containers.RepeatedCompositeFieldContainer[Parameters]
    def __init__(self, room_id: _Optional[str] = ..., experiment: _Optional[_Union[Experiment, _Mapping]] = ..., description: _Optional[str] = ..., params: _Optional[_Iterable[_Union[Parameters, _Mapping]]] = ...) -> None: ...

class CreateExperimentResponse(_message.Message):
    __slots__ = ("experiment_entry",)
    EXPERIMENT_ENTRY_FIELD_NUMBER: _ClassVar[int]
    experiment_entry: ExperimentEntry
    def __init__(self, experiment_entry: _Optional[_Union[ExperimentEntry, _Mapping]] = ...) -> None: ...

class DeleteExperimentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteExperimentResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
