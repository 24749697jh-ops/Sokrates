from __future__ import annotations

import re
import streamlit as st

from formula_library import (
    CATEGORIES,
    FORMULAS,
    GREEK_KEYS,
    NUMBER_KEYS,
    OPERATOR_KEYS,
    VARIABLE_KEYS,
    formulas_for,
)
from ui_components import formula_card_html


GREEK_LATEX = {
    "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta",
    "ε": r"\varepsilon", "ζ": r"\zeta", "η": r"\eta", "θ": r"\theta",
    "ι": r"\iota", "κ": r"\kappa", "λ": r"\lambda", "μ": r"\mu",
    "ν": r"\nu", "ξ": r"\xi", "ο": "o", "π": r"\pi",
    "ρ": r"\rho", "σ": r"\sigma", "τ": r"\tau", "υ": r"\upsilon",
    "φ": r"\varphi", "χ": r"\chi", "ψ": r"\psi", "ω": r"\omega",
    "Δ": r"\Delta", "Σ": r"\Sigma", "Π": r"\Pi", "Ω": r"\Omega",
}


def append_to_draft(value: str) -> None:
    st.session_state.formula_draft = (
        st.session_state.get("formula_draft", "") + value
    )


def set_draft(value: str, latex: str = "") -> None:
    st.session_state.formula_draft = value
    st.session_state.formula_latex_preview = latex


def clear_draft() -> None:
    st.session_state.formula_draft = ""
    st.session_state.formula_latex_preview = ""


def delete_last_character() -> None:
    st.session_state.formula_draft = st.session_state.get("formula_draft", "")[:-1]


def insert_fraction() -> None:
    numerator = st.session_state.get("fraction_numerator", "").strip()
    denominator = st.session_state.get("fraction_denominator", "").strip()
    if numerator and denominator:
        append_to_draft(f"({numerator})/({denominator})")
        st.session_state.fraction_numerator = ""
        st.session_state.fraction_denominator = ""


def insert_root() -> None:
    radicand = st.session_state.get("root_value", "").strip()
    if radicand:
        append_to_draft(f"√({radicand})")
        st.session_state.root_value = ""


def insert_power() -> None:
    base = st.session_state.get("power_base", "").strip()
    exponent = st.session_state.get("power_exponent", "").strip()
    if base and exponent:
        append_to_draft(f"({base})^({exponent})")
        st.session_state.power_base = ""
        st.session_state.power_exponent = ""


def _replace_parenthesized_fractions(text: str) -> str:
    pattern = re.compile(r"\(([^()]*)\)\s*/\s*\(([^()]*)\)")
    previous = None
    while previous != text:
        previous = text
        text = pattern.sub(r"\\frac{\1}{\2}", text)
    return text


def readable_to_latex(text: str) -> str:
    result = text.strip()
    result = _replace_parenthesized_fractions(result)

    replacements = (
        ("·", r"\cdot "),
        ("−", "-"),
        ("≠", r"\neq "),
        ("≈", r"\approx "),
        ("±", r"\pm "),
        ("≤", r"\le "),
        ("≥", r"\ge "),
        ("²", "^2"),
        ("³", "^3"),
        ("°", r"^\circ"),
        ("ₛ", "_s"),
    )
    for old, new in replacements:
        result = result.replace(old, new)

    for symbol, latex in GREEK_LATEX.items():
        result = result.replace(symbol, latex + " ")

    result = re.sub(r"√\(([^()]*)\)", r"\\sqrt{\1}", result)
    result = re.sub(r"\(([^()]*)\)\^\(([^()]*)\)", r"{\1}^{\2}", result)
    return result


def render_key_grid(items, prefix: str, columns: int = 4) -> None:
    cols = st.columns(columns)
    for index, (label, value) in enumerate(items):
        with cols[index % columns]:
            st.button(
                label,
                key=f"{prefix}_{index}",
                use_container_width=True,
                on_click=append_to_draft,
                args=(value,),
            )


def render_formula_workspace(topic_key: str) -> str | None:
    with st.expander("🧮 Schul-Formeleditor", expanded=False):
        st.caption(
            "Formeln können direkt bearbeitet werden. Brüche, Wurzeln, Potenzen, "
            "griechische Buchstaben und mathematische Operatoren stehen als Tasten bereit."
        )

        library_tab, input_tab = st.tabs(("📚 Formelsammlung", "✍️ Eigene Eingabe"))

        with library_tab:
            category = st.selectbox("Bereich", CATEGORIES, key="formula_category")
            formulas = formulas_for(category, topic_key)

            if not formulas:
                st.info("Für diesen Bereich sind noch keine Formeln hinterlegt.")

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
                st.button(
                    "Diese Formel übernehmen",
                    key=f"use_formula_{category}_{index}",
                    use_container_width=True,
                    on_click=set_draft,
                    args=(formula.display, formula.latex),
                )

        with input_tab:
            st.text_area(
                "Formel oder Rechenschritt",
                key="formula_draft",
                height=110,
                placeholder="z. B. Aₛ = α : 360° · π · r²",
            )

            number_tab, operator_tab, greek_tab, variable_tab, template_tab = st.tabs(
                ("Zahlen", "Operatoren", "Griechisch", "Variablen", "Vorlagen")
            )

            with number_tab:
                render_key_grid(NUMBER_KEYS, "number", columns=3)

            with operator_tab:
                render_key_grid(OPERATOR_KEYS, "operator", columns=4)

            with greek_tab:
                render_key_grid(GREEK_KEYS, "greek", columns=4)

            with variable_tab:
                render_key_grid(VARIABLE_KEYS, "variable", columns=4)

            with template_tab:
                st.markdown("**Bruch einsetzen**")
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Zähler", key="fraction_numerator")
                with c2:
                    st.text_input("Nenner", key="fraction_denominator")
                st.button(
                    "Bruch einsetzen",
                    key="insert_fraction",
                    use_container_width=True,
                    on_click=insert_fraction,
                )

                st.markdown("**Wurzel einsetzen**")
                st.text_input("Ausdruck unter der Wurzel", key="root_value")
                st.button(
                    "Wurzel einsetzen",
                    key="insert_root",
                    use_container_width=True,
                    on_click=insert_root,
                )

                st.markdown("**Potenz einsetzen**")
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Basis", key="power_base")
                with c2:
                    st.text_input("Exponent", key="power_exponent")
                st.button(
                    "Potenz einsetzen",
                    key="insert_power",
                    use_container_width=True,
                    on_click=insert_power,
                )

        preview = st.session_state.get("formula_draft", "").strip()
        if preview:
            st.markdown("### Mathematische Vorschau")
            try:
                st.latex(readable_to_latex(preview))
            except Exception:
                st.warning("Die Vorschau konnte noch nicht vollständig dargestellt werden.")
                st.code(preview)

        c1, c2, c3 = st.columns(3)
        with c1:
            send = st.button(
                "An Sokrates senden",
                type="primary",
                use_container_width=True,
                disabled=not bool(preview),
            )
        with c2:
            st.button(
                "⌫ Zeichen löschen",
                use_container_width=True,
                disabled=not bool(preview),
                on_click=delete_last_character,
            )
        with c3:
            st.button(
                "Alles löschen",
                use_container_width=True,
                disabled=not bool(preview),
                on_click=clear_draft,
            )

        if send:
            latex = readable_to_latex(preview)
            message = (
                f"Mein Rechenschritt lautet: {preview}\n\n"
                f"Mathematisch dargestellt:\n$${latex}$$"
            )
            clear_draft()
            return message

    return None
