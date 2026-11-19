# lernen-pakete

Inhalte für die Android-App **[Lernen](https://github.com/SportGermany/lernen)**: Themenpakete als JSON.
Das Repo ist öffentlich, die App liest ohne Token.

```
katalog.json                ← wird per GitHub Action erzeugt (nie von Hand bearbeiten)
faecher.json                ← Fächer: id, name, farbe (hell/dunkel), begleiterTyp
schema/paket.schema.json    ← JSON-Schema für alle Pakettypen
ANLEITUNG-PAKETE.md         ← wie man ein gutes Paket schreibt
pakete/{fach}/…json         ← Themenpakete
pakete/werkzeuge/formelsammlung.json
fragen/offen/               ← hier legt die App Fragen an Claude ab (werden nach 24 h gelöscht)
werkzeuge/katalog.py        ← Prüfung + Katalog (läuft auch lokal)
```

## Neues Paket

1. Datei nach [ANLEITUNG-PAKETE.md](ANLEITUNG-PAKETE.md) schreiben.
2. Lokal prüfen: `pip install jsonschema && python3 werkzeuge/katalog.py --pruefen`
3. Committen und pushen. Die Action prüft das Paket und aktualisiert `katalog.json`.
4. In der App: Katalog → ↻ → „Hinzufügen“.

## Neues Fach

Einen Eintrag in `faecher.json` ergänzen, mit einem vorhandenen `begleiterTyp` (`schreiben`, `rechnen` oder `physik`).
Die App zeigt neue Fächer ohne Update an.

## Fragen an Claude

Die App legt Fragen als Markdown-Datei in `fragen/offen/` ab und löscht sie nach 24 Stunden wieder.
**Gelöschte Fragen sind in der GitHub-Versionsgeschichte weiterhin auffindbar.** Deshalb: keine Namen, keine persönlichen Infos.
