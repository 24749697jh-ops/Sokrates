# Sokrates – Mathematik-Lerncoach

> **Ich begleite dich – denken musst du selbst.**

Ein kleiner Streamlit-Prototyp, der Schülerinnen und Schüler beim Lösen von
Mathematikaufgaben begleitet, ohne fertige Lösungen zu verraten.

## Was die Version kann

- Aufgaben als Text entgegennehmen
- PDFs, Bilder, DOCX- und Textdateien einlesen
- mit einem mehrstufigen Tutorprinzip arbeiten:
  1. Verstehen
  2. Planen
  3. Rechnen
  4. Prüfen
- konkrete Ansätze ehrlich loben
- Fehler durch Rückfragen bearbeiten
- auf Forderungen nach der fertigen Lösung nicht eingehen
- Chatverlauf innerhalb der Sitzung behalten

## Voraussetzungen

- Python 3.10 oder neuer
- ein OpenAI API-Key

Die Nutzung der OpenAI API verursacht abhängig vom gewählten Modell und
Umfang der Dateien Kosten.

## Installation

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
streamlit run app.py
```

Trage in `.env` deinen API-Key ein:

```env
OPENAI_API_KEY=dein_api_key
OPENAI_MODEL=gpt-5-mini
```

Danach öffnet sich Sokrates normalerweise unter:

```text
http://localhost:8501
```

## Ohne `.env`

Der API-Key kann auch links in der Seitenleiste eingegeben werden. Er wird
nicht in den Quellcode geschrieben und gilt nur für die laufende Sitzung.

## Für einen schnellen Online-Test

Das Projekt kann beispielsweise auf Streamlit Community Cloud bereitgestellt
werden. Lege den API-Key dort als Secret ab und veröffentliche ihn niemals im
Repository.

## Datenschutz-Hinweis für den Unterricht

Dieser Prototyp ist noch kein geprüftes Schulprodukt. Lade keine Dokumente mit
Klarnamen, Noten, Gesundheitsdaten oder anderen personenbezogenen Angaben hoch.
Vor einem regulären Schuleinsatz sollten Datenschutz, Auftragsverarbeitung,
Einwilligungen, Löschkonzept und die Vorgaben des Schulträgers geprüft werden.

## Bekannte Grenzen

- Die KI kann mathematische Inhalte oder hochgeladene Aufgaben falsch lesen.
- Der Prompt reduziert das Verraten von Lösungen, garantiert es aber nicht in
  jedem denkbaren Dialog.
- Es gibt noch keine Benutzerkonten, Klassenverwaltung oder Lernstatistik.
- Der Chatverlauf bleibt nur in der aktuellen Browser-Sitzung.
