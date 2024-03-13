# Copyright (C) 2021 Bosutech XXI S.L.
#
# nucliadb is offered under the AGPL v3.0 and as commercial software.
# For commercial licensing, contact us at info@nuclia.com.
#
# AGPL:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Type, TypeVar, Union

from google.protobuf.json_format import MessageToDict
from nucliadb_protos.audit_pb2 import ClientType
from nucliadb_protos.nodereader_pb2 import DocumentScored, OrderBy
from nucliadb_protos.nodereader_pb2 import ParagraphResult as PBParagraphResult
from nucliadb_protos.utils_pb2 import RelationNode
from nucliadb_protos.writer_pb2 import ShardObject as PBShardObject
from nucliadb_protos.writer_pb2 import Shards as PBShards
from pydantic import BaseModel, Field, root_validator, validator
from typing_extensions import Annotated

from nucliadb_models.common import FieldTypeName, ParamDefault
from nucliadb_models.metadata import RelationType, ResourceProcessingStatus
from nucliadb_models.resource import ExtractedDataTypeName, Resource
from nucliadb_models.security import RequestSecurity
from nucliadb_models.vectors import SemanticModelMetadata, VectorSimilarity

_T = TypeVar("_T")


class ModelParamDefaults:
    applied_autofilters = ParamDefault(
        default=[],
        title="Autofilters",
        description="List of filters automatically applied to the search query",
    )


class ResourceProperties(str, Enum):
    BASIC = "basic"
    ORIGIN = "origin"
    EXTRA = "extra"
    RELATIONS = "relations"
    VALUES = "values"
    EXTRACTED = "extracted"
    ERRORS = "errors"
    SECURITY = "security"


class SearchOptions(str, Enum):
    PARAGRAPH = "paragraph"
    DOCUMENT = "document"
    RELATIONS = "relations"
    VECTOR = "vector"


class ChatOptions(str, Enum):
    VECTORS = "vectors"
    PARAGRAPHS = "paragraphs"
    RELATIONS = "relations"


class SuggestOptions(str, Enum):
    PARAGRAPH = "paragraph"
    ENTITIES = "entities"


class NucliaDBClientType(str, Enum):
    API = "api"
    WIDGET = "widget"
    WEB = "web"
    DASHBOARD = "dashboard"
    DESKTOP = "desktop"
    CHROME_EXTENSION = "chrome_extension"

    def to_proto(self) -> int:
        return ClientType.Value(self.name)


class Sort(int, Enum):
    DESC = 0
    ASC = 1


class JsonBaseModel(BaseModel):
    def __str__(self):
        try:
            return self.json()
        except Exception:
            # fallback to BaseModel implementation
            return super().__str__()


class Facet(BaseModel):
    facetresults: Dict[str, int]


FacetsResult = Dict[str, Any]


class TextPosition(BaseModel):
    page_number: Optional[int] = None
    index: int
    start: int
    end: int
    start_seconds: Optional[List[int]] = None
    end_seconds: Optional[List[int]] = None


class Sentence(BaseModel):
    score: float
    rid: str
    text: str
    field_type: str
    field: str
    index: Optional[str] = None
    position: Optional[TextPosition] = None


class Sentences(BaseModel):
    results: List[Sentence] = []
    facets: FacetsResult
    page_number: int = 0
    page_size: int = 20
    min_score: float = Field(
        title="Minimum score",
        description="Minimum similarity score used to filter vector index search. Results with a lower score have been ignored.",  # noqa
    )


class Paragraph(BaseModel):
    score: float
    rid: str
    field_type: str
    field: str
    text: str
    labels: List[str] = []
    start_seconds: Optional[List[int]] = None
    end_seconds: Optional[List[int]] = None
    position: Optional[TextPosition] = None
    fuzzy_result: bool = False


class Paragraphs(BaseModel):
    results: List[Paragraph] = []
    facets: Optional[FacetsResult] = None
    query: Optional[str] = None
    total: int = 0
    page_number: int = 0
    page_size: int = 20
    next_page: bool = False
    min_score: float = Field(
        title="Minimum score",
        description="Minimum bm25 score used to filter bm25 index search. Results with a lower score have been ignored.",  # noqa
    )


class ResourceResult(BaseModel):
    score: Union[float, int]
    rid: str
    field_type: str
    field: str
    labels: Optional[list[str]] = None


class Resources(BaseModel):
    results: List[ResourceResult]
    facets: Optional[FacetsResult] = None
    query: Optional[str] = None
    total: int = 0
    page_number: int = 0
    page_size: int = 20
    next_page: bool = False
    min_score: float = Field(
        title="Minimum score",
        description="Minimum bm25 score used to filter bm25 index search. Results with a lower score have been ignored.",  # noqa
    )


