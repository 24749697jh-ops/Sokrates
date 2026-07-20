# Sokrates 0.4 – Didaktik-Engine

Diese Version verbessert die Qualität der Hilfen.

## Neue Bestandteile

- `didactic_engine.py`
  - erkennt grob das Aufgabengebiet,
  - schätzt die Lernphase,
  - stellt passende Lehrerfragen,
  - enthält abgestufte Hinweise,
  - berücksichtigt typische Fehler.

- `tutor_prompt.py`
  - zwingt Sokrates zu einem kleinen nächsten Denkschritt,
  - verbietet hilflose Antworten,
  - enthält einen festen Fallback,
  - beschränkt jede Antwort auf höchstens eine Frage.

- `APP_AENDERUNGEN.txt`
  - zeigt die drei kleinen Änderungen, die in `app.py` nötig sind.

## Einbau auf GitHub

1. `didactic_engine.py` neu hochladen.
2. `tutor_prompt.py` ersetzen.
3. Die drei Änderungen aus `APP_AENDERUNGEN.txt` in `app.py` übernehmen.
4. Commit durchführen.
5. Streamlit neu laden.

## Erste Tests

Teste mindestens diese Fälle:

1. „Löse 3x + 5 = 20.“
2. „Ein Rechteck ist 6 cm länger als breit und hat 40 cm Umfang.“
3. „Ein Pullover kostet 80 Euro und wird um 25 % reduziert.“
4. „Bestimme die Steigung der Geraden durch A(1|2) und B(5|10).“
5. Eine handschriftliche Aufgabe aus GoodNotes.

Erwartung:
Sokrates stellt jeweils genau eine konkrete Frage und gibt keine vollständige Lösung.
