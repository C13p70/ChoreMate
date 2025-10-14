
# 🧹 ChoreMate – Home Assistant Integration

Eine einfache, lokale Aufgabenverwaltung ("Putzplan xD ") für Home Assistant.
Verteilt Haushaltsaufgaben zufällig auf Personen und Wochentage – mit eigener, kleinen Datenbank.

## ✨ Features
- Eigene Aufgaben-DB in `.storage/choremate_db` (persistente JSON-Struktur)
- Zufällige Neuverteilung per Service `choremate.assign_now`
- Sensoren je Person & Wochentag (`sensor.mama_montag` etc., Inhalt mit Zeilenumbrüchen)
- Aufgaben pflegen via `choremate.add_task`, `choremate.remove_task`
- Automatische Neuverteilung (alle 7 Tage – anpassbar oder via Automation)

## 🛠️ Installation
1. Dieses Repository als **Custom Repository** in HACS hinzufügen oder die Dateien manuell nach
   `config/custom_components/choremate/` kopieren.
2. Home Assistant **neu starten**.
3. **Einstellungen → Integrationen → Integration hinzufügen → „ChoreMate“** und Personen eintragen.

> Domain: `choremate`

## 🧠 Services

| Service | Beschreibung |
|----------|---------------|
| `choremate.assign_now` | Neue zufällige Aufgabenverteilung |
| `choremate.add_task` | Aufgabe hinzufügen |
| `choremate.remove_task` | Aufgabe löschen |
| `choremate.list_tasks` | Tasks eines Tages auflisten (Event `choremate_list_tasks`) |

### Beispiele (Entwicklerwerkzeuge → Dienste)

**Aufgabe hinzufügen**
```yaml
service: choremate.add_task
data:
  person: Mama
  day: Montag
  task: Toilette wischen
```

**Neu zuweisen (jetzt)**
```yaml
service: choremate.assign_now
```

## 📋 Anzeige in der UI (Beispiel-Lovelace)
```yaml
type: grid
columns: 3
square: false
cards:
  - type: markdown
    content: |
      ## Mama
      **Mo**: {{ states('sensor.mama_montag') }}
      **Di**: {{ states('sensor.mama_dienstag') }}
      **Mi**: {{ states('sensor.mama_mittwoch') }}
      **Do**: {{ states('sensor.mama_donnerstag') }}
      **Fr**: {{ states('sensor.mama_freitag') }}
      **Sa**: {{ states('sensor.mama_samstag') }}
      **So**: {{ states('sensor.mama_sonntag') }}
  - type: markdown
    content: |
      ## Lina
      **Mo**: {{ states('sensor.lina_montag') }}
      **Di**: {{ states('sensor.lina_dienstag') }}
      **Mi**: {{ states('sensor.lina_mittwoch') }}
      **Do**: {{ states('sensor.lina_donnerstag') }}
      **Fr**: {{ states('sensor.lina_freitag') }}
      **Sa**: {{ states('sensor.lina_samstag') }}
      **So**: {{ states('sensor.lina_sonntag') }}
  - type: markdown
    content: |
      ## Alysha
      **Mo**: {{ states('sensor.alysha_montag') }}
      **Di**: {{ states('sensor.alysha_dienstag') }}
      **Mi**: {{ states('sensor.alysha_mittwoch') }}
      **Do**: {{ states('sensor.alysha_donnerstag') }}
      **Fr**: {{ states('sensor.alysha_freitag') }}
      **Sa**: {{ states('sensor.alysha_samstag') }}
      **So**: {{ states('sensor.alysha_sonntag') }}
```

## 🔧 Tipps
- Standardmäßig werden 2 Zeilen pro Person/Tag zugewiesen. Das stellst du bei der Einrichtung ein.
- Aufgaben ohne vorhandenen Pool ergeben leere Zeilen (""), damit die Zeilenanzahl immer passt.
- Für wöchentliche Neuverteilung baue dir eine Automation (z. B. So 07:00).

## 📦 HACS
```json
{
  "name": "ChoreMate",
  "content_in_root": false,
  "domains": ["choremate"],
  "homeassistant": "2024.6.0",
  "render_readme": true
}
```

## 🧪 Roadmap
- Optionen nachträglich ändern (OptionsFlow)
- Admin-Panel zur DB-Pflege (Frontend)
- Import/Export als YAML/CSV
- Grocy-Integration als Quelle für Chores
