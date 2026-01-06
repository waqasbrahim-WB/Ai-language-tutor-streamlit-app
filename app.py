import streamlit as st
import random
import textwrap
from typing import List, Dict

# -----------------------------
# App config
# -----------------------------
st.set_page_config(page_title="WB AI Language Tutor", page_icon="🧠", layout="wide")

# -----------------------------
# Theme & styles
# -----------------------------
PRIMARY = "#4B9FEA"
ACCENT = "#7C4DFF"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"
BG_DARK = "#0F172A"
BG_CARD = "#111827"
TEXT = "#E5E7EB"
MUTED = "#9CA3AF"

CUSTOM_CSS = f"""
<style>
/* Global */
html, body, [class*="css"] {{
    font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', Arial, sans-serif;
    color: {TEXT};
}}
/* App background */
.stApp {{
    background: linear-gradient(135deg, {BG_DARK} 0%, #0b1220 50%, #0a0f1a 100%);
}}
/* Headers */
h1, h2, h3 {{
    color: {TEXT};
}}
/* Cards */
.card {{
    background: {BG_CARD};
    border: 1px solid #1F2937;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35);
}}
/* Badges */
.badge {{
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 8px;
}}
.badge-primary {{ background: {PRIMARY}; color: white; }}
.badge-accent {{ background: {ACCENT}; color: white; }}
.badge-success {{ background: {SUCCESS}; color: white; }}
.badge-warning {{ background: {WARNING}; color: black; }}
.badge-danger {{ background: {DANGER}; color: white; }}
/* Buttons */
.stButton>button {{
    background: linear-gradient(135deg, {PRIMARY}, {ACCENT});
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(76, 29, 149, 0.35);
}}
.stButton>button:hover {{
    filter: brightness(1.05);
}}
/* Inputs */
.stTextInput>div>div>input, .stSelectbox>div>div>select {{
    background: #0b1220;
    color: {TEXT};
    border: 1px solid #1F2937;
    border-radius: 10px;
}}
/* Divider */
hr {{
    border: none;
    border-top: 1px solid #1F2937;
}}
/* Code blocks */
pre, code {{
    background: #0b1220 !important;
    color: {TEXT} !important;
}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------
# Data
# -----------------------------
LEVELS = ["Beginner (A1)", "Elementary (A2)", "Intermediate (B1)", "Upper-Intermediate (B2)", "Advanced (C1)"]
TOPICS = [
    "Greetings & Introductions",
    "Daily Routine",
    "Food & Restaurants",
    "Travel & Directions",
    "Shopping & Money",
    "Work & Meetings",
    "Health & Appointments",
    "Technology & Gadgets",
    "Environment & Sustainability",
    "Culture & Hobbies",
]

GRAMMAR_POINTS = {
    "Beginner (A1)": ["Present Simple", "Subject Pronouns", "Basic Question Forms", "Articles (a/an/the)"],
    "Elementary (A2)": ["Past Simple", "Countable/Uncountable Nouns", "Prepositions of Time/Place", "Comparatives"],
    "Intermediate (B1)": ["Present Perfect", "Modal Verbs (should/must/can)", "Reported Speech (intro)", "Relative Clauses"],
    "Upper-Intermediate (B2)": ["Conditionals (1st/2nd)", "Passive Voice", "Phrasal Verbs", "Linking Words"],
    "Advanced (C1)": ["Mixed Conditionals", "Advanced Modals", "Inversion", "Subjunctive & Formal Structures"],
}

VOCAB_SETS = {
    "Greetings & Introductions": ["hello", "nice to meet you", "how are you", "introduce", "name", "friend", "colleague", "welcome"],
    "Daily Routine": ["wake up", "breakfast", "commute", "work", "exercise", "dinner", "sleep", "schedule"],
    "Food & Restaurants": ["menu", "order", "bill", "reservation", "delicious", "spicy", "vegetarian", "dessert"],
    "Travel & Directions": ["ticket", "station", "map", "left", "right", "straight", "hotel", "passport"],
    "Shopping & Money": ["discount", "receipt", "cash", "card", "price", "refund", "exchange", "bargain"],
    "Work & Meetings": ["agenda", "deadline", "presentation", "feedback", "team", "project", "report", "client"],
    "Health & Appointments": ["doctor", "clinic", "symptom", "medicine", "appointment", "checkup", "prescription", "recovery"],
    "Technology & Gadgets": ["software", "update", "battery", "screen", "keyboard", "network", "download", "cloud"],
    "Environment & Sustainability": ["recycle", "pollution", "renewable", "conservation", "climate", "ecosystem", "waste", "green"],
    "Culture & Hobbies": ["music", "festival", "painting", "reading", "sports", "photography", "dance", "travel"],
}

DIALOGUE_TEMPLATES = [
    ("Greetings & Introductions",
     "A: Hi! I'm {name_a}. Nice to meet you.\nB: Hi {name_a}, I'm {name_b}. How are you?\nA: I'm good, thanks! What do you do?\nB: I'm a {job}."),
    ("Food & Restaurants",
     "A: Could I see the menu, please?\nB: Of course. Do you have any dietary preferences?\nA: Yes, I'm {diet}. What's your recommendation?\nB: The {dish} is very popular."),
    ("Travel & Directions",
     "A: Excuse me, how do I get to the {place}?\nB: Go straight, then turn left at the {landmark}.\nA: Thank you! Is it far?\nB: About {minutes} minutes on foot."),
    ("Work & Meetings",
     "A: Can we move the meeting to {time}?\nB: Sure. What's the agenda?\nA: We'll discuss the {topic} and next steps.\nB: Great, I'll prepare the report."),
]

QUIZ_BANK = {
    "Beginner (A1)": [
        {"q": "Choose the correct article: ___ apple", "options": ["a", "an", "the"], "answer": "an"},
        {"q": "Pick the correct verb: She ___ to school.", "options": ["go", "goes", "going"], "answer": "goes"},
        {"q": "Select the pronoun: ___ am happy.", "options": ["I", "Me", "My"], "answer": "I"},
    ],
    "Elementary (A2)": [
        {"q": "Past Simple: They ___ dinner at 7.", "options": ["eat", "ate", "eaten"], "answer": "ate"},
        {"q": "Preposition: The book is ___ the table.", "options": ["on", "in", "at"], "answer": "on"},
        {"q": "Comparative: This car is ___ than that one.", "options": ["fast", "faster", "fastest"], "answer": "faster"},
    ],
    "Intermediate (B1)": [
        {"q": "Present Perfect: I ___ my homework.", "options": ["did", "have done", "do"], "answer": "have done"},
        {"q": "Modal: You ___ see a doctor.", "options": ["should", "must", "can"], "answer": "should"},
        {"q": "Reported Speech: He said he ___ tired.", "options": ["is", "was", "were"], "answer": "was"},
    ],
    "Upper-Intermediate (B2)": [
        {"q": "Conditional: If I ___ time, I would help.", "options": ["have", "had", "has"], "answer": "had"},
        {"q": "Passive: The letter ___ yesterday.", "options": ["was sent", "sent", "is send"], "answer": "was sent"},
        {"q": "Phrasal Verb: Please ___ the lights.", "options": ["turn on", "turns on", "turn onning"], "answer": "turn on"},
    ],
    "Advanced (C1)": [
        {"q": "Inversion: Rarely ___ such talent.", "options": ["I have seen", "have I seen", "I seen"], "answer": "have I seen"},
        {"q": "Mixed Conditional: If he ___ earlier, he would be here now.", "options": ["left", "had left", "has left"], "answer": "had left"},
        {"q": "Subjunctive: It is essential that he ___ present.", "options": ["is", "be", "was"], "answer": "be"},
    ],
}

# -----------------------------
# Helpers
# -----------------------------
def wrap(text: str) -> str:
    return "<br>".join(textwrap.fill(text, width=90).split("\n"))

def generate_lesson(level: str, topic: str) -> Dict[str, List[str]]:
    grammar = random.sample(GRAMMAR_POINTS[level], k=min(2, len(GRAMMAR_POINTS[level])))
    vocab = random.sample(VOCAB_SETS[topic], k=min(8, len(VOCAB_SETS[topic])))
    tips = [
        f"Focus on {grammar[0].lower()} with short, clear sentences.",
        f"Use the vocabulary in context—write 3 sentences about {topic.lower()}.",
        "Record yourself speaking and compare with sample dialogues.",
        "Review mistakes and rewrite with correct grammar.",
    ]
    return {"grammar": grammar, "vocab": vocab, "tips": tips}

def generate_dialogue(level: str, topic: str) -> str:
    template = random.choice([t for t in DIALOGUE_TEMPLATES if t[0] == topic] or DIALOGUE_TEMPLATES)
    _, script = template
    fill = {
        "name_a": random.choice(["Ali", "Sara", "John", "Mina", "Waqas"]),
        "name_b": random.choice(["Aisha", "David", "Noor", "Leo", "Fatima"]),
        "job": random.choice(["software engineer", "designer", "teacher", "doctor", "student"]),
        "diet": random.choice(["vegetarian", "vegan", "gluten-free", "halal"]),
        "dish": random.choice(["grilled salmon", "paneer tikka", "chicken biryani", "veggie pasta"]),
        "place": random.choice(["museum", "city center", "train station", "library"]),
        "landmark": random.choice(["fountain", "statue", "bridge", "square"]),
        "minutes": random.choice(["5", "10", "15"]),
        "time": random.choice(["10 AM", "2 PM", "4:30 PM"]),
        "topic": random.choice(["roadmap", "budget", "timeline", "deliverables"]),
    }
    for k, v in fill.items():
        script = script.replace("{"+k+"}", v)
    return script

def get_quiz(level: str) -> List[Dict]:
    bank = QUIZ_BANK[level]
    return random.sample(bank, k=min(len(bank), 3))

def init_state():
    defaults = {
        "level": LEVELS[2],  # default B1
        "topic": TOPICS[0],
        "quiz_score": 0,
        "quiz_total": 0,
        "quiz_feedback": "",
        "quiz_answers": {},
        "lesson": None,
        "dialogue": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# -----------------------------
# Header
# -----------------------------
st.markdown(f"""
<div class="card">
  <h1>🧠 WB AI Language Tutor</h1>
  <div>
    <span class="badge badge-primary">Lessons</span>
    <span class="badge badge-accent">Quizzes</span>
    <span class="badge badge-success">Dialogues</span>
  </div>
  <p style="color:{MUTED}; margin-top:8px;">
    Personalized language practice—choose your level and topic, then generate lessons, quizzes, and dialogues.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# -----------------------------
