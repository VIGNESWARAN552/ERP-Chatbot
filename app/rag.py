from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

# Replace user/password/host/dbname with your actual credentials
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine and Langchain DB wrapper
engine = create_engine(DATABASE_URL)
db = SQLDatabase(engine)

# Setup OpenAI GPT-4 model
llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# Create the Langchain SQLDatabaseChain
db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)

# Async wrapper to run blocking db_chain.run()
import asyncio
async def answer_query_nl_to_sql(nl_query: str):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, db_chain.run, nl_query)
    return result

print("rag.py loaded successfully")


