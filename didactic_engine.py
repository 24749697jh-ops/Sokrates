from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DidacticProfile:
    topic: str
    topic_label: str
    question_bank: tuple[str, ...]
    hint_ladder: tuple[str, ...]
    common_errors: tuple[str, ...]


PROFILES: dict[str, DidacticProfile] = {
    "linear_equation": DidacticProfile(
        topic="linear_equation",
        topic_label="lineare Gleichung",
        question_bank=(
            "Welche Rechenoperation steht der gesuchten Zahl im Moment am nächsten?",
            "Welche Operation könntest du auf beiden Seiten rückgängig machen?",
            "Was möchtest du zuerst vereinfachen?",
            "Woran erkennst du, ob dein nächster Schritt die Gleichung unverändert lässt?",
        ),
        hint_ladder=(
            "Betrachte zuerst nur die Operation direkt neben der Variablen.",
            "Überlege, welche Gegenoperation diese Operation aufhebt.",
            "Führe dieselbe Gegenoperation auf beiden Seiten aus.",
        ),
        common_errors=(
            "Operation nur auf einer Seite ausführen",
            "Vorzeichen beim Umformen verlieren",
            "zu viele Schritte auf einmal machen",
        ),
    ),
    "geometry": DidacticProfile(
        topic="geometry",
        topic_label="Geometrie",
        question_bank=(
            "Welche Größen sind gegeben und welche Größe wird gesucht?",
            "Welche Figur erkennst du, und welche Eigenschaften dieser Figur helfen dir?",
            "Kannst du die Beziehungen zwischen den Größen zunächst in Worten beschreiben?",
            "Welche Formel passt zu genau der gesuchten Größe?",
        ),
        hint_ladder=(
            "Markiere zuerst Gegebenes und Gesuchtes.",
            "Schreibe die passende Beziehung vollständig mit Größenbezeichnungen auf.",
            "Setze erst danach die bekannten Werte ein.",
        ),
        common_errors=(
            "Umfang und Flächeninhalt verwechseln",
            "Einheiten nicht beachten",
            "Formel zu früh mit Zahlen füllen",
        ),
    ),
    "percent": DidacticProfile(
        topic="percent",
        topic_label="Prozentrechnung",
        question_bank=(
            "Was ist hier der Grundwert, also das Ganze?",
            "Welche Größe ist der Prozentsatz und welche der Prozentwert?",
            "Kannst du die Situation zuerst mit 100 Prozent beschreiben?",
            "Müsste das Ergebnis größer oder kleiner als der Grundwert sein?",
        ),
        hint_ladder=(
            "Ordne zuerst Grundwert, Prozentsatz und Prozentwert zu.",
            "Denke von 100 Prozent zu 1 Prozent.",
            "Gehe von 1 Prozent zur gesuchten Prozentzahl.",
        ),
        common_errors=(
            "Grundwert und Prozentwert vertauschen",
            "Prozentzahl nicht durch 100 teilen",
            "Plausibilitätsprüfung vergessen",
        ),
    ),
    "function": DidacticProfile(
        topic="function",
        topic_label="Funktionen",
        question_bank=(
            "Welche Größe hängt von welcher anderen Größe ab?",
            "Was beschreibt die Steigung in dieser Situation?",
            "Welche Bedeutung hat der Anfangswert?",
            "Kannst du einen Punkt oder ein Wertepaar aus der Aufgabe ablesen?",
        ),
        hint_ladder=(
            "Suche zuerst nach Anfangswert und Veränderung pro Schritt.",
            "Ordne diese Informationen einer Funktionsgleichung zu.",
            "Prüfe die Gleichung an einem bekannten Wertepaar.",
        ),
        common_errors=(
            "Steigung und Anfangswert vertauschen",
            "x- und y-Werte verwechseln",
            "Einheiten der Steigung ignorieren",
        ),
    ),
    "word_problem": DidacticProfile(
        topic="word_problem",
        topic_label="Textaufgabe",
        question_bank=(
            "Was ist in der Aufgabe bekannt?",
            "Was soll am Ende herausgefunden werden?",
            "Welche Beziehung zwischen den Größen wird im Text beschrieben?",
            "Kannst du die Aufgabe in einem eigenen Satz zusammenfassen?",
        ),
        hint_ladder=(
            "Unterstreiche zuerst Gegebenes und Gesuchtes.",
            "Formuliere den Zusammenhang ohne Zahlen.",
            "Übersetze erst danach den Zusammenhang in eine Rechnung oder Gleichung.",
        ),
        common_errors=(
            "zu früh rechnen",
            "gesuchte Größe nicht eindeutig benennen",
            "Textbeziehung falsch in eine Gleichung übersetzen",
        ),
    ),
    "arithmetic": DidacticProfile(
        topic="arithmetic",
        topic_label="Rechenaufgabe",
        question_bank=(
            "Welche Rechenregel ist hier als Nächstes wichtig?",
            "Kannst du den Ausdruck in kleinere Teile zerlegen?",
            "Welche Rechnung würdest du zuerst durchführen und warum?",
            "Wie kannst du dein Zwischenergebnis überschlagen?",
        ),
        hint_ladder=(
            "Achte auf die Reihenfolge der Rechenoperationen.",
            "Berechne zuerst einen klar abgegrenzten Teil.",
            "Vergleiche das Ergebnis mit einem Überschlag.",
        ),
        common_errors=(
            "Punkt-vor-Strich-Regel übersehen",
            "Vorzeichenfehler",
            "kein Überschlag",
        ),
    ),
    "general": DidacticProfile(
        topic="general",
        topic_label="Mathematikaufgabe",
        question_bank=(
            "Was verstehst du an der Aufgabe bereits sicher?",
            "Welche Information ist gegeben und was wird gesucht?",
            "An welcher Stelle beginnt für dich die Unsicherheit?",
            "Welcher kleine nächste Schritt wäre möglich, ohne schon alles zu lösen?",
        ),
        hint_ladder=(
            "Trenne Gegebenes und Gesuchtes.",
            "Beschreibe den mathematischen Zusammenhang in Worten.",
            "Wähle danach eine passende Darstellung oder Formel.",
        ),
        common_errors=(
            "zu viele Schritte gleichzeitig",
            "unklare Bezeichnungen",
            "Ergebnis nicht prüfen",
        ),
    ),
}


