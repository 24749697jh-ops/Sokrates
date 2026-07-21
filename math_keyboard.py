from __future__ import annotations

import re
import streamlit as st


GREEK_LATEX = {
    "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "δ": r"\delta",
    "ε": r"\varepsilon", "ζ": r"\zeta", "η": r"\eta", "θ": r"\theta",
    "ι": r"\iota", "κ": r"\kappa", "λ": r"\lambda", "μ": r"\mu",
    "ν": r"\nu", "ξ": r"\xi", "ο": "o", "π": r"\pi",
    "ρ": r"\rho", "σ": r"\sigma", "τ": r"\tau", "υ": r"\upsilon",
    "φ": r"\varphi", "χ": r"\chi", "ψ": r"\psi", "ω": r"\omega",
    "Δ": r"\Delta", "Σ": r"\Sigma", "Π": r"\Pi", "Ω": r"\Omega",
}

QUICK_KEYS = (
    ("²", "²"), ("³", "³"), ("√", "√("), ("π", "π"),
    ("α", "α"), ("β", "β"), ("γ", "γ"), ("Δ", "Δ"),
)

OPERATOR_KEYS = (
    ("+", " + "), ("−", " − "), ("×", " · "), ("÷", " : "),
    ("=", " = "), ("≠", " ≠ "), ("≤", " ≤ "), ("≥", " ≥ "),
)

BRACKET_KEYS = (
    ("(", "("), (")", ")"), ("[", "["), ("]", "]"),
    ("|x|", "| |"), ("%", "%"), ("°", "°"), ("≈", " ≈ "),
)

GREEK_KEYS = (
    ("α","α"),("β","β"),("γ","γ"),("δ","δ"),
    ("ε","ε"),("ζ","ζ"),("η","η"),("θ","θ"),
    ("ι","ι"),("κ","κ"),("λ","λ"),("μ","μ"),
    ("ν","ν"),("ξ","ξ"),("ο","ο"),("π","π"),
    ("ρ","ρ"),("σ","σ"),("τ","τ"),("υ","υ"),
    ("φ","φ"),("χ","χ"),("ψ","ψ"),("ω","ω"),
    ("Δ","Δ"),("Σ","Σ"),("Π","Π"),("Ω","Ω"),
)

VARIABLE_KEYS = (
    ("x","x"),("y","y"),("z","z"),("a","a"),
    ("b","b"),("c","c"),("d","d"),("g","g"),
    ("h","h"),("m","m"),("n","n"),("p","p"),
    ("q","q"),("r","r"),("s","s"),("t","t"),
    ("A","A"),("G","G"),("M","M"),("O","O"),
    ("U","U"),("V","V"),("W","W"),
)


def append_math(value: str) -> None:
    st.session_state.math_input = st.session_state.get("math_input", "") + value


def clear_math() -> None:
    st.session_state.math_input = ""


def delete_math() -> None:
    st.session_state.math_input = st.session_state.get("math_input", "")[:-1]


def insert_fraction() -> None:
    numerator = st.session_state.get("builder_numerator", "").strip()
    denominator = st.session_state.get("builder_denominator", "").strip()
    if numerator and denominator:
        append_math(f"({numerator})/({denominator})")
        st.session_state.builder_numerator = ""
        st.session_state.builder_denominator = ""


def insert_power() -> None:
    base = st.session_state.get("builder_base", "").strip()
    exponent = st.session_state.get("builder_exponent", "").strip()
    if base and exponent:
        append_math(f"({base})^({exponent})")
        st.session_state.builder_base = ""
        st.session_state.builder_exponent = ""


def insert_root() -> None:
    value = st.session_state.get("builder_root", "").strip()
    if value:
        append_math(f"√({value})")
        st.session_state.builder_root = ""


def insert_index() -> None:
    base = st.session_state.get("builder_index_base", "").strip()
    index = st.session_state.get("builder_index_value", "").strip()
    if base and index:
        append_math(f"{base}_({index})")
        st.session_state.builder_index_base = ""
        st.session_state.builder_index_value = ""


