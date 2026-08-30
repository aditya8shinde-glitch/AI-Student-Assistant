import streamlit as st

from modules.database import get_quiz_results


# ============================================================
# PROGRESS STYLES
# ============================================================

def load_progress_styles():

    st.markdown(
        """
        <style>

        /* ==================================================
           PROGRESS PAGE
           ================================================== */

        .progress-eyebrow {
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 1.1px;
            color: #718096;
            margin-bottom: 5px;
            text-transform: uppercase;
        }

        .progress-subtitle {
            color: #64748B;
            font-size: 0.88rem;
            line-height: 1.4;
            max-width: 720px;
        }

        .progress-space {
            height: 16px;
        }

        .progress-section-title {
            color: #17233B;
            font-size: 1.08rem;
            font-weight: 720;
            margin-bottom: 7px;
        }

        .progress-small {
            color: #64748B;
            font-size: 0.72rem;
        }

        /* ==================================================
           CARDS
           ================================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {

            border-radius: 12px !important;

            border: 1px solid #E2E8F0 !important;

            background: #FFFFFF !important;

            box-shadow:
                0 2px 10px
                rgba(15, 23, 42, 0.025) !important;
        }

        /* ==================================================
           METRICS
           ================================================== */

        [data-testid="stMetricLabel"] {

            font-size: 0.72rem !important;

            color: #64748B !important;
        }

        [data-testid="stMetricValue"] {

            font-size: 1.45rem !important;

            font-weight: 750 !important;

            color: #17233B !important;
        }

        /* ==================================================
           PROGRESS BARS
           ================================================== */

        div[data-testid="stProgress"] > div {

            height: 7px;

            border-radius: 999px;
        }

        /* ==================================================
           CHART
           ================================================== */

        [data-testid="stArrowVegaLiteChart"] {

            border-radius: 12px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION TITLE
# ============================================================

def section_title(icon, title):

    st.markdown(
        f"""
        <div class="progress-section-title">
            {icon} {title}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GET PROGRESS RESULTS
# ============================================================

def get_progress_results():

    return get_quiz_results()


# ============================================================
# CALCULATE TOPIC STATISTICS
# ============================================================

def calculate_topic_stats(results):

    topic_data = {}

    for result in results:

        if len(result) < 6:
            continue

        topic = str(result[0])

        try:
            percentage = float(result[4])
        except (TypeError, ValueError):
            percentage = 0

        if topic not in topic_data:

            topic_data[topic] = {
                "scores": [],
                "attempts": 0
            }

        topic_data[topic]["scores"].append(
            percentage
        )

        topic_data[topic]["attempts"] += 1

    topic_stats = []

    for topic, data in topic_data.items():

        scores = data["scores"]

        average = (
            sum(scores) / len(scores)
            if scores
            else 0
        )

        topic_stats.append(
            {
                "topic": topic,
                "average": round(average),
                "attempts": data["attempts"]
            }
        )

    topic_stats.sort(
        key=lambda item: item["average"],
        reverse=True
    )

    return topic_stats


# ============================================================
# PROGRESS DASHBOARD
# ============================================================

def show_progress():

    load_progress_styles()

    results = get_progress_results()

    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        """
        <div class="progress-eyebrow">
            LEARNING ANALYTICS
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title(
        "Your Progress 📊"
    )

    st.markdown(
        """
        <div class="progress-subtitle">
            Track your quiz performance, identify strengths,
            and understand where you can improve.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not results:

        st.markdown(
            "<div class='progress-space'></div>",
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.subheader(
                "📚 Your learning journey starts here"
            )

            st.write(
                "Complete your first quiz and your "
                "performance statistics will appear here."
            )

        return

    # ========================================================
    # CALCULATE STATISTICS
    # ========================================================

    total_quizzes = len(results)

    total_questions = sum(
        int(result[3])
        for result in results
    )

    total_correct = sum(
        int(result[2])
        for result in results
    )

    percentages = [
        float(result[4])
        for result in results
    ]

    average_score = (
        sum(percentages)
        /
        len(percentages)
    )

    best_score = max(
        percentages
    )

    accuracy = (
        (
            total_correct
            /
            total_questions
        )
        * 100
        if total_questions > 0
        else 0
    )

    # ========================================================
    # PERFORMANCE OVERVIEW
    # ========================================================

    st.markdown(
        "<div class='progress-space'></div>",
        unsafe_allow_html=True
    )

    section_title(
        "📈",
        "Performance Overview"
    )

    c1, c2, c3, c4 = st.columns(4)

    # --------------------------------------------------------
    # QUIZZES
    # --------------------------------------------------------

    with c1:

        with st.container(border=True):

            st.markdown(
                "📚"
            )

            st.metric(
                "Quizzes",
                total_quizzes
            )

            st.caption(
                "Completed"
            )

    # --------------------------------------------------------
    # AVERAGE
    # --------------------------------------------------------

    with c2:

        with st.container(border=True):

            st.markdown(
                "🎯"
            )

            st.metric(
                "Average",
                f"{average_score:.0f}%"
            )

            st.caption(
                "Overall performance"
            )

    # --------------------------------------------------------
    # BEST SCORE
    # --------------------------------------------------------

    with c3:

        with st.container(border=True):

            st.markdown(
                "🏆"
            )

            st.metric(
                "Best Score",
                f"{best_score:.0f}%"
            )

            st.caption(
                "Highest result"
            )

    # --------------------------------------------------------
    # ACCURACY
    # --------------------------------------------------------

    with c4:

        with st.container(border=True):

            st.markdown(
                "✓"
            )

            st.metric(
                "Accuracy",
                f"{accuracy:.0f}%"
            )

            st.caption(
                f"{total_correct}/{total_questions} correct"
            )

    # ========================================================
    # PERFORMANCE TREND
    # ========================================================

    st.markdown(
        "<div class='progress-space'></div>",
        unsafe_allow_html=True
    )

    section_title(
        "📈",
        "Performance Trend"
    )

    chronological = list(
        reversed(results)
    )

    trend_scores = []

    for index, result in enumerate(
        chronological,
        start=1
    ):

        try:

            score = float(
                result[4]
            )

        except (TypeError, ValueError):

            score = 0

        trend_scores.append(
            {
                "Quiz": index,
                "Score": score
            }
        )

    if trend_scores:

        with st.container(border=True):

            st.line_chart(
                trend_scores,
                x="Quiz",
                y="Score",
                height=220
            )

            st.caption(
                "Your score progression across completed quizzes."
            )

    # ========================================================
    # STRENGTHS + AREAS TO IMPROVE
    # ========================================================

    topic_stats = calculate_topic_stats(
        results
    )

    if topic_stats:

        st.markdown(
            "<div class='progress-space'></div>",
            unsafe_allow_html=True
        )

        left, right = st.columns(2)

        # ----------------------------------------------------
        # STRONGEST
        # ----------------------------------------------------

        with left:

            section_title(
                "🏆",
                "Strongest Topics"
            )

            strongest = topic_stats[:3]

            with st.container(border=True):

                for topic in strongest:

                    st.markdown(
                        f"**{topic['topic']}**"
                    )

                    st.progress(
                        min(
                            topic["average"],
                            100
                        ) / 100
                    )

                    st.caption(
                        f"{topic['average']}% average • "
                        f"{topic['attempts']} attempt(s)"
                    )

        # ----------------------------------------------------
        # WEAKNESSES
        # ----------------------------------------------------

        with right:

            section_title(
                "🎯",
                "Areas to Improve"
            )

            weakest = sorted(
                topic_stats,
                key=lambda x: x["average"]
            )[:3]

            with st.container(border=True):

                for topic in weakest:

                    st.markdown(
                        f"**{topic['topic']}**"
                    )

                    st.progress(
                        min(
                            topic["average"],
                            100
                        ) / 100
                    )

                    st.caption(
                        f"{topic['average']}% average • "
                        f"{topic['attempts']} attempt(s)"
                    )

    # ========================================================
    # QUIZ HISTORY
    # ========================================================

    st.markdown(
        "<div class='progress-space'></div>",
        unsafe_allow_html=True
    )

    section_title(
        "📚",
        "Quiz History"
    )

    with st.container(border=True):

        for index, result in enumerate(
            results
        ):

            if len(result) < 6:
                continue

            (
                topic,
                difficulty,
                score,
                total,
                percentage,
                completed_at
            ) = result

            if index > 0:

                st.divider()

            col1, col2, col3 = st.columns(
                [3.2, 1.2, 1]
            )

            with col1:

                st.markdown(
                    f"**{topic}**"
                )

                st.caption(
                    str(completed_at)
                )

            with col2:

                st.write(
                    str(difficulty)
                )

                st.caption(
                    f"{score}/{total}"
                )

            with col3:

                st.metric(
                    "Score",
                    f"{float(percentage):.0f}%"
                )

    # ========================================================
    # LEARNING SUMMARY
    # ========================================================

    st.markdown(
        "<div class='progress-space'></div>",
        unsafe_allow_html=True
    )

    section_title(
        "🧠",
        "Learning Summary"
    )

    with st.container(border=True):

        st.write(
            f"You have completed **{total_quizzes} quizzes**, "
            f"answered **{total_questions} questions**, "
            f"and answered **{total_correct} correctly**."
        )

        if average_score >= 80:

            st.success(
                "🌟 Excellent performance! "
                "Keep challenging yourself."
            )

        elif average_score >= 60:

            st.info(
                "👍 You're making good progress. "
                "Keep practicing your weaker topics."
            )

        else:

            st.warning(
                "💪 Keep practicing regularly. "
                "Consistency will help improve your score."
            )