def classify_topic(text: str) -> str:
    t = text.lower()

    if any(w in t for w in ("prozent", "%", "rabatt", "mehrwertsteuer", "zins")):
        return "percent"
    if any(w in t for w in (
        "rechteck", "dreieck", "kreis", "umfang", "fläche", "flächeninhalt",
        "volumen", "winkel", "seite", "höhe", "radius", "durchmesser"
    )):
        return "geometry"
    if any(w in t for w in (
        "funktion", "steigung", "y-achse", "x-achse", "graph", "parabel",
        "nullstelle", "funktionsgleichung"
    )):
        return "function"
    if re.search(r"\b[a-zA-Z]\s*[+\-*/]?\s*\d*\s*=", text) or (
        "=" in text and any(ch.isalpha() for ch in text)
    ):
        return "linear_equation"
    if len(t.split()) > 18:
        return "word_problem"
    if any(op in text for op in ("+", "-", "·", "*", ":", "/", "^")):
        return "arithmetic"
    return "general"


def infer_phase(messages: Iterable[dict]) -> str:
    conversation = " ".join(
        str(m.get("content", "")) for m in messages
    ).lower()

    if any(w in conversation for w in (
        "probe", "prüfen", "kontrollieren", "stimmt das", "einsetzen"
    )):
        return "PRÜFEN"
    if any(w in conversation for w in (
        "ich rechne", "ergibt", "ausgerechnet", "umformen", "eingesetzt"
    )):
        return "RECHNEN"
    if any(w in conversation for w in (
        "formel", "gleichung aufstellen", "plan", "weg", "strategie"
    )):
        return "PLANEN"
    return "VERSTEHEN"


def build_didactic_context(task_text: str, messages: list[dict]) -> str:
    topic = classify_topic(task_text)
    profile = PROFILES[topic]
    phase = infer_phase(messages)

    questions = "\n".join(f"- {q}" for q in profile.question_bank)
    hints = "\n".join(
        f"{i + 1}. {h}" for i, h in enumerate(profile.hint_ladder)
    )
    errors = "\n".join(f"- {e}" for e in profile.common_errors)

    return f"""
DIDAKTISCHER KONTEXT FÜR DIESE AUFGABE

Erkanntes Themenfeld: {profile.topic_label}
Vermutete Lernphase: {phase}

Geeignete Lehrerfragen:
{questions}

Abgestufte Hinweise:
{hints}

Typische Fehler, auf die du aufmerksam achten sollst:
{errors}

Nutze diese Sammlung als Orientierung. Wähle niemals mehrere Fragen auf einmal.
""".strip()
