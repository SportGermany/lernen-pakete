# Anleitung: Ein gutes Themenpaket schreiben

Diese Anleitung ist für Claude (Chat oder Code) und für Menschen, die Pakete für die App **Lernen** schreiben.
Jedes Paket ist eine JSON-Datei unter `pakete/{fach}/`. Nach dem Push prüft die GitHub Action das Paket gegen
`schema/paket.schema.json` und erzeugt `katalog.json` neu. Danach erscheint das Paket in der App im **Katalog**.

## 1. Zielgruppe

- Ein Schüler der **Realschule Bayern, 9./10. Klasse** (Lehrplan: **LehrplanPLUS**).
- Er lernt oft **allein auf Sport-Lehrgängen** und arbeitet **auf Papier**. Die App liegt daneben und führt ihn.
- Er soll selbst denken: **Tipps in Stufen statt fertiger Lösung**.

## 2. Stil

- **Du-Form**, freundlich, sachlich. Keine Emojis, kein „Super!“.
- **Kurz und fürs Handy**: Ein Abhakpunkt ist höchstens eine Zeile, ein Tipp höchstens zwei bis drei Sätze.
- Fachbegriffe so, wie sie im bayerischen Unterricht heißen (z. B. „Schilderung“, „Gleichungssystem“, „Einsetzungsverfahren“).
- Deutsche Anführungszeichen „…“, Gedankenstrich –, Auslassung …
- In Texten ist nur dieses HTML erlaubt: `<p>`, `<b>`, `<br>` und `<span class="ms|mg|mw|mz|tag">`
  (Markierungen: **ms** Sinne, **mg** Gefühl/Gedanken, **mw** Wortwahl/Bilder, **mz** Satzbau/Zeitlupe, **tag** Korrekturzeichen).
  Keine anderen Tags, keine `style`-Attribute.

## 3. Grundaufbau (alle Pakettypen)

```json
{
  "format": "lernen-paket/2",
  "typ": "thema",
  "id": "deutsch.eroerterung-linear",
  "version": "1.0",
  "fach": "deutsch",
  "titel": "Lineare Erörterung",
  "stufe": "Realschule Bayern · 9. Klasse"
}
```

| Feld | Regel |
|---|---|
| `typ` | `thema`, `arbeitsheft` oder `formelsammlung` |
| `id` | `fach.name-mit-bindestrichen`, nur Kleinbuchstaben, Ziffern, Bindestriche |
| Dateiname | beginnt mit dem Fach, z. B. `pakete/deutsch/deutsch-eroerterung-linear.json` (die id mit Bindestrich statt Punkt) |
| `version` | `1.0`, `1.1`, `2.0` … **Bei jeder Änderung erhöhen**, sonst bekommt die App das Update nicht |
| `fach` | muss in `faecher.json` stehen |

**Schritt-ids nie ändern.** Der Fortschritt in der App hängt an der Schritt-`id`. Wird eine id geändert, verfallen die Haken dieses Schritts.

## 4. Typ `thema`

### 4.1 `ueberblick`
- `aufgabe`: Worum geht's? (2–4 Sätze)
- Beispiel **entweder** als `vorher` (Text) + `nachher` (HTML mit Markierungen) **oder** als
  `ausgangslage` + `auftrag` + `ueberschrift` + `muster` (HTML mit Markierungen).
- `aufbau`: Liste von `[Teil, Beschreibung]`
- `kriterien`: Worauf die Lehrkraft achtet
- `erlaubt` / `verboten`: kurze Listen

### 4.2 `begleiter` (das Herzstück)
Eine Liste von Schritten in Arbeitsreihenfolge. Jeder Schritt:

