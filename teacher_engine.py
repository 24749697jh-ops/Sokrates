from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TaskType:
    key: str
    label: str
    topic_key: str
    patterns: tuple[str, ...]
    opening_questions: tuple[str, ...]
    planning_questions: tuple[str, ...]
    calculation_questions: tuple[str, ...]
    checking_questions: tuple[str, ...]
    hints: tuple[str, ...]
    common_errors: tuple[str, ...]


TASK_TYPES: tuple[TaskType, ...] = (
    TaskType(
        "linear_equation_solve",
        "Lineare Gleichung lösen",
        "linear_equation",
        (
            r"\b(löse|bestimme)\b.*\bx\b",
            r"\bx\b.*=",
            r"=\s*[-+]?\d",
        ),
        (
            "Welche Rechenoperation steht direkt neben der Variablen und muss zuerst rückgängig gemacht werden?",
            "Welcher Term verhindert im Moment, dass die Variable allein steht?",
        ),
        (
            "Welche Gegenoperation musst du auf beiden Seiten ausführen?",
            "In welcher Reihenfolge solltest du die Rechenschritte rückgängig machen?",
        ),
        (
            "Was ergibt sich nach diesem Umformungsschritt auf beiden Seiten?",
            "Welchen einzelnen Rechenschritt kannst du jetzt ausführen?",
        ),
        (
            "Was erhältst du, wenn du deinen Wert in die Ausgangsgleichung einsetzt?",
            "Sind linke und rechte Seite bei der Probe gleich?",
        ),
        (
            "Arbeite von außen nach innen und mache jeden Schritt auf beiden Seiten.",
            "Nutze zuerst die Gegenoperation zur Addition oder Subtraktion.",
            "Teile erst danach durch den Faktor vor der Variablen.",
            "Setze das Ergebnis zur Probe ein.",
        ),
        (
            "Operation nur auf einer Seite",
            "Vorzeichenfehler",
            "falsche Reihenfolge der Gegenoperationen",
        ),
    ),
    TaskType(
        "fraction_add_subtract",
        "Brüche addieren oder subtrahieren",
        "fraction",
        (
            r"\d+\s*/\s*\d+\s*[+-]\s*\d+\s*/\s*\d+",
            r"\b(addiere|subtrahiere)\b.*\bbr",
            r"\bnenner\b",
        ),
        (
            "Sind die Nenner bereits gleich, oder musst du zuerst erweitern?",
            "Welcher gemeinsame Nenner passt zu beiden Brüchen?",
        ),
        (
            "Mit welchen Faktoren musst du die Brüche erweitern?",
            "Welche Zähler entstehen nach dem Erweitern?",
        ),
        (
            "Welche Zähler kannst du jetzt zusammenfassen?",
            "Kannst du den entstandenen Bruch noch kürzen?",
        ),
        (
            "Ist das Ergebnis vollständig gekürzt?",
            "Passt die Größe des Ergebnisses zu den beiden Ausgangsbrüchen?",
        ),
        (
            "Betrachte zuerst nur die Nenner.",
            "Finde einen gemeinsamen Nenner.",
            "Erweitere beide Brüche korrekt.",
            "Rechne die Zähler und kürze am Ende.",
        ),
        (
            "Zähler und Nenner getrennt addiert",
            "falsch erweitert",
            "nicht vollständig gekürzt",
        ),
    ),
    TaskType(
        "percent_value",
        "Prozentwert berechnen",
        "percent",
        (
            r"\b(wie viel|berechne)\b.*\bprozent\b.*\bvon\b",
            r"\bprozentwert\b",
            r"\b\d+(?:[.,]\d+)?\s*%\b.*\bvon\b",
        ),
        (
            "Welche Zahl ist hier das Ganze, also der Grundwert?",
            "Welche Prozentzahl soll von welchem Grundwert berechnet werden?",
        ),
        (
            "Wie viel entspricht zunächst 1 Prozent des Grundwertes?",
            "Welche Formel verbindet Grundwert, Prozentsatz und Prozentwert?",
        ),
        (
            "Mit welchem Faktor musst du den Grundwert multiplizieren?",
            "Welchen Rechenschritt kannst du nun ausführen?",
        ),
        (
            "Ist dein Prozentwert kleiner oder größer als der Grundwert, und ist das plausibel?",
            "Welche Einheit gehört zum Ergebnis?",
        ),
        (
            "Ordne Grundwert und Prozentsatz zuerst eindeutig zu.",
            "Teile den Prozentsatz durch 100.",
            "Multipliziere anschließend mit dem Grundwert.",
            "Prüfe die Größenordnung.",
        ),
        (
            "Grundwert und Prozentwert vertauscht",
            "Prozentzahl nicht durch 100 geteilt",
            "Einheit vergessen",
        ),
    ),
    TaskType(
        "circle_sector_area",
        "Fläche eines Kreisausschnitts",
        "geometry",
        (
            r"\bkreisausschnitt\b.*\bfläche",
            r"\bsektor\b.*\bfläche",
            r"\bmittelpunktswinkel\b",
        ),
        (
            "Welcher Mittelpunktswinkel und welcher Radius sind gegeben?",
            "Welchen Anteil eines vollständigen Kreises beschreibt der Winkel?",
        ),
        (
            "Wie lautet die Formel für die Fläche des ganzen Kreises?",
            "Mit welchem Bruchteil von 360 Grad musst du die Kreisfläche multiplizieren?",
        ),
        (
            "Welche Werte setzt du für Winkel und Radius ein?",
            "Welchen Teil der Rechnung kannst du zuerst vereinfachen?",
        ),
        (
            "Ist deine Fläche kleiner als die Fläche des vollständigen Kreises?",
            "Hast du eine Flächeneinheit verwendet?",
        ),
        (
            "Berechne gedanklich zuerst die Fläche des ganzen Kreises.",
            "Der Kreisausschnitt ist der Anteil α zu 360 Grad.",
            "Multipliziere diesen Anteil mit π mal r².",
            "Prüfe, ob das Ergebnis kleiner als die ganze Kreisfläche ist.",
        ),
        (
            "Winkel nicht durch 360 geteilt",
            "Radius nicht quadriert",
            "Bogenlänge statt Fläche berechnet",
        ),
    ),
    TaskType(
        "circle_arc_length",
        "Bogenlänge berechnen",
        "geometry",
        (
            r"\bkreisbogen\b",
            r"\bbogenlänge\b",
            r"\bkreisausschnitt\b.*\bumfang",
        ),
        (
            "Welcher Winkel und welcher Radius gehören zum Kreisbogen?",
            "Welchen Anteil des vollständigen Kreisumfangs beschreibt der Winkel?",
        ),
        (
            "Wie lautet die Formel für den ganzen Kreisumfang?",
            "Mit welchem Anteil von 360 Grad musst du den Umfang multiplizieren?",
        ),
        (
            "Welche Werte setzt du in die Bogenlängenformel ein?",
            "Welchen Rechenschritt kannst du zuerst vereinfachen?",
        ),
        (
            "Ist die Bogenlänge kleiner als der vollständige Kreisumfang?",
            "Hast du eine Längeneinheit verwendet?",
        ),
        (
            "Beginne mit dem ganzen Kreisumfang 2 mal π mal r.",
            "Multipliziere mit dem Winkelanteil α zu 360 Grad.",
            "Vereinfache den Bruch, wenn möglich.",
            "Prüfe die Größenordnung.",
        ),
        (
            "Kreisfläche statt Umfang verwendet",
            "Winkelanteil vergessen",
            "Längen- und Flächeneinheit verwechselt",
        ),
    ),
    TaskType(
        "rectangle_area",
        "Fläche eines Rechtecks",
        "geometry",
        (
            r"\brechteck\b.*\bfläche",
            r"\bflächeninhalt\b.*\brechteck",
        ),
        (
            "Welche beiden Seitenlängen des Rechtecks sind gegeben?",
            "Welche Größen musst du miteinander multiplizieren?",
        ),
        (
            "Wie lautet die Flächenformel für ein Rechteck?",
            "Welche Einheit muss nach dem Multiplizieren entstehen?",
        ),
        (
            "Welche Werte setzt du für Länge und Breite ein?",
            "Was ergibt das Produkt der beiden Seitenlängen?",
        ),
        (
            "Hast du eine quadratische Einheit verwendet?",
            "Passt die Größenordnung zur Zeichnung oder Aufgabenstellung?",
        ),
        (
            "Nutze Länge mal Breite.",
            "Setze zuerst die beiden Seitenlängen ein.",
            "Multipliziere anschließend.",
            "Schreibe eine Flächeneinheit.",
        ),
        (
            "Umfang statt Fläche berechnet",
            "Seiten addiert statt multipliziert",
            "Quadrateinheit vergessen",
        ),
    ),
    TaskType(
        "triangle_area",
        "Fläche eines Dreiecks",
        "geometry",
        (
            r"\bdreieck\b.*\bfläche",
            r"\bflächeninhalt\b.*\bdreieck",
        ),
        (
            "Welche Grundseite und welche dazugehörige Höhe sind gegeben?",
            "Welche Höhe steht senkrecht auf der gewählten Grundseite?",
        ),
        (
            "Wie lautet die Flächenformel für ein Dreieck?",
            "Warum wird das Produkt aus Grundseite und Höhe durch 2 geteilt?",
        ),
        (
            "Welche Werte setzt du für Grundseite und Höhe ein?",
            "Was ergibt zunächst Grundseite mal Höhe?",
        ),
        (
            "Hast du das Ergebnis durch 2 geteilt?",
            "Hast du eine quadratische Einheit verwendet?",
        ),
        (
            "Wähle Grundseite und zugehörige Höhe.",
            "Multipliziere beide Werte.",
            "Teile das Produkt durch 2.",
            "Prüfe die Einheit.",
        ),
        (
            "falsche Höhe gewählt",
            "Division durch 2 vergessen",
            "Umfang statt Fläche berechnet",
        ),
    ),
    TaskType(
        "pythagoras_hypotenuse",
        "Hypotenuse mit Pythagoras berechnen",
        "pythagoras",
        (
            r"\bpythagoras\b",
            r"\bhypotenuse\b",
            r"\brechtwinklig",
        ),
        (
            "Wo liegt der rechte Winkel und welche Seite ist deshalb die Hypotenuse?",
            "Welche beiden Kathetenlängen sind gegeben?",
        ),
        (
            "Wie ordnest du die Seiten in a² + b² = c² ein?",
            "Welche Seite steht allein auf der rechten Seite der Formel?",
        ),
        (
            "Welche Quadrate musst du addieren?",
            "Wann musst du die Wurzel ziehen?",
        ),
        (
            "Ist die Hypotenuse länger als jede einzelne Kathete?",
            "Passt dein Ergebnis zur Skizze?",
        ),
        (
            "Bestimme zuerst eindeutig die Hypotenuse.",
            "Setze die Katheten in a² + b² ein.",
            "Addiere die Quadrate.",
            "Ziehe erst am Ende die Wurzel.",
        ),
        (
            "falsche Seite als Hypotenuse",
            "Wurzel vergessen",
            "Quadrate falsch berechnet",
        ),
    ),
    TaskType(
        "linear_function_slope",
        "Steigung einer linearen Funktion",
        "function",
        (
            r"\bsteigung\b",
            r"\bm\s*=",
            r"\bzwei punkte\b",
        ),
        (
            "Welche beiden Punkte oder welche Veränderung von x und y sind gegeben?",
            "Wie stark ändert sich y, wenn x zunimmt?",
        ),
        (
            "Welche Differenz gehört in den Zähler und welche in den Nenner?",
            "Warum musst du dieselbe Punktreihenfolge für x und y verwenden?",
        ),
        (
            "Wie groß ist die Änderung von y?",
            "Wie groß ist die zugehörige Änderung von x?",
        ),
        (
            "Passt das Vorzeichen der Steigung zum Verlauf des Graphen?",
            "Ist deine Steigung plausibel?",
        ),
        (
            "Berechne zuerst Δy.",
            "Berechne dann Δx in derselben Punktreihenfolge.",
            "Teile Δy durch Δx.",
            "Prüfe das Vorzeichen am Graphen.",
        ),
        (
            "Punktreihenfolge gemischt",
            "x- und y-Differenz vertauscht",
            "Vorzeichen falsch",
        ),
    ),
    TaskType(
        "word_problem_general",
        "Textaufgabe",
        "word_problem",
        (
            r".{90,}",
            r"\b(insgesamt|zusammen|jeweils|kostet|fährt|alter|mehr als|weniger als)\b",
        ),
        (
            "Welche konkrete Größe soll am Ende bestimmt werden?",
            "Welche Angaben im Text gehören unmittelbar zur gesuchten Größe?",
        ),
        (
            "Welchen Zusammenhang kannst du zuerst in Worten beschreiben?",
            "Welche Rechnung oder Gleichung bildet diesen Zusammenhang ab?",
        ),
        (
            "Welchen ersten Rechenschritt kannst du mit den gegebenen Zahlen ausführen?",
            "Welche Zwischengröße brauchst du als Nächstes?",
        ),
        (
            "Beantwortet dein Ergebnis wirklich die Frage des Textes?",
            "Ist das Ergebnis in der beschriebenen Situation plausibel?",
        ),
        (
            "Markiere zuerst Gegebenes und Gesuchtes.",
            "Formuliere den Zusammenhang ohne Zahlen.",
            "Übersetze ihn in eine Rechnung oder Gleichung.",
            "Prüfe das Ergebnis an der Alltagssituation.",
        ),
        (
            "zu früh gerechnet",
            "Frage des Textes nicht beantwortet",
            "Einheit oder Bedeutung des Ergebnisses vergessen",
        ),
    ),
    TaskType(
        "arithmetic_expression",
        "Rechenausdruck",
        "arithmetic",
        (
            r"\d+\s*[\+\-\*·:/]\s*\d+",
            r"\bvereinfache\b",
            r"\bberechne\b",
        ),
        (
            "Welche Rechenoperation muss nach den Rechenregeln zuerst ausgeführt werden?",
            "Gibt es Klammern oder Punktrechnungen, die Vorrang haben?",
        ),
        (
            "In welche kleinen Teilschritte kannst du den Ausdruck zerlegen?",
            "Welchen Teil solltest du zuerst berechnen?",
        ),
        (
            "Was ergibt der erste Teil des Ausdrucks?",
            "Welcher Rest bleibt danach noch zu berechnen?",
        ),
        (
            "Passt das Ergebnis zu einem Überschlag?",
            "Hast du die Rechenreihenfolge eingehalten?",
        ),
        (
            "Achte auf Klammern.",
            "Beachte Punkt vor Strich.",
            "Rechne schrittweise.",
            "Prüfe mit einem Überschlag.",
        ),
        (
            "Reihenfolge übersehen",
            "Vorzeichenfehler",
            "Zwischenschritte ausgelassen",
        ),
    ),
)


