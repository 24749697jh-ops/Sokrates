# Sokrates 0.7

Sokrates 0.7 ist eine saubere modulare Neuentwicklung des bisherigen Prototyps.

## Neu

- echter Schul-Formeleditor ohne sichtbaren LaTeX-Code
- große Formelkarten
- thematische Formelsammlung
- Touch-Tastatur für iPad
- normale Schulzeichen wie `·`, `:`, `²`, `√` und `π`
- mathematische Vorschau
- direkte Übergabe eines Rechenschritts an Sokrates
- stabilere modulare Architektur

## Dateien

- `app.py` – Hauptanwendung
- `config.py` – zentrale Einstellungen
- `didactic_engine.py` – Themen- und Phasenerkennung
- `formula_library.py` – Formelsammlung
- `formula_ui.py` – Schul-Formeleditor
- `ui_components.py` – Darstellung und Gestaltung
- `requirements.txt`

## Installation auf GitHub

Am sichersten ist es, die bisherigen Python-Dateien im Repository zu ersetzen
und alle Dateien aus diesem Paket hochzuladen.

Das Streamlit Secret bleibt:

```toml
OPENAI_API_KEY="dein-openai-api-key"
```

Der API-Key darf nicht in GitHub oder direkt in `app.py` stehen.

## Test

Nach dem Commit:

1. Streamlit etwa eine Minute aktualisieren lassen.
2. App neu laden.
3. Eine Aufgabe beginnen.
4. „🧮 Schul-Formeleditor“ öffnen.
5. Eine Formel wählen oder über die Tasten eingeben.
