import streamlit as st
from pathlib import Path
import random

from modules.chatbot import generate_response
from modules.quiz import generate_quiz

from modules.database import (
    initialize_database,
    save_quiz_result,
    get_quiz_results
)

from modules.planner import generate_study_plan

from modules.notes import (
    extract_text_from_pdf,
    create_notes_index,
    ask_about_notes,
    summarize_notes,
    generate_quiz_from_notes,
    validate_quiz
)

from modules.dashboard import show_dashboard


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Student Assistant",
    page_icon="🎓",
    layout="wide"
)
# ============================================================
# LOAD CUSTOM CSS
# ============================================================

css_path = Path(".streamlit/style.css")

if css_path.exists():

    with open(
        css_path,
        "r",
        encoding="utf-8"
    ) as css_file:

        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# SESSION STATE
# ============================================================

# -----------------------------
# Normal AI Chat
# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI study assistant "
                "for college students. "
                "Explain concepts clearly and simply. "
                "Use examples when helpful. "
                "Keep answers reasonably short unless "
                "the student asks for more detail."
            )
        }
    ]


# -----------------------------
# General Quiz
# -----------------------------

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None

if "quiz_percentage" not in st.session_state:
    st.session_state.quiz_percentage = None

if "quiz_saved" not in st.session_state:
    st.session_state.quiz_saved = False


# -----------------------------
# Notes Assistant
# -----------------------------

if "notes_chat" not in st.session_state:
    st.session_state.notes_chat = []

if "notes_question_count" not in st.session_state:
    st.session_state.notes_question_count = 0

if "notes_summary" not in st.session_state:
    st.session_state.notes_summary = None

if "notes_quiz" not in st.session_state:
    st.session_state.notes_quiz = None

if "notes_quiz_submitted" not in st.session_state:
    st.session_state.notes_quiz_submitted = False

if "notes_quiz_score" not in st.session_state:
    st.session_state.notes_quiz_score = None


# ============================================================
# SIDEBAR
# ============================================================

# Sidebar artwork
ASSETS_DIR = Path("assets")
SIDEBAR_LOGO = ASSETS_DIR / "sidebar_logo.png"
SIDEBAR_BOOKS = ASSETS_DIR / "sidebar_books.png"

# ------------------------------------------------------------
# SIDEBAR BRANDING
# ------------------------------------------------------------

if SIDEBAR_LOGO.exists():

    st.sidebar.image(
        str(SIDEBAR_LOGO),
        width=150
    )