class RelationDirection(str, Enum):
    IN = "in"
    OUT = "out"


class EntityType(str, Enum):
    ENTITY = "entity"
    LABEL = "label"
    RESOURCE = "resource"
    USER = "user"


RelationNodeTypeMap = {
    RelationNode.NodeType.ENTITY: EntityType.ENTITY,
    RelationNode.NodeType.LABEL: EntityType.LABEL,
    RelationNode.NodeType.RESOURCE: EntityType.RESOURCE,
    RelationNode.NodeType.USER: EntityType.USER,
}


class DirectionalRelation(BaseModel):
    entity: str
    entity_type: EntityType
    relation: RelationType
    relation_label: str
    direction: RelationDirection


class EntitySubgraph(BaseModel):
    related_to: List[DirectionalRelation]


# TODO: uncomment and implement (next iteration)
# class RelationPath(BaseModel):
#     origin: str
#     destination: str
#     path: List[DirectionalRelation]


class Relations(BaseModel):
    entities: Dict[str, EntitySubgraph]
    # TODO: implement in the next iteration of knowledge graph search
    # graph: List[RelationPath]


class RelatedEntity(BaseModel, frozen=True):
    family: str
    value: str


class RelatedEntities(BaseModel):
    total: int = 0
    entities: List[RelatedEntity] = []


class ResourceSearchResults(JsonBaseModel):
    """Search on resource results"""

    sentences: Optional[Sentences] = None
    paragraphs: Optional[Paragraphs] = None
    relations: Optional[Relations] = None
    nodes: Optional[List[Dict[str, str]]] = None
    shards: Optional[List[str]] = None


class KnowledgeboxSearchResults(JsonBaseModel):
    """Search on knowledgebox results"""

    resources: Dict[str, Resource] = {}
    sentences: Optional[Sentences] = None
    paragraphs: Optional[Paragraphs] = None
    fulltext: Optional[Resources] = None
    relations: Optional[Relations] = None
    nodes: Optional[List[Dict[str, str]]] = None
    shards: Optional[List[str]] = None
    autofilters: List[str] = ModelParamDefaults.applied_autofilters.to_pydantic_field()


class KnowledgeboxSuggestResults(JsonBaseModel):
    """Suggest on resource results"""

    paragraphs: Optional[Paragraphs] = None
    entities: Optional[RelatedEntities] = None
    shards: Optional[List[str]] = None


class KnowledgeboxCounters(BaseModel):
    resources: int
    paragraphs: int
    fields: int
    sentences: int
    shards: Optional[List[str]] = None
    index_size: float = Field(default=0.0, title="Index size (bytes)")


class SortField(str, Enum):
    SCORE = "score"
    CREATED = "created"
    MODIFIED = "modified"
    TITLE = "title"


SortFieldMap = {
    SortField.SCORE: None,
    SortField.CREATED: OrderBy.OrderField.CREATED,
    SortField.MODIFIED: OrderBy.OrderField.MODIFIED,
    SortField.TITLE: None,
}


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


SortOrderMap = {
    SortOrder.ASC: Sort.ASC,
    SortOrder.DESC: Sort.DESC,
}


class SortOptions(BaseModel):
    field: SortField
    limit: Optional[int] = Field(None, gt=0)
    order: SortOrder = SortOrder.DESC


class KnowledgeBoxCount(BaseModel):
    paragraphs: int
    fields: int
    sentences: int


class DocumentServiceEnum(str, Enum):
    DOCUMENT_V0 = "DOCUMENT_V0"
    DOCUMENT_V1 = "DOCUMENT_V1"
    DOCUMENT_V2 = "DOCUMENT_V2"


class ParagraphServiceEnum(str, Enum):
    PARAGRAPH_V0 = "PARAGRAPH_V0"
    PARAGRAPH_V1 = "PARAGRAPH_V1"


class VectorServiceEnum(str, Enum):
    VECTOR_V0 = "VECTOR_V0"
    VECTOR_V1 = "VECTOR_V1"


class RelationServiceEnum(str, Enum):
    RELATION_V0 = "RELATION_V0"
    RELATION_V1 = "RELATION_V1"
    RELATION_V2 = "RELATION_V2"


class ShardCreated(BaseModel):
    id: str
    document_service: DocumentServiceEnum
    paragraph_service: ParagraphServiceEnum
    vector_service: VectorServiceEnum
    relation_service: RelationServiceEnum


