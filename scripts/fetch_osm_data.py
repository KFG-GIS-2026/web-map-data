"""
fetch_osm_data.py
=================
Lädt OSM-POIs für Neckargemünd via Overpass API und speichert sie als GeoJSON.

Räumlicher Filter: OSM-Relation 453391 (Verwaltungsgrenze Neckargemünd),
direkt in der Overpass-Query via area-Filter – keine eigene Boundary-GeoJSON nötig.

- `beschränkung` wird automatisch aus OSM-Tags (fee / access) berechnet.
- Manuell ergänzte Felder (z.B. Solarwerte wie `0401_08`) bleiben erhalten,
  indem sie aus der bestehenden GeoJSON per osm_id zurückgemergt werden.

Ausgabe-Ordner: osm_poi/
    Brunnen.geojson
    Bücherei.geojson
    Gewässer.geojson
    Kirche.geojson
    Museum.geojson
    Park.geojson
    Park_Punkte.geojson
    Sitzbank.geojson
    Spielplatz.geojson
    Spielplatz_Punkte.geojson
    Toilete.geojson
    Trinkwasserstelle.geojson
"""

import json
import re
import time
import requests
from pathlib import Path


# ── Konfiguration ─────────────────────────────────────────────────────────────

# OSM-Relation Neckargemünd (Verwaltungsgrenze admin_level=8)
# Overpass erwartet: Relation-ID + 3.6e9
AREA_ID = 3600453391

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

OUTPUT_DIR = Path(__file__).parent / "../osm_poi"

MAX_RETRIES    = 5
BACKOFF_FACTOR = 6  # Sekunden × Versuch


# ── Overpass-Query ────────────────────────────────────────────────────────────
# Räumlicher Filter direkt über OSM-Verwaltungsgrenze (area), keine BBOX nötig.

QUERY = f"""
[out:json][timeout:180];
area({AREA_ID})->.city;
(
  node["building"="church"](area.city);
  way["building"="church"](area.city);

  node["amenity"="place_of_worship"](area.city);
  way["amenity"="place_of_worship"](area.city);

  node["amenity"="fountain"](area.city);
  way["amenity"="fountain"](area.city);

  node["leisure"="playground"](area.city);
  way["leisure"="playground"](area.city);

  way["natural"="water"](area.city);
  way["water"="river"](area.city);
  way["leisure"="swimming_pool"](area.city);

  way["leisure"="park"](area.city);
  way["landuse"="recreation_ground"](area.city);

  node["amenity"="toilets"](area.city);
  way["amenity"="toilets"](area.city);

  node["amenity"="bench"](area.city);

  node["amenity"="library"](area.city);
  way["amenity"="library"](area.city);

  node["tourism"="museum"](area.city);
  way["tourism"="museum"](area.city);

  node["amenity"="drinking_water"](area.city);
  node["amenity"="water_point"](area.city);
  way["amenity"="water_point"](area.city);
  node["man_made"="water_tap"](area.city);
  way["man_made"="water_tap"](area.city);
);
out body;
>;
out skel qt;
"""


# ── Layer-Konfiguration ───────────────────────────────────────────────────────

LAYER_MAPPING = {
    ("building",  "church"):            "Kirche",
    ("amenity",   "place_of_worship"):  "Kirche",
    ("tourism",   "museum"):            "Museum",
    ("amenity",   "library"):           "Bücherei",
    ("amenity",   "fountain"):          "Brunnen",
    ("leisure",   "playground"):        "Spielplatz",
    ("leisure",   "park"):              "Park",
    ("landuse",   "recreation_ground"): "Park",
    ("natural",   "water"):             "Gewässer",
    ("leisure",   "swimming_pool"):     "Gewässer",
    ("water",     "river"):             "Gewässer",
    ("amenity",   "toilets"):           "Toilete",
    ("amenity",   "bench"):             "Sitzbank",
    ("amenity",   "drinking_water"):    "Trinkwasserstelle",
    ("amenity",   "water_point"):       "Trinkwasserstelle",
    ("man_made",  "water_tap"):         "Trinkwasserstelle",
}

