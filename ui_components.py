from __future__ import annotations

import html
import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {max-width: 940px; padding-top: 1.6rem;}
        .hero {
            padding: 1.3rem 1.4rem;
            border-radius: 20px;
            border: 1px solid rgba(128,128,128,.20);
            margin-bottom: 1rem;
        }
        .formula-card {
            padding: 1rem 1.1rem;
            border: 1px solid rgba(128,128,128,.24);
            border-radius: 16px;
            margin: .45rem 0 .7rem 0;
            background: rgba(128,128,128,.035);
        }
        .formula-display {
            font-size: 1.45rem;
            font-weight: 700;
            line-height: 1.5;
            margin: .5rem 0;
        }
        .formula-subtitle {
            opacity: .72;
            font-size: .92rem;
        }
        .student-entry {
            font-size: 1.35rem;
            font-weight: 650;
            padding: .75rem 1rem;
            border-radius: 14px;
            border: 1px solid rgba(128,128,128,.24);
            min-height: 3rem;
        }
        
        .math-dock-title {
            font-weight: 750;
            font-size: 1.05rem;
            margin-top: 1rem;
            margin-bottom: .2rem;
        }
        div[data-testid="stTextArea"] textarea {
            font-size: 1.15rem;
        }
        div[data-testid="stButton"] button {
            min-height: 2.65rem;
        }
        </style>
    
        """,
        unsafe_allow_html=True,
    )


def formula_card_html(title: str, subtitle: str, display: str, explanation: str) -> str:
    return f"""
    <div class="formula-card">
      <strong>{html.escape(title)}</strong>
      <div class="formula-subtitle">{html.escape(subtitle)}</div>
      <div class="formula-display">{html.escape(display)}</div>
      <div>{html.escape(explanation)}</div>
    </div>
    """


def student_entry_html(text: str) -> str:
    safe = html.escape(text) if text else "Noch keine Eingabe"
    return f'<div class="student-entry">{safe}</div>'
