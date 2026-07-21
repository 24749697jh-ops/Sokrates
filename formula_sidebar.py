from __future__ import annotations

import streamlit as st

from formula_library import CATEGORIES, formulas_for


def render_formula_sidebar(topic_key: str) -> None:
    st.subheader("📚 Formelsammlung")
    category = st.selectbox(
        "Bereich",
        CATEGORIES,
        key="sidebar_formula_category",
    )

    formulas = formulas_for(category, topic_key)
    if not formulas:
        st.caption("Für diesen Bereich sind noch keine Formeln hinterlegt.")
        return

    for index, formula in enumerate(formulas):
        with st.container(border=True):
            st.markdown(f"**{formula.title} – {formula.subtitle}**")
            st.markdown(f"### {formula.display}")
            st.caption(formula.explanation)
            st.button(
                "In Eingabe übernehmen",
                key=f"sidebar_formula_{category}_{index}",
                use_container_width=True,
                on_click=_copy_formula,
                args=(formula.display,),
            )


def _copy_formula(display: str) -> None:
    st.session_state.math_input = display