class ShardReplica(BaseModel):
    node: str
    shard: ShardCreated


class ShardObject(BaseModel):
    shard: str
    replicas: List[ShardReplica]

    @classmethod
    def from_message(cls: Type[_T], message: PBShardObject) -> _T:
        return cls(
            **MessageToDict(
                message,
                preserving_proto_field_name=True,
                including_default_value_fields=True,
            )
        )


class KnowledgeboxShards(BaseModel):
    kbid: str
    actual: int
    similarity: VectorSimilarity
    shards: List[ShardObject]
    model: Optional[SemanticModelMetadata]

    @classmethod
    def from_message(cls: Type[_T], message: PBShards) -> _T:
        as_dict = MessageToDict(
            message,
            preserving_proto_field_name=True,
            including_default_value_fields=True,
        )
        as_dict["similarity"] = VectorSimilarity.from_message(message.similarity)
        if message.HasField("model"):
            as_dict["model"] = SemanticModelMetadata.from_message(message.model)
        return cls(**as_dict)


class SearchParamDefaults:
    query = ParamDefault(
        default="", title="Query", description="The query to search for"
    )
    suggest_query = ParamDefault(
        default=..., title="Query", description="The query to get suggestions for"
    )
    fields = ParamDefault(
        default=[],
        title="Fields",
        description="The list of fields to search in. For instance: `a/title` to search only on title field. For more details on filtering by field, see: https://docs.nuclia.dev/docs/docs/using/search/#search-in-a-specific-field",  # noqa: E501
    )
    filters = ParamDefault(
        default=[],
        title="Filters",
        description="The list of filters to apply. Filtering examples can be found here: https://docs.nuclia.dev/docs/docs/using/search/#filters",  # noqa: E501
    )
    resource_filters = ParamDefault(
        default=[],
        title="Resources filter",
        description="List of resource ids to filter search results for. Only paragraphs from the specified resources will be returned.",  # noqa: E501
    )
    faceted = ParamDefault(
        default=[],
        title="Faceted",
        description="The list of facets to calculate. The facets follow the same syntax as filters: https://docs.nuclia.dev/docs/docs/using/search/#filters",  # noqa: E501
        max_items=50,
    )
    autofilter = ParamDefault(
        default=False,
        title="Automatic search filtering",
        description="If set to true, the search will automatically add filters to the query. For example, it will filter results containing the entities detected in the query",  # noqa: E501
    )
    chat_query = ParamDefault(
        default=...,
        title="Query",
        description="The query to get a generative answer for",
    )
    shards = ParamDefault(
        default=[],
        title="Shards",
        description="The list of shard replicas to search in. If empty, random replicas will be selected.",
    )
    page_number = ParamDefault(
        default=0,
        title="Page number",
        description="The page number of the results to return",
    )
    page_size = ParamDefault(
        default=20,
        title="Page size",
        description="The number of results to return per page",
    )
    highlight = ParamDefault(
        default=False,
        title="Highlight",
        description="If set to true, the query terms will be highlighted in the results between <mark>...</mark> tags",  # noqa: E501
    )
    with_duplicates = ParamDefault(
        default=False,
        title="With duplicate paragraphs",
        description="Whether to return duplicate paragraphs on the same document",  # noqa: E501
    )
    with_status = ParamDefault(
        default=None,
        title="With processing status",
        description="Filter results by resource processing status",
    )
    with_synonyms = ParamDefault(
        default=False,
        title="With custom synonyms",
        description="Whether to return matches for custom knowledge box synonyms of the query terms. Note: only supported for `paragraph` and `document` search options.",  # noqa: E501
    )
    sort_order = ParamDefault(
        default=SortOrder.DESC,
        title="Sort order",
        description="Order to sort results with",
    )
    sort_limit = ParamDefault(
        default=None,
        title="Sort limit",
        description="",
        gt=0,
    )
    sort_field = ParamDefault(
        default=None,
        title="Sort field",
        description="Field to sort results with",
    )
    sort = ParamDefault(
        default=None,
        title="Sort options",
        description="Options for results sorting",
    )
    search_features = ParamDefault(
        default=None,
        title="Search features",
        description="List of search features to use. Each value corresponds to a lookup into on of the different indexes.",  # noqa
    )
    debug = ParamDefault(
        default=False,
        title="Debug mode",
        description="If set, the response will include some extra metadata for debugging purposes, like the list of queried nodes.",  # noqa
    )
    show = ParamDefault(
        default=[ResourceProperties.BASIC],
        title="Show metadata",
        description="Controls which types of metadata are serialized on resources of search results",
    )
    extracted = ParamDefault(
        default=[],
        title="Extracted metadata",
        description="Controls which parts of the extracted metadata are serialized on search results",
    )
    field_type_filter = ParamDefault(
        default=list(FieldTypeName),
        title="Field type filter",
        description="Filter search results to match paragraphs of a specific field type. E.g: `['conversation', 'text']`",  # noqa
    )
    range_creation_start = ParamDefault(
        default=None,
        title="Resource creation range start",
        description="Resources created before this date will be filtered out of search results. Datetime are represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.",  # noqa
    )
    range_creation_end = ParamDefault(
        default=None,
        title="Resource creation range end",
        description="Resources created after this date will be filtered out of search results. Datetime are represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.",  # noqa
    )
    range_modification_start = ParamDefault(
        default=None,
        title="Resource modification range start",
        description="Resources modified before this date will be filtered out of search results. Datetime are represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.",  # noqa
    )
    range_modification_end = ParamDefault(
        default=None,
        title="Resource modification range end",
        description="Resources modified after this date will be filtered out of search results. Datetime are represented as a str in ISO 8601 format, like: 2008-09-15T15:53:00+05:00.",  # noqa
    )
    vector = ParamDefault(
        default=None,
        title="Search Vector",
        description="The vector to perform the search with. If not provided, NucliaDB will use Nuclia Predict API to create the vector off from the query.",  # noqa
    )
    vectorset = ParamDefault(
        default=None,
        title="Vectorset id",
        description="Id of the vectorset to perform the vector search into.",
    )
    chat_context = ParamDefault(
        default=None,
        title="Chat history",
        description="Use to rephrase the new LLM query by taking into account the chat conversation history",  # noqa
    )
    chat_features = ParamDefault(
        default=[ChatOptions.VECTORS, ChatOptions.PARAGRAPHS, ChatOptions.RELATIONS],
        title="Chat features",
        description="Features enabled for the chat endpoint. Semantic search is done if `vectors` is included. If `paragraphs` is included, the results will include matching paragraphs from the bm25 index. If `relations` is included, a graph of entities related to the answer is returned.",  # noqa
    )
    prompt = ParamDefault(
        default=None,
        title="Prompt",
        description="Input here your prompt with the words {context} and {question} in brackets where you want those fields to be placed, in case you want them in your prompt. Context will be the data returned by the retrieval step.",  # noqa
    )
    suggest_features = ParamDefault(
        default=[
            SuggestOptions.PARAGRAPH,
            SuggestOptions.ENTITIES,
        ],
        title="Suggest features",
        description="Features enabled for the suggest endpoint.",
    )
    security = ParamDefault(
        default=None,
        title="Security",
        description="Security metadata for the request. If not provided, the search request is done without the security lookup phase.",  # noqa
    )
    security_groups = ParamDefault(
        default=[],
        title="Security groups",
        description="List of security groups to filter search results for. Only resources matching the query and containing the specified security groups will be returned. If empty, all resources will be considered for the search.",  # noqa
    )


