#  Moodle to Notion Scraper (TU Darmstadt)

Ein automatisierter Scraper, der Hausaufgaben und Deadlines aus dem **TU Darmstadt Moodle** und dem **Lernportal Informatik** extrahiert und direkt in eine **Notion-Datenbank** überträgt.

##  Features
* **Multi-Moodle Support:** Unterstützt das Standard-Moodle sowie das Informatik-Lernportal.
* **Automatischer Abgleich:** Neue Aufgaben werden erkannt; Duplikate werden vermieden.
* **GitHub Actions:** Läuft vollautomatisch (z. B. jeden Morgen um 08:00 Uhr).
* **Modul-Mapping:** Ordnet Aufgaben automatisch den richtigen Modulen in Notion zu.

##  Setup

### 1. Notion Vorbereitung
1. Erstelle eine Datenbank in Notion mit folgenden Spalten:
   * `Task` (Titel)
   * `Deadline` (Datum)
   * `Modul` (Relation zu einer Modul-Datenbank)
   * `MoodleName`(Text) (Der Name des Moduls, wie es in Moodle eingetragen ist)
2. Erstelle eine **Integration** unter [notion.so/my-integrations](https://www.notion.so/my-integrations).
3. Verbinde die Integration mit deiner Datenbank (Oben rechts: `...` -> `Add connections`).

### 2. GitHub Secrets konfigurieren
Gehe in deinem GitHub-Repo zu `Settings > Secrets and variables > Actions` und lege folgende Secrets an:

| Secret | Beschreibung |
| :--- | :--- |
| `TUOTP`| Geheimniss der TOTP 2FA |
| `TUUSERNAME` |  TU-ID |
| `TUPASSWORD` |  TU-ID Passwort |
| `NOTIONSECRET` |  API-Key der Notion-Integration (`ntn_...`) |
| `NOTIONID` |  32-stellige ID der Notion-Datenbank |
| `NOTIONVERSION` | Aktuelle Notion-Version (z.B 2026-03-11) |
| `MODULDBID` | 32-stellige ID der Modul-Datenbank

### 3. Modul-Mapping (Automatisch oder Manuell)

Das Projekt nutzt eine `config.json`, um die Kursnamen aus Moodle den internen Notion-IDs deiner Modul-Datenbank zuzuordnen. 

#### A) Automatische Generierung (Empfohlen)
Statt die IDs händisch zu suchen, kannst du die Konfiguration direkt aus Notion exportieren:
1. Stelle sicher, dass das Secret `MODULDBID` (ID deiner Modul-Datenbank) gesetzt ist.
2. Trage in deiner Notion-Modul-Datenbank in der Spalte `MoodleName` den exakten Namen des Kurses ein, wie er im Moodle-Dashboard erscheint.
3. Führe das Skript aus:
   ```bash
   python config_gen.py
    ```

#### B) Manuelle Konfiguration
Falls du die Zuordnung händisch vornehmen möchtest, erstelle im Hauptverzeichnis eine Datei namens `config.json`. Das Format ist ein einfaches JSON-Objekt, bei dem der **Moodle-Kursname** der Schlüssel und die **Notion-Page-ID** des Moduls der Wert ist:

```json
{
  "Kursname in Moodle": "Notion-Page-ID-des-Moduls",
  "Mathematik I für Informatiker": "11ed2df067f44e84a657f0df45f3387f",
  "Allgemeine Informatik I": "188d2df055f44e84a657f0df45f3387a"
}
```

## Technik & Stack

Das Projekt nutzt moderne Automatisierungstools, um einen stabilen Sync zwischen Moodle und Notion zu gewährleisten:

* **Laufzeitumgebung:** `Python 3.12`
* **Browser-Automatisierung:** `Playwright` (wird im `headless`-Modus auf GitHub Actions ausgeführt)
* **API-Kommunikation:** `Requests` Library für die Interaktion mit der `Notion API`
* **CI/CD / Hosting:** `GitHub Actions` (automatische Ausführung per Cron-Job)
* **Datenverarbeitung:** `JSON` für das Modul-Mapping und die Konfiguration
* **Sicherheit:** `GitHub Secrets` zur Verschlüsselung von Zugangsdaten (keine Passwörter im Code!)

### Workflow-Ablauf
1. **Trigger:** GitHub Action startet (Zeitplan oder manuell).
2. **Scraping:** Playwright loggt sich im Moodle ein und extrahiert Aufgaben-Daten.
3. **Processing:** Abgleich der gefundenen Aufgaben mit der `config.json`.
4. **Sync:** Vergleich mit bestehenden Einträgen in Notion via API.
5. **Update:** Neue Aufgaben werden als neue Seiten in der Notion-Datenbank angelegt.
