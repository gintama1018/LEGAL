# 🏛️ Legal AI - Constitutional Rights Chatbot

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![Google Gemini](https://img.shields.io/badge/Gemini-2.5--Flash-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Legal AI** is an intelligent chatbot powered by Google's Gemini 2.5 Flash that provides instant legal assistance based on the Indian Constitution. Get constitutional guidance, draft legal documents, and understand your rights - all in a beautiful, minimal interface.

---

## ✨ Features

### 🤖 Three AI Modes

1. **⚡ Quick Mode** (Simple AI)
   - Fast, instant answers to legal questions
   - Constitutional article lookups
   - Basic rights information
   - ChatGPT-like streaming responses

2. **🤖 Multi-Agent Mode** (Advanced AI)
   - **4-Agent System** working in parallel:
     - 📋 **Classifier Agent**: Categorizes legal issues (Criminal, Civil, Cyber, etc.)
     - 🔍 **Retrieval Agent**: Finds relevant constitutional articles
     - 🧠 **Reasoning Agent**: Provides detailed legal analysis
     - 📝 **Drafting Agent**: Creates ready-to-file FIRs & complaints
   - Comprehensive legal analysis
   - Professional document generation

3. **📄 PDF Analysis Mode**
   - Upload legal documents (contracts, notices, etc.)
   - AI-powered document analysis
   - Extract key legal points
   - Identify risks and obligations

### 🎨 Modern UI/UX

- **Ultra-minimal design** inspired by ChatGPT and Notion
- **Real-time streaming responses** with character-by-character typing
- **Stop button** to pause AI mid-response
- **Free scrolling** - read while AI generates more content
- **Voice input support** with animated visualizer
- **Drag & drop** image upload
- **Dark theme** with legal-tech aesthetic (#0e0f11 background)
- **Icon-only mode selectors** for clean interface

### 🛡️ Safety Features

- **Emotional Safety Layer**: Detects crisis situations (abuse, self-harm, violence)
- **Emergency Response**: Provides helpline numbers for critical situations
- **Content Filtering**: Safe, professional responses

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/gintama1018/LEGAL.git
cd LEGAL
```

2. **Create virtual environment**
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install flask flask-cors google-generativeai pypdf2 python-dotenv
```

4. **Set up API Key**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

5. **Run the application**
```bash
python server.py
```

6. **Open browser**
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
LEGAL/
├── server.py                 # Flask backend server
├── index.html                # Frontend UI (single-page app)
├── legal_ai_gemini.py        # Simple AI mode & RAG system
├── multi_agent_system.py     # Multi-agent orchestration
├── emotional_safety.py       # Crisis detection & safety layer
├── pdf_analyzer.py           # PDF document analysis
├── chunker.py                # Constitutional text chunker
├── Constitution.txt          # Indian Constitution (full text)
├── chunks/                   # Pre-chunked constitutional articles (467 chunks)
│   ├── chunk_0.txt
│   ├── chunk_1.txt
│   └── ...
├── uploads/                  # User-uploaded PDFs (auto-created)
├── .env                      # Environment variables (API keys)
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

---

## 🔧 How It Works

### RAG Architecture (Retrieval-Augmented Generation)

1. **Constitution Chunking**: The entire Indian Constitution is split into 467 semantic chunks
2. **Query Processing**: User questions are analyzed for relevant keywords
3. **Chunk Retrieval**: Top 5 most relevant constitutional chunks are fetched
4. **Context Injection**: Retrieved chunks are passed to Gemini AI
5. **Response Generation**: AI generates accurate, context-aware answers

### Multi-Agent System

```
User Question
     ↓
[Classifier Agent] → Categorizes issue (Criminal/Civil/Cyber/etc.)
     ↓
[Retrieval Agent] → Fetches relevant constitutional articles
     ↓
[Reasoning Agent] → Provides legal analysis & user rights
     ↓
[Drafting Agent] → Creates ready-to-file legal documents
     ↓
Structured Response (4 sections with emoji headers)
```

### Streaming Technology

- **Server-Sent Events (SSE)** for real-time response streaming
- **Character-by-character rendering** with variable speed (3-15ms delays)
- **Natural typing effect** mimicking human conversation
- **Stop functionality** to pause generation at any point

---

## 🎯 Use Cases

### For Citizens
- ✅ Understand fundamental rights (Articles 14-32)
- ✅ Learn how to file FIR or complaint
- ✅ Get legal guidance on property disputes
- ✅ Understand employment laws
- ✅ Know your rights during arrest

### For Students
- ✅ Study constitutional law
- ✅ Learn legal document drafting
- ✅ Understand article interpretations
- ✅ Research legal precedents

### For Professionals
- ✅ Quick constitutional reference
- ✅ Draft legal notices
- ✅ Analyze legal documents
- ✅ Client consultation aid

---

## 📊 API Endpoints

### 1. **GET /** - Serve Frontend
Returns the `index.html` interface.

### 2. **POST /ask-stream** - Quick AI (Streaming)
```json
{
  "question": "What is Article 21?"
}
```
**Response**: SSE stream with real-time text generation

### 3. **POST /multi-agent** - Multi-Agent Analysis
```json
{
  "question": "My landlord is not returning my security deposit"
}
```
**Response**: Comprehensive 4-section analysis with classification, legal info, reasoning, and document draft

### 4. **POST /analyze-pdf** - PDF Analysis
```json
{
  "question": "What are the key obligations in this contract?",
  "pdf": "<file upload>"
}
```
**Response**: Detailed PDF analysis with legal insights

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
# Required
GEMINI_API_KEY=your_google_gemini_api_key_here

# Optional
PORT=5000
FLASK_ENV=development
```

---

## 🛠️ Configuration

### Modify AI Behavior

**Edit `legal_ai_gemini.py`** to adjust:
- Number of chunks retrieved (`n=5` in `pick_chunks_for_query()`)
- AI model version (default: `gemini-2.5-flash`)
- Response temperature and creativity

**Edit `multi_agent_system.py`** to customize:
- Agent prompts and instructions
- Document templates (FIR, Complaint formats)
- Classification categories
- Urgency levels

### UI Customization

**Edit `index.html`** CSS section:
```css
/* Background color */
body { background: #0e0f11; }

/* Accent color */
.send-btn { background: #3b82f6; }

/* Font family */
body { font-family: 'Inter', sans-serif; }
```

---

## 🐛 Troubleshooting

### Issue: 404 Error on http://127.0.0.1:5000
**Solution**: Check if `server.py` has the root route:
```python
@app.route("/")
def home():
    return send_file("index.html")
```

### Issue: API Key Error
**Solution**: Verify `.env` file exists with correct key:
```bash
cat .env  # Linux/Mac
type .env  # Windows
```

### Issue: Chunks Not Loading
**Solution**: Run `chunker.py` to regenerate chunks:
```bash
python chunker.py
```

### Issue: PDF Upload Fails
**Solution**: Ensure `uploads/` folder exists and has write permissions:
```bash
mkdir uploads
chmod 755 uploads  # Linux/Mac
```

---

## 📚 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Backend language |
| **Flask 3.1.2** | Web framework |
| **Google Gemini 2.5 Flash** | AI/LLM model |
| **Server-Sent Events (SSE)** | Real-time streaming |
| **PyPDF2** | PDF text extraction |
| **Flask-CORS** | Cross-origin requests |
| **Vanilla JS** | Frontend (no frameworks!) |
| **HTML5 + CSS3** | UI design |

---

## 🎨 Design Philosophy

- **Minimal is more**: Remove unnecessary elements, focus on content
- **Instant feedback**: Streaming responses for real-time interaction
- **User control**: Stop button, free scrolling, no forced auto-scroll
- **Professional aesthetic**: Legal-tech dark theme, clean typography
- **Accessibility first**: Clear contrast, readable fonts, intuitive icons

---

## 🚧 Roadmap

- [ ] Add more Indian laws (IPC, CrPC, CPC sections)
- [ ] Voice output (text-to-speech for responses)
- [ ] Multi-language support (Hindi, Tamil, Bengali, etc.)
- [ ] Case law database integration
- [ ] Lawyer directory & consultation booking
- [ ] User authentication & history
- [ ] Mobile app (React Native)
- [ ] WhatsApp bot integration
- [ ] Legal document templates library

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python
- Use meaningful variable names
- Add comments for complex logic
- Test before committing

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Indian Constitution** - Public domain text from [india.gov.in](https://www.india.gov.in/)
- **Google Gemini** - AI model powering the chatbot
- **Flask** - Lightweight web framework
- **Open Source Community** - For inspiration and tools

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/gintama1018/LEGAL/issues)
- **Email**: [Your Email]
- **Discussions**: [GitHub Discussions](https://github.com/gintama1018/LEGAL/discussions)

---

## ⚖️ Legal Disclaimer

This chatbot provides **general legal information only** and is not a substitute for professional legal advice. For serious legal matters, always consult a qualified lawyer. The creators are not responsible for any actions taken based on information provided by this AI.

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=gintama1018/LEGAL&type=Date)](https://star-history.com/#gintama1018/LEGAL&Date)

---

**Made with ❤️ for accessible legal justice in India**

[⬆ Back to Top](#-legal-ai---constitutional-rights-chatbot)
