from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize ChatGroq with API key from .env
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- WIKIPEDIA TOOL ----------------

wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# ---------------- DUCKDUCKGO SEARCH TOOL ----------------

ddg_search = DuckDuckGoSearchRun()

# ---------------- CALCULATOR TOOL ----------------

def calculator_tool(query: str):
    try:
        return str(eval(query))
    except:
        return "Math error"

# ---------------- RAG SETUP ----------------

loader = TextLoader("notes.txt")
documents = loader.load()

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(split_docs, embeddings)

# ---------------- RAG FUNCTION ----------------

def rag_search(query):
    docs = db.similarity_search(query, k=2)
    context = "\n".join([d.page_content for d in docs])
    prompt = f"Answer using this context:\n{context}\n\nQuestion:{query}"
    result = llm.invoke(prompt)
    return result.content if hasattr(result, 'content') else str(result)

# --------------- SIMPLE AGENT ----------------

available_tools = {
    "Wikipedia": wiki.run,
    "DuckDuckGo": ddg_search.run,
    "Calculator": calculator_tool,
    "NotesSearch": rag_search
}

def process_query(query):
    """Simple agent that uses LLM to decide which tool to use"""
    
    # Create a prompt for the LLM to decide which tool to use
    tool_descriptions = "\n".join([
        f"- {name}: {description}" 
        for name, description in [
            ("Wikipedia", "Search Wikipedia for information"),
            ("DuckDuckGo", "Search the web using DuckDuckGo"),
            ("Calculator", "Perform mathematical calculations"),
            ("NotesSearch", "Search the local notes database using RAG")
        ]
    ])
    
    decision_prompt = f"""You have access to these tools:
{tool_descriptions}

User query: {query}

Decide which tool would be most helpful. Respond with ONLY the tool name, nothing else.
If none are suitable, respond with 'None'."""
    
    # Get the decision
    response = llm.invoke(decision_prompt)
    tool_choice = response.content.strip() if hasattr(response, 'content') else str(response).strip()
    
    # Execute the chosen tool
    if tool_choice == "Calculator":
        try:
            # For calculator, ask the LLM to extract the math expression first
            extract_prompt = f"Extract only the mathematical expression from this query: '{query}'. Respond with ONLY the expression, nothing else."
            expr_response = llm.invoke(extract_prompt)
            expression = expr_response.content.strip() if hasattr(expr_response, 'content') else str(expr_response).strip()
            result = calculator_tool(expression)
            return result
        except Exception as e:
            return f"Error with Calculator: {str(e)}"
    elif tool_choice in available_tools:
        try:
            result = available_tools[tool_choice](query)
            return result
        except Exception as e:
            return f"Error with {tool_choice}: {str(e)}"
    else:
        # If no specific tool, just answer directly with LLM
        direct_response = llm.invoke(query)
        return direct_response.content if hasattr(direct_response, 'content') else str(direct_response)

print("\n🤖 Smart Student Agent Ready (type exit to stop)\n")

chat_history = []

while True:
    q = input("\nYou: ")
    if q.lower() == "exit":
        break

    res = process_query(q)
    chat_history.append((q, res))
    print("AI:", res)
