from __future__ import annotations

import base64
import io
import mimetypes
import os
import re
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit_paste_button import paste_image_button

from config import (
    APP_ICON,
    APP_TITLE,
    DEFAULT_MODEL,
    MAX_FILE_SIZE_MB,
    SUPPORTED_TYPES,
)
from didactic_engine import build_tutor_instructions, classify_topic
from formula_ui import render_formula_workspace
from ui_components import inject_styles

load_dotenv()

st.set_page_config(
    page_title=f"{APP_TITLE} – Mathe-Lerncoach",
    page_icon=APP_ICON,
    layout="centered",
)

inject_styles()


def normalize_math_markdown(text: str) -> str:
    if not text:
        return text
    text = re.sub(
        r"\\\[\s*(.*?)\s*\\\]",
        lambda m: f"\n$$\n{m.group(1).strip()}\n$$\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"\\\(\s*(.*?)\s*\\\)",
        lambda m: f"${m.group(1).strip()}$",
        text,
        flags=re.DOTALL,
    )
    return text


def render_chat_content(content: str) -> None:
    st.markdown(normalize_math_markdown(content))


def ensure_state() -> None:
    defaults = {
        "messages": [],
        "task_started": False,
        "task_text": "",
        "uploaded_name": None,
        "uploaded_bytes": None,
        "uploaded_mime": None,
        "help_level": 1,
        "formula_draft": "",
        "formula_latex_preview": "",
        "formula_keyboard_input": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session() -> None:
    for key in list(st.session_state.keys()):
        if key not in {"formula_category"}:
            del st.session_state[key]
    ensure_state()


def data_url(file_bytes: bytes, mime_type: str) -> str:
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def store_pasted_image(image: Any) -> None:
    image_buffer = io.BytesIO()
    image.convert("RGB").save(image_buffer, format="PNG")
    st.session_state.uploaded_name = "goodnotes-zwischenablage.png"
    st.session_state.uploaded_bytes = image_buffer.getvalue()
    st.session_state.uploaded_mime = "image/png"


def build_first_user_content(task_text: str) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = [
        {
            "type": "input_text",
            "text": (
                "Hier ist meine Mathematikaufgabe. Beginne sofort mit VERSTEHEN. "
                "Stelle genau eine fachliche Frage zur Aufgabe. Frage niemals, "
                "ob du die Aufgabe lösen, erklären oder bearbeiten sollst. "
                "Rechne noch nichts vollständig vor.\n\n"
                f"Zusätzlicher Text:\n{task_text.strip() or '(kein Text)'}"
            ),
        }
    ]

    file_bytes = st.session_state.uploaded_bytes
    file_name = st.session_state.uploaded_name
    mime_type = st.session_state.uploaded_mime

    if file_bytes and file_name and mime_type:
        encoded = data_url(file_bytes, mime_type)
        if mime_type.startswith("image/"):
            content.append(
                {"type": "input_image", "image_url": encoded, "detail": "high"}
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
        if message["role"] == "user" and index == 0:
            api_input.append(
                {
                    "role": "user",
                    "content": build_first_user_content(message["content"]),
                }
            )
        else:
            api_input.append(
                {"role": message["role"], "content": message["content"]}
            )
    return api_input


def get_answer(api_key: str, model: str) -> str:
    client = OpenAI(api_key=api_key)
    instructions = build_tutor_instructions(
        st.session_state.task_text,
        st.session_state.messages,
        st.session_state.help_level,
    )
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=build_api_input(),
        max_output_tokens=700,
    )
    return response.output_text.strip() or (
        "Welche Größe ist gesucht, und welche Angabe verbindet sie "
        "mit dem bereits Bekannten?"
    )


def send_student_message(message: str, api_key: str, model: str) -> None:
    cleaned = message.strip()
    if not cleaned:
        return
    st.session_state.messages.append({"role": "user", "content": cleaned})
    with st.spinner("Sokrates denkt über deinen Gedanken nach ..."):
        answer = get_answer(api_key, model)
    st.session_state.messages.append({"role": "assistant", "content": answer})


ensure_state()

st.markdown(
    """
    <div class="hero">
      <h1 style="margin:0">🧭 Sokrates</h1>
      <p style="font-style:italic; opacity:.78; margin:.5rem 0">
      Ich begleite dich – denken musst du selbst.
      </p>
      <p style="margin:0">
      Verstehen → Planen → Rechnen → Prüfen
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_key = os.getenv("OPENAI_API_KEY")
model = DEFAULT_MODEL

with st.sidebar:
    st.header("Sokrates")
    if api_key:
        st.success("✅ Sokrates ist bereit")
    else:
        st.error("Der OpenAI-Schlüssel fehlt.")
    st.caption("Sokrates gibt keine fertigen Lösungen aus.")
    if st.button("Neue Aufgabe", use_container_width=True):
        reset_session()
        st.rerun()

if not st.session_state.task_started:
    task_text = st.text_area(
        "Aufgabe als Text",
        placeholder="Schreibe oder kopiere deine Mathematikaufgabe hier hinein.",
        height=160,
    )

    st.markdown("### Aus GoodNotes einfügen")
    st.caption("Mit dem Lasso markieren, kopieren und hier einfügen.")
    paste_result = paste_image_button(
        label="📋 Aus Zwischenablage einfügen",
        key="goodnotes_paste",
        errors="raise",
    )

    if paste_result.image_data is not None:
        store_pasted_image(paste_result.image_data)
        st.success("Die Aufgabe aus GoodNotes wurde eingefügt.")
        st.image(paste_result.image_data, use_container_width=True)

    upload = st.file_uploader(
        "Oder Datei hochladen",
        type=SUPPORTED_TYPES,
        help=f"Maximal {MAX_FILE_SIZE_MB} MB.",
    )

    if upload is not None:
        size_mb = len(upload.getvalue()) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            st.error(f"Die Datei ist größer als {MAX_FILE_SIZE_MB} MB.")
        else:
            st.session_state.uploaded_name = upload.name
            st.session_state.uploaded_bytes = upload.getvalue()
            st.session_state.uploaded_mime = (
                upload.type
                or mimetypes.guess_type(upload.name)[0]
                or "application/octet-stream"
            )
            st.success(f"Datei bereit: {upload.name}")

    if st.button("Mit Sokrates beginnen", type="primary", use_container_width=True):
        has_task = bool(task_text.strip()) or st.session_state.uploaded_bytes is not None
        if not api_key:
            st.error("Der OpenAI-Schlüssel wurde auf dem Server nicht eingerichtet.")
        elif not has_task:
            st.error("Bitte gib eine Aufgabe ein oder lade eine Datei hoch.")
        else:
            st.session_state.task_text = task_text
            st.session_state.messages = [{"role": "user", "content": task_text}]
            st.session_state.task_started = True
            try:
                answer = get_answer(api_key, model)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
                st.rerun()
            except Exception as exc:
                st.session_state.task_started = False
                st.error(f"Die Anfrage konnte nicht verarbeitet werden: {exc}")

else:
    if st.session_state.uploaded_name:
        st.caption(f"📎 {st.session_state.uploaded_name}")

    for message in st.session_state.messages[1:]:
        avatar = "🧭" if message["role"] == "assistant" else "🧑‍🎓"
        with st.chat_message(message["role"], avatar=avatar):
            render_chat_content(message["content"])

    st.caption(f"Hilfestufe {st.session_state.help_level} von 4")

    col_hint, col_reset = st.columns(2)
    with col_hint:
        if st.button("💡 Kleiner Hinweis", use_container_width=True):
            st.session_state.help_level = min(4, st.session_state.help_level + 1)
            try:
                send_student_message(
                    "Ich brauche einen etwas deutlicheren Hinweis, "
                    "aber noch keine vollständige Lösung.",
                    api_key,
                    model,
                )
                st.rerun()
            except Exception as exc:
                st.error(f"Fehler: {exc}")

    with col_reset:
        if st.button("↩️ Hilfestufe zurücksetzen", use_container_width=True):
            st.session_state.help_level = 1
            st.rerun()

    profile = classify_topic(
        st.session_state.task_text,
        st.session_state.messages,
    )
    formula_message = render_formula_workspace(profile.key)
    if formula_message:
        try:
            send_student_message(formula_message, api_key, model)
            st.rerun()
        except Exception as exc:
            st.error(f"Fehler: {exc}")

    student_message = st.chat_input(
        "Dein Gedanke, deine Idee oder dein nächster Schritt ..."
    )
    if student_message:
        try:
            send_student_message(student_message, api_key, model)
            st.rerun()
        except Exception as exc:
            st.error(f"Die Anfrage konnte nicht verarbeitet werden: {exc}")
