from rag import db_chain, answer_query_nl_to_sql  # db_chain is from rag.py
from vector_store import vector_store  # your vector store setup
import asyncio
import re  # for regex matching

# Intent keywords dictionary (add more intents as needed)
intents = {
    "assets_under_maintenance": ["under maintenance", "currently under maintenance"],
    "last_service_date": ["last service", "recent service", "last maintenance"],
    "employee_designation": ["designation", "role", "position"],  # new intent
}

async def get_relevant_docs(message: str):
    loop = asyncio.get_event_loop()
    docs = await loop.run_in_executor(None, vector_store.similarity_search, message, 3)
    return docs

async def match_intent(message: str):
    lowered = message.lower()
    for intent, keywords in intents.items():
        if any(keyword in lowered for keyword in keywords):
            return intent
    return None

def extract_asset_tag(message: str):
    # Regex to find asset tags like GNT-243 or similar pattern
    match = re.search(r'\b[A-Z]{2,}-\d{1,}\b', message)
    if match:
        return match.group(0)
    return None

def extract_employee_name(message: str):
    # Simple regex to extract name after keywords like "designation of"
    match = re.search(r'designation of ([a-zA-Z ]+)', message.lower())
    if match:
        name = match.group(1).strip()
        # Capitalize each word in name (simple title-case)
        return " ".join(w.capitalize() for w in name.split())
    return None

async def answer_query_from_intent(intent: str, message: str):
    loop = asyncio.get_event_loop()

    if intent == "assets_under_maintenance":
        query = """
        SELECT asset_tag, name, location
        FROM Assets
        WHERE status = 'Under Maintenance';
        """
        result = await loop.run_in_executor(None, db_chain.run, query)
        if not result or "No results" in result:
            return "No assets are currently under maintenance."
        return result

    elif intent == "last_service_date":
        asset_tag = extract_asset_tag(message)
        if not asset_tag:
            return "I couldn't find an asset tag in your message. Please specify it like 'GNT-243'."
        query = f"""
        SELECT v.service_type, v.last_service_date
        FROM Asset_Vendor_Link v
        JOIN Assets a ON v.asset_id = a.id
        WHERE a.asset_tag = '{asset_tag}';
        """
        result = await loop.run_in_executor(None, db_chain.run, query)
        if not result or "No results" in result:
            return f"No service information found for asset '{asset_tag}'."
        return result

    elif intent == "employee_designation":
        employee_name = extract_employee_name(message)
        if not employee_name:
            return "Please specify the employee name for the designation query."
        query = f"""
        SELECT designation FROM Employees
        WHERE name = '{employee_name}';
        """
        result = await loop.run_in_executor(None, db_chain.run, query)
        if not result or "No results" in result:
            return f"No designation found for employee '{employee_name}'."
        return result

    return "Sorry, I couldn't find relevant information for your query."

async def process_message(message: str):
    # Greetings
    if message.lower() in ["hi", "hello", "hey"]:
        return "Hello!👋🏻 How can I assist you with company assets today?🤩"
    if message.lower() in ["bye", "goodbye", "Bye", "Tata"]:
        return "Goodbye! Have a great day!🥰"
    if message.lower() in ["Thanks", "Thank you", "thanks", "thank you"]:
        return "You're welcome! If you have any more questions, feel free to ask.🥰"
    if message.lower() in ["Hi, how are you?", "Hello, how are you?"]:
        return "Hey there! I'm fine, thanks for asking. What can I do for you?🥰" 
    # Match intents first
    intent = await match_intent(message)
    if intent:
        return await answer_query_from_intent(intent, message)

    # Try NL-to-SQL (RAG) next
    answer = await answer_query_nl_to_sql(message)
    if answer and answer.strip() != "" and "No results" not in answer:
        return answer

    # Finally fallback to vector store search
    relevant_docs = await get_relevant_docs(message)
    if relevant_docs:
        return f"I found some related information: {', '.join([doc.page_content for doc in relevant_docs])}"

    return "Sorry, I couldn't find relevant information for your query."






