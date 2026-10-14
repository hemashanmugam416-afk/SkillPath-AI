
import streamlit as st
from google import genai
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""

/* Force all student form fields to light blue */
.stTextInput div[data-baseweb="input"],
.stTextInput div[data-baseweb="input"] input,
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background: #EAF3FF !important;
    background-color: #EAF3FF !important;
    color: #163A70 !important;
    border: 1px solid #B7D2F5 !important;
    border-radius: 10px !important;
    -webkit-text-fill-color: #163A70 !important;
}

/* Text inside input boxes */
.stTextInput input {
    color: #163A70 !important;
    -webkit-text-fill-color: #163A70 !important;
    caret-color: #163A70 !important;
}

/* Role and level dropdown text */
.stSelectbox [data-baseweb="select"] *,
.stMultiSelect [data-baseweb="select"] * {
    color: #163A70 !important;
}

/* Skills selected chips */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #D5E7FF !important;
    border: 1px solid #B7D2F5 !important;
}

/* Dropdown options menu */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
div[role="listbox"],
div[role="option"] {
    background-color: #EAF3FF !important;
    color: #163A70 !important;
}

/* Daily learning time slider */
.stSlider [data-baseweb="slider"] {
    accent-color: #2457A7;
}

<style>
/* Main app background */
.stApp {
    background-color: #F7F9FC;
    color: #1E293B;
}

/* Main headings */
h1, h2, h3 {
    color: #163A70 !important;
    font-weight: 700 !important;
}

/* Buttons */
div.stButton > button {
    background-color: #163A70;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    transition: 0.2s ease;
}

/* Button hover */
div.stButton > button:hover {
    background-color: #2457A7;
    color: white;
    border: 1px solid #2457A7;
}

/* Light input boxes */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

/* Placeholder text */
.stTextInput input::placeholder {
    color: #94A3B8 !important;
    opacity: 1;
}


/* Light input boxes */
.stTextInput div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

.stTextInput input {
    background-color: transparent !important;
    color: #1E293B !important;
}

/* Light dropdown boxes */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] span {
    color: #1E293B !important;
}

/* Dropdown options menu */
div[data-baseweb="popover"] ul,
div[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
}

div[role="option"] {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
}

div[role="option"]:hover {
    background-color: #E8EFFA !important;
    color: #163A70 !important;
}



/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #EDF2FA;
}

