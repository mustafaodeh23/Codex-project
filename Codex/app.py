from flask import Flask, render_template, request
from ai_engine import analyze_idea_ai, analyze_code_ai

app = Flask(__name__)


CURRENT_LEVEL = 20  

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/languages")
def languages():
    langs = [
        {"name": "HTML", "icon": "🧱"},
        {"name": "CSS", "icon": "🎨"},
        {"name": "JavaScript", "icon": "⚡"},
        {"name": "Python", "icon": "🐍"},
        {"name": "C++", "icon": "🧩"},
    ]
    return render_template("languages.html", languages=langs)

@app.route("/levels/<language>")
def levels(language):
    levels_list = []
    for i in range(1, 101):
        levels_list.append({
            "num": i,
            "open": i <= CURRENT_LEVEL,
            "quiz": (i % 20 == 0)
        })
    return render_template("levels.html", language=language, levels=levels_list)

@app.route("/idea", methods=["GET", "POST"])
def idea():
    result = None
    idea_text = ""
    if request.method == "POST":
        idea_text = request.form.get("idea", "").strip()
        if idea_text:
            result = analyze_idea_ai(idea_text)
    return render_template("idea.html", result=result, idea_text=idea_text)

@app.route("/code", methods=["GET", "POST"])
def code():
    result = None
    code_text = ""
    language = "Python"
    if request.method == "POST":
        language = request.form.get("language", "Python")
        code_text = request.form.get("code", "")
        if code_text.strip():
            result = analyze_code_ai(code_text, language)
    return render_template("code.html", result=result, code_text=code_text, language=language)

if __name__ == "__main__":
    app.run(debug=True)