class Filter(BaseModel):
    all: Optional[List[str]] = Field(default=None, min_items=1)
    any: Optional[List[str]] = Field(default=None, min_items=1)
    none: Optional[List[str]] = Field(default=None, min_items=1)
    not_all: Optional[List[str]] = Field(default=None, min_items=1)

    @root_validator(pre=True)
    def validate_filter(cls, values):
        if len({k for k, v in values.items() if v is not None}) != 1:
            raise ValueError("Only one of 'all', 'any', 'none' or 'not_all' can be set")
        return values


class CatalogRequest(BaseModel):
    query: str = SearchParamDefaults.query.to_pydantic_field()
    filters: Union[List[str], List[Filter]] = Field(
        default=[],
        title="Filters",
        description="The list of filters to apply. Filtering examples can be found here: https://docs.nuclia.dev/docs/docs/using/search/#filters",  # noqa: E501
    )
    faceted: List[str] = SearchParamDefaults.faceted.to_pydantic_field()
    sort: Optional[SortOptions] = SearchParamDefaults.sort.to_pydantic_field()
    page_number: int = SearchParamDefaults.page_number.to_pydantic_field()
    page_size: int = SearchParamDefaults.page_size.to_pydantic_field()
    shards: List[str] = SearchParamDefaults.shards.to_pydantic_field()
    debug: bool = SearchParamDefaults.debug.to_pydantic_field()
    with_status: Optional[ResourceProcessingStatus] = Field(
        default=None,
        title="With processing status",
        description="Filter results by resource processing status",
    )

    @validator("faceted")
    def nested_facets_not_supported(cls, facets):
        return validate_facets(facets)