GENERIC_TASK = TaskType(
    "generic_math",
    "Mathematikaufgabe",
    "general",
    (),
    (
        "Welcher konkrete Teil der Aufgabe ist für den ersten Schritt entscheidend?",
        "Welche Information aus der Aufgabe brauchst du zuerst, um sinnvoll beginnen zu können?",
    ),
    (
        "Welcher mathematische Zusammenhang steckt in der Aufgabe?",
        "Welche Darstellung, Formel oder Rechenregel könnte hier passen?",
    ),
    (
        "Welchen einzelnen Rechenschritt kannst du jetzt sicher ausführen?",
        "Was ergibt sich aus diesem Zwischenschritt?",
    ),
    (
        "Wie kannst du dein Ergebnis an der Aufgabe überprüfen?",
        "Passt dein Ergebnis zur Größenordnung und zur Einheit?",
    ),
    (
        "Konzentriere dich auf einen einzigen ersten Schritt.",
        "Ordne Gegebenes und Gesuchtes.",
        "Wähle eine passende Regel oder Formel.",
        "Prüfe das Ergebnis an der Aufgabenstellung.",
    ),
    (
        "zu viele Schritte gleichzeitig",
        "unpassende Formel gewählt",
        "Ergebnis nicht geprüft",
    ),
)


