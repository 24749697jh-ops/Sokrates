# Sokrates 0.5

Diese Version verbindet die bestehende GoodNotes-/PDF-Funktion mit einer
erweiterten Didaktik-Engine.

## Neu

- automatische grobe Themenklassifikation
- Erkennung der Lernphase
- vier Hilfestufen
- Button „Kleiner Hinweis“
- passendere Lehrerfragen
- typische Fehler pro Themengebiet
- Prüfung auf wiederholte Antworten
- fester Fallback statt hilfloser Formulierungen

## Installation auf GitHub

Ersetze oder ergänze im Repository:

- `app.py`
- `didactic_engine.py`
- `requirements.txt`

Danach Commit durchführen. Streamlit startet die App automatisch neu.

## Wichtig

`tutor_prompt.py` wird in Version 0.5 nicht mehr benötigt. Er kann im Repository
bleiben, wird aber von `app.py` nicht mehr verwendet.