# Controls
# -----------------------------
colA, colB, colC = st.columns([1.2, 1.2, 2])
with colA:
    st.subheader("Level")
    st.session_state.level = st.selectbox("Select level", LEVELS, index=LEVELS.index(st.session_state.level))
with colB:
    st.subheader("Topic")
    st.session_state.topic = st.selectbox("Select topic", TOPICS, index=TOPICS.index(st.session_state.topic))
with colC:
    st.subheader("Actions")
    gen_lesson = st.button("📘 Generate Lesson")
    gen_quiz = st.button("📝 Generate Quiz")
    gen_dialogue = st.button("💬 Generate Dialogue")

st.markdown("<hr/>", unsafe_allow_html=True)

# -----------------------------
# Lesson
# -----------------------------
if gen_lesson or st.session_state.lesson is None:
    st.session_state.lesson = generate_lesson(st.session_state.level, st.session_state.topic)

lesson = st.session_state.lesson
lcol1, lcol2 = st.columns([1, 1])

with lcol1:
    st.markdown(f"""
    <div class="card">
      <h3>📘 Lesson — {st.session_state.level} • {st.session_state.topic}</h3>
      <h4 style="color:{PRIMARY};">Grammar Focus</h4>
      <ul>
        {"".join([f"<li>{g}</li>" for g in lesson["grammar"]])}
      </ul>
      <h4 style="color:{PRIMARY};">Vocabulary</h4>
      <div style="display:flex; flex-wrap:wrap; gap:8px;">
        {"".join([f'<span class="badge badge-warning">{v}</span>' for v in lesson["vocab"]])}
      </div>
    </div>
    """, unsafe_allow_html=True)

