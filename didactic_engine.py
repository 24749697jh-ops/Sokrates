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
        key="linear_equation",
        label="lineare Gleichung",
        questions=(
            "Welche Rechenoperation steht der gesuchten Zahl im Moment am nächsten?",
            "Welche Gegenoperation hebt den nächsten Rechenschritt auf?",
            "Was musst du auf beiden Seiten gleich machen?",
            "Wie kannst du deinen Wert anschließend durch Einsetzen prüfen?",
        ),
        hints=(
            "Betrachte zuerst nur die Operation direkt neben der Variablen.",
            "Nutze die passende Gegenoperation auf beiden Seiten.",
            "Vereinfache anschließend beide Seiten.",
            "Bestimme die Variable und prüfe durch Einsetzen.",
        ),
        common_errors=(
            "Operation nur auf einer Seite durchführen",
            "Vorzeichenfehler beim Umformen",
            "Faktor vor der Variablen nicht berücksichtigen",
        ),
    ),
    "fraction": TopicProfile(
        key="fraction",
        label="Bruchrechnung",
        questions=(
            "Welche Nenner kommen vor?",
            "Welcher gemeinsame Nenner wäre geeignet?",
            "Musst du zuerst erweitern oder kannst du bereits kürzen?",
            "Welche Rechenregel gilt bei dieser Bruchoperation?",
        ),
        hints=(
            "Schau zuerst nur auf die Nenner.",
            "Finde einen gemeinsamen Nenner.",
            "Erweitere die Brüche passend.",
            "Führe die Rechnung aus und kürze am Ende.",
        ),
        common_errors=(
            "Zähler und Nenner getrennt addieren",
            "falsch erweitern",
            "Vorzeichen übersehen",
        ),
    ),
    "percent": TopicProfile(
        key="percent",
        label="Prozentrechnung",
        questions=(
            "Was ist hier das Ganze, also der Grundwert?",
            "Welche Größe ist der Prozentsatz?",
            "Welche Größe ist der Prozentwert?",
            "Müsste das Ergebnis größer oder kleiner als der Grundwert sein?",
        ),
        hints=(
            "Ordne Grundwert, Prozentsatz und Prozentwert zu.",
            "Denke von 100 Prozent zu 1 Prozent.",
            "Gehe von 1 Prozent zur gesuchten Prozentzahl.",
            "Prüfe, ob das Ergebnis zur Situation passt.",
        ),
        common_errors=(
            "Grundwert und Prozentwert vertauschen",
            "Prozentzahl nicht durch 100 teilen",
            "Ergebnis nicht auf Plausibilität prüfen",
        ),
    ),
    "geometry": TopicProfile(
        key="geometry",
        label="Geometrie",
        questions=(
            "Welche Figur erkennst du?",
            "Welche Größen sind gegeben und welche wird gesucht?",
            "Welche Eigenschaft der Figur hilft dir weiter?",
            "Welche Formel passt genau zur gesuchten Größe?",
        ),
        hints=(
            "Markiere Gegebenes und Gesuchtes.",
            "Schreibe die passende Formel zuerst ohne Zahlen auf.",
            "Setze die bekannten Werte ein.",
            "Achte auf die richtige Einheit.",
        ),
        common_errors=(
            "Umfang und Flächeninhalt verwechseln",
            "Einheiten nicht beachten",
            "Formel falsch umstellen",
        ),
    ),
    "function": TopicProfile(
        key="function",
        label="Funktionen",
        questions=(
            "Welche Größe hängt von welcher anderen Größe ab?",
            "Was beschreibt die Steigung in dieser Situation?",
            "Welche Bedeutung hat der Anfangswert?",
            "Welches Wertepaar kannst du zur Kontrolle einsetzen?",
        ),
        hints=(
            "Suche nach Anfangswert und Veränderung pro Schritt.",
            "Ordne diese Informationen einer Funktionsgleichung zu.",
            "Setze ein bekanntes Wertepaar ein.",
            "Prüfe, ob Graph und Gleichung zusammenpassen.",
        ),
        common_errors=(
            "Steigung und Anfangswert vertauschen",
            "x- und y-Werte verwechseln",
            "Vorzeichen der Steigung falsch deuten",
        ),
    ),
    "pythagoras": TopicProfile(
        key="pythagoras",
        label="Satz des Pythagoras",
        questions=(
            "Wo liegt der rechte Winkel?",
            "Welche Seite ist die Hypotenuse?",
            "Welche beiden Seiten sind Katheten?",
            "Welche Länge soll berechnet werden?",
        ),
        hints=(
            "Bestimme zuerst die Hypotenuse.",
            "Ordne die Seiten in $a^2+b^2=c^2$ ein.",
            "Setze die bekannten Längen ein.",
            "Ziehe erst am Ende die Wurzel.",
        ),
        common_errors=(
            "falsche Seite als Hypotenuse wählen",
            "Wurzel vergessen",
            "Einheiten nicht angeben",
        ),
    ),
    "word_problem": TopicProfile(
        key="word_problem",
        label="Textaufgabe",
        questions=(
            "Was ist in der Aufgabe gegeben?",
            "Was soll am Ende herausgefunden werden?",
            "Welche Beziehung zwischen den Größen beschreibt der Text?",
            "Kannst du den Zusammenhang zunächst in eigenen Worten ausdrücken?",
        ),
        hints=(
            "Trenne Gegebenes und Gesuchtes.",
            "Beschreibe den Zusammenhang ohne Zahlen.",
            "Übersetze ihn in eine Rechnung oder Gleichung.",
            "Prüfe, ob das Ergebnis zur Geschichte passt.",
        ),
        common_errors=(
            "zu früh rechnen",
            "gesuchte Größe nicht klar benennen",
            "Textbeziehung falsch übersetzen",
        ),
    ),
    "arithmetic": TopicProfile(
        key="arithmetic",
        label="Rechenaufgabe",
        questions=(
            "Welche Rechenoperation kommt zuerst?",
            "Kannst du den Ausdruck in kleinere Teile zerlegen?",
            "Welche Regel ist an dieser Stelle wichtig?",
            "Wie kannst du das Ergebnis überschlagen?",
        ),
        hints=(
            "Achte auf Klammern sowie Punkt vor Strich.",
            "Berechne zuerst einen klar abgegrenzten Teil.",
            "Arbeite schrittweise weiter.",
            "Vergleiche mit einem Überschlag.",
        ),
        common_errors=(
            "Reihenfolge der Rechenoperationen übersehen",
            "Vorzeichenfehler",
            "Zwischenschritte überspringen",
        ),
    ),
    "general": TopicProfile(
        key="general",
        label="Mathematikaufgabe",
        questions=(
            "Was verstehst du an der Aufgabe bereits sicher?",
            "Welche Information ist gegeben und was wird gesucht?",
            "An welcher Stelle beginnt deine Unsicherheit?",
            "Welcher kleine nächste Schritt wäre möglich?",
        ),
        hints=(
            "Trenne Gegebenes und Gesuchtes.",
            "Beschreibe den Zusammenhang in Worten.",
            "Wähle eine passende Darstellung oder Formel.",
            "Führe einen ersten kleinen Rechenschritt aus.",
        ),
        common_errors=(
            "zu viele Schritte gleichzeitig",
            "unklare Bezeichnungen",
            "Ergebnis nicht prüfen",
        ),
    ),
}


