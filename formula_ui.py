from __future__ import annotations

import re
import streamlit as st

from formula_library import CATEGORIES, KEYPAD, formulas_for
from ui_components import formula_card_html, student_entry_html


def readable_to_latex(text: str) -> str:
    result = text.strip()
    result = result.replace("·", r"\cdot ")
    result = result.replace("−", "-")
    result = result.replace("π", r"\pi ")
    result = result.replace("²", "^2")
    result = result.replace("³", "^3")
    result = re.sub(r"√\(([^()]*)\)", r"\\sqrt{\1}", result)
    result = re.sub(r"√([A-Za-z0-9]+)", r"\\sqrt{\1}", result)
    return result


def append_to_draft(value: str) -> None:
    st.session_state.formula_draft += value


def render_formula_workspace(topic_key: str) -> str | None:
    with st.expander("🧮 Schul-Formeleditor", expanded=False):
        st.caption(
            "Wähle eine Formel oder schreibe deinen eigenen Rechenschritt. "
            "Es werden nur normale Schulzeichen angezeigt."
        )

        category = st.selectbox(
            "Bereich",
            CATEGORIES,
            index=0,
            key="formula_category",
        )

        formulas = formulas_for(category, topic_key)
        for index, formula in enumerate(formulas):
            st.markdown(
                formula_card_html(
                    formula.title,
                    formula.subtitle,
                    formula.display,
                    formula.explanation,
                ),
                unsafe_allow_html=True,
            )
            col_use, col_preview = st.columns(2)
            with col_use:
                if st.button(
                    "Diese Formel verwenden",
                    key=f"use_formula_{category}_{index}",
                    use_container_width=True,
                ):
                    st.session_state.formula_draft = formula.display
                    st.session_state.formula_latex_preview = formula.latex
                    st.rerun()
            with col_preview:
                if st.button(
                    "Mathematisch anzeigen",
                    key=f"show_formula_{category}_{index}",
                    use_container_width=True,
                ):
                    st.session_state.formula_latex_preview = formula.latex
                    st.rerun()

        if st.session_state.get("formula_latex_preview"):
            st.markdown("**Saubere mathematische Darstellung**")
            st.latex(st.session_state.formula_latex_preview)

        st.divider()
        st.markdown("### Eigener Rechenschritt")

        keypad_columns = st.columns(4)
        for index, (label, value) in enumerate(KEYPAD):
            with keypad_columns[index % 4]:
                if st.button(
                    label,
                    key=f"keypad_{index}",
                    use_container_width=True,
                ):
                    append_to_draft(value)
                    st.rerun()

        st.markdown("**Deine Eingabe**")
        st.markdown(
            student_entry_html(st.session_state.formula_draft),
            unsafe_allow_html=True,
        )

        text = st.text_input(
            "Alternativ mit der Tastatur ergänzen",
            key="formula_keyboard_input",
            placeholder="z. B. A = 6 · 4",
            label_visibility="collapsed",
        )
        if text:
            st.session_state.formula_draft += text
            st.session_state.formula_keyboard_input = ""
            st.rerun()

        preview = st.session_state.formula_draft.strip()
        if preview:
            st.markdown("**Vorschau**")
            try:
                st.latex(readable_to_latex(preview))
            except Exception:
                st.write(preview)

        col_send, col_back, col_clear = st.columns(3)

        with col_send:
            if st.button(
                "An Sokrates senden",
                type="primary",
                use_container_width=True,
                disabled=not bool(preview),
            ):
                readable = preview
                latex = readable_to_latex(readable)
                st.session_state.formula_draft = ""
                st.session_state.formula_latex_preview = ""
                return (
                    f"Mein Rechenschritt lautet: {readable}\n\n"
                    f"Mathematisch dargestellt:\n$${latex}$$"
                )

        with col_back:
            if st.button(
                "⌫ Letztes Zeichen",
                use_container_width=True,
                disabled=not bool(preview),
            ):
                st.session_state.formula_draft = st.session_state.formula_draft[:-1]
                st.rerun()

        with col_clear:
            if st.button(
                "Alles löschen",
                use_container_width=True,
                disabled=not bool(preview),
            ):
                st.session_state.formula_draft = ""
                st.session_state.formula_latex_preview = ""
                st.rerun()

    return None
