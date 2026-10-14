
import streamlit as st
from google import genai
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎓",
    layout="wide"
)

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
st.subheader("Your Campus-to-Career Assistant")
st.write(
    "Discover skill gaps, build a career roadmap "
    "and track your internship preparation."
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
