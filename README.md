🩺 Medical AI Chatbot — RAG + Pinecone + Llama 3.3
<div align="center">












🚀 AI-Powered Medical Assistant with RAG Architecture

Production-style multilingual medical chatbot powered by:

🧠 Llama 3.3 (Groq)
📚 Pinecone Vector Database
🔍 Retrieval-Augmented Generation (RAG)
🎙 Voice Recognition
🌐 Multi-language Support
🚨 Emergency Detection
🩺 AI Symptom Checker

</div>
📌 Overview

This project is an advanced AI Medical Assistant capable of answering medical-related queries using:

Large Language Models (LLM)
Retrieval-Augmented Generation (RAG)
Vector Search with Pinecone
Medical Knowledge Retrieval
Multi-language conversation
AI Symptom Analysis

The chatbot supports:

✅ English
✅ বাংলা (Bengali)
✅ हिन्दी (Hindi)

✨ Key Features
🧠 AI Medical Chatbot

Users can ask medical questions naturally.

Example Queries
I have fever and headache

আমার জ্বর এবং মাথা ব্যথা

मुझे बुखार और सिरदर्द है
🔍 RAG Architecture (Retrieval-Augmented Generation)

Instead of relying only on the LLM, the chatbot first retrieves relevant medical information from Pinecone.

Workflow
User Question
      ↓
Text Embedding
      ↓
Pinecone Vector Search
      ↓
Relevant Medical Chunks
      ↓
LLM Context Injection
      ↓
AI Response Generation
Benefits

✅ Higher accuracy
✅ Reduced hallucination
✅ Better context awareness
✅ Evidence-based answers

📚 Pinecone Vector Database

Medical documents are converted into embeddings and stored in Pinecone.

Used For
Semantic Search
Similarity Matching
Context Retrieval
Medical Knowledge Base
🌐 Multi-language Support

The chatbot automatically understands:

Language	Support
English	✅
Bengali	✅
Hindi	✅
Example
User: আমার জ্বর
Bot: আপনার জ্বরের কারণ হতে পারে...
🎙 Voice Recognition

Supports speech-to-text using the browser SpeechRecognition API.

Supported Languages
English
Bengali
Hindi
🔊 Text-to-Speech (TTS)

The AI can read responses aloud using:

speechSynthesis
🩺 AI Symptom Checker

Advanced AI-powered symptom analysis system.

Features

✅ Disease Prediction
✅ Severity Detection
✅ Recommended Actions
✅ Emergency Identification

🚨 Emergency Detection System

Detects dangerous medical conditions instantly.

Detectable Emergencies
Chest pain
Severe bleeding
Heart attack symptoms
Breathing problems
Stroke symptoms
Loss of consciousness
Emergency Actions

✅ Popup Alert
✅ Emergency Call Buttons
✅ Immediate Warning

📄 PDF Export

Users can export the entire chat conversation as a PDF document.

Includes:

User questions
AI responses
Medical summaries
Disease images
Timestamps

└──────────────────────┘
🧱 Tech Stack
Technology	Purpose
Flask	Backend Framework
Pinecone	Vector Database
LangChain	RAG Pipeline
Groq	LLM Inference
Llama 3.3	AI Model
HuggingFace	Embeddings
Bootstrap	UI Framework
jQuery	AJAX Requests
jsPDF	PDF Export
SpeechRecognition API	Voice Input

⚙️ Installation Guide
1️⃣ Clone Repository
git clone https://github.com/A-tri-j/Medical-Chatbottt

cd Medical-Chatbottt
2️⃣ Create Virtual Environment
Windows
python -m venv venv

venv\Scripts\activate
Linux / Mac
python3 -m venv venv

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment Variables

Create a .env file.

PINECONE_API_KEY=your_pinecone_api_key

OPENAI_API_KEY=your_groq_api_key

SECRET_KEY=your_secret_key
5️⃣ Run Application
python app.py
🌐 Open in Browser
http://localhost:8080
🔍 RAG Pipeline Explained
Step-by-Step Flow
User Question
      ↓
Convert into Embedding Vector
      ↓
Search Similar Chunks in Pinecone
      ↓
Retrieve Top Medical Documents
      ↓
Inject Context into LLM Prompt
      ↓
Generate Final Medical Response
🧠 Embedding Model
embeddings = download_hugging_face_embeddings()

Converts text into numerical vectors.

Used for:

Similarity Search
Semantic Retrieval
Context Matching
📚 Pinecone Retrieval
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k":3}
)

Returns the most relevant medical chunks.

🤖 LLM Model
ChatGroq(
    model_name="llama-3.3-70b-versatile"
)

Used for:

Medical reasoning
Response generation
Symptom analysis
Multi-language support
🩺 Symptom Checker Workflow
User Symptoms
      ↓
LLM Medical Analysis
      ↓
Disease Prediction
      ↓
Severity Classification
      ↓
Recommended Actions
      ↓
Emergency Detection
🚨 Emergency Detection Workflow
User Message
      ↓
Keyword Detection
      ↓
Emergency Validation
      ↓
Popup Alert
      ↓
Emergency Contacts
📞 Emergency Numbers
Service	Number
Ambulance	108
Emergency	112
Health Helpline	102
📈 Future Improvements
✅ Pinecone-based Symptom Checker

Current version:

Symptoms → Direct LLM Analysis

Future architecture:

Symptoms
    ↓
Embedding Generation
    ↓
Pinecone Vector Search
    ↓
Medical Retrieval
    ↓
Evidence-based AI Analysis
Benefits

✅ More accurate diagnosis
✅ Reduced hallucination
✅ Better medical grounding
✅ Faster retrieval

🚀 Planned Features
AI Triage System
Doctor Recommendation
OCR Prescription Reader
Image-based Disease Detection
Medical Confidence Score
Hybrid Search (BM25 + Vector)
Medical Report Generation
Patient Dashboard
Authentication System
MongoDB Chat Storage
🔒 Security Features

✅ Rate Limiting
✅ Session Isolation
✅ Input Validation
✅ Request Throttling
✅ Secure Environment Variables

⚠️ Disclaimer

This project is intended for:

✅ Educational Purposes
✅ Research & Learning
✅ AI Demonstration

It is NOT a substitute for:

❌ Professional medical advice
❌ Diagnosis
❌ Clinical treatment

Always consult a licensed healthcare professional.

In Emergencies Call
108 / 112
👨‍💻 Author
Atrij Ghosh
Connect
GitHub: A-tri-j
⭐ Support the Project

If you like this project:

⭐ Star the repository
🍴 Fork the project
🧠 Contribute improvements

📜 License
MIT License
<div align="center">
❤️ Built with AI + RAG + Pinecone
</div>