# 🤖 Smart Student Agent

A powerful AI agent built with **LangChain** that combines multiple tools and Retrieval-Augmented Generation (RAG) to provide intelligent responses to user queries.

## 📋 Features

- **Multi-Tool Agent**: Intelligently selects and uses the best tool for each query
- **Two LangChain Community Tools**:
  - 📖 **Wikipedia Search**: Access Wikipedia for factual information
  - 🌐 **DuckDuckGo Search**: Search the web for real-time information
- **RAG System**: Retrieval-Augmented Generation using local notes for context-aware answers
- **Calculator Tool**: Perform mathematical calculations
- **LLM Integration**: Uses Groq API with Llama 3.3-70b model for intelligent reasoning
- **Chat History**: Maintains conversation history for multi-turn interactions

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Groq API key (get from [Groq Console](https://console.groq.com))

### Installation

1. **Clone or download the project**
   ```bash
   cd /Users/sivakumar/proj1
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   
   Create a `.env` file in the project root with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. **Prepare your notes (optional)**
   
   Create a `notes.txt` file with any notes you want the agent to have access to through the RAG system.

### Running the Agent

```bash
python3 main.py
```

The agent will start in interactive mode:
```
🤖 Smart Student Agent Ready (type exit to stop)

You: [type your question here]
```

## 🧪 Testing

### Test Wikipedia Tool
```bash
cd /Users/sivakumar/proj1 && python3 main.py << 'EOF'
Tell me about Albert Einstein
exit
EOF
```

### Test DuckDuckGo Search
```bash
cd /Users/sivakumar/proj1 && python3 main.py << 'EOF'
What are the latest AI developments in 2026?
exit
EOF
```

### Test Calculator
```bash
cd /Users/sivakumar/proj1 && python3 main.py << 'EOF'
What is 100 * 50?
exit
EOF
```

### Test RAG (Local Notes)
```bash
cd /Users/sivakumar/proj1 && python3 main.py << 'EOF'
What is in my notes?
exit
EOF
```

## 📁 Project Structure

```
proj1/
├── main.py                 # Main agent implementation
├── notes.txt              # Local knowledge base for RAG
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── README.md             # This file
└── venv/                 # Virtual environment
```

## 🔧 Configuration

### Groq Model
The agent uses `llama-3.3-70b-versatile` model. To change it, edit line 16 in `main.py`:
```python
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",  # Change model here
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
```

### RAG Settings
Customize the RAG behavior in the RAG SETUP section (lines 38-44):
- **chunk_size**: Size of document chunks (default: 500)
- **chunk_overlap**: Overlap between chunks (default: 50)
- **model_name**: HuggingFace embedding model (default: "all-MiniLM-L6-v2")
- **k**: Number of similar documents to retrieve (default: 2)

## 📦 Dependencies

Main packages:
- **langchain**: Core LLM framework
- **langchain-community**: Community tools (Wikipedia, DuckDuckGo)
- **langchain-groq**: Groq API integration
- **langchain-huggingface**: HuggingFace embeddings
- **faiss-cpu**: Vector database for RAG
- **sentence-transformers**: Embedding models
- **python-dotenv**: Environment variable management
- **wikipedia**: Wikipedia API
- **ddgs**: DuckDuckGo search

See `requirements.txt` for complete list with versions.

## 🎯 How It Works

1. **User Query**: You provide a question or command
2. **Tool Selection**: The agent uses the LLM to decide which tool is best:
   - Wikipedia for general knowledge
   - DuckDuckGo for web search
   - Calculator for math
   - RAG for local notes
3. **Tool Execution**: The selected tool processes the query
4. **Response**: The agent returns the tool's output
5. **History**: The interaction is saved for context

## 🔐 Security Notes

- Keep your `.env` file secure and never commit it to version control
- Never share your Groq API key publicly
- Add `.env` to `.gitignore` if using git

## 🤝 Contributing

Feel free to extend the agent with:
- Additional tools from LangChain Community
- Custom tools
- Different LLM providers
- Enhanced RAG capabilities

## 📝 License

This project is open source and available for educational purposes.

## 🆘 Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: API Key error
**Solution**: Verify your `.env` file has the correct `GROQ_API_KEY`

### Issue: RAG not finding notes
**Solution**: Ensure `notes.txt` exists in the project root and contains text

### Issue: DuckDuckGo search fails
**Solution**: Make sure you have internet connection and `ddgs` package is installed
```bash
pip install -U ddgs
```

## 📞 Support

For issues or questions about LangChain, visit:
- [LangChain Documentation](https://python.langchain.com/)
- [Groq Console](https://console.groq.com/)
- [DuckDuckGo Search](https://duckduckgo.com/)

---

**Happy querying! 🚀**