def _conversation_text(messages: Iterable[dict]) -> str:
    return " ".join(
        str(message.get("content", ""))
        for message in messages
        if message.get("role") == "user"
    )


def infer_phase(messages: list[dict]) -> str:
    text = _conversation_text(messages[-8:]).lower()
    if any(word in text for word in ("probe", "prüfen", "kontrolle", "stimmt", "einsetzen")):
        return "PRÜFEN"
    if any(word in text for word in ("gerechnet", "ergibt", "umformen", "multipliziert", "geteilt")):
        return "RECHNEN"
    if any(word in text for word in ("formel", "plan", "strategie", "ich würde", "ansatz")):
        return "PLANEN"
    return "VERSTEHEN"


def classify_task(task_text: str, messages: list[dict]) -> TaskType:
    text = f"{task_text}\n{_conversation_text(messages)}".lower().strip()

    best_type = GENERIC_TASK
    best_score = 0

    for task_type in TASK_TYPES:
        score = 0
        for pattern in task_type.patterns:
            if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
                score += 1
        if score > best_score:
            best_score = score
            best_type = task_type

    return best_type


def _question_for_phase(task_type: TaskType, phase: str, index: int = 0) -> str:
    pools = {
        "VERSTEHEN": task_type.opening_questions,
        "PLANEN": task_type.planning_questions,
        "RECHNEN": task_type.calculation_questions,
        "PRÜFEN": task_type.checking_questions,
    }
    questions = pools.get(phase, task_type.opening_questions)
    return questions[index % len(questions)]


