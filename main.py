# main_part1 

import io
from io import BytesIO
import streamlit as st
from huggingface_hub import InferenceClient
import config

# Switch provider by changing the import line:
from groq import generate_response
# from hf import generate_response


MATH_SYSTEM = """You are a Math Mastermind.
Solve with clear step-by-step reasoning, correct notation, and a final answer.
Verify when possible; mention an alternative method briefly if relevant."""


CHAT_CSS = """
<style>
.wrap {
    max-height: 520px;
    overflow-y: auto;
    padding-right: 6px;
}

.card {
    border:1px solid #e6e6e6;
    background:#fff;
    border-radius:10px;
    padding:14px 16px;
    margin:10px 0;
    box-shadow:0 1px 2px rgba(0,0,0,0.04);
}

.q {
    font-weight:700;
    color:#0a6ebd;
    margin-bottom:8px;
}

.meta {
    display:inline-block;
    background:#FF9800;
    color:#fff;
    padding:2px 8px;
    border-radius:12px;
    font-size:12px;
    margin-left:8px;
}

.a {
    white-space:pre-wrap;
    color:#333;
    line-height:1.5;
}
</style>
"""


def export_txt(history):
    txt = "".join(
        [f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n"
         for i, h in enumerate(history, 1)]
    )
    bio = io.BytesIO(txt.encode("utf-8"))
    bio.seek(0)
    return bio


def teaching_answer(q: str) -> str:
    return generate_response(
        q,
        temperature=0.3,
        max_tokens=1024
    )


def math_answer(q: str, level: str) -> str:
    prompt = f"""
{MATH_SYSTEM}

Difficulty: {level}

Math Problem:
{q}
"""
    return generate_response(
        prompt,
        temperature=0.1,
        max_tokens=1024
    )


def run_ai_teaching_assistant():

    st.title("🤖 AI Teaching Assistant")
    st.caption("Ask questions and learn with an AI-powered tutor.")

    st.info("""
💡 Example questions:
- Explain photosynthesis
- What caused World War 2?
- How does gravity work?
""")

    st.session_state.setdefault("history_ata", [])

    c1, c2 = st.columns([1,2])

    if c1.button("🧹 Clear", key="c_ata"):
        st.session_state.history_ata = []
        st.rerun()

    if st.session_state.history_ata:
        c2.download_button(
            "📄 Export",
            export_txt(st.session_state.history_ata),
            "AI_Teaching_Assistant_Conversation.txt",
            "text/plain"
        )

    q = st.text_input(
        "💬 Enter your question:",
        key="q_ata"
    )

    if st.button("🚀 Ask AI", key="a_ata"):

        if not q.strip():
            st.warning("⚠️ Enter a question.")

        else:
            with st.spinner("Thinking..."):
                answer = teaching_answer(q.strip())

                st.session_state.history_ata.append(
                    {
                        "question": q.strip(),
                        "answer": answer
                    }
                )

            st.success("✅ Answer generated!")
            st.rerun()


    if not st.session_state.history_ata:
        return


    st.caption(
        f"Questions Asked: {len(st.session_state.history_ata)}"
    )

    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    html = '<div class="wrap">'

    for i, qa in enumerate(
        st.session_state.history_ata, 1
    ):
        html += (
            f'<div class="card">'
            f'<div class="q">Q{i}: {qa["question"]}</div>'
            f'<div class="a">{qa["answer"]}</div>'
            f'</div>'
        )

    st.markdown(
        html + "</div>",
        unsafe_allow_html=True
    )


def run_math_mastermind():

    st.title("🧮 Math Mastermind")
    st.caption("Solve math problems with step-by-step explanations.")

    st.info("""
💡 Example problems:
- Solve 2x + 5 = 15
- Find the area of a circle
- Simplify √144
""")

    st.session_state.setdefault(
        "history_mm",
        []
    )

    st.session_state.setdefault(
        "k_mm",
        0
    )


    c1, c2 = st.columns([1,2])


    if c1.button("🧹 Clear", key="c_mm"):
        st.session_state.history_mm = []
        st.rerun()


    if st.session_state.history_mm:
        c2.download_button(
            "📄 Export",
            export_txt(st.session_state.history_mm),
            "Math_Mastermind_Solutions.txt",
            "text/plain"
        )


    with st.form(
        "mm_form",
        clear_on_submit=True
    ):

        q = st.text_area(
            "📝 Math problem:",
            height=100,
            key=f"mm_{st.session_state.k_mm}"
        )


        a,b = st.columns([3,1])

        go = a.form_submit_button(
            "🚀 Solve",
            use_container_width=True
        )

        lvl = b.selectbox(
            "Level",
            [
                "Basic",
                "Intermediate",
                "Advanced"
            ],
            index=1
        )


        if go:

            if not q.strip():

                st.warning(
                    "⚠️ Enter a problem."
                )

            else:

                with st.spinner(
                    "Solving..."
                ):

                    ans = math_answer(
                        q.strip(),
                        lvl
                    )


                st.session_state.history_mm.insert(
                    0,
                    {
                        "question":q.strip(),
                        "answer":ans,
                        "difficulty":lvl
                    }
                )

                st.success(
                    "✅ Solution completed!"
                )

                st.session_state.k_mm += 1

                st.rerun()


    if not st.session_state.history_mm:
        return


    st.caption(
        f"Problems Solved: {len(st.session_state.history_mm)}"
    )


    st.markdown(
        CHAT_CSS,
        unsafe_allow_html=True
    )


    html='<div class="wrap">'


    for i,qa in enumerate(
        st.session_state.history_mm,
        1
    ):

        html += (
            f'<div class="card">'
            f'<div class="q">Q{i}: {qa["question"]}'
            f'<span class="meta">{qa["difficulty"]}</span>'
            f'</div>'
            f'<div class="a">{qa["answer"]}</div>'
            f'</div>'
        )


    st.markdown(
        html+"</div>",
        unsafe_allow_html=True
    )


def run_safe_ai_image_generator():

    st.info(
        "🖼️ Safe AI Image Generator will be available after Part 2 is added."
    )


def main():

    st.set_page_config(
        page_title="AI Learning Hub",
        page_icon="🎓"
    )


    st.sidebar.title(
        "🎓 AI Learning Hub"
    )

    st.sidebar.write(
        "Choose an AI-powered learning tool:"
    )


    opt = st.sidebar.radio(
        "",
        [
            "🤖 AI Teaching Assistant",
            "🧮 Math Mastermind",
            "🖼️ Safe AI Image Generator"
        ]
    )


    st.sidebar.divider()


    with st.sidebar.expander(
        "ℹ About"
    ):

        st.write("""
This app includes:

🤖 AI tutor

🧮 Math solver

🖼️ AI image generator

Built with Streamlit and AI.
""")


    if opt == "🤖 AI Teaching Assistant":
        run_ai_teaching_assistant()

    elif opt == "🧮 Math Mastermind":
        run_math_mastermind()

    else:
        run_safe_ai_image_generator()


    st.divider()

    st.caption(
        "✨ Created with Streamlit + AI"
    )


if __name__ == "__main__":
    main()