class MinScore(BaseModel):
    semantic: Optional[float] = Field(
        default=None,
        title="Minimum semantic score",
        description="Minimum semantic similarity score used to filter vector index search. If not specified, the default minimum score of the semantic model associated to the Knowledge Box will be used. Check out the documentation for more information on how to use this parameter: https://docs.nuclia.dev/docs/docs/using/search/#minimum-score",  # noqa: E501
    )
    bm25: float = Field(
        default=0,
        title="Minimum bm25 score",
        description="Minimum score used to filter bm25 index search. Check out the documentation for more information on how to use this parameter: https://docs.nuclia.dev/docs/docs/using/search/#minimum-score",
        ge=0,
    )


class BaseSearchRequest(BaseModel):
    query: str = SearchParamDefaults.query.to_pydantic_field()
    fields: List[str] = SearchParamDefaults.fields.to_pydantic_field()
    filters: Union[List[str], List[Filter]] = Field(
        default=[],
        title="Filters",
        description="The list of filters to apply. Filtering examples can be found here: https://docs.nuclia.dev/docs/docs/using/search/#filters",  # noqa: E501
    )
    page_number: int = SearchParamDefaults.page_number.to_pydantic_field()
    page_size: int = SearchParamDefaults.page_size.to_pydantic_field()
    min_score: Optional[Union[float, MinScore]] = Field(
        default=None,
        title="Minimum score",
        description="Minimum score to filter search results. Results with a lower score will be ignored. Accepts either a float or a dictionary with the minimum scores for the bm25 and vector indexes. If a float is provided, it is interpreted as the minimum score for vector index search.",  # noqa
    )
    range_creation_start: Optional[
        datetime
    ] = SearchParamDefaults.range_creation_start.to_pydantic_field()
    range_creation_end: Optional[
        datetime
    ] = SearchParamDefaults.range_creation_end.to_pydantic_field()
    range_modification_start: Optional[
        datetime
    ] = SearchParamDefaults.range_modification_start.to_pydantic_field()
    range_modification_end: Optional[
        datetime
    ] = SearchParamDefaults.range_modification_end.to_pydantic_field()
    features: List[
        SearchOptions
    ] = SearchParamDefaults.search_features.to_pydantic_field(
        default=[
            SearchOptions.PARAGRAPH,
            SearchOptions.DOCUMENT,
            SearchOptions.VECTOR,
        ]
    )
    debug: bool = SearchParamDefaults.debug.to_pydantic_field()
    highlight: bool = SearchParamDefaults.highlight.to_pydantic_field()
    show: List[ResourceProperties] = SearchParamDefaults.show.to_pydantic_field()
    field_type_filter: List[
        FieldTypeName
    ] = SearchParamDefaults.field_type_filter.to_pydantic_field()
    extracted: List[
        ExtractedDataTypeName
    ] = SearchParamDefaults.extracted.to_pydantic_field()
    shards: List[str] = SearchParamDefaults.shards.to_pydantic_field()
    vector: Optional[List[float]] = SearchParamDefaults.vector.to_pydantic_field()
    vectorset: Optional[str] = SearchParamDefaults.vectorset.to_pydantic_field()
    with_duplicates: bool = SearchParamDefaults.with_duplicates.to_pydantic_field()
    with_synonyms: bool = SearchParamDefaults.with_synonyms.to_pydantic_field()
    autofilter: bool = SearchParamDefaults.autofilter.to_pydantic_field()
    resource_filters: List[
        str
    ] = SearchParamDefaults.resource_filters.to_pydantic_field()
    security: Optional[
        RequestSecurity
    ] = SearchParamDefaults.security.to_pydantic_field()


class SearchRequest(BaseSearchRequest):
    faceted: List[str] = SearchParamDefaults.faceted.to_pydantic_field()
    sort: Optional[SortOptions] = SearchParamDefaults.sort.to_pydantic_field()

    @validator("faceted")
    def nested_facets_not_supported(cls, facets):
        return validate_facets(facets)


class Author(str, Enum):
    NUCLIA = "NUCLIA"
    USER = "USER"


class ChatContextMessage(BaseModel):
    author: Author
    text: str


# For bw compatibility
Message = ChatContextMessage


class UserPrompt(BaseModel):
    prompt: str


