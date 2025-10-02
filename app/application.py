from flask import Flask, render_template, request, session, redirect, url_for
from app.components.retriever import create_qa_chain
from app.common.logger import get_logger
from dotenv import load_dotenv
import os

logger = get_logger(__name__)

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])

def index():
    if "messages" not in session:
        session["messages"] = []
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form.get("prompt")
        if not user_input:
            return render_template("index.html", error="Please enter a question")
        
        session["messages"].append({"role": "user", "content": user_input})
        qa_chain = create_qa_chain()
        
        # ConversationalRetrievalChain expects chat_history as list of tuples (question, answer)
        response = qa_chain.invoke({
            "question": user_input,
            "chat_history": session["chat_history"]
        })
        
        result = response.get("answer", "No response")
        session["messages"].append({"role": "assistant", "content": result})
        logger.info(f"Assistant response: {result}")
        # Update chat history for context
        session["chat_history"].append((user_input, result))
                # Mark the session as modified to ensure changes are saved
        session.modified = True

        return redirect(url_for("index"))
    return render_template("index.html", messages=session.get("messages", []))

@app.route("/clear")
def clear():
    session.pop("messages", None)
    session.pop("chat_history", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
        