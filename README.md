# Geodaten der Kühle-Orte-Karte Neckargemünd

Dieses Repository enthält die öffentlich bereitgestellten Geodaten und Kartensymbole der **Kühle-Orte-Karte Neckargemünd**. Die Dateien werden über GitHub Pages statisch ausgeliefert und von der Webanwendung direkt im Browser geladen.

- [Kühle-Orte-Karte öffnen](https://kfg-gis-2026.github.io/web-map/)
- [Repository der Webkarte](https://github.com/KFG-GIS-2026/web-map)
- [Repository der Datenverarbeitung](https://github.com/KFG-GIS-2026/data_processing)

> **Hinweis:** Die Sonnen- und Schattenwerte sind modellierte Näherungen für einen wolkenfreien Himmel. Sie ersetzen keine Messungen vor Ort und werden ohne Gewähr bereitgestellt.

## Inhalt

```text
web-map-data/
├── boundary/
│   └── Neckargemuend_boundary.geojson
├── osm_poi/
│   ├── Brunnen.geojson
│   ├── Bücherei.geojson
│   ├── Gewässer.geojson
│   ├── Kirche.geojson
│   ├── Museum.geojson
│   ├── Park_Punkte.geojson
│   ├── Sitzbank.geojson
│   ├── Spielplatz_Punkte.geojson
│   ├── Toilete.geojson
│   └── Trinkwasserstelle.geojson
├── poi_symbols/
│   └── *.png
└── shadows/
    ├── 5_1/
    ├── 5_15/
    ├── 6_1/
    ├── 6_15/
    ├── 7_1/
    ├── 7_15/
    ├── 8_1/
    ├── 8_15/
    ├── 9_1/
    └── 9_15/
```

## Datenkatalog

### Points of Interest

Alle POI-Dateien sind GeoJSON-`FeatureCollection`s. Die in der Webkarte dargestellten Objekte besitzen Punktgeometrien in WGS 84.

| Datei | Kategorie | Objekte | Verwendung in der Webkarte |
| --- | --- | ---: | --- |
| `Spielplatz_Punkte.geojson` | Spielplätze | 20 | POI und Sonnenbelastung |
| `Park_Punkte.geojson` | Parks | 5 | POI und Sonnenbelastung |
| `Sitzbank.geojson` | Sitzbänke | 377 | POI und Sonnenbelastung |
| `Trinkwasserstelle.geojson` | Trinkwasserstellen | 16 | POI |
| `Toilete.geojson` | öffentliche Toiletten | 9 | POI |
| `Kirche.geojson` | Kirchen | 13 | POI |
| `Brunnen.geojson` | Brunnen | 17 | POI |
| `Bücherei.geojson` | Büchereien | 1 | POI |
| `Museum.geojson` | Museen | 1 | POI |
| `Gewässer.geojson` | Gewässer | 28 | derzeit nicht als POI-Kategorie eingebunden |

Die Objektzahlen entsprechen dem aktuellen Datenstand und können sich mit späteren Aktualisierungen ändern.

Viele Eigenschaften stammen aus OpenStreetMap, beispielsweise `name`, `amenity`, `opening_hours`, `wheelchair` und `osm_id`. Nicht jedes Objekt besitzt alle Attribute. Anwendungen müssen daher mit fehlenden oder leeren Werten umgehen können.

### Attribute zur Sonnenbelastung

`Park_Punkte.geojson`, `Spielplatz_Punkte.geojson` und `Sitzbank.geojson` enthalten zusätzlich modellierte Werte der solaren Globalstrahlung in **W/m²**. Die stündlichen Attributnamen folgen diesem Schema:

```text
MMTT_SS
```

Dabei stehen:

- `MM` für den Monat,
- `TT` für den Tag,
- `SS` für die volle Stunde.

Beispiele:

```text
0501_08  → 1. Mai, 08:00 Uhr
0715_14  → 15. Juli, 14:00 Uhr
0901_20  → 1. September, 20:00 Uhr
```

Der Datenbestand umfasst stündliche Werte von 08:00 bis 20:00 Uhr für den 1. und 15. der Monate April bis September. Zusätzlich sind vorberechnete Tagesmittelwerte mit Bezeichnungen wie `0105_mean` und `1505_mean` enthalten. Die aktuelle Webkarte berechnet den angezeigten Tagesmittelwert aus den vorhandenen Stundenwerten.

### Stadtgrenze

`boundary/Neckargemuend_boundary.geojson` enthält die Grenze Neckargemünds als `MultiPolygon` im Koordinatenreferenzsystem OGC CRS84. Die Webkarte verwendet sie zur räumlichen Abgrenzung des Untersuchungsgebiets.

### Schattenraster

Der Ordner `shadows/` enthält 130 Raster-PMTiles-Dateien für zehn Referenztage:

- jeweils den 1. und 15. der Monate Mai bis September,
- jeweils für volle Stunden von 08:00 bis 20:00 Uhr.

Die Verzeichnis- und Dateinamen folgen diesem Schema:

```text
shadows/{Monat}_{Tag}/shadow_{Stunde}00.pmtiles
```

Beispiel:

```text
shadows/7_15/shadow_1400.pmtiles
```

Diese Datei enthält die modellierte Schattendarstellung für den 15. Juli um 14:00 Uhr. Die PMTiles wurden aus georeferenzierten RGBA-Schattenmasken erzeugt. Bereiche mit einer modellierten Einstrahlung von höchstens 5 W/m² werden dabei als Schatten behandelt; übrige Bereiche sind transparent.

### Kartensymbole

`poi_symbols/` enthält neun PNG-Symbole. Die Zuordnung in der Webkarte lautet:

| Datei | Kategorie |
| --- | --- |
| `001-slide.png` | Spielplatz |
| `002-park.png` | Park |
| `003-bank.png` | Sitzbank |
| `004-water.png` | Trinkwasserstelle |
| `005-toilet.png` | Toilette |
| `006-church.png` | Kirche |
| `007-fountain.png` | Brunnen |
| `008-open-book.png` | Bücherei |
| `009-museum-art.png` | Museum |

## Daten abrufen

Die Inhalte werden über GitHub Pages unter folgender Basisadresse ausgeliefert:

```text
https://kfg-gis-2026.github.io/web-map-data
```

Beispiele:

- [Brunnen als GeoJSON](https://kfg-gis-2026.github.io/web-map-data/osm_poi/Brunnen.geojson)
- [Stadtgrenze als GeoJSON](https://kfg-gis-2026.github.io/web-map-data/boundary/Neckargemuend_boundary.geojson)
- [Schatten-PMTiles für den 15. Juli um 14:00 Uhr](https://kfg-gis-2026.github.io/web-map-data/shadows/7_15/shadow_1400.pmtiles)

GeoJSON kann beispielsweise direkt mit JavaScript geladen werden:

```javascript
const response = await fetch(
  "https://kfg-gis-2026.github.io/web-map-data/osm_poi/Brunnen.geojson"
);
const geojson = await response.json();
```

PMTiles-Dateien können mit einer kompatiblen Kartenbibliothek wie MapLibre GL JS und dem PMTiles-Protokoll eingebunden werden. Die Dateien sind für bereichsbasierte HTTP-Anfragen optimiert, sodass nicht das gesamte Archiv geladen werden muss.

## Verwendung in der Webkarte

Die Webanwendung greift zur Laufzeit auf dieses Repository zu. Dateinamen und Verzeichnisstruktur sind deshalb Teil der Schnittstelle zwischen den beiden Repositories.

Die zentrale Zuordnung befindet sich im Webkarten-Repository in `src/js/config.js`. Schatten-URLs werden nach folgendem Muster erzeugt:

```javascript
`${DATA_BASE_URL}/shadows/${month}_${day}/shadow_${hour}00.pmtiles`
```

Beim Umbenennen oder Verschieben einer Datei muss daher auch die Konfiguration beziehungsweise die URL-Erzeugung der Webkarte angepasst werden.

## Daten erstellen und aktualisieren

Die Skripte zur Erzeugung und Aufbereitung der Daten befinden sich im Repository [data_processing](https://github.com/KFG-GIS-2026/data_processing). Der dort dokumentierte Workflow umfasst:

1. Download und räumliche Auswahl von OpenStreetMap-Daten
2. Berechnung der Sonnenstrahlung und des Schattenwurfs mit GRASS GIS
3. Erzeugung transparenter Schattenmasken als GeoTIFF
4. Konvertierung der Rasterdaten über MBTiles nach PMTiles
5. Übernahme der fertigen Webdaten in dieses Repository

Bei einer Aktualisierung sollten folgende Bedingungen erhalten bleiben:

- GeoJSON-Dateien verwenden WGS 84 beziehungsweise CRS84.
- Die von der Webkarte geladenen POI-Dateien enthalten Punktgeometrien.
- Dateinamen einschließlich Groß-/Kleinschreibung und Umlauten stimmen mit `src/js/config.js` überein.
- Strahlungsattribute verwenden das Schema `MMTT_SS`.
- Schattenordner und PMTiles-Dateien verwenden das oben beschriebene Namensschema.
- Neue Referenztage oder Uhrzeiten werden auch in der Webkarte ergänzt.

Vor einem Commit sollten alle GeoJSON-Dateien auf gültiges JSON, erwartete Geometrietypen und plausible Koordinaten geprüft werden. Wegen der Größe der PMTiles-Dateien sollten außerdem Dateigrößen und Git-Diff kontrolliert werden.

## Lokale Kontrolle

Für eine einfache lokale Bereitstellung kann im Repository-Stammverzeichnis ein Webserver gestartet werden:

```bash
python -m http.server 8000
```

Danach ist beispielsweise die Brunnen-Datei unter folgender Adresse erreichbar:

```text
http://localhost:8000/osm_poi/Brunnen.geojson
```

Für eine vollständige visuelle Prüfung sollte die lokale Kopie der Webkarte vorübergehend auf diese Basisadresse verweisen.

## Deployment

Das Repository benötigt keinen Build-Prozess. GitHub Pages veröffentlicht die Dateien statisch aus dem konfigurierten Branch. Nach einem Push kann es einige Minuten dauern, bis neue oder geänderte Daten unter der öffentlichen Basisadresse verfügbar sind.

## Datenquellen und Lizenzen

Die POI-Daten und die Gebietsgrenze basieren ganz oder teilweise auf [OpenStreetMap](https://www.openstreetmap.org/copyright) und unterliegen der Open Data Commons Open Database License (ODbL). Bei Nutzung und Weitergabe sind insbesondere die vorgeschriebene Quellenangabe und die Bedingungen der ODbL zu beachten.

Für abgeleitete Rasterdaten, Kartensymbole und weitere Ausgangsdaten gelten zusätzlich die jeweiligen Rechte und Lizenzbedingungen ihrer ursprünglichen Anbieter. Die konkreten Quellen und Lizenzen der Symboldateien sind in diesem Repository derzeit nicht separat ausgewiesen und müssen vor einer Weiterverwendung außerhalb des Projekts geprüft werden.

Für das Repository ist derzeit keine separate Lizenzdatei hinterlegt. Aus der öffentlichen Abrufbarkeit der Dateien folgt daher nicht automatisch eine uneingeschränkte Nutzungserlaubnis.

## Mitwirken

Fehlerberichte und Verbesserungsvorschläge können über die [GitHub Issues](https://github.com/KFG-GIS-2026/web-map-data/issues) eingereicht werden. Änderungen an Datenstruktur oder Dateinamen sollten mit dem Repository der Webkarte abgestimmt und gemeinsam getestet werden.