class ChatModel(BaseModel):
    """
    This is the model for the predict request payload on the chat endpoint
    """

    question: str = Field(description="Question to ask the generative model")
    user_id: str
    retrieval: bool = True
    system: Optional[str] = None
    query_context: Dict[str, str] = Field(
        default={},
        description="The information retrieval context for the current query",
    )
    query_context_order: Optional[Dict[str, int]] = Field(
        default=None,
        description="The order of the query context elements. This is used to sort the context elements by relevance before sending them to the generative model",  # noqa
    )
    chat_history: List[ChatContextMessage] = Field(
        default=[], description="The chat conversation history"
    )
    truncate: bool = Field(
        default=True,
        description="Truncate the chat context in case it doesn't fit the generative input",
    )
    user_prompt: Optional[UserPrompt] = Field(
        default=None, description="Optional custom prompt input by the user"
    )
    citations: bool = Field(
        default=False, description="Whether to include the citations in the answer"
    )
    generative_model: Optional[str] = Field(
        default=None,
        title="Generative model",
        description="The generative model to use for the predict chat endpoint. If not provided, the model configured for the Knowledge Box is used.",
    )


class RephraseModel(BaseModel):
    question: str
    chat_history: List[ChatContextMessage] = []
    user_id: str
    user_context: List[str] = []
    generative_model: Optional[str] = Field(
        default=None,
        title="Generative model",
        description="The generative model to use for the rephrase endpoint. If not provided, the model configured for the Knowledge Box is used.",
    )


class AskDocumentModel(BaseModel):
    question: str = Field(description="The question to ask on the document")
    blocks: List[List[str]] = Field(
        description="The complete list of text blocks of a document"
    )
    user_id: str = Field(description="The id of the user associated to the request")


class RagStrategyName:
    FIELD_EXTENSION = "field_extension"
    FULL_RESOURCE = "full_resource"


class RagStrategy(BaseModel):
    name: str


ALLOWED_FIELD_TYPES: dict[str, str] = {
    "l": "layout",
    "t": "text",
    "f": "file",
    "u": "link",
    "d": "datetime",
    "k": "keywordset",
    "a": "generic",
    "c": "conversation",
}


class FieldExtensionStrategy(RagStrategy):
    name: Literal["field_extension"]
    fields: List[str] = Field(
        title="Fields",
        description="List of field ids to extend the context with. It will try to extend the retrieval context with the specified fields in the matching resources. The field ids have to be in the format `{field_type}/{field_name}`, like 'a/title', 'a/summary' for title and summary fields or 't/amend' for a text field named 'amend'.",  # noqa
        min_items=1,
        unique_items=True,
    )

    @root_validator(pre=True)
    def fields_validator(cls, values):
        if values.get("fields") is None:
            return values

        # Check that the fields are in the format {field_type}/{field_name}
        for field in values.get("fields"):
            try:
                field_type, _ = field.strip("/").split("/")
            except ValueError:
                raise ValueError(
                    f"Field '{field}' is not in the format {{field_type}}/{{field_name}}"
                )
            if field_type not in ALLOWED_FIELD_TYPES:
                allowed_field_types_part = ", ".join(
                    [
                        f"'{fid}' for '{fname}' fields"
                        for fid, fname in ALLOWED_FIELD_TYPES.items()
                    ]
                )
                raise ValueError(
                    f"Field '{field}' does not have a valid field type. "
                    f"Valid field types are: {allowed_field_types_part}."
                )

        return values


class FullResourceStrategy(RagStrategy):
    name: Literal["full_resource"]


RagStrategies = Annotated[
    Union[FieldExtensionStrategy, FullResourceStrategy], Field(discriminator="name")
]
PromptContext = dict[str, str]
PromptContextOrder = dict[str, int]


