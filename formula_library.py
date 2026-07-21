from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Formula:
    category: str
    topic_keys: tuple[str, ...]
    title: str
    subtitle: str
    display: str
    latex: str
    explanation: str


FORMULAS: tuple[Formula, ...] = (
    Formula(
        "Geometrie", ("geometry",), "Rechteck", "Flächeninhalt",
        "A = Länge · Breite",
        r"A=\mathrm{Länge}\cdot\mathrm{Breite}",
        "Berechnet die Fläche eines Rechtecks.",
    ),
    Formula(
        "Geometrie", ("geometry",), "Rechteck", "Umfang",
        "U = 2 · Länge + 2 · Breite",
        r"U=2\cdot\mathrm{Länge}+2\cdot\mathrm{Breite}",
        "Addiert alle vier Seiten.",
    ),
    Formula(
        "Geometrie", ("geometry",), "Dreieck", "Flächeninhalt",
        "A = g · h : 2",
        r"A=\frac{g\cdot h}{2}",
        "Grundseite mal Höhe, anschließend durch 2.",
    ),
    Formula(
        "Geometrie", ("geometry",), "Kreis", "Flächeninhalt",
        "A = π · r²",
        r"A=\pi r^2",
        "Berechnet die Kreisfläche.",
    ),
    Formula(
        "Geometrie", ("geometry",), "Kreis", "Umfang",
        "U = 2 · π · r",
        r"U=2\pi r",
        "Berechnet den Kreisumfang.",
    ),
    Formula(
        "Körper", ("geometry", "word_problem"), "Prisma", "Volumen",
        "V = G · h",
        r"V=G\cdot h",
        "Grundfläche mal Körperhöhe.",
    ),
    Formula(
        "Körper", ("geometry", "word_problem"), "Quader", "Volumen",
        "V = Länge · Breite · Höhe",
        r"V=\mathrm{Länge}\cdot\mathrm{Breite}\cdot\mathrm{Höhe}",
        "Berechnet das Volumen eines Quaders.",
    ),
    Formula(
        "Pythagoras", ("pythagoras",), "Rechtwinkliges Dreieck", "Satz des Pythagoras",
        "a² + b² = c²",
        r"a^2+b^2=c^2",
        "c ist die Hypotenuse.",
    ),
    Formula(
        "Prozentrechnung", ("percent",), "Prozentwert", "W gesucht",
        "W = G · p : 100",
        r"W=G\cdot\frac{p}{100}",
        "Berechnet den Prozentwert.",
    ),
    Formula(
        "Prozentrechnung", ("percent",), "Prozentsatz", "p gesucht",
        "p = W : G · 100",
        r"p=\frac{W}{G}\cdot100",
        "Berechnet den Prozentsatz.",
    ),
    Formula(
        "Prozentrechnung", ("percent",), "Grundwert", "G gesucht",
        "G = W · 100 : p",
        r"G=\frac{W\cdot100}{p}",
        "Berechnet den Grundwert.",
    ),
    Formula(
        "Funktionen", ("function",), "Lineare Funktion", "Funktionsgleichung",
        "y = m · x + b",
        r"y=m\cdot x+b",
        "m ist die Steigung, b der y-Achsenabschnitt.",
    ),
    Formula(
        "Funktionen", ("function",), "Steigung", "Aus zwei Punkten",
        "m = (y₂ − y₁) : (x₂ − x₁)",
        r"m=\frac{y_2-y_1}{x_2-x_1}",
        "Berechnet die Steigung zwischen zwei Punkten.",
    ),
    Formula(
        "Gleichungen", ("linear_equation",), "Lineare Gleichung", "Allgemeine Form",
        "a · x + b = c",
        r"a\cdot x+b=c",
        "Eine typische lineare Gleichung.",
    ),
    Formula(
        "Bruchrechnung", ("fraction",), "Brüche addieren", "Gleicher Nenner",
        "a/c + b/c = (a + b)/c",
        r"\frac{a}{c}+\frac{b}{c}=\frac{a+b}{c}",
        "Bei gleichem Nenner werden die Zähler addiert.",
    ),
    Formula(
        "Bruchrechnung", ("fraction",), "Brüche multiplizieren", "Zähler und Nenner",
        "a/b · c/d = (a · c)/(b · d)",
        r"\frac{a}{b}\cdot\frac{c}{d}=\frac{ac}{bd}",
        "Zähler mal Zähler, Nenner mal Nenner.",
    ),
)

CATEGORIES = (
    "Passend zur Aufgabe",
    "Geometrie",
    "Körper",
    "Pythagoras",
    "Prozentrechnung",
    "Funktionen",
    "Gleichungen",
    "Bruchrechnung",
)

KEYPAD: tuple[tuple[str, str], ...] = (
    ("7", "7"), ("8", "8"), ("9", "9"), ("+", " + "),
    ("4", "4"), ("5", "5"), ("6", "6"), ("−", " − "),
    ("1", "1"), ("2", "2"), ("3", "3"), ("·", " · "),
    ("0", "0"), (",", ","), ("=", " = "), (":", " : "),
    ("²", "²"), ("³", "³"), ("√", "√"), ("π", "π"),
    ("(", "("), (")", ")"), ("x", "x"), ("h", "h"),
)


def formulas_for(category: str, topic_key: str) -> tuple[Formula, ...]:
    if category == "Passend zur Aufgabe":
        matches = tuple(f for f in FORMULAS if topic_key in f.topic_keys)
        return matches or FORMULAS[:6]
    return tuple(f for f in FORMULAS if f.category == category)
