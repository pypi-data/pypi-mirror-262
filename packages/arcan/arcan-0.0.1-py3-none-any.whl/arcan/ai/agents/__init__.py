# %%
import ast
import asyncio
import os
import pickle
import weakref
from datetime import datetime
from tempfile import TemporaryDirectory
from typing import Dict

from fastapi.responses import StreamingResponse
from langchain.agents import AgentExecutor, load_tools
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits import FileManagementToolkit, SQLDatabaseToolkit
from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy.dialects.postgresql import insert

from arcan.ai.agents.helpers import AsyncIteratorCallbackHandler
from arcan.ai.llm import LLM
from arcan.ai.prompts import vortex_prompt
from arcan.ai.router import semantic_layer
from arcan.ai.tools import tools as spells
from arcan.api.datamodels.chat_history import ChatsHistory
from arcan.api.datamodels.conversation import Conversation


class ArcanAgent:
    """
    Represents a Arcan Agent that interacts with the user and provides responses using OpenAI tools.

    Attributes:
        llm (LLM): The Language Model Manager used by the agent.
        tools (list): The list of tools used by the agent.
        hub_prompt (str): The prompt for the OpenAI tools agent.
        agent_type (str): The type of the agent.
        chat_history (list): The chat history of the agent.
        llm_with_tools: The Language Model Manager with the tools bound.
        prompt: The chat prompt template for the agent.
        agent: The agent pipeline.
        agent_executor: The executor for the agent.
        user_id: The unique identifier for the user.
        verbose: A boolean indicating whether to print verbose output.

    Methods:
        get_response: Gets the response from the agent given user input.

    """

    def __init__(
        self,
        llm: LLM = LLM().llm,
        tools: list = spells,
        hub_prompt: str = "broomva/arcan",
        agent_type="arcan_spells_agent",
        context: list = [],  # represents the chat history, can be pulled from a db
        user_id: str = None,
        verbose: bool = False,
    ):
        self.llm: LLM = llm
        self.tools: list = tools
        self.hub_prompt: str = hub_prompt
        self.agent_type: str = agent_type
        self.chat_history: list = context
        self.user_id: str = user_id
        self.verbose: bool = verbose

        self.db = SQLDatabase.from_uri(os.environ.get("SQLALCHEMY_URL"))
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.context = self.toolkit.get_context()
        self.prompt = vortex_prompt.partial(**self.context)
        self.sql_tools = self.toolkit.get_tools()
        self.working_directory = TemporaryDirectory()
        self.file_system_tools = FileManagementToolkit(
            root_dir=str(self.working_directory.name)
        ).get_tools()
        self.parser = OpenAIToolsAgentOutputParser()
        self.bare_tools = load_tools(
            [
                "llm-math",
                # "human",
                # "wolfram-alpha"
            ],
            llm=self.llm,
        )
        self.agent_tools = (
            self.tools + self.bare_tools  # + self.sql_tools + self.file_system_tools
        )
        self.llm_with_tools = self.llm.bind_tools(self.agent_tools)
        self.agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
            }
            | self.prompt
            | self.llm_with_tools
            | self.parser
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent, tools=self.agent_tools, verbose=self.verbose
        )

    def get_response(self, user_content: str):
        """
        Gets the response from the agent given user input.

        Args:
            user_content (str): The user input.

        Returns:
            str: The response from the agent.

        """
        routed_content = semantic_layer(query=user_content, user_id=self.user_id)
        response = self.agent_executor.invoke(
            {"input": routed_content, "chat_history": self.chat_history}
        )
        self.chat_history.extend(
            [
                HumanMessage(content=user_content),
                AIMessage(content=response["output"]),
            ]
        )
        return response["output"]