class ChatRequest(BaseModel):
    query: str = SearchParamDefaults.chat_query.to_pydantic_field()
    fields: List[str] = SearchParamDefaults.fields.to_pydantic_field()
    filters: Union[List[str], List[Filter]] = Field(
        default=[],
        title="Filters",
        description="The list of filters to apply. Filtering examples can be found here: https://docs.nuclia.dev/docs/docs/using/search/#filters",  # noqa: E501
    )
    min_score: Optional[Union[float, MinScore]] = Field(
        default=None,
        title="Minimum score",
        description="Minimum score to filter search results. Results with a lower score will be ignored. Accepts either a float or a dictionary with the minimum scores for the bm25 and vector indexes. If a float is provided, it is interpreted as the minimum score for vector index search.",  # noqa
    )
    features: List[ChatOptions] = SearchParamDefaults.chat_features.to_pydantic_field()
    range_creation_start: Optional[
        datetime
    ] = SearchParamDefaults.range_creation_start.to_pydantic_field()
    range_creation_end: Optional[
        datetime
    ] = SearchParamDefaults.range_creation_end.to_pydantic_field()
    range_modification_start: Optional[
        datetime
    ] = SearchParamDefaults.range_modification_start.to_pydantic_field()
    range_modification_end: Optional[
        datetime
    ] = SearchParamDefaults.range_modification_end.to_pydantic_field()
    show: List[ResourceProperties] = SearchParamDefaults.show.to_pydantic_field()
    field_type_filter: List[
        FieldTypeName
    ] = SearchParamDefaults.field_type_filter.to_pydantic_field()
    extracted: List[
        ExtractedDataTypeName
    ] = SearchParamDefaults.extracted.to_pydantic_field()
    shards: List[str] = SearchParamDefaults.shards.to_pydantic_field()
    context: Optional[
        List[ChatContextMessage]
    ] = SearchParamDefaults.chat_context.to_pydantic_field()
    extra_context: Optional[List[str]] = Field(
        default=None,
        title="Extra query context",
        description="""Additional context that is added to the retrieval context sent to the LLM.
        It allows extending the chat feature with content that may not be in the Knowledge Box.""",
    )
    autofilter: bool = SearchParamDefaults.autofilter.to_pydantic_field()
    highlight: bool = SearchParamDefaults.highlight.to_pydantic_field()
    resource_filters: List[
        str
    ] = SearchParamDefaults.resource_filters.to_pydantic_field()
    prompt: Optional[str] = SearchParamDefaults.prompt.to_pydantic_field()
    citations: bool = Field(
        default=False,
        description="Whether to include the citations for the answer in the response",
    )
    security: Optional[
        RequestSecurity
    ] = SearchParamDefaults.security.to_pydantic_field()
    rag_strategies: list[RagStrategies] = Field(
        default=[],
        title="RAG context building strategies",
        description="Options for tweaking how the context for the LLM model is crafted. `full_resource` will add the full text of the matching resources to the context. `field_extension` will add the text of the matching resource's specified fields to the context. If empty, the default strategy is used.",  # noqa
    )
    debug: bool = SearchParamDefaults.debug.to_pydantic_field()

    generative_model: Optional[str] = Field(
        default=None,
        title="Generative model",
        description="The generative model to use for the chat endpoint. If not provided, the model configured for the Knowledge Box is used.",
    )

    @root_validator(pre=True)
    def rag_features_validator(cls, values):
        chosen_strategies = [s.get("name") for s in values.get("rag_strategies") or []]

        # There must be at most one strategy of each type
        if len(chosen_strategies) > len(set(chosen_strategies)):
            raise ValueError("There must be at most one strategy of each type")

        # If full resource strategy is chosen, it must be the only strategy
        if (
            RagStrategyName.FULL_RESOURCE in chosen_strategies
            and len(chosen_strategies) > 1
        ):
            raise ValueError(
                f"If '{RagStrategyName.FULL_RESOURCE}' strategy is chosen, it must be the only strategy"
            )

        return values


class SummarizeResourceModel(BaseModel):
    fields: Dict[str, str] = {}


class SummaryKind(str, Enum):
    SIMPLE = "simple"
    EXTENDED = "extended"


class SummarizeModel(BaseModel):
    """
    Model for the summarize predict api request payload
    """

    resources: Dict[str, SummarizeResourceModel] = {}
    generative_model: Optional[str] = None
    user_prompt: Optional[str] = None
    summary_kind: SummaryKind = SummaryKind.SIMPLE


class SummarizeRequest(BaseModel):
    """
    Model for the request payload of the summarize endpoint
    """

    generative_model: Optional[str] = Field(
        default=None,
        title="Generative model",
        description="The generative model to use for the summarization. If not provided, the model configured for the Knowledge Box is used.",
    )

    user_prompt: Optional[str] = Field(
        default=None,
        title="User prompt",
        description="Optional custom prompt input by the user",
    )

    resources: List[str] = Field(
        ...,
        min_items=1,
        max_items=100,
        title="Resources",
        description="Uids or slugs of the resources to summarize. If the resources are not found, they will be ignored.",
    )

    summary_kind: SummaryKind = Field(
        default=SummaryKind.SIMPLE,
        title="Summary kind",
        description="Option to customize how the summary will be",
    )


class SummarizedResource(BaseModel):
    summary: str = Field(..., title="Summary", description="Summary of the resource")
    tokens: int


class SummarizedResponse(BaseModel):
    resources: Dict[str, SummarizedResource] = Field(
        default={},
        title="Resources",
        description="Individual resource summaries. The key is the resource id or slug.",
    )
    summary: str = Field(
        default="",
        title="Summary",
        description="Global summary of all resources combined.",
    )


