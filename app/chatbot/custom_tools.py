from langchain.memory import ConversationBufferMemory
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import Tool
from langchain_core.tools import BaseTool
from .tools_functions import analyze_all_tables
from typing import Type
import sqlite3
from langchain.schema import HumanMessage, SystemMessage
from langchain.schema import HumanMessage, SystemMessage
from config import model


DATABASE_PATH = "app\database\studytime.sqlite3"

memory = ConversationBufferMemory(memory_key="chat_history")

class QueryDataInput(BaseModel):
    query: str = Field(..., description="SQLite3 query (sql)")

    class Config:
        arbitrary_types_allowed = True

class QueryData(BaseTool):
    name: str = "query_data"    
    args_schema: Type[BaseModel] = QueryDataInput
    description: str =  f"""A SQLite query executor. Useful for when you need to answer
    about user's tasks and notes. Input should be a SQLite3 command."""          

    def _run(self, query) -> tuple:
        try:
            with sqlite3.connect(DATABASE_PATH) as conn:
                cursor = conn.cursor()

                # Execute the query
                cursor.execute(query)
                results = cursor.fetchall()

                # Get the last row id
                last_row_id = cursor.lastrowid

                return f"Results: {results}, Last row id:{last_row_id}"
        except sqlite3.Error as e:
            return None, f"Query failed with error: {e}"


class DatabaseInfo(BaseTool):
    name: str = "database_info"
    description: str = f"""Retrieves information about a database. Useful
    when you need to answer about user's tasks or notes. No input needed.
    Contains all the relevant structure about a data base (tables, columns,
    additional information)."""
    
    def _run(self, _=None) -> str:
        try:
            database_schema_string = analyze_all_tables()
            memory.chat_memory.add_ai_message(database_schema_string)
            return database_schema_string
        except Exception as e:
            return f"Error occurred while retrieving database information: {e}"

class RespondInput(BaseModel):
    user_message: str = Field(..., description="User message")

class Respond(BaseTool):
    name: str = "respond"
    args_schema: Type[BaseModel] = RespondInput
    description: str = f"""This function is useful to respond the user on topics 
                        not related to databases."""

    def _run(self, user_message) -> str:
        try:
            messages = [
            SystemMessage(
                content="You are a helpful assistant. You answer in the user's language."
            ),
            HumanMessage(
                content=user_message
            ),
            ]
            response = model(messages)
            memory.chat_memory.add_ai_message(response)
            return response
        except Exception as e:
            return f"Error occured while responding user message: {e}"
        
db_info = DatabaseInfo()
db_query = QueryData()
respond = Respond()

tools = [
    Tool(
        name="DatabaseInfo",
        func=db_info.run,
        description="Useful to understand the structure of an sqlite database, such as table names and columns. Takes no arguments."
    ),
    Tool(
        name="QueryData",
        func=db_query.run,
        description="Useful to query data from a structural database. Takes only the SQL query. Adjust the user input so that it matches the database dtypes."
    ),
    # Tool(
    #     name="respond",
    #     func=respond.run,
    #     description="Useful to respond the user when the message is not related to databases."
    # )
]