class ArcanSession:
    def __init__(self, session_factory):
        """
        Initializes a new instance of the ArcanSession class.

        :param session_factory: A callable that returns a new SQLAlchemy Session instance when called.
        """
        self.session_factory = session_factory
        self.agents: Dict[str, weakref.ref] = weakref.WeakValueDictionary()

    def get_or_create_agent(
        self, user_id: str, provided_agent: ArcanAgent = None
    ) -> ArcanAgent:
        """
        Retrieves or creates a ArcanAgent for a given user_id.

        :param user_id: The unique identifier for the user.
        :return: An instance of ArcanAgent.
        """
        if provided_agent is not None:
            provided_agent.user_id = user_id
            self.agents[user_id] = provided_agent
            return provided_agent

        agent = self.agents.get(user_id)
        chat_history = []

        # Obtain a new database session
        try:
            chat_history = self.get_chat_history(user_id)
        except Exception as e:
            print(f"Error getting chat history for {user_id}: {e}")

        if agent is not None and chat_history:
            print(f"Using existing agent {agent}")
        elif agent is None and chat_history:
            print(f"Using reloaded agent with history {chat_history}")
            agent = ArcanAgent(
                context=chat_history, user_id=user_id
            )  # Initialize with chat history
        elif agent is None and not chat_history:
            print("Using a new agent")
            agent = ArcanAgent(user_id=user_id)  # Initialize without chat history

        self.agents[user_id] = agent
        return agent

    def store_message(self, user_id: str, body: str, response: str):
        """
        Stores a message in the database.

        :param user_id: The unique identifier for the user.
        :param Body: The body of the message sent by the user.
        :param response: The response generated by the system.
        """
        with self.session_factory as db_session:
            conversation = Conversation(sender=user_id, message=body, response=response)
            db_session.add(conversation)
            db_session.commit()
            print(f"Conversation #{conversation.id} stored in database")

    def store_chat_history(self, user_id, agent_history):
        """
        Stores or updates the chat history for a user in the database.

        :param user_id: The unique identifier for the user.
        :param agent_history: The chat history to be stored.
        """
        history = pickle.dumps(agent_history)
        # Upsert statement
        stmt = (
            insert(ChatsHistory)
            .values(
                sender=user_id,
                history=str(history),
                updated_at=datetime.utcnow(),  # Explicitly set updated_at on insert
            )
            .on_conflict_do_update(
                index_elements=["sender"],  # Specify the conflict target
                set_={
                    "history": str(history),  # Update the history field upon conflict
                    "updated_at": datetime.utcnow(),  # Update the updated_at field upon conflict
                },
            )
        )
        # Execute the upsert
        with self.session_factory as db:
            db.execute(stmt)
            db.commit()
            print(f"Upsert chat history for user {user_id} with statement {stmt}")

    def get_chat_history(self, user_id: str) -> list:
        """
        Retrieves the chat history for a user from the database.

        :param db_session: The SQLAlchemy Session instance.
        :param user_id: The unique identifier for the user.
        :return: A list representing the chat history.
        """
        with self.session_factory as db_session:
            history = (
                db_session.query(ChatsHistory)
                .filter(ChatsHistory.sender == user_id)
                .order_by(ChatsHistory.updated_at.asc())
                .all()
            ) or []
        if not history:
            return []
        chat_history = history[0].history
        loaded = pickle.loads(ast.literal_eval(chat_history))
        return loaded


# %%
#

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel

from arcan.ai.parser import ArcanOutputParser


class ArcanConversationAgent:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.llm = LLM().llm
        self.embeddings = OpenAIEmbeddings()
        self.memory = ConversationBufferMemory(  # ConversationBufferWindowMemory k=10
            memory_key="chat_history", return_messages=True, output_key="output"
        )
        self.tools = load_tools(["llm-math"], llm=self.llm)
        self.agent = initialize_agent(
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
            memory=self.memory,
            return_intermediate_steps=True,
            agent_kwargs={"output_parser": ArcanOutputParser()},
            # output_parser=ArcanOutputParser
        )


class Query(BaseModel):
    text: str


async def run_call(query: str, stream_it: AsyncIteratorCallbackHandler, agent):
    try:
        # assign callback handler
        agent.agent.llm_chain.llm.callbacks = [stream_it]
        # now query
        await agent.acall(inputs={"input": query})
    except Exception as e:
        print(f"run_call {e}")
        raise (e)


async def create_gen(query: str, stream_it: AsyncIteratorCallbackHandler, agent):
    try:
        task = asyncio.create_task(run_call(query, stream_it, agent))
        async for token in stream_it.aiter():
            yield token
        await task
    except Exception as e:
        print(f"Error: {e}")
        yield str(e)
        raise e


async def agent_chat(text: str, agent):  # query: Query = Body(...),):
    stream_it = AsyncIteratorCallbackHandler()  # AsyncCallbackHandler()
    query = Query(text=text)
    try:
        gen = create_gen(query.text, stream_it, agent)
    except Exception as e:
        raise (e)
    return StreamingResponse(gen, media_type="text/event-stream")