def _conversation_text(messages: Iterable[dict]) -> str:
    return " ".join(
        str(message.get("content", ""))
        for message in messages
    ).lower()


def classify_topic(task_text: str, messages: list[dict]) -> TopicProfile:
    text = f"{task_text} {_conversation_text(messages)}".lower()

    if any(term in text for term in ("pythagoras", "hypotenuse", "kathete")):
        return TOPICS["pythagoras"]
    if any(term in text for term in (
        "prozent", "%", "rabatt", "mehrwertsteuer", "zins"
    )):
        return TOPICS["percent"]
    if any(term in text for term in (
        "bruch", "nenner", "zähler", "erweitern", "kürzen"
    )) or re.search(r"\d+\s*/\s*\d+", text):
        return TOPICS["fraction"]
    if any(term in text for term in (
        "rechteck", "dreieck", "kreis", "umfang", "fläche",
        "flächeninhalt", "volumen", "winkel", "radius", "durchmesser"
    )):
        return TOPICS["geometry"]
    if any(term in text for term in (
        "funktion", "steigung", "y-achse", "x-achse",
        "graph", "parabel", "nullstelle"
    )):
        return TOPICS["function"]
    if re.search(r"\b[a-z]\s*[+\-*/]?\s*\d*\s*=", text) or (
        "=" in text and any(char.isalpha() for char in text)
    ):
        return TOPICS["linear_equation"]
    if len(task_text.split()) > 18:
        return TOPICS["word_problem"]
    if any(operator in text for operator in ("+", "-", "·", "*", ":", "/", "^")):
        return TOPICS["arithmetic"]
    return TOPICS["general"]