def _replace_structures(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\(([^()]*)\)\s*/\s*\(([^()]*)\)", r"\\frac{\1}{\2}", text)
        text = re.sub(r"\(([^()]*)\)\s*\^\s*\(([^()]*)\)", r"{\1}^{\2}", text)
        text = re.sub(r"([A-Za-zΑ-Ωα-ω])_\(([^()]*)\)", r"\1_{\2}", text)
        text = re.sub(r"√\(([^()]*)\)", r"\\sqrt{\1}", text)
    return text


def readable_to_latex(text: str) -> str:
    result = _replace_structures(text.strip())

    for old, new in (
        ("·", r"\cdot "),
        ("−", "-"),
        ("≠", r"\neq "),
        ("≈", r"\approx "),
        ("≤", r"\le "),
        ("≥", r"\ge "),
        ("±", r"\pm "),
        ("²", "^2"),
        ("³", "^3"),
        ("°", r"^\circ"),
        ("ₛ", "_s"),
    ):
        result = result.replace(old, new)

    for symbol, latex in GREEK_LATEX.items():
        result = result.replace(symbol, latex + " ")

    return result


def _key_row(keys, prefix: str, columns: int = 8) -> None:
    cols = st.columns(columns)
    for index, (label, value) in enumerate(keys):
        with cols[index % columns]:
            st.button(
                label,
                key=f"{prefix}_{index}",
                use_container_width=True,
                on_click=append_math,
                args=(value,),
            )


def render_math_input() -> str | None:
    st.markdown('<div class="math-dock-title">✍️ Mathematische Eingabe</div>', unsafe_allow_html=True)
    st.caption("Schreibe Text und Formeln gemeinsam. Die wichtigsten Zeichen sind sofort erreichbar.")

    st.text_area(
        "Dein Gedanke oder Rechenschritt",
        key="math_input",
        height=95,
        placeholder="z. B. Aₛ = α : 360° · π · r²",
        label_visibility="collapsed",
    )

    _key_row(QUICK_KEYS, "quick")
    _key_row(OPERATOR_KEYS, "operator")

    with st.expander("Weitere Zeichen und Formelvorlagen", expanded=False):
        symbol_tab, greek_tab, variable_tab, builder_tab = st.tabs(
            ("Zeichen", "Griechisch", "Variablen", "Formel-Builder")
        )

        with symbol_tab:
            _key_row(BRACKET_KEYS, "bracket", columns=4)

        with greek_tab:
            _key_row(GREEK_KEYS, "greek", columns=4)

        with variable_tab:
            _key_row(VARIABLE_KEYS, "variable", columns=4)

        with builder_tab:
            st.markdown("**Bruch**")
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Zähler", key="builder_numerator")
            with c2:
                st.text_input("Nenner", key="builder_denominator")
            st.button(
                "Bruch einsetzen",
                key="builder_fraction_button",
                use_container_width=True,
                on_click=insert_fraction,
            )

            st.markdown("**Potenz**")
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Basis", key="builder_base")
            with c2:
                st.text_input("Exponent", key="builder_exponent")
            st.button(
                "Potenz einsetzen",
                key="builder_power_button",
                use_container_width=True,
                on_click=insert_power,
            )

            st.markdown("**Wurzel**")
            st.text_input("Ausdruck unter der Wurzel", key="builder_root")
            st.button(
                "Wurzel einsetzen",
                key="builder_root_button",
                use_container_width=True,
                on_click=insert_root,
            )

            st.markdown("**Index**")
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Zeichen", key="builder_index_base")
            with c2:
                st.text_input("Index", key="builder_index_value")
            st.button(
                "Index einsetzen",
                key="builder_index_button",
                use_container_width=True,
                on_click=insert_index,
            )

    text = st.session_state.get("math_input", "").strip()
    if text:
        st.markdown("**Vorschau**")
        try:
            st.latex(readable_to_latex(text))
        except Exception:
            st.code(text)

    c1, c2, c3 = st.columns(3)
    with c1:
        send = st.button(
            "Senden",
            type="primary",
            use_container_width=True,
            disabled=not bool(text),
            key="math_send",
        )
    with c2:
        st.button(
            "⌫",
            use_container_width=True,
            disabled=not bool(text),
            key="math_delete",
            on_click=delete_math,
        )
    with c3:
        st.button(
            "Löschen",
            use_container_width=True,
            disabled=not bool(text),
            key="math_clear",
            on_click=clear_math,
        )

    if send:
        latex = readable_to_latex(text)
        clear_math()
        return (
            f"Mein Gedanke oder Rechenschritt lautet: {text}\n\n"
            f"Mathematisch dargestellt:\n$${latex}$$"
        )

    return None
