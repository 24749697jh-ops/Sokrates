from __future__ import annotations

import base64
import mimetypes
import os
import re
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from tutor_prompt import SOKRATES_INSTRUCTIONS

load_dotenv()

APP_TITLE = "Sokrates"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
MAX_FILE_SIZE_MB = 20
SUPPORTED_TYPES = ["pdf", "png", "jpg", "jpeg", "webp", "docx", "txt"]

st.set_page_config(
    page_title="Sokrates – Mathe-Lerncoach",
    page_icon="🧭",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 850px; padding-top: 2rem;}
    .sokrates-card {
        padding: 1.2rem 1.4rem;
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    .motto {font-size: 1.1rem; font-style: italic; opacity: .8;}
    </style>
    """,
    unsafe_allow_html=True,
)


def normalize_math_markdown(text: str) -> str:
    """
    Vereinheitlicht häufige LaTeX-Ausgaben für Streamlit.

    Das Modell soll bereits $...$ und $$...$$ liefern. Diese Funktion ist
    eine zusätzliche Absicherung für Antworten mit \\(...\\) oder \\[...\\].
    """
    if not text:
        return text

    # Abgesetzte Mathematik zuerst umwandeln.
    text = re.sub(
        r"\\\[\s*(.*?)\s*\\\]",
        lambda match: f"\n$$\n{match.group(1).strip()}\n$$\n",
        text,
        flags=re.DOTALL,
    )

    # Inline-Mathematik umwandeln.
    text = re.sub(
        r"\\\(\s*(.*?)\s*\\\)",
        lambda match: f"${match.group(1).strip()}$",
        text,
        flags=re.DOTALL,
    )

    return text


def render_chat_content(content: str) -> None:
    """Zeigt Text und Mathematik in Streamlit-kompatiblem Markdown an."""
    st.markdown(normalize_math_markdown(content))


def reset_session() -> None:
    st.session_state.messages = []
    st.session_state.task_started = False
    st.session_state.task_text = ""
    st.session_state.uploaded_name = None
    st.session_state.uploaded_bytes = None
    st.session_state.uploaded_mime = None


def ensure_state() -> None:
    defaults = {
        "messages": [],
        "task_started": False,
        "task_text": "",
        "uploaded_name": None,
        "uploaded_bytes": None,
        "uploaded_mime": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def data_url(file_bytes: bytes, mime_type: str) -> str:
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def build_first_user_content(task_text: str) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = []

    prompt = (
        "Hier ist meine Mathematikaufgabe. Beginne mit der Phase VERSTEHEN. "
        "Stelle zunächst genau eine hilfreiche Frage. "
        "Rechne noch nichts vor und verrate kein Ergebnis. "
        "Verwende für mathematische Schreibweisen ausschließlich "
        "Streamlit-kompatibles Markdown-LaTeX mit $...$ oder $$...$$.\n\n"
        f"Zusätzlicher Text des Schülers:\n"
        f"{task_text.strip() or '(kein zusätzlicher Text)'}"
    )
    content.append({"type": "input_text", "text": prompt})

    file_bytes = st.session_state.uploaded_bytes
    file_name = st.session_state.uploaded_name
    mime_type = st.session_state.uploaded_mime

    if file_bytes and file_name and mime_type:
        encoded = data_url(file_bytes, mime_type)
        if mime_type.startswith("image/"):
            content.append(
                {
                    "type": "input_image",
                    "image_url": encoded,
                    "detail": "high",
                }
            )
        else:
            item: dict[str, Any] = {
                "type": "input_file",
                "filename": file_name,
                "file_data": encoded,
            }
            if mime_type == "application/pdf":
                item["detail"] = "high"
            content.append(item)

    return content


def build_api_input() -> list[dict[str, Any]]:
    api_input: list[dict[str, Any]] = []

    for index, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            if index == 0:
                api_input.append(
                    {
                        "role": "user",
                        "content": build_first_user_content(message["content"]),
                    }
                )
            else:
                api_input.append(
                    {"role": "user", "content": message["content"]}
                )
        else:
            api_input.append(
                {"role": "assistant", "content": message["content"]}
            )

    return api_input


def get_answer(api_key: str, model: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        instructions=SOKRATES_INSTRUCTIONS,
        input=build_api_input(),
        max_output_tokens=700,
    )
    answer = response.output_text.strip()
    return answer or (
        "Ich habe gerade keine passende Rückfrage formulieren können. "
        "Beschreibe bitte kurz, was du an der Aufgabe bereits verstanden hast."
    )


ensure_state()

st.title("🧭 Sokrates")
st.markdown(
    '<div class="motto">Ich begleite dich – denken musst du selbst.</div>',
    unsafe_allow_html=True,
)
st.write(
    "Ein Mathematik-Lerncoach, der zuerst mit dir versteht und plant – "
    "und erst danach beim Rechnen begleitet."
)

with st.sidebar:
    st.header("Einstellungen")
    api_key = st.text_input(
        "OpenAI API-Key",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
        help="Der Schlüssel wird nur für diese laufende Sitzung verwendet.",
    )
    model = st.text_input("Modell", value=DEFAULT_MODEL)

    st.divider()
    st.caption("Sokrates gibt keine fertigen Lösungen aus.")
    if st.button("Neue Aufgabe", use_container_width=True):
        reset_session()
        st.rerun()

if not st.session_state.task_started:
    st.markdown(
        """
        <div class="sokrates-card">
        <strong>Unser Weg</strong><br><br>
        ① Verstehen &nbsp;→&nbsp; ② Planen &nbsp;→&nbsp; ③ Rechnen &nbsp;→&nbsp; ④ Prüfen
        </div>
        """,
        unsafe_allow_html=True,
    )

    task_text = st.text_area(
        "Aufgabe hineinkopieren",
        placeholder="Zum Beispiel: Ein Rechteck ist 6 cm länger als breit ...",
        height=170,
    )

    upload = st.file_uploader(
        "Oder PDF, Bild, Word-Datei oder Textdatei hochladen",
        type=SUPPORTED_TYPES,
        help=f"Maximal {MAX_FILE_SIZE_MB} MB.",
    )

    if upload is not None:
        size_mb = len(upload.getvalue()) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            st.error(f"Die Datei ist größer als {MAX_FILE_SIZE_MB} MB.")
        else:
            st.success(f"Datei bereit: {upload.name} ({size_mb:.1f} MB)")

    start = st.button(
        "Mit Sokrates beginnen",
        type="primary",
        use_container_width=True,
    )

    if start:
        if not api_key:
            st.error("Bitte trage links deinen OpenAI API-Key ein.")
        elif not task_text.strip() and upload is None:
            st.error("Bitte gib eine Aufgabe ein oder lade eine Datei hoch.")
        elif (
            upload is not None
            and len(upload.getvalue()) > MAX_FILE_SIZE_MB * 1024 * 1024
        ):
            st.error("Die Datei ist zu groß.")
        else:
            st.session_state.task_text = task_text
            if upload is not None:
                raw = upload.getvalue()
                guessed_mime = upload.type or mimetypes.guess_type(upload.name)[0]
                st.session_state.uploaded_name = upload.name
                st.session_state.uploaded_bytes = raw
                st.session_state.uploaded_mime = (
                    guessed_mime or "application/octet-stream"
                )

            st.session_state.messages = [
                {"role": "user", "content": task_text}
            ]
            st.session_state.task_started = True

            try:
                with st.spinner("Sokrates betrachtet die Aufgabe ..."):
                    answer = get_answer(api_key, model)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
                st.rerun()
            except Exception as exc:
                st.session_state.task_started = False
                st.error(
                    f"Die Anfrage konnte nicht verarbeitet werden: {exc}"
                )

else:
    if st.session_state.uploaded_name:
        st.caption(
            f"📎 Aufgabe aus Datei: {st.session_state.uploaded_name}"
        )

    for message in st.session_state.messages[1:]:
        avatar = "🧭" if message["role"] == "assistant" else "🧑‍🎓"
        with st.chat_message(message["role"], avatar=avatar):
            render_chat_content(message["content"])

    student_message = st.chat_input(
        "Dein Gedanke, deine Idee oder dein nächster Schritt ..."
    )

    if student_message:
        st.session_state.messages.append(
            {"role": "user", "content": student_message}
        )

        with st.chat_message("user", avatar="🧑‍🎓"):
            render_chat_content(student_message)

        try:
            with st.chat_message("assistant", avatar="🧭"):
                with st.spinner(
                    "Sokrates denkt über deinen Gedanken nach ..."
                ):
                    answer = get_answer(api_key, model)
                render_chat_content(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception as exc:
            st.error(
                f"Die Anfrage konnte nicht verarbeitet werden: {exc}"
            )
