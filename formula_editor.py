from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FormulaItem:
    label: str
    latex: str
    explanation: str


FORMULA_LIBRARY = {
    "linear_equation": (
        FormulaItem("Allgemeine Form", r"$ax+b=c$", "Lineare Gleichung mit einer Variablen."),
        FormulaItem("Auf beiden Seiten gleich", r"$a=b \\Rightarrow a+c=b+c$", "Dieselbe Operation auf beiden Seiten."),
        FormulaItem("Durch Faktor teilen", r"$ax=b \\Rightarrow x=\\frac{b}{a}$", "Den Faktor vor der Variablen aufheben."),
    ),
    "fraction": (
        FormulaItem("Brüche addieren", r"$\\frac{a}{c}+\\frac{b}{c}=\\frac{a+b}{c}$", "Bei gleichem Nenner die Zähler addieren."),
        FormulaItem("Brüche multiplizieren", r"$\\frac{a}{b}\\cdot\\frac{c}{d}=\\frac{ac}{bd}$", "Zähler mal Zähler, Nenner mal Nenner."),
        FormulaItem("Brüche dividieren", r"$\\frac{a}{b}:\\frac{c}{d}=\\frac{a}{b}\\cdot\\frac{d}{c}$", "Mit dem Kehrwert multiplizieren."),
    ),
    "percent": (
        FormulaItem("Prozentwert", r"$W=G\\cdot\\frac{p}{100}$", "Berechnet den Prozentwert."),
        FormulaItem("Prozentsatz", r"$p=\\frac{W}{G}\\cdot100$", "Berechnet den Prozentsatz."),
        FormulaItem("Grundwert", r"$G=\\frac{W\\cdot100}{p}$", "Berechnet den Grundwert."),
    ),
    "geometry": (
        FormulaItem("Rechteckfläche", r"$A=\\text{Länge}\\cdot\\text{Breite}$", "Flächeninhalt eines Rechtecks."),
        FormulaItem("Rechteckumfang", r"$U=2\\cdot\\text{Länge}+2\\cdot\\text{Breite}$", "Umfang eines Rechtecks."),
        FormulaItem("Dreiecksfläche", r"$A=\\frac{g\\cdot h}{2}$", "Flächeninhalt eines Dreiecks."),
        FormulaItem("Kreisfläche", r"$A=\\pi r^2$", "Flächeninhalt eines Kreises."),
        FormulaItem("Kreisumfang", r"$U=2\\pi r$", "Umfang eines Kreises."),
    ),
    "function": (
        FormulaItem("Lineare Funktion", r"$y=mx+b$", "Steigung $m$ und y-Achsenabschnitt $b$."),
        FormulaItem("Steigung", r"$m=\\frac{y_2-y_1}{x_2-x_1}$", "Steigung aus zwei Punkten."),
        FormulaItem("Quadratische Funktion", r"$y=ax^2+bx+c$", "Allgemeine Form einer Parabel."),
    ),
    "pythagoras": (
        FormulaItem("Pythagoras", r"$a^2+b^2=c^2$", "Gilt im rechtwinkligen Dreieck."),
        FormulaItem("Hypotenuse", r"$c=\\sqrt{a^2+b^2}$", "Berechnet die Hypotenuse."),
        FormulaItem("Kathete", r"$a=\\sqrt{c^2-b^2}$", "Berechnet eine Kathete."),
    ),
    "word_problem": (
        FormulaItem("Gesuchte Größe", r"$x=\\text{gesuchte Größe}$", "Die gesuchte Größe als Variable benennen."),
        FormulaItem("Beziehung", r"$\\text{Gesuchtes}=\\text{bekannte Beziehung}$", "Den Text in Mathematik übersetzen."),
    ),
    "arithmetic": (
        FormulaItem("Punkt vor Strich", r"$\\cdot, : \\text{ vor } +, -$", "Reihenfolge der Rechenoperationen."),
        FormulaItem("Klammern zuerst", r"$(\\ldots)$", "Klammern werden zuerst berechnet."),
        FormulaItem("Potenz", r"$a^n$", "Mehrfache Multiplikation derselben Zahl."),
    ),
    "general": (
        FormulaItem("Gleichung", r"$\\text{linke Seite}=\\text{rechte Seite}$", "Zwei gleich große Ausdrücke."),
        FormulaItem("Bruch", r"$\\frac{a}{b}$", "Zähler über Nenner."),
        FormulaItem("Wurzel", r"$\\sqrt{x}$", "Die Zahl, die quadriert $x$ ergibt."),
    ),
}

SYMBOLS = (
    ("+", "+"), ("−", "-"), ("·", r"\\cdot "), (":", ":"), ("=", "="),
    ("²", "^2"), ("³", "^3"), ("√", r"\\sqrt{}"), ("Bruch", r"\\frac{}{}"),
    ("(", "("), (")", ")"), ("x", "x"), ("y", "y"), ("π", r"\\pi"),
)


def formulas_for_topic(topic_key: str):
    return FORMULA_LIBRARY.get(topic_key, FORMULA_LIBRARY["general"])