| Feld | Pflicht | Inhalt |
|---|---|---|
| `id` | ja | kurz, z. B. `einleitung` |
| `kurz` | ja | Text für die Schritt-Leiste (1–2 Wörter) |
| `titel` | ja | Überschrift des Schritts |
| `ziel` | ja | ein Satz: Was kann der Schüler danach? |
| `muss` | ja | Abhakliste (4–8 Punkte), jeweils eine prüfbare Handlung oder ein Merkmal |
| `label` | nein | Überschrift der Liste. Fehlt → „Muss rein“. Für Vorbereitungsschritte „Erledigt?“ |
| `wissen` | nein | „Gut zu wissen“: eine Regel in 1–2 Sätzen |
| `fehler` | nein | typische Fehler |
| `hinweise` | nein | **Tipps in Stufen** (höchstens 3, siehe 4.3) |
| `frage` | nein | Prüffrage: `frage`, `optionen`, `richtig` (Index ab 0), `warum` |
| `vorher` / `nachher` / `vnLabel` | nein | eigenes Mini-Beispiel; `vnLabel` z. B. `["So nicht", "So schon"]` |
| `hilfen` | nein | aufklappbare Listen `{ "t": "Titel", "items": [...] }` |
| `wortkiste` | nein | `true` zeigt den Knopf „Wortkiste öffnen“ |
| `phrases` | nein | Englisch: „Useful phrases“ |

### 4.3 Tipps in Stufen (`hinweise`)
1. **Tipp 1 – allgemein:** eine Denkrichtung oder Frage („Zähl mal, wie viele Zeilen …“).
2. **Tipp 2 – Ort:** wo genau suchen (Zeilen, Absatz, Teilaufgabe).
3. **Tipp 3 – konkret:** einzelne Wörter oder der entscheidende Ansatz, **aber nicht die fertige Lösung**.

Die Prüffrage verrät bei falscher Antwort die richtige **nicht**. Die Erklärung (`warum`) erscheint nur bei richtiger Antwort.

### 4.4 `uebungen`
Drei Stufen: `einstieg` (Grundwissen, meist `auswahl`), `sicher` (Anwenden), `schulaufgabe` (Prüfungsniveau).

| `typ` | Felder |
|---|---|
| `auswahl` | `frage`, `optionen`, `richtig`, `warum` |
| `tippen` | `frage`, `tokens` als `[["Wort oder ganzer Satz", 1 oder 0], …]`, `warum` |
| `umschreiben` | `frage`, `satz`, `tipp`, `loesung` |
| `text` | `titel`, `vlabel`, `auftrag`, `vorlage`, `loesung` (HTML) – mit Selbstcheck über `raster` |
| `rechenaufgabe` | `aufgabe`, `loesung` (HTML, Schritt für Schritt), optional `ergebnis`, `tipp` |

Optional hat jede Übung eine feste `id`. Sonst ergibt sich die id aus Stufe und Position.
**Wer Übungen umsortiert, sollte feste ids vergeben**, damit „Wiederholen“ stimmt.

### 4.5 Weitere Teile
- `raster`: Selbstcheck für Schreibaufgaben (Liste)
- `merkzettel`: `[Stichwort, Text]` – das Wichtigste auf einer Seite
- `wortkiste`: `{ "g": "Gruppe", "i": ["Wort", …] }`
- `korrektur`: `[Zeichen, Bedeutung, Beispiel]`

## 5. Typ `arbeitsheft`

Für **genau eine Seite** in einem Arbeitsheft oder Buch. Das Heft liegt neben dem Handy, die App verweist auf **Zeilennummern**.
Zusätzlich im `ueberblick`:
- `quelle`: z. B. „Arbeitsheft Deutsch, S. 31 · Aufgaben 1a–c und 2“
- `karte`: `[Zeilen, Teil, Was tun]`, z. B. `["Z. 1–6", "Einleitung", "Beurteilen (1a)"]`
- `ziel`: Was am Ende im Text sein muss
- `regel`: z. B. wann das Lösungsheft aufgeschlagen werden darf

## 6. Urheberrecht (wichtig!)

Pakete dürfen **keine Texte aus Schulbüchern, Arbeitsheften oder Lösungsheften** enthalten.
Erlaubt sind nur:
- **Zeilenverweise** („Z. 7–8“),
- **einzelne Wörter** als Suchhilfe („achte auf: lodernde · spiegelt“),
- **eigene, neu geschriebene Beispiele** (als solche kennzeichnen, z. B. „Eigenes Beispiel“).

