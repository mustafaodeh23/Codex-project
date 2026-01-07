import re

def _contains_arabic(text: str) -> bool:
    return any("\u0600" <= ch <= "\u06FF" for ch in text)

def analyze_idea_ai(idea: str) -> dict:
    text = idea.strip()
    lower = text.lower()

    language_detected = "Arabic" if _contains_arabic(text) else "English"

    # project type detection
    project_type = "General Software"
    if any(k in lower for k in ["website", "web", "landing", "frontend", "html", "css", "javascript"]):
        project_type = "Web Application"
    if any(k in lower for k in ["mobile", "android", "ios", "flutter"]):
        project_type = "Mobile Application"
    if any(k in lower for k in ["ai", "machine learning", "ml", "model", "dataset"]):
        project_type = "AI / Data Project"
    if any(k in lower for k in ["game", "engine", "graphics"]):
        project_type = "Game / Interactive Project"

    # feature signals
    signals = []
    def add_signal(word, label):
        if word in lower:
            signals.append(label)

    add_signal("login", "Auth/Login")
    add_signal("account", "Accounts")
    add_signal("dashboard", "Dashboard")
    add_signal("admin", "Admin Panel")
    add_signal("payment", "Payments")
    add_signal("chat", "Chat/Realtime")
    add_signal("api", "API Integration")
    add_signal("database", "Database")
    add_signal("search", "Search")
    add_signal("recommend", "Recommendations")

    # recommended stack
    stack = []
    if project_type == "Web Application":
        stack += ["HTML", "CSS", "JavaScript"]
        if any(s in signals for s in ["Auth/Login", "Accounts", "Admin Panel", "Database", "API Integration", "Payments"]):
            stack += ["Python (Flask)", "SQLite (or PostgreSQL)"]
        else:
            stack += ["Python (Flask)"]
    elif project_type == "AI / Data Project":
        stack += ["Python", "Pandas/NumPy (optional)"]
    elif project_type == "Game / Interactive Project":
        stack += ["C++ (core logic)", "Optional: Web UI (HTML/CSS/JS)"]
    else:
        stack += ["Python", "HTML/CSS (optional UI)"]

    # difficulty scoring
    words = re.findall(r"\w+", lower)
    length_score = min(25, len(words))  # cap
    feature_score = min(40, len(signals) * 8)
    complexity_bonus = 0
    if "payments" in [s.lower() for s in signals]:
        complexity_bonus += 10
    if "chat/realtime" in [s.lower() for s in signals]:
        complexity_bonus += 10
    if project_type == "AI / Data Project":
        complexity_bonus += 10

    score = min(100, 20 + length_score + feature_score + complexity_bonus)

    if score < 45:
        difficulty = "Beginner"
    elif score < 75:
        difficulty = "Intermediate"
    else:
        difficulty = "Advanced"

    roadmap = [
        "Write a 1-page scope: goals, users, main features",
        "Build a simple UI prototype (pages only)",
        "Implement core feature (MVP) with clean structure",
        "Add database if needed + improve UX",
        "Test with 3–5 users and refine"
    ]

    return {
        "language_detected": language_detected,
        "project_type": project_type,
        "signals": signals if signals else ["Basic idea detected"],
        "recommended_stack": sorted(list(set(stack))),
        "difficulty": difficulty,
        "score": score,
        "roadmap": roadmap
    }

def analyze_code_ai(code: str, language: str) -> dict:
    src = code
    lower = src.lower()

    # generic signals
    score = 0
    feedback = []

    def hit(cond, pts, msg):
        nonlocal score
        if cond:
            score += pts
            feedback.append(msg)

    # common patterns
    hit("for " in lower or "while " in lower, 12, "Uses loops")
    hit("if " in lower, 8, "Uses conditions")
    hit("try" in lower or "catch" in lower, 10, "Uses error handling")
    hit("import " in lower or "#include" in lower, 10, "Uses libraries/modules")

    # language-specific
    lang = language.lower()
    if "python" in lang:
        hit("def " in lower, 18, "Uses functions (def)")
        hit("class " in lower, 18, "Uses OOP (class)")
        hit("list" in lower or "dict" in lower or "set(" in lower, 8, "Uses data structures")
    elif "javascript" in lang:
        hit("function" in lower or "=>" in lower, 18, "Uses functions")
        hit("class " in lower, 14, "Uses classes (OOP)")
        hit("fetch(" in lower or "axios" in lower, 10, "Uses API calls")
        hit("document." in lower or "addEventListener" in lower, 10, "Uses DOM interaction")
    elif "c++" in lang or "cpp" in lang:
        hit("int main" in lower, 10, "Has main() entry")
        hit("class " in lower, 16, "Uses OOP (class)")
        hit("vector" in lower or "map" in lower or "unordered_" in lower, 10, "Uses STL containers")
        hit("cout" in lower or "cin" in lower, 6, "Uses I/O")
    elif "html" in lang:
        hit("<html" in lower, 10, "Has HTML structure")
        hit("<form" in lower, 10, "Uses forms")
        hit("class=" in lower or "id=" in lower, 8, "Uses selectors hooks (class/id)")
    elif "css" in lang:
        hit("{" in src and "}" in src, 10, "Has CSS rules")
        hit("display:" in lower, 10, "Uses layout properties")
        hit("grid" in lower or "flex" in lower, 12, "Uses Grid/Flex layout")

    # size complexity
    lines = len(src.splitlines())
    if lines >= 40:
        score += 12
        feedback.append("Code length indicates higher complexity")
    elif lines >= 15:
        score += 6
        feedback.append("Code length indicates some complexity")

    score = min(100, score)

    if score < 35:
        level = "Beginner"
        next_steps = [
            "Practice functions + loops",
            "Build 2 small mini-projects",
            "Learn clean code formatting"
        ]
    elif score < 70:
        level = "Intermediate"
        next_steps = [
            "Learn OOP properly",
            "Build a project with API + data storage",
            "Start testing and debugging skills"
        ]
    else:
        level = "Advanced"
        next_steps = [
            "Improve architecture & patterns",
            "Optimize performance & security",
            "Work on a full-featured portfolio project"
        ]

    if not feedback:
        feedback = ["Basic code detected — add more structure for better evaluation"]

    return {
        "language": language,
        "lines": lines,
        "score": score,
        "level": level,
        "feedback": feedback,
        "next_steps": next_steps
    }
