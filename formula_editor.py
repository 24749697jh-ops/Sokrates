from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class FormulaItem:
    label: str
    display_text: str
    latex: str
    explanation: str


FORMULA_LIBRARY: dict[str, tuple[FormulaItem, ...]] = {
    "linear_equation": (
        FormulaItem("Allgemeine Form", "a · x + b = c", r"a\cdot x+b=c", "Lineare Gleichung mit einer Variablen."),
        FormulaItem("Auf beiden Seiten gleich", "a = b  →  a + c = b + c", r"a=b\Rightarrow a+c=b+c", "Auf beiden Seiten wird dasselbe gerechnet."),
        FormulaItem("Durch Faktor teilen", "a · x = b  →  x = b : a", r"a\cdot x=b\Rightarrow x=\frac{b}{a}", "Der Faktor vor x wird aufgehoben."),
    ),
    "fraction": (
        FormulaItem("Brüche addieren", "a/c + b/c = (a + b)/c", r"\frac{a}{c}+\frac{b}{c}=\frac{a+b}{c}", "Bei gleichem Nenner die Zähler addieren."),
        FormulaItem("Brüche multiplizieren", "a/b · c/d = (a · c)/(b · d)", r"\frac{a}{b}\cdot\frac{c}{d}=\frac{ac}{bd}", "Zähler mal Zähler, Nenner mal Nenner."),
        FormulaItem("Brüche dividieren", "a/b : c/d = a/b · d/c", r"\frac{a}{b}:\frac{c}{d}=\frac{a}{b}\cdot\frac{d}{c}", "Mit dem Kehrwert multiplizieren."),
    ),
    "percent": (
        FormulaItem("Prozentwert", "W = G · p/100", r"W=G\cdot\frac{p}{100}", "Berechnet den Prozentwert."),
        FormulaItem("Prozentsatz", "p = W/G · 100", r"p=\frac{W}{G}\cdot100", "Berechnet den Prozentsatz."),
        FormulaItem("Grundwert", "G = W · 100/p", r"G=\frac{W\cdot100}{p}", "Berechnet den Grundwert."),
    ),
    "geometry": (
        FormulaItem("Rechteckfläche", "A = Länge · Breite", r"A=\mathrm{Länge}\cdot\mathrm{Breite}", "Flächeninhalt eines Rechtecks."),
        FormulaItem("Rechteckumfang", "U = 2 · Länge + 2 · Breite", r"U=2\cdot\mathrm{Länge}+2\cdot\mathrm{Breite}", "Umfang eines Rechtecks."),
        FormulaItem("Dreiecksfläche", "A = (g · h) : 2", r"A=\frac{g\cdot h}{2}", "Flächeninhalt eines Dreiecks."),
        FormulaItem("Kreisfläche", "A = π · r²", r"A=\pi r^2", "Flächeninhalt eines Kreises."),
        FormulaItem("Kreisumfang", "U = 2 · π · r", r"U=2\pi r", "Umfang eines Kreises."),
    ),
    "function": (
        FormulaItem("Lineare Funktion", "y = m · x + b", r"y=m\cdot x+b", "m ist die Steigung, b der y-Achsenabschnitt."),
        FormulaItem("Steigung", "m = (y₂ − y₁) : (x₂ − x₁)", r"m=\frac{y_2-y_1}{x_2-x_1}", "Steigung aus zwei Punkten."),
        FormulaItem("Quadratische Funktion", "y = a · x² + b · x + c", r"y=ax^2+bx+c", "Allgemeine Form einer Parabel."),
    ),
    "pythagoras": (
        FormulaItem("Satz des Pythagoras", "a² + b² = c²", r"a^2+b^2=c^2", "Gilt im rechtwinkligen Dreieck."),
        FormulaItem("Hypotenuse", "c = √(a² + b²)", r"c=\sqrt{a^2+b^2}", "Berechnet die Hypotenuse."),
        FormulaItem("Kathete", "a = √(c² − b²)", r"a=\sqrt{c^2-b^2}", "Berechnet eine Kathete."),
    ),
    "word_problem": (
        FormulaItem("Gesuchte Größe", "x = gesuchte Größe", r"x=\mathrm{gesuchte\ Größe}", "Die gesuchte Größe als Variable benennen."),
        FormulaItem("Beziehung", "Gesuchtes = bekannte Beziehung", r"\mathrm{Gesuchtes}=\mathrm{bekannte\ Beziehung}", "Den Text in Mathematik übersetzen."),
    ),
    "arithmetic": (
        FormulaItem("Punkt vor Strich", "· und : vor + und −", r"\cdot,\ :\ \mathrm{vor}\ +,\ -", "Reihenfolge der Rechenoperationen."),
        FormulaItem("Klammern zuerst", "( … ) zuerst", r"(\ldots)", "Klammern werden zuerst berechnet."),
        FormulaItem("Potenz", "aⁿ", r"a^n", "Mehrfache Multiplikation derselben Zahl."),
    ),
    "general": (
        FormulaItem("Gleichung", "linke Seite = rechte Seite", r"\mathrm{linke\ Seite}=\mathrm{rechte\ Seite}", "Zwei gleich große Ausdrücke."),
        FormulaItem("Bruch", "a/b", r"\frac{a}{b}", "Zähler über Nenner."),
        FormulaItem("Wurzel", "√x", r"\sqrt{x}", "Die Zahl, die quadriert x ergibt."),
    ),
}


SYMBOLS: tuple[tuple[str, str], ...] = (
    ("+", "+"),
    ("−", "−"),
    ("·", "·"),
    (":", ":"),
    ("=", "="),
    ("²", "²"),
    ("³", "³"),
    ("√", "√"),
    ("Bruch", "()/()"),
    ("(", "("),
    (")", ")"),
    ("x", "x"),
    ("y", "y"),
    ("π", "π"),
)


def formulas_for_topic(topic_key: str) -> tuple[FormulaItem, ...]:
    return FORMULA_LIBRARY.get(topic_key, FORMULA_LIBRARY["general"])


def readable_to_latex(text: str) -> str:
    """Wandelt eine schülerfreundliche Eingabe grob in LaTeX um."""
    result = text.strip()
    result = result.replace("·", r"\cdot ")
    result = result.replace("−", "-")
    result = result.replace("π", r"\pi ")
    result = result.replace("²", "^2")
    result = result.replace("³", "^3")

    # Einfache Wurzeln wie √(a²+b²) oder √x
    result = re.sub(r"√\(([^()]*)\)", r"\\sqrt{\1}", result)
    result = re.sub(r"√([A-Za-z0-9]+)", r"\\sqrt{\1}", result)

    # Häufige einfache Brüche a/b; komplexere Eingaben bleiben lesbar erhalten.
    result = re.sub(
        r"(?<![\w)])([A-Za-z0-9]+)\s*/\s*([A-Za-z0-9]+)(?![\w(])",
        r"\\frac{\1}{\2}",
        result,
    )
    return result