Keine ganzen Sätze oder Absätze aus dem Heft abschreiben, auch nicht „nur kurz“. Musterlösungen immer selbst schreiben.
Erfundene Buchvorlagen als „für diese Übung erfunden“ kennzeichnen.

## 7. Mathe und Physik

Mathe- und Physik-Pakete nutzen denselben Aufbau. Ein Schritt ist ein **Rezept-Schritt** zum Abhaken.
Zusätzlich gibt es:
- `pruefung`: `aequivalenz` (Umformung prüfen), `loesung` (Ergebnis prüfen) oder `einheit` (Zahl und Einheit prüfen)
- `muster`: Musteraufgabe Schritt für Schritt (HTML, mit `<br>`)
- `mitrechnen`: Daten für „Meine Aufgabe mitrechnen“

```json
"mitrechnen": {
  "art": "rechnen",
  "aufgabe": ["y = 2x - 1", "3x + 2y = 12"],
  "tipps": ["Setze den Term für y in die zweite Gleichung ein.", "Klammer nicht vergessen: 2·(2x − 1)"]
}
```

```json
"mitrechnen": {
  "art": "physik",
  "gegeben": [{ "zeichen": "U", "name": "Spannung", "wert": "230", "einheit": "V" },
              { "zeichen": "P", "name": "Leistung", "wert": "2000", "einheit": "W" }],
  "gesucht": { "zeichen": "I", "name": "Stromstärke", "einheit": "A" },
  "formel": "elektrische-leistung",
  "ergebnis": { "zeichen": "I", "wert": "8,7", "einheit": "A", "toleranz": 0.02 }
}
```

Schreibweise für Terme: `*` oder `·` für mal, `:` oder `/` für geteilt, `^` für Potenz, `sqrt(…)` oder `√` für Wurzel, Komma oder Punkt als Dezimalzeichen.
`formel` verweist auf eine Formel-`id` aus `pakete/werkzeuge/formelsammlung.json`.

## 8. Typ `formelsammlung`

Es gibt genau eine Formelsammlung: `pakete/werkzeuge/formelsammlung.json`, id `werkzeuge.formelsammlung`.
Sie besteht aus `gebiete`, jedes mit `id`, `titel`, `fach`, `klasse` und `formeln`:

```json
{ "id": "elektrische-leistung", "name": "Elektrische Leistung", "formel": "P = U · I",
  "groessen": [["P", "Leistung", "W (Watt)"], ["U", "Spannung", "V (Volt)"], ["I", "Stromstärke", "A (Ampere)"]],
  "umstellungen": ["U = P : I", "I = P : U"], "stichwoerter": ["Watt", "Strom"] }
```

Formeln **sorgfältig gegenprüfen** (Einheiten, Umstellungen). Lieber eine Formel weniger als eine falsche.

## 9. Englisch

Wie Deutsch (Schreib-Begleiter). Pro Schritt zusätzlich `phrases` mit **Useful phrases**.
Grammatik-Themen laufen als Rezept: Regel in einem Satz (`wissen`) → Signalwörter (`hilfen`) → Muster (`vorher`/`nachher`) → Abhak-Check (`muss`).
**Keine** Vokabellisten (dafür gibt es eine andere App), keine Aussprache.

## 10. Vor dem Hochladen

```bash
pip install jsonschema
python3 werkzeuge/katalog.py --pruefen
```

Checkliste:
- [ ] `version` erhöht (bei Änderungen)
- [ ] Schritt-ids unverändert
- [ ] Keine Texte aus Schulbüchern/Arbeitsheften/Lösungsheften
- [ ] Tipps in drei Stufen, keine fertige Lösung im letzten Tipp
- [ ] Prüffragen: `richtig` zeigt auf die richtige Option
- [ ] Nur erlaubtes HTML
