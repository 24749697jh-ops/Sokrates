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

FORMULAS = (
    Formula("Geometrie", ("geometry",), "Rechteck", "Flächeninhalt", "A = Länge · Breite", r"A=\mathrm{Länge}\cdot\mathrm{Breite}", "Fläche eines Rechtecks."),
    Formula("Geometrie", ("geometry",), "Rechteck", "Umfang", "U = 2 · Länge + 2 · Breite", r"U=2\cdot\mathrm{Länge}+2\cdot\mathrm{Breite}", "Umfang eines Rechtecks."),
    Formula("Geometrie", ("geometry",), "Quadrat", "Flächeninhalt", "A = a²", r"A=a^2", "Fläche eines Quadrats."),
    Formula("Geometrie", ("geometry",), "Dreieck", "Flächeninhalt", "A = g · h : 2", r"A=\frac{g\cdot h}{2}", "Grundseite mal Höhe, geteilt durch 2."),
    Formula("Geometrie", ("geometry",), "Parallelogramm", "Flächeninhalt", "A = g · h", r"A=g\cdot h", "Grundseite mal Höhe."),
    Formula("Geometrie", ("geometry",), "Trapez", "Flächeninhalt", "A = (a + c) · h : 2", r"A=\frac{(a+c)\cdot h}{2}", "Fläche eines Trapezes."),
    Formula("Kreis", ("geometry",), "Kreis", "Flächeninhalt", "A = π · r²", r"A=\pi r^2", "Fläche eines Kreises."),
    Formula("Kreis", ("geometry",), "Kreis", "Umfang", "U = 2 · π · r", r"U=2\pi r", "Umfang eines Kreises."),
    Formula("Kreis", ("geometry",), "Kreisausschnitt", "Flächeninhalt", "Aₛ = α : 360° · π · r²", r"A_s=\frac{\alpha}{360^\circ}\cdot\pi r^2", "Fläche eines Kreisausschnitts."),
    Formula("Kreis", ("geometry",), "Kreisbogen", "Bogenlänge", "b = α : 360° · 2 · π · r", r"b=\frac{\alpha}{360^\circ}\cdot2\pi r", "Länge des Kreisbogens."),
    Formula("Kreis", ("geometry",), "Kreisausschnitt", "Umfang", "Uₛ = 2 · r + b", r"U_s=2r+b", "Zwei Radien plus Kreisbogen."),
    Formula("Kreis", ("geometry",), "Kreisring", "Flächeninhalt", "A = π · (R² − r²)", r"A=\pi(R^2-r^2)", "Fläche eines Kreisrings."),
    Formula("Körper", ("geometry","word_problem"), "Quader", "Volumen", "V = Länge · Breite · Höhe", r"V=\mathrm{Länge}\cdot\mathrm{Breite}\cdot\mathrm{Höhe}", "Volumen eines Quaders."),
    Formula("Körper", ("geometry","word_problem"), "Prisma", "Volumen", "V = G · h", r"V=G\cdot h", "Volumen eines Prismas."),
    Formula("Körper", ("geometry","word_problem"), "Zylinder", "Volumen", "V = π · r² · h", r"V=\pi r^2h", "Volumen eines Zylinders."),
    Formula("Körper", ("geometry","word_problem"), "Pyramide", "Volumen", "V = G · h : 3", r"V=\frac{G\cdot h}{3}", "Volumen einer Pyramide."),
    Formula("Körper", ("geometry","word_problem"), "Kegel", "Volumen", "V = π · r² · h : 3", r"V=\frac{\pi r^2h}{3}", "Volumen eines Kegels."),
    Formula("Körper", ("geometry","word_problem"), "Kugel", "Volumen", "V = 4 : 3 · π · r³", r"V=\frac{4}{3}\pi r^3", "Volumen einer Kugel."),
    Formula("Pythagoras", ("pythagoras",), "Rechtwinkliges Dreieck", "Satz des Pythagoras", "a² + b² = c²", r"a^2+b^2=c^2", "c ist die Hypotenuse."),
    Formula("Prozentrechnung", ("percent",), "Prozentwert", "W gesucht", "W = G · p : 100", r"W=G\cdot\frac{p}{100}", "Berechnet den Prozentwert."),
    Formula("Prozentrechnung", ("percent",), "Prozentsatz", "p gesucht", "p = W : G · 100", r"p=\frac{W}{G}\cdot100", "Berechnet den Prozentsatz."),
    Formula("Prozentrechnung", ("percent",), "Grundwert", "G gesucht", "G = W · 100 : p", r"G=\frac{W\cdot100}{p}", "Berechnet den Grundwert."),
    Formula("Funktionen", ("function",), "Lineare Funktion", "Funktionsgleichung", "y = m · x + b", r"y=m\cdot x+b", "Lineare Funktion."),
    Formula("Gleichungen", ("linear_equation",), "Lineare Gleichung", "Allgemeine Form", "a · x + b = c", r"a\cdot x+b=c", "Allgemeine Form."),
)

CATEGORIES = ("Passend zur Aufgabe","Geometrie","Kreis","Körper","Pythagoras","Prozentrechnung","Funktionen","Gleichungen")
KEYPAD = (
    ("7","7"),("8","8"),("9","9"),("+"," + "),
    ("4","4"),("5","5"),("6","6"),("−"," − "),
    ("1","1"),("2","2"),("3","3"),("·"," · "),
    ("0","0"),(",",","),("="," = "),(":", " : "),
    ("²","²"),("³","³"),("√","√"),("π","π"),
    ("(","("),(")",")"),("r","r"),("α","α"),
    ("°","°"),("x","x"),("h","h"),("b","b"),
)

def formulas_for(category: str, topic_key: str):
    if category == "Passend zur Aufgabe":
        matches = tuple(f for f in FORMULAS if topic_key in f.topic_keys)
        return matches[:12] if matches else FORMULAS[:8]
    return tuple(f for f in FORMULAS if f.category == category)
