# Sokrates 0.8 – Teacher Engine

Version 0.8 ersetzt die bisherige allgemeine Themenlogik durch eine Teacher Engine.

## Was sich ändert

Sokrates erkennt nun nicht nur das Fachgebiet, sondern konkrete Aufgabentypen, zum Beispiel:

- lineare Gleichung lösen
- Brüche addieren oder subtrahieren
- Prozentwert berechnen
- Fläche eines Rechtecks oder Dreiecks
- Kreisausschnitt
- Kreisbogen
- Satz des Pythagoras
- Steigung einer linearen Funktion
- Textaufgabe
- Rechenausdruck

Für jeden Aufgabentyp kennt die Engine:

- passende Einstiegsfragen
- Planungsfragen
- Rechenfragen
- Prüffragen
- abgestufte Hinweise
- typische Fehler

Die allgemeine Standardfrage wird ausdrücklich unterdrückt, wenn eine passendere fachliche Frage möglich ist.

## Für GitHub

Am sichersten ist es, alle Dateien aus diesem ZIP in das Repository hochzuladen und gleichnamige Dateien zu ersetzen.

Neu ist insbesondere:

- `teacher_engine.py`

Aktualisiert wurden:

- `app.py`
- `didactic_engine.py`

Das Streamlit Secret bleibt unverändert:

```toml
OPENAI_API_KEY="dein-openai-api-key"
```