# Diese Typen immer als Punkt speichern (nie als Polygon)
FORCE_POINT = {
    ("building",  "church"),
    ("amenity",   "place_of_worship"),
    ("tourism",   "museum"),
    ("amenity",   "library"),
    ("amenity",   "fountain"),
    ("amenity",   "toilets"),
    ("amenity",   "bench"),
    ("amenity",   "drinking_water"),
    ("amenity",   "water_point"),
    ("man_made",  "water_tap"),
}

# Für diese Layer zusätzlich einen Punkte-Layer (Zentroid) erzeugen
ALSO_AS_POINTS = {"Spielplatz", "Park"}

# Manuell ergänzte Felder: nur Solarwerte im Format "MMTT_HH" z.B. "0401_08"
MANUAL_FIELD_PATTERN = re.compile(r"^\d{4}_\d{2}$")


def is_manual_field(key: str) -> bool:
    return bool(MANUAL_FIELD_PATTERN.match(key))


# ── Hilfsfunktionen ───────────────────────────────────────────────────────────

def compute_beschraenkung(tags: dict, layer_name: str = "") -> str | None:
    """
    Leitet `beschränkung` aus OSM-Tags ab.
    Gibt None zurück wenn das Objekt gefiltert werden soll.
    drinking_water=no greift nur bei Trinkwasserstellen.
    """
    if tags.get("access") == "private":
        return None
    if layer_name == "Trinkwasserstelle" and tags.get("drinking_water") == "no":
        return None
    if tags.get("fee") == "yes" or tags.get("access") == "customers":
        return "Zahlungspflichtig"
    return "Kostenfrei"


def overpass_download(query: str) -> dict:
    """Sendet Overpass-Query mit Retry und Endpoint-Fallback."""
    endpoint_idx = 0
    for attempt in range(1, MAX_RETRIES + 1):
        url = OVERPASS_ENDPOINTS[endpoint_idx % len(OVERPASS_ENDPOINTS)]
        try:
            print(f"  Versuch {attempt} ({url}) …")
            response = requests.post(
                url,
                data=query.encode("utf-8"),
                headers={"User-Agent": "KuehleKarte-Neckargemuend/1.0"},
                timeout=150,
            )
            response.raise_for_status()
            print(f"  HTTP {response.status_code} ✓")
            return response.json()
        except Exception as exc:
            print(f"  Versuch {attempt} fehlgeschlagen: {exc}")
            if attempt == MAX_RETRIES:
                raise
            endpoint_idx += 1
            wait = BACKOFF_FACTOR * attempt
            print(f"  Warte {wait}s …")
            time.sleep(wait)


def way_to_coords(way_el: dict, nodes: dict) -> list[tuple]:
    return [
        (nodes[nid]["lon"], nodes[nid]["lat"])
        for nid in way_el.get("nodes", [])
        if nid in nodes
    ]


def centroid(coords: list[tuple]) -> tuple[float, float]:
    return (
        sum(c[0] for c in coords) / len(coords),
        sum(c[1] for c in coords) / len(coords),
    )


def make_point(lon: float, lat: float, tags: dict, osm_id: int, layer_name: str = "") -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "osm_id": osm_id,
            "beschränkung": compute_beschraenkung(tags, layer_name),
            **tags,
        },
    }


def make_polygon(coords: list[tuple], tags: dict, osm_id: int, layer_name: str = "") -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [coords]},
        "properties": {
            "osm_id": osm_id,
            "beschränkung": compute_beschraenkung(tags, layer_name),
            **tags,
        },
    }


def as_feature_collection(features: list) -> dict:
    return {"type": "FeatureCollection", "features": features}


def load_manual_props(path: Path) -> dict[int, dict]:
    """
    Liest bestehende GeoJSON und gibt nur manuell ergänzte Properties zurück
    (Solarwerte wie `0401_08`), indexiert per osm_id.
    """
    if not path.exists():
        return {}
    try:
        fc = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

    result = {}
    for feat in fc.get("features", []):
        props = feat.get("properties") or {}
        osm_id = props.get("osm_id")
        if osm_id is None:
            continue
        manual = {k: v for k, v in props.items() if is_manual_field(k)}
        if manual:
            result[osm_id] = manual
    return result