st.sidebar.markdown(
    """
    <div style="
        margin-top:4px;
        margin-bottom:2px;
        color:#17233B;
        font-size:1.18rem;
        font-weight:750;
        letter-spacing:-0.3px;
        line-height:1.25;
    ">
        AI Student Assistant
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div style="
        color:#64748B;
        font-size:0.78rem;
        line-height:1.4;
        margin-bottom:4px;
    ">
        Your personal study companion
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

pages = [
    "🏠 Dashboard",
    "💬 AI Study Chat",
    "📝 Quiz Generator",
    "📅 Study Planner",
    "📚 Notes Assistant",
    "📊 Progress"
]

# Check whether a Dashboard Quick Action requested navigation
navigation_target = st.session_state.pop(
    "dashboard_navigation_target",
    None
)

# ------------------------------------------------------------
# SIDEBAR NAVIGATION STATE
# ------------------------------------------------------------

if "selected_page" not in st.session_state:

    st.session_state.selected_page = "🏠 Dashboard"

# Dashboard Quick Action requested a page
if navigation_target in pages:

    st.session_state.selected_page = navigation_target

# Sidebar navigation
page = st.sidebar.radio(
    "MENU",
    pages,
    key="selected_page"
)

# ============================================================
# SIDEBAR STATUS
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-footer">
        <div style="font-size: 0.9rem;">
            🤖 <strong>Local AI</strong>
        </div>
        <div style="margin-top: 5px;">
            🟢 System Ready
        </div>
        <div style="margin-top: 5px;">
            AI Student Assistant
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# SIDEBAR DECORATION
# ------------------------------------------------------------

if SIDEBAR_BOOKS.exists():

    st.sidebar.markdown(
        "<div style='height:14px;'></div>",
        unsafe_allow_html=True
    )

    st.sidebar.image(
        str(SIDEBAR_BOOKS),
        width=210
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    show_dashboard()


# ============================================================
# AI STUDY CHAT
# ============================================================

elif page == "💬 AI Study Chat":

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
        <div class="dashboard-eyebrow">
            AI-POWERED STUDY ASSISTANT
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title(
        "Study Chat 💬"
    )

    st.markdown(
        """
        <div class="dashboard-subtitle">
            Ask questions, understand difficult concepts,
            and learn through a continuous conversation
            with your local AI study assistant.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )

    # ========================================================
    # CHAT WORKSPACE
    # ========================================================

    with st.container(border=True):

        header_col1, header_col2 = st.columns(
            [5, 1]
        )

        with header_col1:

            st.markdown(
                "### 💡 Learning Conversation"
            )

            st.caption(
                "Your conversation stays available while "
                "you continue learning."
            )

        with header_col2:

            if st.button(
                "🗑️ Clear Chat",
                use_container_width=True,
                key="clear_study_chat"
            ):

                st.session_state.messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI study assistant "
                            "for college students. "
                            "Explain concepts clearly and simply. "
                            "Use examples when helpful. "
                            "Keep answers reasonably short unless "
                            "the student asks for more detail."
                        )
                    }
                ]

                st.rerun()

    # ========================================================
    # CONVERSATION
    # ========================================================

    visible_messages = [
        message
        for message in st.session_state.messages
        if message["role"] != "system"
    ]

    if not visible_messages:

        st.markdown(
            "<div class='dashboard-space'></div>",
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(
                "### 👋 Start learning"
            )

            st.write(
                "Ask your first study question and "
                "start a conversation with your AI assistant."
            )

            st.markdown(
                """
                <div style="
                    margin-top:16px;
                    padding:14px 16px;
                    border:1px solid #E2E8F0;
                    border-radius:12px;
                    background:#F8FAFC;
                    color:#64748B;
                    font-size:0.82rem;
                ">
                    💭 Example: Explain REST API in simple words.
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            "<div class='dashboard-space'></div>",
            unsafe_allow_html=True
        )

        for message in visible_messages:

            with st.chat_message(
                message["role"]
            ):

                st.write(
                    message["content"]
                )

    # ========================================================
    # CHAT INPUT
    # ========================================================

    question = st.chat_input(
        "Ask your study question..."
    )

    if question:

        # ----------------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # ----------------------------------------------------
        # DISPLAY USER MESSAGE
        # ----------------------------------------------------

        with st.chat_message(
            "user"
        ):

            st.write(
                question
            )

        # ----------------------------------------------------
        # GENERATE AI RESPONSE
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🤖 Thinking..."
            ):

                response = generate_response(
                    st.session_state.messages
                )

            st.write(
                response
            )

        # ----------------------------------------------------
        # SAVE AI RESPONSE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


# ============================================================
# GENERAL QUIZ GENERATOR
# ============================================================

elif page == "📝 Quiz Generator":

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
        <div class="dashboard-eyebrow">
            AI-POWERED ASSESSMENT
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title(
        "Quiz Generator 📝"
    )

    st.markdown(
        """
        <div class="dashboard-subtitle">
            Create an AI-generated quiz, test your knowledge,
            and track your performance automatically.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )

    # ========================================================
    # QUIZ SETTINGS
    # ========================================================

    with st.container(border=True):

        st.markdown(
            "### ⚙️ Quiz Settings"
        )

        st.caption(
            "Choose what you want to practice."
        )

        col1, col2 = st.columns(2)

        with col1:

            topic = st.text_input(
                "📚 Topic",
                placeholder="Example: Machine Learning",
                key="quiz_topic_input"
            )

        with col2:

            difficulty = st.selectbox(
                "🎯 Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard"
                ],
                key="quiz_difficulty_input"
            )

        number_of_questions = st.slider(
            "🔢 Number of questions",
            min_value=1,
            max_value=10,
            value=5,
            key="quiz_question_count"
        )

        st.markdown(
            "<div class='dashboard-space-small'></div>",
            unsafe_allow_html=True
        )

        if st.button(
            "🚀 Generate Quiz",
            use_container_width=True,
            key="generate_quiz_button"
        ):

            if not topic.strip():

                st.warning(
                    "⚠️ Please enter a topic first."
                )

            else:

                with st.spinner(
                    "🤖 AI is creating your quiz..."
                ):

                    try:

                        quiz = generate_quiz(
                            topic,
                            difficulty,
                            number_of_questions
                        )

                        # ------------------------------------
                        # Shuffle answer options
                        # ------------------------------------

                        shuffled_quiz = []

                        for question in quiz:

                            new_question = question.copy()

                            new_question["options"] = (
                                question["options"].copy()
                            )

                            random.shuffle(
                                new_question["options"]
                            )

                            shuffled_quiz.append(
                                new_question
                            )

                        # ------------------------------------
                        # Save quiz to session
                        # ------------------------------------

                        st.session_state.quiz = (
                            shuffled_quiz
                        )

                        st.session_state.quiz_topic = (
                            topic
                        )

                        st.session_state.quiz_difficulty = (
                            difficulty
                        )

                        st.session_state.quiz_submitted = (
                            False
                        )

                        st.session_state.quiz_score = (
                            None
                        )

                        st.session_state.quiz_percentage = (
                            None
                        )

                        st.session_state.quiz_saved = (
                            False
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            "❌ The AI could not generate "
                            "the quiz."
                        )

                        st.caption(
                            f"Technical details: {error}"
                        )

    # ========================================================
    # DISPLAY QUIZ
    # ========================================================

    if "quiz" in st.session_state:

        st.markdown(
            "<div class='dashboard-space'></div>",
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # QUIZ HEADER
        # ----------------------------------------------------

        with st.container(border=True):

            st.markdown(
                f"### 📚 {st.session_state.quiz_topic}"
            )

            st.caption(
                f"Difficulty: "
                f"{st.session_state.quiz_difficulty}"
                f"  •  "
                f"Questions: "
                f"{len(st.session_state.quiz)}"
            )

        st.markdown(
            "<div class='dashboard-space'></div>",
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # QUESTIONS
        # ----------------------------------------------------

        answers = []

        for index, question in enumerate(
            st.session_state.quiz
        ):

            with st.container(border=True):
                st.markdown(
                    f"**Question {index + 1} of "
                    f"{len(st.session_state.quiz)}**"
                )

                st.caption(
                    f"{st.session_state.quiz_topic} • "
                    f"{st.session_state.quiz_difficulty}"
                )

                 

                st.write(
                    question["question"]
                )

                selected_answer = st.radio(
                    "Choose your answer:",
                    question["options"],
                    key=f"quiz_question_{index}"
                )

                answers.append(
                    selected_answer
                )

        st.markdown(
            "<div class='dashboard-space'></div>",
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # SUBMIT
        # ----------------------------------------------------

        if not st.session_state.get(
            "quiz_submitted",
            False
        ):

            if st.button(
                "✅ Submit Quiz",
                use_container_width=True,
                key="submit_quiz_button"
            ):

                score = 0

                for index, question in enumerate(
                    st.session_state.quiz
                ):

                    if (
                        answers[index]
                        == question["answer"]
                    ):

                        score += 1

                total_questions = len(
                    st.session_state.quiz
                )

                percentage = (
                    score
                    /
                    total_questions
                ) * 100

                st.session_state.quiz_score = (
                    score
                )

                st.session_state.quiz_percentage = (
                    percentage
                )

                st.session_state.quiz_submitted = (
                    True
                )

                # ----------------------------------------
                # Save result once
                # ----------------------------------------

                if not st.session_state.quiz_saved:

                    save_quiz_result(
                        topic=(
                            st.session_state.quiz_topic
                        ),
                        difficulty=(
                            st.session_state.quiz_difficulty
                        ),
                        score=score,
                        total_questions=(
                            total_questions
                        )
                    )

                    st.session_state.quiz_saved = (
                        True
                    )

                st.rerun()

        # ====================================================
        # RESULT
        # ====================================================

        if st.session_state.get(
            "quiz_submitted",
            False
        ):

            score = (
                st.session_state.quiz_score
            )

            total_questions = len(
                st.session_state.quiz
            )

            percentage = (
                st.session_state.quiz_percentage
            )

            st.markdown(
                "<div class='dashboard-space'></div>",
                unsafe_allow_html=True
            )

            section_col1, section_col2 = st.columns(
                [3, 1]
            )

            with section_col1:

                st.markdown(
                    "### 🏆 Quiz Result"
                )

            with section_col2:

                st.metric(
                    "Score",
                    f"{percentage:.0f}%"
                )

            # --------------------------------------------
            # Performance message
            # --------------------------------------------

            if percentage >= 80:

                st.success(
                    f"🎉 Excellent work! "
                    f"You scored "
                    f"{score}/{total_questions}."
                )

            elif percentage >= 50:

                st.info(
                    f"👍 Good effort! "
                    f"You scored "
                    f"{score}/{total_questions}."
                )

            else:

                st.warning(
                    f"💪 Keep practicing! "
                    f"You scored "
                    f"{score}/{total_questions}."
                )

            st.progress(
                percentage / 100
            )

            # =================================================
            # ANSWER REVIEW
            # =================================================

            st.markdown(
                "<div class='dashboard-space'></div>",
                unsafe_allow_html=True
            )

            st.markdown(
                "### 📋 Answer Review"
            )

            for index, question in enumerate(
                st.session_state.quiz
            ):

                correct_answer = (
                    question["answer"]
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"**Question {index + 1}**"
                    )

                    st.write(
                        question["question"]
                    )

                    st.markdown(
                        f"**Correct answer:** "
                        f"{correct_answer}"
                    )

            # =================================================
            # NEW QUIZ
            # =================================================

            st.markdown(
                "<div class='dashboard-space'></div>",
                unsafe_allow_html=True
            )

            if st.button(
                "🔄 Create New Quiz",
                use_container_width=True,
                key="new_quiz_button"
            ):

                # Remove current quiz state

                for key in [
                    "quiz",
                    "quiz_topic",
                    "quiz_difficulty",
                    "quiz_submitted",
                    "quiz_score",
                    "quiz_percentage",
                    "quiz_saved"
                ]:

                    if key in st.session_state:

                        del st.session_state[key]

                st.rerun()


# ============================================================
# STUDY PLANNER
# ============================================================

# STUDY PLANNER
# ============================================================

elif page == "📅 Study Planner":

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
        <div class="dashboard-eyebrow">
            AI-POWERED STUDY PLANNING
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title(
        "Study Planner 📅"
    )

    st.markdown(
        """
        <div class="dashboard-subtitle">
            Build a personalized study schedule based on
            your subjects, priorities, available time, and exam date.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )

    # ========================================================
    # SUBJECTS
    # ========================================================

    with st.container(border=True):

        st.markdown(
            "### 📚 Your Subjects"
        )

        st.caption(
            "Enter the subjects you want to include in your plan."
        )

        subjects_input = st.text_input(
            "Subjects",
            placeholder=(
                "Example: Python, Machine Learning, "
                "Data Engineering, Statistics"
            ),
            label_visibility="collapsed"
        )

    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )

    # ========================================================
    # EXAM + STUDY TIME
    # ========================================================

    with st.container(border=True):

        st.markdown(
            "### 📅 Study Schedule"
        )

        col1, col2 = st.columns(2)

        with col1:

            exam_date = st.date_input(
                "Exam date"
            )

        with col2:

            daily_hours = st.slider(
                "⏱️ Study hours per day",
                min_value=1,
                max_value=12,
                value=3
            )

        study_days = st.slider(
            "📆 Number of days available",
            min_value=1,
            max_value=60,
            value=7
        )

    # ========================================================
    # SUBJECT PRIORITIES
    # ========================================================

    subjects = [
        subject.strip()
        for subject in subjects_input.split(",")
        if subject.strip()
    ]

    priorities = {}

    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(
            "### 🎯 Subject Priorities"
        )

        if subjects:

            st.caption(
                "Set the importance of each subject."
            )

            priority_columns = st.columns(
                min(len(subjects), 3)
            )

            for index, subject in enumerate(subjects):

                with priority_columns[
                    index % len(priority_columns)
                ]:

                    priorities[subject] = st.selectbox(
                        subject,
                        [
                            "High",
                            "Medium",
                            "Low"
                        ],
                        key=f"priority_{subject}"
                    )

        else:

            st.info(
                "Enter your subjects above to set priorities."
            )

    # ========================================================
    # GENERATE PLAN
    # ========================================================

    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )

    if st.button(
        "🚀 Generate Study Plan",
        use_container_width=True,
        key="generate_study_plan_button"
    ):

        if not subjects:

            st.warning(
                "⚠️ Please enter at least one subject."
            )

        else:

            with st.spinner(
                "🤖 Creating your study plan..."
            ):

                try:

                    plan = generate_study_plan(
                        subjects=subjects,
                        exam_date=str(exam_date),
                        daily_hours=daily_hours,
                        study_days=study_days,
                        priorities=priorities
                    )

                    st.session_state.study_plan = plan

                    st.rerun()

                except Exception as error:

                    st.error(
                        "❌ The AI could not create "
                        "your study plan."
                    )

                    st.caption(
                        f"Technical details: {error}"
                    )

    # ========================================================
    # GENERATED PLAN
    # ========================================================

    if "study_plan" in st.session_state:

        st.markdown(
            "<div class='dashboard-space'></div>",
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(
                "### 🗓️ Your Personalized Study Plan"
            )

            st.markdown(
                st.session_state.study_plan
            )

        st.markdown(
            "<div class='dashboard-space'></div>",
            unsafe_allow_html=True
        )

        st.success(
            "✅ Study plan generated successfully!"
        )

        if st.button(
            "🔄 Create New Study Plan",
            use_container_width=True,
            key="new_study_plan_button"
        ):

            st.session_state.pop(
                "study_plan",
                None
            )

            st.rerun()


# ============================================================
# NOTES ASSISTANT — RAG + CHAT + QUIZ
# ============================================================

elif page == "📚 Notes Assistant":

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
        <div class="dashboard-eyebrow">
            AI-POWERED NOTES WORKSPACE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title(
        "Notes Assistant 📚"
    )

    st.markdown(
        """
        <div class="dashboard-subtitle">
            Upload your study material, ask questions from
            your notes, create revision summaries, and test
            yourself with AI-generated quizzes.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )

    # ========================================================
    # PDF UPLOAD
    # ========================================================

    with st.container(border=True):

        st.markdown(
            "### 📄 Study Material"
        )

        st.caption(
            "Upload a PDF to create your personal AI notes workspace."
        )

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            label_visibility="collapsed"
        )

    # ========================================================
    # PROCESS PDF
    # ========================================================

    if uploaded_file is not None:

        if (
            "notes_file_name"
            not in st.session_state
            or
            st.session_state.notes_file_name
            != uploaded_file.name
        ):

            with st.spinner(
                "📖 Reading your notes..."
            ):

                try:

                    extracted_text = (
                        extract_text_from_pdf(
                            uploaded_file
                        )
                    )

                    if not extracted_text.strip():

                        st.error(
                            "❌ No readable text was "
                            "found in this PDF."
                        )

                    else:

                        st.session_state.notes_text = (
                            extracted_text
                        )

                        st.session_state.notes_file_name = (
                            uploaded_file.name
                        )

                        with st.spinner(
                            "🧠 Preparing notes for faster questions..."
                        ):

                            notes_index = (
                                create_notes_index(
                                    extracted_text
                                )
                            )

                        st.session_state.notes_index = (
                            notes_index
                        )

                        # Reset notes workspace

                        st.session_state.notes_chat = []

                        st.session_state.notes_question_count = 0

                        st.session_state.notes_summary = None

                        st.session_state.notes_quiz = None

                        st.session_state.notes_quiz_submitted = False

                        st.session_state.notes_quiz_score = None

                        st.success(
                            "✅ Notes loaded and indexed!"
                        )

                except Exception as error:

                    st.error(
                        "❌ Could not process the PDF."
                    )

                    st.caption(
                        f"Technical details: {error}"
                    )

        # ====================================================
        # NOTES READY
        # ====================================================

        if "notes_index" in st.session_state:

            st.markdown(
                "<div class='dashboard-space'></div>",
                unsafe_allow_html=True
            )

            with st.container(border=True):

                st.markdown(
                    "### 📖 Notes Ready"
                )

                st.caption(
                    f"File: {st.session_state.notes_file_name}"
                )

                # --------------------------------------------
                # NOTE STATISTICS
                # --------------------------------------------

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.metric(
                        "Characters",
                        f"{len(st.session_state.notes_text):,}"
                    )

                with c2:

                    st.metric(
                        "Text Chunks",
                        len(st.session_state.notes_index)
                    )

                with c3:

                    st.metric(
                        "Questions",
                        st.session_state.notes_question_count
                    )

            # =================================================
            # QUICK ACTIONS
            # =================================================

            st.markdown(
                "<div class='dashboard-space'></div>",
                unsafe_allow_html=True
            )

            with st.container(border=True):

                st.markdown(
                    "### ⚡ Quick Actions"
                )

                st.caption(
                    "Use your notes for revision or testing."
                )

                action1, action2, action3 = st.columns(3)

                with action1:

                    summarize_button = st.button(
                        "📝 Summarize",
                        use_container_width=True,
                        key="notes_summarize_button"
                    )

                with action2:

                    generate_notes_quiz_button = st.button(
                        "🧠 Generate Quiz",
                        use_container_width=True,
                        key="notes_generate_quiz_button"
                    )

                with action3:

                    clear_chat_button = st.button(
                        "🗑️ Clear Chat",
                        use_container_width=True,
                        key="notes_clear_chat_button"
                    )

            # =================================================
            # CLEAR CHAT
            # =================================================

            if clear_chat_button:

                st.session_state.notes_chat = []

                st.session_state.notes_question_count = 0

                st.rerun()

            # =================================================
            # SUMMARY
            # =================================================

            if summarize_button:

                with st.spinner(
                    "🤖 Creating revision summary..."
                ):

                    try:

                        summary = summarize_notes(
                            st.session_state.notes_text
                        )

                        st.session_state.notes_summary = (
                            summary
                        )

                    except Exception as error:

                        st.error(
                            "❌ Could not generate "
                            "the summary."
                        )

                        st.caption(
                            f"Technical details: {error}"
                        )

            if st.session_state.get(
                "notes_summary"
            ):

                st.markdown(
                    "<div class='dashboard-space'></div>",
                    unsafe_allow_html=True
                )

                with st.container(border=True):

                    st.markdown(
                        "### 📝 Revision Summary"
                    )

                    st.markdown(
                        st.session_state.notes_summary
                    )

            # =================================================
            # GENERATE NOTES QUIZ
            # =================================================

            if generate_notes_quiz_button:

                with st.spinner(
                    "🤖 Creating a quiz from your notes..."
                ):

                    try:

                        notes_quiz = (
                            generate_quiz_from_notes(
                                st.session_state.notes_index,
                                number_of_questions=5,
                                difficulty="Medium"
                            )
                        )

                        if validate_quiz(
                            notes_quiz,
                            5
                        ):

                            shuffled_quiz = []

                            for question in notes_quiz:

                                new_question = (
                                    question.copy()
                                )

                                new_question["options"] = (
                                    question["options"].copy()
                                )

                                random.shuffle(
                                    new_question["options"]
                                )

                                shuffled_quiz.append(
                                    new_question
                                )

                            st.session_state.notes_quiz = (
                                shuffled_quiz
                            )

                            st.session_state.notes_quiz_submitted = (
                                False
                            )

                            st.session_state.notes_quiz_score = (
                                None
                            )

                            st.rerun()

                        else:

                            st.error(
                                "❌ The AI generated an "
                                "invalid quiz. Please try again."
                            )

                    except Exception as error:

                        st.error(
                            "❌ Could not generate "
                            "the notes quiz."
                        )

                        st.caption(
                            f"Technical details: {error}"
                        )

            # =================================================
            # NOTES QUIZ
            # =================================================

            if st.session_state.get(
                "notes_quiz"
            ):

                st.markdown(
                    "<div class='dashboard-space'></div>",
                    unsafe_allow_html=True
                )

                with st.container(border=True):

                    st.markdown(
                        "### 📝 Quiz From Your Notes"
                    )

                    st.caption(
                        "Questions are generated directly "
                        "from your uploaded study material."
                    )

                notes_answers = []

                for index, question in enumerate(
                    st.session_state.notes_quiz
                ):

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"**Question {index + 1} "
                            f"of {len(st.session_state.notes_quiz)}**"
                        )

                        st.write(
                            question["question"]
                        )

                        selected_answer = st.radio(
                            "Choose your answer:",
                            question["options"],
                            key=f"notes_quiz_question_{index}"
                        )

                        notes_answers.append(
                            selected_answer
                        )

                # ------------------------------------------------
                # SUBMIT NOTES QUIZ
                # ------------------------------------------------

                if not st.session_state.get(
                    "notes_quiz_submitted",
                    False
                ):

                    if st.button(
                        "✅ Submit Notes Quiz",
                        use_container_width=True,
                        key="submit_notes_quiz_button"
                    ):

                        score = 0

                        for index, question in enumerate(
                            st.session_state.notes_quiz
                        ):

                            if (
                                notes_answers[index]
                                == question["answer"]
                            ):

                                score += 1

                        total_questions = len(
                            st.session_state.notes_quiz
                        )

                        st.session_state.notes_quiz_score = (
                            score
                        )

                        st.session_state.notes_quiz_submitted = (
                            True
                        )

                        # ----------------------------------------
                        # SAVE NOTES QUIZ
                        # ----------------------------------------

                        save_quiz_result(
                            topic=(
                                "Notes: "
                                +
                                st.session_state.notes_file_name
                            ),
                            difficulty="Medium",
                            score=score,
                            total_questions=total_questions
                        )

                        st.rerun()

                # =================================================
                # NOTES QUIZ RESULT
                # =================================================

                if st.session_state.get(
                    "notes_quiz_submitted",
                    False
                ):

                    score = (
                        st.session_state.notes_quiz_score
                    )

                    total_questions = len(
                        st.session_state.notes_quiz
                    )

                    percentage = (
                        score
                        /
                        total_questions
                    ) * 100

                    st.markdown(
                        "<div class='dashboard-space'></div>",
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        "### 🏆 Notes Quiz Result"
                    )

                    col1, col2 = st.columns(
                        [3, 1]
                    )

                    with col1:

                        if percentage >= 80:

                            st.success(
                                f"🎉 Excellent! "
                                f"You scored "
                                f"{score}/{total_questions}."
                            )

                        elif percentage >= 50:

                            st.info(
                                f"👍 Good job! "
                                f"You scored "
                                f"{score}/{total_questions}."
                            )

                        else:

                            st.warning(
                                f"💪 Keep revising! "
                                f"You scored "
                                f"{score}/{total_questions}."
                            )

                    with col2:

                        st.metric(
                            "Score",
                            f"{percentage:.0f}%"
                        )

                    st.progress(
                        percentage / 100
                    )

            # =================================================
            # NOTES CHAT
            # =================================================

            st.markdown(
                "<div class='dashboard-space'></div>",
                unsafe_allow_html=True
            )

            with st.container(border=True):

                st.markdown(
                    "### 💬 Ask Your Notes"
                )

                st.caption(
                    "Ask questions and get answers based "
                    "on the uploaded study material."
                )

                for message in (
                    st.session_state.notes_chat
                ):

                    with st.chat_message(
                        message["role"]
                    ):

                        st.write(
                            message["content"]
                        )

            # ------------------------------------------------
            # NOTES CHAT INPUT
            # ------------------------------------------------

            question = st.chat_input(
                "Ask a question about your notes...",
                key="notes_chat_input"
            )

            if question:

                st.session_state.notes_chat.append(
                    {
                        "role": "user",
                        "content": question
                    }
                )

                with st.chat_message(
                    "user"
                ):

                    st.write(
                        question
                    )

                with st.chat_message(
                    "assistant"
                ):

                    with st.spinner(
                        "🤖 Searching your notes..."
                    ):

                        try:
                            result = ask_about_notes(
                                st.session_state.notes_text,
                                question,
                                st.session_state.notes_index
                            )

                            answer = result["answer"]
                        except Exception as error:

                            answer = (
                                "I couldn't answer that "
                                "from your notes."
                            )

                            st.caption(
                                f"Technical details: {error}"
                            )

                    st.write(
                        answer
                    )

                st.session_state.notes_chat.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                st.session_state.notes_question_count += 1

    else:

        st.markdown(
            "<div class='dashboard-space'></div>",
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(
                "### 📄 No notes loaded"
            )

            st.write(
                "Upload a PDF above to start asking "
                "questions, creating summaries, and "
                "generating quizzes from your study material."
            )


# ============================================================
# PROGRESS DASHBOARD
# ============================================================

elif page == "📊 Progress":

    from modules.progress import show_progress

    show_progress()