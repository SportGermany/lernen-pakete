#!/usr/bin/env python3
"""Prüft alle Pakete gegen schema/paket.schema.json und erzeugt katalog.json.

Aufruf:  python3 werkzeuge/katalog.py           (prüfen + katalog.json schreiben)
         python3 werkzeuge/katalog.py --pruefen (nur prüfen)
Der Ordner fragen/ wird ignoriert.
"""
import json, os, re, subprocess, sys
from datetime import datetime, timezone

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("Bitte zuerst installieren:  pip install jsonschema")

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")
KLASSEN = {"ms", "mg", "mw", "mz", "tag"}


def geaendert(pfad):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cI", "--", pfad], cwd=WURZEL,
                             capture_output=True, text=True).stdout.strip()
        if out:
            return out
    except OSError:
        pass
    return datetime.fromtimestamp(os.path.getmtime(os.path.join(WURZEL, pfad)), timezone.utc).isoformat(timespec="seconds")


def html_fehler(wert, ort, fehler):
    """Prüft rekursiv alle Texte auf erlaubtes HTML (wie die App)."""
    if isinstance(wert, dict):
        for k, v in wert.items():
            html_fehler(v, f"{ort}.{k}", fehler)
    elif isinstance(wert, list):
        for i, v in enumerate(wert):
            html_fehler(v, f"{ort}[{i}]", fehler)
    elif isinstance(wert, str):
        for m in HTML_TAG.finditer(wert):
            name, attr = m.group(2).lower(), m.group(3).strip().rstrip("/").strip()
            if name not in {"p", "b", "br", "span"}:
                fehler.append(f"{ort}: HTML <{name}> nicht erlaubt")
            elif name == "span" and not m.group(1):
                k = re.fullmatch(r'class="([^"]*)"', attr)
                if not k or k.group(1) not in KLASSEN:
                    fehler.append(f"{ort}: <span {attr}> nicht erlaubt")
            elif name != "span" and attr:
                fehler.append(f"{ort}: <{name} {attr}> nicht erlaubt")


def zusatzpruefung(p, datei):
    """Regeln, die JSON-Schema nicht ausdrücken kann."""
    f = []
    erwartet = p["id"].replace(".", "-")
    name = os.path.splitext(os.path.basename(datei))[0]
    if p["typ"] != "formelsammlung" and not name.startswith(p["fach"] + "-"):
        f.append(f"Dateiname sollte mit '{p['fach']}-' beginnen (id: {erwartet})")
    if p["typ"] != "formelsammlung" and not p["id"].startswith(p["fach"] + "."):
        f.append("id muss mit dem Fach beginnen")
    ids = [s["id"] for s in p.get("begleiter", [])]
    if len(ids) != len(set(ids)):
        f.append("Schritt-ids doppelt")
    for i, s in enumerate(p.get("begleiter", [])):
        q = s.get("frage")
        if q and not 0 <= q["richtig"] < len(q["optionen"]):
            f.append(f"begleiter[{i}].frage.richtig außerhalb")
    for stufe, liste in p.get("uebungen", {}).items():
        for i, u in enumerate(liste):
            if u.get("typ") == "auswahl" and not 0 <= u["richtig"] < len(u["optionen"]):
                f.append(f"uebungen.{stufe}[{i}].richtig außerhalb")
    html_fehler(p, "paket", f)
    return f


def main():
    nur_pruefen = "--pruefen" in sys.argv
    schema = json.load(open(os.path.join(WURZEL, "schema", "paket.schema.json"), encoding="utf-8"))
    validator = Draft7Validator(schema)
    faecher = {f["id"] for f in json.load(open(os.path.join(WURZEL, "faecher.json"), encoding="utf-8"))}
    eintraege, fehler, ids = [], [], {}

    for ordner, _, dateien in sorted(os.walk(os.path.join(WURZEL, "pakete"))):
        for d in sorted(dateien):
            if not d.endswith(".json"):
                continue
            pfad = os.path.relpath(os.path.join(ordner, d), WURZEL).replace(os.sep, "/")
            try:
                p = json.load(open(os.path.join(WURZEL, pfad), encoding="utf-8"))
            except json.JSONDecodeError as e:
                fehler.append(f"{pfad}: kein gültiges JSON ({e})")
                continue
            for e in sorted(validator.iter_errors(p), key=lambda e: list(e.path)):
                ort = "/".join(str(x) for x in e.path) or "(Wurzel)"
                fehler.append(f"{pfad}: {ort}: {e.message}")
            if not isinstance(p, dict) or "id" not in p:
                continue
            fehler += [f"{pfad}: {x}" for x in zusatzpruefung(p, pfad)] if "typ" in p and "fach" in p else []
            if p.get("fach") not in faecher and p.get("typ") != "formelsammlung":
                fehler.append(f"{pfad}: Fach '{p.get('fach')}' fehlt in faecher.json")
            if p["id"] in ids:
                fehler.append(f"{pfad}: id '{p['id']}' gibt es schon in {ids[p['id']]}")
            ids[p["id"]] = pfad
            eintraege.append({
                "id": p["id"], "typ": p.get("typ"), "fach": p.get("fach"), "titel": p.get("titel"),
                "stufe": p.get("stufe", ""), "version": p.get("version"), "pfad": pfad,
                "groesse": os.path.getsize(os.path.join(WURZEL, pfad)), "geaendert": geaendert(pfad),
            })

    if fehler:
        print("FEHLER:\n  " + "\n  ".join(fehler))
        sys.exit(1)
    print(f"{len(eintraege)} Pakete geprüft, alles in Ordnung.")
    if nur_pruefen:
        return
    katalog = {"format": "lernen-katalog/1", "pakete": sorted(eintraege, key=lambda e: (e["fach"], e["titel"]))}
    alt = None
    ziel = os.path.join(WURZEL, "katalog.json")
    if os.path.exists(ziel):
        alt = json.load(open(ziel, encoding="utf-8"))
    if alt != katalog:
        with open(ziel, "w", encoding="utf-8") as f:
            json.dump(katalog, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("katalog.json aktualisiert.")


if __name__ == "__main__":
    main()
