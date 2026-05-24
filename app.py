from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from collections import defaultdict

from src.helper import download_hugging_face_embeddings
from src.prompt import *

from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY     = os.environ.get("OPENAI_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"]     = GROQ_API_KEY

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medical-chatbot-secret-2024")

embeddings  = download_hugging_face_embeddings()
index_name  = "medical-chatbot"
docsearch   = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
retriever   = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
chatModel   = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("system", "Previous conversation for context:\n{chat_history}"),
    ("human", "{input}"),
])
question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# ── In-memory stores ──
chat_histories = {}       # sid -> list of {role, text, time}
feedback_logs  = []
MAX_HISTORY    = 10

# ── Rate limiting store ──
# ip -> {"count": int, "window_start": float}
rate_limit_store = defaultdict(lambda: {"count": 0, "window_start": time.time()})
RATE_LIMIT_MAX    = 10    # max requests
RATE_LIMIT_WINDOW = 60    # per 60 seconds


def get_session_id():
    if "sid" not in session:
        import uuid
        session["sid"] = str(uuid.uuid4())
    return session["sid"]


def get_history_text(history_list):
    if not history_list:
        return "No previous conversation."
    lines = []
    for entry in history_list[-MAX_HISTORY:]:
        role = "User" if entry["role"] == "user" else "Assistant"
        lines.append(f"{role}: {entry['text']}")
    return "\n".join(lines)


def check_rate_limit(ip):
    """Returns (allowed: bool, remaining: int, retry_after: int)"""
    now  = time.time()
    data = rate_limit_store[ip]
    # Reset window if expired
    if now - data["window_start"] > RATE_LIMIT_WINDOW:
        data["count"]        = 0
        data["window_start"] = now
    if data["count"] >= RATE_LIMIT_MAX:
        retry_after = int(RATE_LIMIT_WINDOW - (now - data["window_start"])) + 1
        return False, 0, retry_after
    data["count"] += 1
    remaining = RATE_LIMIT_MAX - data["count"]
    return True, remaining, 0


# ── Routes ──

@app.route("/")
def index():
    get_session_id()
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    # Rate limiting by IP
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    allowed, remaining, retry_after = check_rate_limit(ip)
    if not allowed:
        return jsonify({
            "error": "rate_limited",
            "message": f"Too many requests. Please wait {retry_after} seconds.",
            "retry_after": retry_after
        }), 429

    msg = request.form["msg"]
    sid = get_session_id()
    print("User Input:", msg)

    if sid not in chat_histories:
        chat_histories[sid] = []

    history_text = get_history_text(chat_histories[sid])
    response = rag_chain.invoke({"input": msg, "chat_history": history_text})
    answer   = response["answer"]
    print("Response:", answer)

    ts = datetime.now().strftime("%H:%M")
    chat_histories[sid].append({"role": "user", "text": msg,    "time": ts})
    chat_histories[sid].append({"role": "bot",  "text": answer, "time": ts})
    if len(chat_histories[sid]) > MAX_HISTORY * 2:
        chat_histories[sid] = chat_histories[sid][-(MAX_HISTORY * 2):]

    return jsonify({"answer": answer, "remaining": remaining})


@app.route("/history", methods=["GET"])
def get_history():
    sid     = get_session_id()
    history = chat_histories.get(sid, [])
    pairs   = []
    i = 0
    while i < len(history) - 1:
        if history[i]["role"] == "user" and history[i+1]["role"] == "bot":
            pairs.append({
                "question": history[i]["text"],
                "answer":   history[i+1]["text"],
                "time":     history[i]["time"],
            })
            i += 2
        else:
            i += 1
    return jsonify({"history": pairs})


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    sid  = get_session_id()
    feedback_logs.append({
        "sid":      sid,
        "question": data.get("question", ""),
        "answer":   data.get("answer",   ""),
        "vote":     data.get("vote", ""),
        "time":     datetime.now().isoformat(),
    })
    print(f"Feedback [{data.get('vote')}]: {data.get('question','')[:60]}")
    return jsonify({"status": "ok"})


@app.route("/clear", methods=["POST"])
def clear_history():
    sid = get_session_id()
    chat_histories[sid] = []
    return jsonify({"status": "cleared"})


@app.route("/symptom-check", methods=["POST"])
def symptom_check():
    """Takes a list of symptoms, returns possible diseases via LLM."""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    allowed, _, retry_after = check_rate_limit(ip)
    if not allowed:
        return jsonify({"error": "rate_limited", "retry_after": retry_after}), 429

    data     = request.get_json()
    symptoms = data.get("symptoms", "")

    sc_prompt = (
        "You are a medical assistant. Based on these symptoms, suggest the top 3 most likely "
        "conditions/diseases. For each: give the name, a 1-line description, severity level "
        "(Mild/Moderate/Severe), and 2 recommended actions. "
        "If the symptoms suggest a medical emergency, start your response with 'EMERGENCY:'. "
        "Format as JSON array: "
        '[{"name":"...","description":"...","severity":"...","actions":["...","..."]}]. '
        "Reply in the same language as the symptoms.\n\nSymptoms: " + symptoms
    )

    try:
        result = chatModel.invoke(sc_prompt)
        raw    = result.content.strip()
        # Try to parse JSON
        import json, re
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if match:
            diseases = json.loads(match.group())
        else:
            diseases = []
        is_emergency = raw.upper().startswith("EMERGENCY")
        return jsonify({"diseases": diseases, "emergency": is_emergency, "raw": raw})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)