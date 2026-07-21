from __future__ import annotations
import re
import streamlit as st
from formula_library import CATEGORIES, KEYPAD, formulas_for
from ui_components import formula_card_html, student_entry_html

def readable_to_latex(text: str) -> str:
    result = text.strip()
    for old, new in (("·", r"\\cdot "),("−","-"),("π",r"\\pi "),("²","^2"),("³","^3"),("α",r"\\alpha "),("°",r"^\\circ"),("ₛ","_s")):
        result = result.replace(old, new)
    result = re.sub(r"√\(([^()]*)\)", r"\\sqrt{\1}", result)
    result = re.sub(r"√([A-Za-z0-9]+)", r"\\sqrt{\1}", result)
    return result

def append_to_draft(value: str) -> None:
    st.session_state.formula_draft = st.session_state.get("formula_draft", "") + value

def apply_keyboard_input() -> None:
    value = st.session_state.get("formula_keyboard_input", "")
    if value:
        append_to_draft(value)
        st.session_state.formula_keyboard_input = ""

def render_formula_workspace(topic_key: str) -> str | None:
    with st.expander("🧮 Schul-Formeleditor", expanded=False):
        st.caption("Wähle eine Formel oder schreibe einen eigenen Rechenschritt.")
        category = st.selectbox("Bereich", CATEGORIES, key="formula_category")
        formulas = formulas_for(category, topic_key)

        if not formulas:
            st.info("Für diesen Bereich sind noch keine Formeln hinterlegt.")

        for index, formula in enumerate(formulas):
            st.markdown(formula_card_html(formula.title, formula.subtitle, formula.display, formula.explanation), unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Diese Formel verwenden", key=f"use_{category}_{index}", use_container_width=True):
                    st.session_state.formula_draft = formula.display
                    st.session_state.formula_latex_preview = formula.latex
                    st.rerun()
            with c2:
                if st.button("Mathematisch anzeigen", key=f"show_{category}_{index}", use_container_width=True):
                    st.session_state.formula_latex_preview = formula.latex
                    st.rerun()

        latex_preview = st.session_state.get("formula_latex_preview", "")
        if latex_preview:
            st.markdown("**Saubere mathematische Darstellung**")
            try:
                st.latex(latex_preview)
            except Exception:
                st.code(latex_preview)

        st.divider()
        st.markdown("### Eigener Rechenschritt")
        cols = st.columns(4)
        for index, (label, value) in enumerate(KEYPAD):
            with cols[index % 4]:
                if st.button(label, key=f"keypad_{index}", use_container_width=True):
                    append_to_draft(value)
                    st.rerun()

        st.markdown("**Deine Eingabe**")
        st.markdown(student_entry_html(st.session_state.get("formula_draft", "")), unsafe_allow_html=True)

        st.text_input("Mit der Tastatur ergänzen", key="formula_keyboard_input", placeholder="z. B. A = 6 · 4", on_change=apply_keyboard_input)

        preview = st.session_state.get("formula_draft", "").strip()
        if preview:
            st.markdown("**Vorschau**")
            try:
                st.latex(readable_to_latex(preview))
            except Exception:
                st.write(preview)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("An Sokrates senden", type="primary", use_container_width=True, disabled=not bool(preview)):
                latex = readable_to_latex(preview)
                message = f"Mein Rechenschritt lautet: {preview}\n\nMathematisch dargestellt:\n$${latex}$$"
                st.session_state.formula_draft = ""
                st.session_state.formula_latex_preview = ""
                return message
        with c2:
            if st.button("⌫ Letztes Zeichen", use_container_width=True, disabled=not bool(preview)):
                st.session_state.formula_draft = st.session_state.formula_draft[:-1]
                st.rerun()
        with c3:
            if st.button("Alles löschen", use_container_width=True, disabled=not bool(preview)):
                st.session_state.formula_draft = ""
                st.session_state.formula_latex_preview = ""
                st.rerun()
    return None
