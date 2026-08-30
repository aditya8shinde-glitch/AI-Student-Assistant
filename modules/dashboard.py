import streamlit as st
from pathlib import Path
from datetime import datetime


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

HERO_BOOKS = ASSETS_DIR / "hero_books.png"
LEARNING_ART = ASSETS_DIR / "learning_art.png"


# ============================================================
# DATABASE RESULTS
# ============================================================

def get_dashboard_results():

    try:

        from modules.database import get_quiz_results

        results = get_quiz_results()

        if results is None:
            return []

        return results

    except Exception:

        return []


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def get_dashboard_stats():

    results = get_dashboard_results()

    if not results:

        return {
            "quizzes": 0,
            "average": 0,
            "best": 0,
            "questions": 0,
            "correct": 0,
            "accuracy": 0,
            "recent": []
        }

    total_quizzes = len(results)

    total_questions = 0
    total_correct = 0

    percentages = []
    recent = []

    for row in results:

        if len(row) < 6:
            continue

        (
            topic,
            difficulty,
            score,
            questions,
            percentage,
            completed_at
        ) = row

        try:
            score = int(score)
        except (TypeError, ValueError):
            score = 0

        try:
            questions = int(questions)
        except (TypeError, ValueError):
            questions = 0

        try:
            percentage = float(percentage)
        except (TypeError, ValueError):
            percentage = 0

        total_questions += questions
        total_correct += score
        percentages.append(percentage)

        date_text = str(completed_at)

        try:

            date_object = datetime.strptime(
                date_text,
                "%Y-%m-%d %H:%M:%S"
            )

            date_text = date_object.strftime(
                "%d %b %Y"
            )

        except Exception:

            pass

        recent.append(
            {
                "topic": str(topic),
                "difficulty": str(difficulty),
                "score": round(percentage),
                "correct": score,
                "questions": questions,
                "date": date_text
            }
        )

    if percentages:

        average = round(
            sum(percentages) / len(percentages)
        )

        best = round(
            max(percentages)
        )

    else:

        average = 0
        best = 0

    if total_questions > 0:

        accuracy = round(
            (
                total_correct
                /
                total_questions
            ) * 100
        )

    else:

        accuracy = 0

    return {
        "quizzes": total_quizzes,
        "average": average,
        "best": best,
        "questions": total_questions,
        "correct": total_correct,
        "accuracy": accuracy,
        "recent": recent[:3]
    }


# ============================================================
# DASHBOARD STYLES
# ============================================================