def save_geojson(path: Path, features: list) -> None:
    """
    Speichert GeoJSON. Solarwerte aus der bestehenden Datei werden
    per osm_id zurückgemergt. OSM-Properties gewinnen bei Konflikten.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    manual_props = load_manual_props(path)
    merged_count = 0

    for feat in features:
        osm_id = feat["properties"].get("osm_id")
        if osm_id in manual_props:
            feat["properties"] = {
                **manual_props[osm_id],  # Solarwerte zuerst (niedrigere Priorität)
                **feat["properties"],    # OSM-Daten + beschränkung gewinnen
            }
            merged_count += 1

    fc = as_feature_collection(features)
    path.write_text(json.dumps(fc, ensure_ascii=False, indent=2), encoding="utf-8")

    note = f", {merged_count} mit Solarwerten" if merged_count else ""
    print(f"  → {path.name}  ({len(features)} Features{note})")


# ── Hauptlogik ────────────────────────────────────────────────────────────────

def process_elements(elements: list) -> dict[str, list]:
    """Sortiert OSM-Elemente in Layer und baut GeoJSON-Features."""
    nodes = {el["id"]: el for el in elements if el["type"] == "node"}

    layers: dict[str, list] = {}
    point_layers: dict[str, list] = {}

    for el in elements:
        tags = el.get("tags", {})
        if not tags:
            continue

        # Layer-Zuordnung
        layer_name = None
        force_pt = False
        for (key, value), name in LAYER_MAPPING.items():
            if tags.get(key) == value:
                layer_name = name
                force_pt = (key, value) in FORCE_POINT
                break

        if layer_name is None:
            continue

        # Objekte nach layer-spezifischen Regeln filtern
        if compute_beschraenkung(tags, layer_name) is None:
            continue

        layers.setdefault(layer_name, [])

        # ── Node ────────────────────────────────────────────────────────────
        if el["type"] == "node":
            layers[layer_name].append(
                make_point(el["lon"], el["lat"], tags, el["id"], layer_name)
            )

        # ── Way ─────────────────────────────────────────────────────────────
        elif el["type"] == "way":
            coords = way_to_coords(el, nodes)
            if len(coords) < 2:
                continue

            closed = len(coords) >= 4 and coords[0] == coords[-1]

            if force_pt or not closed:
                cx, cy = centroid(coords)
                layers[layer_name].append(make_point(cx, cy, tags, el["id"], layer_name))

            else:
                cx, cy = centroid(coords)
                layers[layer_name].append(make_polygon(coords, tags, el["id"], layer_name))

                # Zusätzlicher Punkte-Layer für Parks & Spielplätze
                if layer_name in ALSO_AS_POINTS:
                    pt_name = f"{layer_name}_Punkte"
                    point_layers.setdefault(pt_name, [])
                    point_layers[pt_name].append(
                        make_point(cx, cy, tags, el["id"], layer_name)
                    )

    layers.update(point_layers)
    return layers


def main():
    print("=== Kühle Karte – OSM Daten abrufen ===\n")
    print(f"Räumlicher Filter: OSM-Relation {AREA_ID} (Neckargemünd)\n")

    print("Sende Overpass-Anfrage …")
    data = overpass_download(QUERY)

    elements = data.get("elements", [])
    if not elements:
        raise RuntimeError("Overpass hat keine Elemente zurückgegeben.")
    print(f"  {len(elements)} OSM-Elemente empfangen\n")

    print("Verarbeite Elemente …")
    layers = process_elements(elements)

    print(f"\nSpeichere GeoJSON-Dateien in {OUTPUT_DIR}/ …")
    total = 0
    for layer_name, features in sorted(layers.items()):
        if not features:
            print(f"  (leer: {layer_name})")
            continue
        save_geojson(OUTPUT_DIR / f"{layer_name}.geojson", features)
        total += len(features)

    print(f"\n✓ Fertig — {total} Features in {len(layers)} Layer(n) gespeichert.")


if __name__ == "__main__":
    main()