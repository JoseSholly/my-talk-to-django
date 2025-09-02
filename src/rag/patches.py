import logging
from typing import Any, Optional, Union

from llama_index.core.callbacks.base import CallbackManager
from llama_index.core.query_engine.sql_vector_query_engine import DEFAULT_SQL_VECTOR_SYNTHESIS_PROMPT
from llama_index.core.query_engine import SQLAutoVectorQueryEngine
from llama_index.core.indices.struct_store.sql_query import (
    BaseSQLTableQueryEngine,
    NLSQLTableQueryEngine,
)
from llama_index.core.indices.vector_store.retrievers.auto_retriever import VectorIndexAutoRetriever

from llama_index.core.llms.llm import LLM
from llama_index.core.prompts.base import BasePromptTemplate, PromptTemplate
from llama_index.core.prompts.mixin import PromptDictType, PromptMixinType
from llama_index.core.query_engine.retriever_query_engine import (
    RetrieverQueryEngine,
)
from llama_index.core.query_engine.sql_join_query_engine import (
    SQLAugmentQueryTransform,
    SQLJoinQueryEngine,
)
from llama_index.core.selectors.llm_selectors import LLMSingleSelector
from llama_index.core.selectors.pydantic_selectors import PydanticSingleSelector
from llama_index.core.tools.query_engine import QueryEngineTool


class MySQLAutoVectorQueryEngine(SQLAutoVectorQueryEngine):
    def __init__(
        self,
        sql_query_tool: QueryEngineTool,
        vector_query_tool: QueryEngineTool,
        selector: Optional[Union[LLMSingleSelector, PydanticSingleSelector]] = None,
        llm: Optional[LLM] = None,
        # service_context: Optional[ServiceContext] = None,
        
        sql_vector_synthesis_prompt: Optional[BasePromptTemplate] = None,
        sql_augment_query_transform: Optional[SQLAugmentQueryTransform] = None,
        use_sql_vector_synthesis: bool = True,
        callback_manager: Optional[CallbackManager] = None,
        verbose: bool = True,
    ) -> None:
        """Initialize params."""
        # validate that the query engines are of the right type
        if not isinstance(
            sql_query_tool.query_engine,
            (BaseSQLTableQueryEngine, NLSQLTableQueryEngine),
        ):
            raise ValueError(
                "sql_query_tool.query_engine must be an instance of "
                "BaseSQLTableQueryEngine or NLSQLTableQueryEngine"
            )
        if not isinstance(vector_query_tool.query_engine, RetrieverQueryEngine):
            raise ValueError(
                "vector_query_tool.query_engine must be an instance of "
                "RetrieverQueryEngine"
            )
        # if not isinstance(
        #     vector_query_tool.query_engine.retriever, VectorIndexAutoRetriever
        # ):
        #     raise ValueError(
        #         "vector_query_tool.query_engine.retriever must be an instance "
        #         "of VectorIndexAutoRetriever"
        #     )

        sql_vector_synthesis_prompt = (
            sql_vector_synthesis_prompt or DEFAULT_SQL_VECTOR_SYNTHESIS_PROMPT
        )
        SQLJoinQueryEngine.__init__( # This class also needs to be imported
            self,
            sql_query_tool,
            vector_query_tool,
            selector=selector,
            llm=llm,
            # service_context=service_context,
            sql_join_synthesis_prompt=sql_vector_synthesis_prompt,
            sql_augment_query_transform=sql_augment_query_transform,
            use_sql_join_synthesis=use_sql_vector_synthesis,
            callback_manager=callback_manager,
            verbose=verbose,
        )