class FindRequest(BaseSearchRequest):
    features: List[
        SearchOptions
    ] = SearchParamDefaults.search_features.to_pydantic_field(
        default=[
            SearchOptions.PARAGRAPH,
            SearchOptions.VECTOR,
        ]
    )

    @validator("features")
    def fulltext_not_supported(cls, v):
        if SearchOptions.DOCUMENT in v or SearchOptions.DOCUMENT == v:
            raise ValueError("fulltext search not supported")
        return v


class SCORE_TYPE(str, Enum):
    VECTOR = "VECTOR"
    BM25 = "BM25"
    BOTH = "BOTH"


class FindTextPosition(BaseModel):
    page_number: Optional[int]
    start_seconds: Optional[List[int]] = None
    end_seconds: Optional[List[int]] = None
    index: int
    start: int
    end: int


class FindParagraph(BaseModel):
    score: float
    score_type: SCORE_TYPE
    order: int = Field(default=0, ge=0)
    text: str
    id: str
    labels: Optional[List[str]] = []
    position: Optional[TextPosition] = None
    fuzzy_result: bool = False


@dataclass
class TempFindParagraph:
    rid: str
    field: str
    score: float
    start: int
    end: int
    id: str
    split: Optional[str] = None
    paragraph: Optional[FindParagraph] = None
    vector_index: Optional[DocumentScored] = None
    paragraph_index: Optional[PBParagraphResult] = None
    fuzzy_result: bool = False


class FindField(BaseModel):
    paragraphs: Dict[str, FindParagraph]


class FindResource(Resource):
    fields: Dict[str, FindField]

    def updated_from(self, origin: Resource):
        for key in origin.__fields__.keys():
            self.__setattr__(key, getattr(origin, key))


class KnowledgeboxFindResults(JsonBaseModel):
    """Find on knowledgebox results"""

    resources: Dict[str, FindResource]
    relations: Optional[Relations] = None
    query: Optional[str] = None
    total: int = 0
    page_number: int = 0
    page_size: int = 20
    next_page: bool = False
    nodes: Optional[List[Dict[str, str]]] = Field(
        default=None,
        title="Nodes",
        description="List of nodes queried in the search",
    )
    shards: Optional[List[str]] = Field(
        default=None,
        title="Shards",
        description="The list of shard replica ids used for the search.",
    )
    autofilters: List[str] = ModelParamDefaults.applied_autofilters.to_pydantic_field()
    min_score: Optional[Union[float, MinScore]] = Field(
        title="Minimum result score",
        description="The minimum scores that have been used for the search operation.",
    )
    best_matches: List[str] = Field(
        default=[],
        title="Best matches",
        description="List of ids of best matching paragraphs. The list is sorted by decreasing relevance (most relevant first).",  # noqa
    )


class FeedbackTasks(str, Enum):
    CHAT = "CHAT"


class FeedbackRequest(BaseModel):
    ident: str = Field(
        title="Request identifier",
        description="Id of the request to provide feedback for. This id is returned in the response header `Nuclia-Learning-Id` of the chat endpoint.",  # noqa
    )
    good: bool = Field(title="Good", description="Whether the result was good or not")
    task: FeedbackTasks = Field(
        title="Task",
        description="The task the feedback is for. For now, only `CHAT` task is available",
    )
    feedback: Optional[str] = Field(title="Feedback", description="Feedback text")


TextBlocks = List[List[str]]


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        title="Question",
        description="Question asked to the document",
        example="Does this document contain personal information?",
    )


class AskResponse(BaseModel):
    answer: str = Field(
        ...,
        title="Answer",
        description="Answer to the question received from the generative AI model",
    )


def validate_facets(facets):
    """
    Raises ValueError if provided facets contains nested facets, like:
    ["/a/b", "/a/b/c"]
    """
    if len(facets) < 2:
        return facets

    # Sort facets alphabetically to make sure that nested facets appear right after their parents
    sorted_facets = sorted(facets)
    facet = sorted_facets.pop(0)
    while True:
        try:
            next_facet = sorted_facets.pop(0)
        except IndexError:
            # No more facets to check
            break
        if next_facet == facet:
            raise ValueError(
                f"Facet {next_facet} is already present in facets. Faceted list must be unique."
            )
        if next_facet.startswith(facet):
            if next_facet.replace(facet, "").startswith("/"):
                raise ValueError(
                    "Nested facets are not allowed: {child} is a child of {parent}".format(
                        child=next_facet, parent=facet
                    )
                )
        facet = next_facet
    return facets