def load_dashboard_styles():

    st.markdown(
        """
        <style>

        /* ====================================================
           MAIN DASHBOARD
           ==================================================== */

        .dashboard-eyebrow {

            font-size: 0.72rem;

            font-weight: 800;

            letter-spacing: 1.15px;

            color: #6558D8;

            margin-bottom: 7px;
        }


        .dashboard-hero-title {

            color: #132D5B;

            font-size: 2.45rem;

            font-weight: 800;

            line-height: 1.08;

            letter-spacing: -1.2px;

            margin-top: 3px;

            margin-bottom: 10px;
        }


        .dashboard-subtitle {

            color: #60708C;

            font-size: 0.91rem;

            line-height: 1.5;
        }


        .dashboard-space {

            height: 12px;
        }


        .dashboard-space-large {

            height: 20px;
        }


        /* ====================================================
           METRIC CARDS
           ==================================================== */

        .reference-metric-card {

            min-height: 132px;

            padding: 18px 18px 15px 18px;

            border-radius: 14px;

            border: 1px solid #E2E7F0;

            box-shadow:
                0 4px 16px
                rgba(23, 45, 91, 0.045);

            box-sizing: border-box;
        }


        .metric-purple {

            background:
                linear-gradient(
                    135deg,
                    #FBF9FF 0%,
                    #F5F1FF 100%
                );

            border-color: #E8E0FF;
        }


        .metric-blue {

            background:
                linear-gradient(
                    135deg,
                    #FAFCFF 0%,
                    #EEF6FF 100%
                );

            border-color: #DDEBFA;
        }


        .metric-yellow {

            background:
                linear-gradient(
                    135deg,
                    #FFFEFB 0%,
                    #FFF7E9 100%
                );

            border-color: #F6E6C7;
        }


        .metric-green {

            background:
                linear-gradient(
                    135deg,
                    #FBFFFD 0%,
                    #EEF9F3 100%
                );

            border-color: #DCEFE5;
        }


        .metric-top {

            display: flex;

            align-items: center;

            gap: 10px;

            margin-bottom: 9px;
        }


        .metric-icon-circle {

            width: 38px;

            height: 38px;

            border-radius: 50%;

            display: flex;

            align-items: center;

            justify-content: center;

            font-size: 1.15rem;

            flex-shrink: 0;
        }


        .icon-purple {

            background: #E8DFFF;

        }


        .icon-blue {

            background: #DDEBFF;

        }


        .icon-yellow {

            background: #FFECC8;

        }


        .icon-green {

            background: #D9F0E2;

        }


        .metric-label {

            color: #172F5F;

            font-size: 0.82rem;

            font-weight: 750;
        }


        .metric-value {

            color: #132D5B;

            font-size: 1.85rem;

            font-weight: 800;

            line-height: 1;

            margin: 2px 0 7px 0;
        }


        .metric-description {

            color: #657590;

            font-size: 0.7rem;
        }


        /* ====================================================
           SECTION TITLES
           ==================================================== */

        .section-title {

            color: #172F5F;

            font-size: 1.08rem;

            font-weight: 800;

            letter-spacing: -0.2px;

            margin-bottom: 8px;
        }


        /* ====================================================
           COLOURED PANEL HEADERS
           ==================================================== */

        .panel-heading {

            display: flex;

            align-items: center;

            gap: 9px;

            color: #172F5F;

            font-size: 1.02rem;

            font-weight: 800;
        }


        .panel-heading-icon {

            width: 34px;

            height: 34px;

            border-radius: 9px;

            display: flex;

            align-items: center;

            justify-content: center;

            font-size: 1rem;
        }


        .panel-purple {

            background: #EEE9FF;
        }


        .panel-green {

            background: #E6F6EC;
        }


        .panel-blue {

            background: #E9F3FF;
        }


        .panel-yellow {

            background: #FFF2D9;
        }


        /* ====================================================
           PERFORMANCE / ACCURACY
           ==================================================== */

        .performance-card {

            border: 1px solid #E3E4F5;

            border-radius: 14px;

            background:
                linear-gradient(
                    135deg,
                    #FFFFFF 0%,
                    #FBF9FF 100%
                );

            padding: 18px;
        }


        .accuracy-card {

            border: 1px solid #F0E0E7;

            border-radius: 14px;

            background:
                linear-gradient(
                    135deg,
                    #FFFFFF 0%,
                    #FFF9FB 100%
                );

            padding: 18px;
        }


        .inner-label {

            color: #66758F;

            font-size: 0.72rem;

            margin-bottom: 6px;
        }


        .large-percentage {

            color: #172F5F;

            font-size: 1.8rem;

            font-weight: 800;

            line-height: 1;

            margin-bottom: 8px;
        }


        .accuracy-percentage {

            color: #D94B69;

            font-size: 1.8rem;

            font-weight: 800;

            line-height: 1;

            margin-bottom: 8px;
        }


        .success-note {

            border-radius: 10px;

            padding: 9px 12px;

            background: #F1EEFF;

            color: #5747B7;

            font-size: 0.72rem;

            font-weight: 600;
        }


        .info-note {

            border-radius: 10px;

            padding: 9px 12px;

            background: #EEF5FF;

            color: #2762A5;

            font-size: 0.72rem;

            font-weight: 600;
        }


        .warning-note {

            border-radius: 10px;

            padding: 9px 12px;

            background: #FFF5E5;

            color: #9B6818;

            font-size: 0.72rem;

            font-weight: 600;
        }


        /* ====================================================
           QUICK ACTION CARDS
           ==================================================== */

        .quick-action-title {

            color: #172F5F;

            font-size: 0.8rem;

            font-weight: 800;

            line-height: 1.25;

            margin-bottom: 4px;
        }


        .quick-action-description {

            color: #64748B;

            font-size: 0.67rem;

            line-height: 1.4;
        }


        /* ====================================================
           LEARNING BANNER
           ==================================================== */

        .learning-title {

            color: #173A34;

            font-size: 0.95rem;

            font-weight: 800;

            margin-bottom: 5px;
        }


        .learning-text {

            color: #61756F;

            font-size: 0.7rem;

            line-height: 1.45;
        }


        /* ====================================================
           STREAMLIT BUTTONS
           ==================================================== */

        .stButton > button {

            min-height: 34px !important;

            height: 34px !important;

            padding: 0 10px !important;

            border-radius: 9px !important;

            border: 1px solid #D9E0EA !important;

            background: #FFFFFF !important;

            color: #172F5F !important;

            font-size: 0.78rem !important;

            font-weight: 700 !important;

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease,
                border-color 0.15s ease;
        }


        .stButton > button:hover {

            border-color: #7567D9 !important;

            background: #F8F6FF !important;

            color: #5D50C6 !important;

            transform: translateY(-1px);

            box-shadow:
                0 4px 10px
                rgba(93, 80, 198, 0.10);
        }


        /* ====================================================
           BORDERED STREAMLIT CONTAINERS
           ==================================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {

            border-radius: 14px !important;

            border: 1px solid #E2E7F0 !important;

            background: #FFFFFF !important;

            box-shadow:
                0 3px 12px
                rgba(23, 45, 91, 0.035) !important;
        }


        /* ====================================================
           PROGRESS
           ==================================================== */

        div[data-testid="stProgress"] {

            margin-top: 4px;

            margin-bottom: 9px;
        }


        div[data-testid="stProgress"] > div {

            height: 7px;

            border-radius: 999px;
        }


        /* ====================================================
           IMAGE SPACING
           ==================================================== */

        [data-testid="stImage"] {

            margin-bottom: 0 !important;
        }


        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# METRIC CARD
# ============================================================

def metric_card(
    icon,
    label,
    value,
    description,
    variant,
    icon_variant
):
    html = (
        f'<div class="reference-metric-card {variant}">'
        f'<div class="metric-top">'
        f'<div class="metric-icon-circle {icon_variant}">{icon}</div>'
        f'<div class="metric-label">{label}</div>'
        f'</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-description">{description}</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )



# ============================================================
# SECTION TITLE
# ============================================================

def section_title(
    icon,
    title
):

    st.markdown(
        f"""
        <div class="section-title">
            {icon} {title}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RECENT QUIZ ACTIVITY
# ============================================================

def show_recent_quizzes(
    recent
):

    section_title(
        "📖",
        "Recent Quiz Activity"
    )

    if not recent:

        with st.container(
            border=True
        ):

            st.caption(
                "No quizzes completed yet."
            )

        return

    with st.container(
        border=True
    ):

        for index, quiz in enumerate(
            recent
        ):

            if index > 0:
                st.divider()

            left, right = st.columns(
                [4, 1]
            )

            with left:

                st.markdown(
                    f"**{quiz['topic']}**"
                )

                st.caption(
                    f"{quiz['difficulty']}  •  "
                    f"{quiz['date']}"
                )

            with right:

                st.markdown(
                    f"**{quiz['score']}%**"
                )

                st.caption(
                    f"{quiz['correct']}/"
                    f"{quiz['questions']}"
                )


# ============================================================
# QUICK ACTION
# ============================================================

def quick_action(
    icon,
    title,
    description,
    page_name,
    key
):

    with st.container(
        border=True
    ):

        col1, col2 = st.columns(
            [5, 1]
        )

        with col1:

            st.markdown(
                f"""
                <div class="quick-action-title">
                    {icon} {title}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="quick-action-description">
                    {description}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            if st.button(
                "→",
                key=key,
                use_container_width=True
            ):

                st.session_state[
                    "dashboard_navigation_target"
                ] = page_name

                st.rerun()


# ============================================================
# QUICK ACTIONS
# ============================================================

def show_quick_actions():

    section_title(
        "⚡",
        "Quick Actions"
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        quick_action(
            "💬",
            "AI Study Chat",
            "Ask questions and learn with AI",
            "💬 AI Study Chat",
            "dashboard_chat_action"
        )

        st.markdown(
            "<div style='height:10px;'></div>",
            unsafe_allow_html=True
        )

        quick_action(
            "📚",
            "Notes Assistant",
            "Ask questions from your study notes",
            "📚 Notes Assistant",
            "dashboard_notes_action"
        )

    with col2:

        quick_action(
            "📝",
            "Quiz Generator",
            "Generate quizzes and test yourself",
            "📝 Quiz Generator",
            "dashboard_quiz_action"
        )

        st.markdown(
            "<div style='height:10px;'></div>",
            unsafe_allow_html=True
        )

        quick_action(
            "📅",
            "Study Planner",
            "Organize your study schedule",
            "📅 Study Planner",
            "dashboard_planner_action"
        )


# ============================================================
# MAIN DASHBOARD
# ============================================================

def show_dashboard():

    load_dashboard_styles()

    stats = get_dashboard_stats()


    # ========================================================
    # HERO
    # ========================================================

    hero_col1, hero_col2 = st.columns(
        [3.5, 1.5]
    )

    with hero_col1:

        st.markdown(
            """
            <div class="dashboard-eyebrow">
                AI-POWERED LEARNING WORKSPACE
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="dashboard-hero-title">
                Welcome back 👋
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="dashboard-subtitle">
                Keep learning, keep improving, and stay
                consistent with your studies.
            </div>
            """,
            unsafe_allow_html=True
        )

    with hero_col2:

        if HERO_BOOKS.exists():

            st.image(
                str(HERO_BOOKS),
                width=460
            )


    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # FOUR METRICS
    # ========================================================

    c1, c2, c3, c4 = st.columns(
        4
    )

    with c1:

        metric_card(
            "📋",
            "Quizzes",
            stats["quizzes"],
            "Attempted",
            "metric-purple",
            "icon-purple"
        )

    with c2:

        metric_card(
            "🎯",
            "Average Score",
            f'{stats["average"]}%',
            "Across all quizzes",
            "metric-blue",
            "icon-blue"
        )

    with c3:

        metric_card(
            "🏆",
            "Best Score",
            f'{stats["best"]}%',
            "Your highest score",
            "metric-yellow",
            "icon-yellow"
        )

    with c4:

        metric_card(
            "❔",
            "Questions",
            stats["questions"],
            "Answered",
            "metric-green",
            "icon-green"
        )


    # ========================================================
    # PERFORMANCE + ACCURACY
    # ========================================================

    st.markdown(
        "<div class='dashboard-space-large'></div>",
        unsafe_allow_html=True
    )

    performance_col, accuracy_col = st.columns(
        [1.4, 1]
    )

    with performance_col:

        st.markdown(
            """
            <div class="panel-heading">
                <div class="panel-heading-icon panel-purple">
                    📈
                </div>
                Overall Performance
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<div style='height:8px;'></div>",
            unsafe_allow_html=True
        )

        with st.container(
            border=True
        ):

            st.markdown(
                '<div class="inner-label">'
                'Current Average'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="large-percentage">'
                f'{stats["average"]}%'
                f'</div>',
                unsafe_allow_html=True
            )

            progress_value = min(
                max(
                    stats["average"],
                    0
                ),
                100
            )

            st.progress(
                progress_value / 100
            )

            if stats["average"] >= 80:

                st.markdown(
                    '<div class="success-note">'
                    '⭐ Excellent performance! Keep pushing.'
                    '</div>',
                    unsafe_allow_html=True
                )

            elif stats["average"] >= 60:

                st.markdown(
                    '<div class="info-note">'
                    '💡 Good progress! Keep practicing.'
                    '</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '<div class="warning-note">'
                    '💪 Keep revising and practicing regularly.'
                    '</div>',
                    unsafe_allow_html=True
                )

    with accuracy_col:

        st.markdown(
            """
            <div class="panel-heading">
                <div class="panel-heading-icon panel-green">
                    🎯
                </div>
                Accuracy
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<div style='height:8px;'></div>",
            unsafe_allow_html=True
        )

        with st.container(
            border=True
        ):

            st.markdown(
                '<div class="inner-label">'
                'Correct Answers'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="accuracy-percentage">'
                f'{stats["accuracy"]}%'
                f'</div>',
                unsafe_allow_html=True
            )

            st.caption(
                f'{stats["correct"]} correct out of '
                f'{stats["questions"]} questions'
            )


    # ========================================================
    # RECENT ACTIVITY + QUICK ACTIONS
    # ========================================================

    st.markdown(
        "<div class='dashboard-space-large'></div>",
        unsafe_allow_html=True
    )

    recent_col, actions_col = st.columns(
        [1.05, 1]
    )

    with recent_col:

        show_recent_quizzes(
            stats["recent"]
        )

    with actions_col:

        show_quick_actions()


    # ========================================================
    # LEARNING BANNER
    # ========================================================

    st.markdown(
        "<div class='dashboard-space'></div>",
        unsafe_allow_html=True
    )

    with st.container(
        border=True
    ):

        learning_col1, learning_col2 = st.columns(
            [3.4, 1]
        )

        with learning_col1:

            st.markdown(
                """
                <div class="learning-title">
                    🎓 Empower Your Learning Journey
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="learning-text">
                    AI Student Assistant brings together
                    AI study help, smart quizzes, notes
                    assistance, and study planning in one
                    focused workspace.
                </div>
                """,
                unsafe_allow_html=True
            )

        with learning_col2:

            if LEARNING_ART.exists():

                st.image(
                    str(LEARNING_ART),
                    width=300
                )
