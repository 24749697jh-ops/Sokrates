from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TopicProfile:
    key: str
    label: str
    questions: tuple[str, ...]
    hints: tuple[str, ...]
    common_errors: tuple[str, ...]


TOPICS: dict[str, TopicProfile] = {
    "linear_equation": TopicProfile(
        "linear_equation", "Lineare Gleichung",
        (
            "Welche Rechenoperation steht der gesuchten Zahl im Moment am nächsten?",
            "Welche Gegenoperation hebt den nächsten Schritt auf?",
            "Was musst du auf beiden Seiten gleich machen?",
        ),
        (
            "Betrachte zuerst nur die Operation direkt neben der Variablen.",
            "Nutze die passende Gegenoperation auf beiden Seiten.",
            "Vereinfache anschließend beide Seiten.",
            "Bestimme die Variable und prüfe durch Einsetzen.",
        ),
        (
            "Operation nur auf einer Seite",
            "Vorzeichenfehler",
            "Faktor vor der Variablen übersehen",
        ),
    ),
    "fraction": TopicProfile(
        "fraction", "Bruchrechnung",
        (
            "Welche Nenner kommen vor?",
            "Welcher gemeinsame Nenner wäre geeignet?",
            "Musst du zuerst erweitern oder kannst du kürzen?",
        ),
        (
            "Schau zuerst nur auf die Nenner.",
            "Finde einen gemeinsamen Nenner.",
            "Erweitere passend.",
            "Rechne und kürze am Ende.",
        ),
        (
            "Zähler und Nenner getrennt addieren",
            "falsch erweitern",
            "Vorzeichen übersehen",
        ),
    ),
    "percent": TopicProfile(
        "percent", "Prozentrechnung",
        (
            "Was ist hier das Ganze, also der Grundwert?",
            "Welche Größe ist der Prozentsatz?",
            "Welche Größe ist der Prozentwert?",
        ),
        (
            "Ordne Grundwert, Prozentsatz und Prozentwert zu.",
            "Denke von 100 Prozent zu 1 Prozent.",
            "Gehe von 1 Prozent zur gesuchten Prozentzahl.",
            "Prüfe, ob das Ergebnis zur Situation passt.",
        ),
        (
            "Grundwert und Prozentwert vertauschen",
            "Prozentzahl nicht durch 100 teilen",
            "Plausibilität nicht prüfen",
        ),
    ),
    "geometry": TopicProfile(
        "geometry", "Geometrie",
        (
            "Welche Figur oder welchen Körper erkennst du?",
            "Welche Größen sind gegeben und welche wird gesucht?",
            "Welche Formel passt genau zur gesuchten Größe?",
        ),
        (
            "Markiere Gegebenes und Gesuchtes.",
            "Schreibe die Formel zunächst ohne Zahlen auf.",
            "Setze die bekannten Werte ein.",
            "Achte auf die Einheit.",
        ),
        (
            "Umfang, Fläche und Volumen verwechseln",
            "Einheiten übersehen",
            "Formel falsch umstellen",
        ),
    ),
    "function": TopicProfile(
        "function", "Funktionen",
        (
            "Welche Größe hängt von welcher anderen Größe ab?",
            "Was beschreibt die Steigung?",
            "Welche Bedeutung hat der Anfangswert?",
        ),
        (
            "Suche nach Anfangswert und Veränderung pro Schritt.",
            "Ordne die Angaben einer Funktionsgleichung zu.",
            "Setze ein bekanntes Wertepaar ein.",
            "Prüfe Graph und Gleichung gemeinsam.",
        ),
        (
            "Steigung und Anfangswert vertauschen",
            "x- und y-Werte verwechseln",
            "Vorzeichen der Steigung falsch deuten",
        ),
    ),
    "pythagoras": TopicProfile(
        "pythagoras", "Satz des Pythagoras",
        (
            "Wo liegt der rechte Winkel?",
            "Welche Seite ist die Hypotenuse?",
            "Welche Länge wird gesucht?",
        ),
        (
            "Bestimme zuerst die Hypotenuse.",
            "Ordne die Seiten in a² + b² = c² ein.",
            "Setze die Längen ein.",
            "Ziehe erst am Ende die Wurzel.",
        ),
        (
            "falsche Seite als Hypotenuse",
            "Wurzel vergessen",
            "Einheit fehlt",
        ),
    ),
    "word_problem": TopicProfile(
        "word_problem", "Textaufgabe",
        (
            "Was ist gegeben?",
            "Was soll herausgefunden werden?",
            "Welche Beziehung beschreibt der Text?",
        ),
        (
            "Trenne Gegebenes und Gesuchtes.",
            "Beschreibe den Zusammenhang ohne Zahlen.",
            "Übersetze ihn in eine Gleichung.",
            "Prüfe das Ergebnis an der Situation.",
        ),
        (
            "zu früh rechnen",
            "gesuchte Größe unklar",
            "Textbeziehung falsch übersetzen",
        ),
    ),
    "arithmetic": TopicProfile(
        "arithmetic", "Rechenaufgabe",
        (
            "Welche Rechenoperation kommt zuerst?",
            "Kannst du den Ausdruck in kleinere Teile zerlegen?",
            "Welche Regel ist hier wichtig?",
        ),
        (
            "Achte auf Klammern und Punkt vor Strich.",
            "Berechne zuerst einen klaren Teil.",
            "Arbeite schrittweise weiter.",
            "Prüfe mit einem Überschlag.",
        ),
        (
            "Reihenfolge übersehen",
            "Vorzeichenfehler",
            "Zwischenschritte übersprungen",
        ),
    ),
    "general": TopicProfile(
        "general", "Mathematikaufgabe",
        (
            "Was verstehst du bereits sicher?",
            "Welche Information ist gegeben und was wird gesucht?",
            "Wo beginnt deine Unsicherheit?",
        ),
        (
            "Trenne Gegebenes und Gesuchtes.",
            "Beschreibe den Zusammenhang in Worten.",
            "Wähle eine passende Formel.",
            "Führe einen kleinen Schritt aus.",
        ),
        (
            "zu viele Schritte gleichzeitig",
            "unklare Bezeichnungen",
            "Ergebnis nicht geprüft",
        ),
    ),
}


