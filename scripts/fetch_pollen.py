#!/usr/bin/env python3
"""
Fetches the current pollen/spore forecast for each Catalan station from
aerobiologia.cat (Punt d'Informació Aerobiològica, XAC-UAB) and writes a
single JSON file to data/pollen.json.

This script runs server-side (GitHub Actions), NOT in the user's browser,
so it is not affected by CORS. The published site's data is under
CC BY-NC-SA 4.0 (https://aerobiologia.cat/pia/es/terms) — this script only
reads the public forecast pages and keeps the required attribution in the
generated JSON and in the app itself.

If you use this data in a public project, PIA kindly asks to be notified
at aerobiologia.pia@uab.cat.
"""
import json
import re
import sys
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

STATIONS = [
    "barcelona", "bellaterra", "girona", "lleida",
    "manresa", "roquetes", "tarragona", "vielha", "son",
]

BASE_URL = "https://aerobiologia.cat/pia/es/forecast/{station}"
HEADERS = {
    "User-Agent": "PolenYo-personal-app/1.0 (+https://github.com/; contacto para dudas: ver README del repo)"
}
TREND_SYMBOLS = {"=", "A", "D", "!"}
TREND_LABELS = {"=": "Estable", "A": "Aumenta", "D": "Descenso", "!": "Situación excepcional"}


def parse_station_page(html):
    soup = BeautifulSoup(html, "html.parser")

    # Find the main data table: the one that is NOT the legend/"Clave" table.
    data_table = None
    for table in soup.find_all("table"):
        text = table.get_text(" ", strip=True)
        if "Clave" in text or "Nivel actual" in text:
            continue
        if "Taxon" in text or re.search(r"\b[0-4]\b", text):
            data_table = table
            break
    if data_table is None:
        return [], None

    taxa = []
    for tr in data_table.find_all("tr"):
        cells = [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
        cells = [c for c in cells if c not in ("", "📷", "📄")]
        if len(cells) < 2:
            continue

        trend = None
        rest = cells
        if cells[-1] in TREND_SYMBOLS:
            trend = cells[-1]
            rest = cells[:-1]

        if not rest or not rest[-1].isdigit() or rest[-1] not in "01234":
            continue
        level = int(rest[-1])
        name = " ".join(rest[:-1]).strip()
        if not name or name.lower().startswith("taxones"):
            continue

        taxa.append({"name": name, "level": level, "trend": trend})

    # Prediction week label, e.g. "27 de Julio a 02 de Agosto de 2026"
    week_match = re.search(r"\d{1,2} de [A-Za-zÀ-ÿ]+ a \d{1,2} de [A-Za-zÀ-ÿ]+ de \d{4}", soup.get_text(" ", strip=True))
    week_label = week_match.group(0) if week_match else None

    return taxa, week_label


def main():
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "https://aerobiologia.cat/pia/es/",
        "license": "CC BY-NC-SA 4.0 — https://aerobiologia.cat/pia/es/terms",
        "attribution_note": "Datos de niveles de polen y esporas: Punt d'Informació Aerobiològica (XAC-UAB).",
        "level_scale": {"0": "Nulo", "1": "Bajo", "2": "Medio", "3": "Alto", "4": "Máximo"},
        "trend_scale": TREND_LABELS,
        "stations": {},
    }

    had_error = False
    for station in STATIONS:
        url = BASE_URL.format(station=station)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            taxa, week_label = parse_station_page(resp.text)
            if not taxa:
                print(f"[warn] no se pudo extraer tabla de datos para {station}", file=sys.stderr)
                had_error = True
            result["stations"][station] = {
                "week": week_label,
                "url": url,
                "taxa": taxa,
            }
            print(f"[ok] {station}: {len(taxa)} taxones")
        except Exception as e:
            print(f"[error] {station}: {e}", file=sys.stderr)
            had_error = True
        time.sleep(1.5)  # be polite to the source server

    with open("data/pollen.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    if had_error and not any(s["taxa"] for s in result["stations"].values()):
        # Total failure: don't silently commit an empty file over good data.
        sys.exit(1)


if __name__ == "__main__":
    main()