def infer_phase(messages: list[dict]) -> str:
    if not messages:
        return "VERSTEHEN"

    last_user_messages = [
        str(message.get("content", "")).lower()
        for message in messages
        if message.get("role") == "user"
    ]
    recent = " ".join(last_user_messages[-3:])

    if any(term in recent for term in (
        "probe", "prüfen", "kontrollieren", "stimmt das",
        "einsetzen", "ergebnis"
    )):
        return "PRÜFEN"
    if any(term in recent for term in (
        "ich rechne", "ergibt", "ausgerechnet", "umformen",
        "geteilt", "multipliziert", "addiert", "subtrahiert"
    )):
        return "RECHNEN"
    if any(term in recent for term in (
        "formel", "gleichung aufstellen", "plan", "strategie",
        "ich würde", "mein weg"
    )):
        return "PLANEN"
    return "VERSTEHEN"


def detect_response_pattern(messages: list[dict]) -> str:
    assistant_messages = [
        str(message.get("content", "")).lower()
        for message in messages
        if message.get("role") == "assistant"
    ]

    if len(assistant_messages) < 2:
        return "keine Wiederholung erkennbar"

    last = assistant_messages[-1]
    previous = assistant_messages[-2]
    overlap = set(last.split()) & set(previous.split())

    if len(overlap) >= 8:
        return (
            "Die letzten beiden Antworten ähneln sich. "
            "Formuliere diesmal deutlich anders."
        )
    return "keine Wiederholung erkennbar"


def help_instruction(help_level: int, profile: TopicProfile) -> str:
    level = max(1, min(4, help_level))
    hint = profile.hints[level - 1]

    levels = {
        1: (
            "Hilfestufe 1: Stelle eine kleine, konkrete Denkfrage. "
            "Gib noch keinen Rechenschritt vor."
        ),
        2: (
            "Hilfestufe 2: Gib einen kurzen Denkimpuls und stelle danach "
            "eine konkrete Frage."
        ),
        3: (
            "Hilfestufe 3: Mache einen kleinen Teilschritt sichtbar, "
            "aber lasse den Lernenden den nächsten Schritt ausführen."
        ),
        4: (
            "Hilfestufe 4: Entwickle den Lösungsweg gemeinsam in sehr "
            "kleinen Schritten. Verrate trotzdem nicht sofort das Endergebnis."
        ),
    }

    return f"{levels[level]}\nPassender Hinweis dieser Stufe: {hint}"


def build_tutor_instructions(
    task_text: str,
    messages: list[dict],
    help_level: int = 1,
) -> str:
    profile = classify_topic(task_text, messages)
    phase = infer_phase(messages)
    repetition_note = detect_response_pattern(messages)

    question_list = "\n".join(
        f"- {question}" for question in profile.questions
    )
    error_list = "\n".join(
        f"- {error}" for error in profile.common_errors
    )

    return f"""
Du bist Sokrates, ein geduldiger Mathematik-Lerncoach.

Motto:
„Ich begleite dich – denken musst du selbst.“

ZIEL
Hilf dem Lernenden, den kleinsten sinnvollen nächsten Denkschritt selbst zu tun.
Gib nicht sofort die vollständige Lösung und kein ungefragtes Endergebnis.

ERKANNTER DIDAKTISCHER KONTEXT
Thema: {profile.label}
Phase: {phase}
Wiederholungsprüfung: {repetition_note}

PASSENDE LEHRERFRAGEN
{question_list}

TYPISCHE FEHLER
{error_list}

{help_instruction(help_level, profile)}

VERBINDLICHE ANTWORTREGELN
- Antworte in 1 bis 4 kurzen Sätzen.
- Stelle höchstens eine echte Frage.
- Die Frage muss konkret zur Aufgabe und zur letzten Schüleräußerung passen.
- Wiederhole nicht einfach die Aufgabenstellung.
- Verwende keine Floskeln wie „Interessante Überlegung“.
- Lobe nur konkret, zum Beispiel: „Bis hier hast du sauber umgeformt.“
- Benenne Fehler freundlich und präzise.
- Verwende mathematische Schreibweise nur mit $...$ oder $$...$$.
- Führe niemals mehrere Lösungswege gleichzeitig ein.
- Bleibe in der erkannten Phase, außer die letzte Schülerantwort zeigt klar,
  dass die nächste Phase erreicht ist.

INTERNE ENTSCHEIDUNG
Entscheide still:
1. Was hat der Lernende bereits verstanden?
2. Wo liegt die aktuelle Hürde?
3. Was ist der kleinste nächste Schritt?
4. Braucht es eine Frage, einen Hinweis oder einen kleinen Teilschritt?
5. Ist die Formulierung natürlich und nicht wiederholend?

FALLBACK
Du darfst niemals sagen, dass dir keine passende Frage einfällt.
Wenn du unsicher bist, frage:
„Welche Größe ist gesucht, und welche Angabe verbindet sie mit dem bereits Bekannten?“
""".strip()