def _conversation_text(messages: Iterable[dict]) -> str:
    return " ".join(str(m.get("content", "")) for m in messages).lower()


def classify_topic(task_text: str, messages: list[dict]) -> TopicProfile:
    text = f"{task_text} {_conversation_text(messages)}".lower()
    if any(t in text for t in ("pythagoras", "hypotenuse", "kathete")):
        return TOPICS["pythagoras"]
    if any(t in text for t in ("prozent", "%", "rabatt", "mehrwertsteuer", "zins")):
        return TOPICS["percent"]
    if any(t in text for t in ("bruch", "nenner", "zähler", "erweitern", "kürzen")) or re.search(r"\d+\s*/\s*\d+", text):
        return TOPICS["fraction"]
    if any(t in text for t in ("rechteck", "dreieck", "kreis", "umfang", "fläche", "volumen", "höhe", "radius", "durchmesser", "prisma", "quader")):
        return TOPICS["geometry"]
    if any(t in text for t in ("funktion", "steigung", "graph", "parabel", "nullstelle")):
        return TOPICS["function"]
    if "=" in text and any(c.isalpha() for c in text):
        return TOPICS["linear_equation"]
    if len(task_text.split()) > 18:
        return TOPICS["word_problem"]
    if any(op in text for op in ("+", "-", "·", "*", ":", "/", "^")):
        return TOPICS["arithmetic"]
    return TOPICS["general"]


def infer_phase(messages: list[dict]) -> str:
    user_text = " ".join(
        str(m.get("content", "")).lower()
        for m in messages[-6:]
        if m.get("role") == "user"
    )
    if any(t in user_text for t in ("probe", "prüfen", "kontrollieren", "stimmt das", "einsetzen")):
        return "PRÜFEN"
    if any(t in user_text for t in ("ergibt", "ausgerechnet", "umformen", "geteilt", "multipliziert")):
        return "RECHNEN"
    if any(t in user_text for t in ("formel", "gleichung", "plan", "strategie", "ich würde")):
        return "PLANEN"
    return "VERSTEHEN"


def build_tutor_instructions(
    task_text: str,
    messages: list[dict],
    help_level: int = 1,
) -> str:
    profile = classify_topic(task_text, messages)
    phase = infer_phase(messages)
    help_level = max(1, min(4, help_level))

    questions = "\n".join(f"- {q}" for q in profile.questions)
    errors = "\n".join(f"- {e}" for e in profile.common_errors)
    hint = profile.hints[help_level - 1]

    return f"""
Du bist Sokrates, ein geduldiger Mathematik-Lerncoach.

Motto: „Ich begleite dich – denken musst du selbst.“

Erkanntes Thema: {profile.label}
Aktuelle Phase: {phase}
Hilfestufe: {help_level}
Passender Impuls: {hint}

Mögliche Lehrerfragen:
{questions}

Typische Fehler:
{errors}

Regeln:
- Antworte in 1 bis 4 kurzen Sätzen.
- Stelle höchstens eine konkrete Frage.
- Passe die Frage an die letzte Schüleräußerung an.
- Verrate nicht sofort die vollständige Lösung oder das Endergebnis.
- Lobe nur konkret.
- Benenne Fehler freundlich und genau.
- Verwende für Mathematik nur $...$ oder $$...$$.
- Wiederhole nicht unnötig die Aufgabenstellung.
- Bleibe möglichst in der aktuellen Lernphase.
""".strip()