/* Dividers */
hr {
    border-color: #D9E2F0;
}
</style>
""", unsafe_allow_html=True)


# ---------- Career data ----------
CAREERS = {
    "Software Developer": {
        "skills": ["Python", "SQL", "Git",
                   "Problem Solving", "Projects"],
        "tasks": [
            "Revise Python fundamentals",
            "Practice coding problems",
            "Learn SQL and database basics",
            "Learn Git and GitHub",
            "Build a Python project",
            "Prepare a resume and apply for internships"
        ]
    },
    "QA Tester": {
        "skills": ["Testing", "SQL", "Python",
                   "Test Cases", "Projects"],
        "tasks": [
            "Learn software testing fundamentals",
            "Write test cases",
            "Practice SQL queries",
            "Learn Python basics",
            "Test a sample application",
            "Prepare a resume and apply for internships"
        ]
    },
    "Data Analyst": {
        "skills": ["Excel", "SQL", "Python",
                   "Statistics", "Projects"],
        "tasks": [
            "Learn Excel formulas and charts",
            "Practice SQL queries",
            "Learn Python for data analysis",
            "Study basic statistics",
            "Build a data analysis project",
            "Prepare a resume and apply for internships"
        ]
    }
}

PROJECTS = {
    "Python": "Build a student marks calculator.",
    "SQL": "Create a student database.",
    "Git": "Upload a project to GitHub.",
    "Problem Solving": "Solve 10 beginner coding problems.",
    "Projects": "Build and document a portfolio project.",
    "Testing": "Test a sample login page.",
    "Test Cases": "Write positive and negative test cases.",
    "Excel": "Create a student performance dashboard.",
    "Statistics": "Analyse a sample student dataset."
}

# ---------- Session state ----------
if "completed" not in st.session_state:
    st.session_state.completed = {}

# ---------- Header ----------

st.title("🎓 SkillPath AI")
st.subheader("Your Personal AI Career Mentor 🚀")
st.write(
    "Turn your career goals into action. Discover skill gaps, "
    "explore projects, build your learning roadmap, and prepare "
    "for internships — all in one place."
)


st.info(
    "Version 1: A rule-based career planning prototype. "
    "AI-powered recommendations will be added in a later version."
)

# ---------- Student profile ----------
st.header("1. Student Profile")

with st.form("student_form"):
    name = st.text_input("Your name")
    degree = st.text_input(
        "Your degree",
        placeholder="e.g. B.Sc Computer Science with AI"
    )
    role = st.selectbox(
        "Your target role",
        list(CAREERS.keys())
    )
    level = st.selectbox(
        "Your current level",
        ["Beginner", "Intermediate", "Advanced"]
    )
    hours = st.slider(
        "Daily learning time (hours)",
        min_value=1,
        max_value=8,
        value=2
    )
    known_skills = st.multiselect(
        "Skills you already know",
        CAREERS[role]["skills"]
    )

    submitted = st.form_submit_button(
        "Generate My Career Plan",
        type="primary"
    )

# ---------- Personalised plan ----------
if submitted:
    if not name.strip() or not degree.strip():
        st.warning("Please enter your name and degree.")
    else:
        st.session_state.profile = {
            "name": name.strip(),
            "degree": degree.strip(),
            "role": role,
            "level": level,
            "hours": hours,
            "known": known_skills
        }

        st.session_state.completed.setdefault(
            name.strip(), []
        )

# ---------- Display results ----------
profile = st.session_state.get("profile")

if profile:
    
    st.divider()
    st.subheader("🗺️ Your Career Journey")

    steps = [
        ("1", "Student Profile", "Set up your career goals"),
        ("2", "Skill Assessment", "Discover your missing skills"),
        ("3", "Build Projects", "Practice with real projects"),
        ("4", "Learning Roadmap", "Follow your weekly plan"),
        ("5", "Internship Ready", "Prepare for internship applications"),
    ]

    for number, title, description in steps:
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 15px;
                background: white;
                border: 1px solid #D9E2F0;
                border-radius: 12px;
                padding: 14px;
                margin-bottom: 10px;
            ">
                <div style="
                    background: #163A70;
                    color: white;
                    min-width: 38px;
                    height: 38px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                ">{number}</div>
                <div>
                    <div style="color: #163A70; font-weight: 700;">
                        {title}
                    </div>
                    <div style="color: #64748B; font-size: 14px;">
                        {description}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    role = profile["role"]
    known = profile["known"]
    tasks = CAREERS[role]["tasks"]
    gaps = [
        skill for skill in CAREERS[role]["skills"]
        if skill not in known
    ]

    st.divider()
    st.header(f"Welcome, {profile['name']}! 👋")
    st.write(f"**Degree:** {profile['degree']}")
    st.write(f"**Career goal:** {role}")
    st.divider()
    st.subheader("🤖 Your AI Career Mentor")

    if st.button("Generate AI Career Advice", type="primary"):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]

            client = genai.Client(api_key=api_key)

            prompt = f"""
            You are SkillPath AI, a friendly campus-to-career mentor.

            Student degree: {profile['degree']}
            Target role: {profile['role']}
            Current level: {profile['level']}
            Daily study hours: {profile['hours']}
            Skills already known: {', '.join(profile['known']) or 'None yet'}
            Skills to learn: {', '.join(gaps) or 'Strengthen existing skills'}

            Give this student:
            1. A personalized 4-week learning roadmap.
            2. Three beginner-friendly project ideas.
            3. Practical internship preparation tips.
            4. A realistic daily study routine.

            Use simple English, clear headings and bullet points.
            Make the advice practical for a college student.
            Do not promise jobs or guaranteed placements.
            """

            with st.spinner("Your AI mentor is preparing advice..."):
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

            st.markdown(response.text)

        except KeyError:
            st.error(
                "API key not found. Check Streamlit Settings > Secrets."
            )
        except Exception as e:
            st.error(
                "AI advice could not be generated. "
                "Please check your API key, model access, "
                "and API usage limits."
            )
            st.caption(str(e))
            st.divider()
            
    st.divider()
    st.header("🤖 SkillPath AI Chatbot")
    st.write("Ask me about skills, careers, projects, or internships!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
     
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Ask your career question here...")

    if user_question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        try:
            client = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            conversation = "\n".join(
                f"{msg['role']}: {msg['content']}"
                for msg in st.session_state.chat_history[-10:]
            )

            prompt = f"""
            You are SkillPath AI, a friendly campus-to-career mentor.
            Help college students learn skills, build projects,
            prepare resumes, and find internships.
            Give practical, beginner-friendly advice in simple English.
            Do not guarantee jobs or placements.

            Conversation:
            {conversation}

            Reply to the latest student question.
            """

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )
                    answer = response.text or "Please try asking again."
                    st.markdown(answer)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error("Sorry, the chatbot could not reply.")
            st.caption(str(e))

                   
    left, right = st.columns(2)

    with left:
        st.subheader("2. Your Skill Assessment")
        st.write("**Skills you selected:**")
        st.write(", ".join(known) if known else "None selected yet")
        st.write("**Skills to develop:**")
        st.write(", ".join(gaps) if gaps else
                 "Review and strengthen your skills.")

    with right:
        st.subheader("3. Recommended Projects")
        if gaps:
            for skill in gaps:
                st.write(
                    f"**{skill}:** "
                    f"{PROJECTS.get(skill, 'Build a small practice project.')}"
                )
        else:
            st.write(
                "Build more advanced projects and "
                "demonstrate your skills."
            )

    st.divider()
    st.header("4. Your Learning Roadmap")

    completed = st.session_state.completed[
        profile["name"]
    ]

    for index, task in enumerate(tasks):
        key = f"{profile['name']}_{index}"
        is_done = st.checkbox(
            f"Week {index + 1}: {task}",
            value=task in completed,
            key=key
        )

        if is_done and task not in completed:
            completed.append(task)
        elif not is_done and task in completed:
            completed.remove(task)

    progress = len(completed) / len(tasks)
    st.progress(progress)
    st.write(
        f"**Progress: {len(completed)}/{len(tasks)} "
        f"tasks ({progress:.0%})**"
    )

    st.caption(
        "Progress is kept during this app session. "
        "Persistent storage will be added later."
    )

    if progress == 1:
        st.success(
            "Great work! Review your projects and "
            "continue preparing for internships."
        )
    else:
        st.info(
            "Next action: Start with one incomplete task "
            "and record your progress."
        )

st.divider()
st.caption(
    "SkillPath AI | Learn • Build • Track • Grow"
)

if st.sidebar.button("Check Available Gemini Models"):
    try:
        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"]
        )

        st.subheader("Available Gemini Models")

        for model in client.models.list():
            if "generateContent" in (model.supported_actions or []):
                st.write(model.name)

    except Exception as e:
        st.error(f"Could not list models: {e}")