def build_teacher_instructions(
    task_text: str,
    messages: list[dict],
    help_level: int = 1,
) -> str:
    task_type = classify_task(task_text, messages)
    phase = infer_phase(messages)
    help_level = max(1, min(4, help_level))
    question_index = max(0, len([m for m in messages if m.get("role") == "assistant"]) - 1)
    preferred_question = _question_for_phase(task_type, phase, question_index)
    hint = task_type.hints[help_level - 1]
    errors = "\n".join(f"- {error}" for error in task_type.common_errors)

    return f"""
Du bist Sokrates, ein erfahrener Mathematiklehrer und Lerncoach.

Motto: „Ich begleite dich – denken musst du selbst.“

Konkreter Aufgabentyp: {task_type.label}
Aktuelle Lernphase: {phase}
Hilfestufe: {help_level}
Bevorzugte Lehrerfrage für diesen Moment:
„{preferred_question}“

Passender Hinweis:
„{hint}“

Typische Fehler bei diesem Aufgabentyp:
{errors}

Verbindliche Regeln:
- Analysiere immer zuerst die konkrete Aufgabe.
- Beginne niemals mit einer allgemeinen Standardfrage, wenn eine fachlich genauere Frage möglich ist.
- Verwende die bevorzugte Lehrerfrage sinngemäß, passe sie aber an konkrete Zahlen, Begriffe und Figuren der Aufgabe an.
- Stelle genau eine fachliche Frage.
- Frage niemals, ob du helfen, erklären, anfangen oder die Aufgabe lösen sollst.
- Verwende nicht die allgemeine Frage „Welche Größe ist gesucht, und welche Angabe verbindet sie mit dem bereits Bekannten?“, außer sie passt nachweislich genau zur Aufgabe.
- Gib keine vollständige Musterlösung und kein Endergebnis vor.
- Antworte kurz: höchstens vier Sätze.
- Gehe nur einen Denkschritt weiter.
- Wenn die letzte Antwort des Lernenden richtig ist, bestätige konkret und stelle die nächste passende Frage.
- Wenn sie falsch ist, benenne genau den Denkfehler und stelle eine korrigierende Frage.
- Wenn der Lernende nur „ja“, „okay“ oder ähnlich schreibt, fahre sofort mit der nächsten fachlichen Frage fort.
- Nutze für Mathematik nur $...$ oder $$...$$.
- Bleibe in der aktuellen Lernphase, solange kein sinnvoller Übergang nötig ist.
""".strip()


def topic_key_for(task_text: str, messages: list[dict]) -> str:
    return classify_task(task_text, messages).topic_key


def fallback_teacher_question(task_text: str, messages: list[dict]) -> str:
    """Return a task-specific question if the model produces no usable text."""
    task_type = classify_task(task_text, messages)
    phase = infer_phase(messages)
    question_index = len(
        [message for message in messages if message.get("role") == "assistant"]
    )
    return _question_for_phase(task_type, phase, question_index)