with lcol2:
    st.markdown(f"""
    <div class="card">
      <h3>🎯 Practice Tips</h3>
      <ol>
        {"".join([f"<li>{wrap(t)}</li>" for t in lesson["tips"]])}
      </ol>
      <p style="color:{MUTED};">Try writing a short paragraph using today’s grammar and vocabulary.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# -----------------------------
# Quiz
# -----------------------------
if gen_quiz:
    st.session_state.quiz_score = 0
    st.session_state.quiz_total = 0
    st.session_state.quiz_feedback = ""
    st.session_state.quiz_answers = {}

quiz_items = get_quiz(st.session_state.level)

st.markdown(f"""
<div class="card">
  <h3>📝 Quiz — {st.session_state.level}</h3>
  <p style="color:{MUTED};">Answer the questions below. Click "Submit Quiz" to see your score.</p>
</div>
""", unsafe_allow_html=True)

q_cols = st.columns(1)
with q_cols[0]:
    for i, item in enumerate(quiz_items, start=1):
        st.write(f"**Q{i}. {item['q']}**")
        choice = st.radio(f"q_{i}", item["options"], index=0, horizontal=True, key=f"quiz_{i}")
        st.session_state.quiz_answers[f"q_{i}"] = choice
        st.markdown("<br/>", unsafe_allow_html=True)

submit_quiz = st.button("✅ Submit Quiz")
if submit_quiz:
    score = 0
    for i, item in enumerate(quiz_items, start=1):
        if st.session_state.quiz_answers.get(f"q_{i}") == item["answer"]:
            score += 1
    st.session_state.quiz_score = score
    st.session_state.quiz_total = len(quiz_items)
    if score == len(quiz_items):
        st.session_state.quiz_feedback = f"🎉 Perfect! {score}/{len(quiz_items)}"
    elif score >= len(quiz_items) - 1:
        st.session_state.quiz_feedback = f"👍 Great job! {score}/{len(quiz_items)}"
    else:
        st.session_state.quiz_feedback = f"💡 Keep practicing: {score}/{len(quiz_items)}"

if st.session_state.quiz_total > 0:
    pct = int(100 * st.session_state.quiz_score / st.session_state.quiz_total)
    st.progress(pct / 100)
    if pct >= 80:
        st.success(st.session_state.quiz_feedback)
    elif pct >= 50:
        st.warning(st.session_state.quiz_feedback)
    else:
        st.error(st.session_state.quiz_feedback)

st.markdown("<hr/>", unsafe_allow_html=True)

# -----------------------------
# Dialogue
# -----------------------------
if gen_dialogue or st.session_state.dialogue is None:
    st.session_state.dialogue = generate_dialogue(st.session_state.level, st.session_state.topic)

dialogue_text = st.session_state.dialogue

dcol1, dcol2 = st.columns([2, 1])
with dcol1:
    st.markdown(f"""
    <div class="card">
      <h3>💬 Practice Dialogue — {st.session_state.topic}</h3>
      <pre style="white-space: pre-wrap; line-height: 1.6;">{dialogue_text}</pre>
    </div>
    """, unsafe_allow_html=True)

with dcol2:
    st.markdown(f"""
    <div class="card">
      <h3>🗣️ Speaking Task</h3>
      <p>Read the dialogue aloud. Then, replace highlighted words with your own (e.g., job, place, time).</p>
      <ul>
        <li>Record yourself and note pronunciation.</li>
        <li>Rewrite the dialogue using today’s grammar focus.</li>
        <li>Create 3 follow-up questions.</li>
      </ul>
      <p style="color:{MUTED};">Tip: Keep sentences clear and natural.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown(f"""
<div class="card">
  <h3>📈 Progress & Notes</h3>
  <p style="color:{MUTED};">Track your learning: note new words, grammar mistakes, and speaking confidence.</p>
  <ul>
    <li>Level: <span class="badge badge-primary">{st.session_state.level}</span></li>
    <li>Topic: <span class="badge badge-accent">{st.session_state.topic}</span></li>
    <li>Quiz Score: <span class="badge badge-success">{st.session_state.quiz_score}/{st.session_state.quiz_total}</span></li>
  </ul>
  <p style="color:{MUTED};">Built with Streamlit • WB_chatbot learning</p>
</div>
""", unsafe_allow_html=True)
