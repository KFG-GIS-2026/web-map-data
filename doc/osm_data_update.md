# Wie Änderungen in OSM in der Webkarte erscheinen

Wenn etwas in OpenStreetMap geändert wird, z. B.:

- einen Brunnen hinzufügst  
- eine Bank verschiebst
- ein Trinkwasserbrunnen löschst  
- eine Kirche korrigierst  
- Öffnungszeiten ergänzt  

So läuft der Prozess ab:

### 1. Änderung in OSM  
Ein Objekt wird in OSM bearbeitet (iD‑Editor, JOSM).

### 2. Änderung wird in Overpass sichtbar  
Nach wenigen Minuten bis Stunden.

### 3. Daten werden aktualisiert  
Jede Nacht werden neue Daten aktualisiert

### 4. Webkarte zeigt die neuen Daten  
Beim nächsten Öffnen der Webkarte sind die neuen Daten sichtbar

---

## Relevante OSM‑Tags

### Kirchen
Objekte erscheinen als „Kirche“, wenn sie einen der folgenden Tags besitzen:

- `building=church`
- `amenity=place_of_worship`

---

### Brunnen
Klassische Brunnen, dekorative Wasserobjekte oder historische Brunnen:

- `amenity=fountain`

---

### Trinkwasserstellen
Alle Arten von öffentlichen Wasserentnahmestellen:

- `amenity=drinking_water`
- `amenity=water_point`
- `man_made=water_tap`

---

### Parks
Flächen, die als Park oder Erholungsfläche gelten:

- `leisure=park`
- `landuse=recreation_ground`

---

### Spielplätze

- `leisure=playground`

---

### Sitzbänke

- `amenity=bench`

---

### Toiletten
Öffentliche Toiletten:

- `amenity=toilets`

---

### Bücherei
Bibliotheken und öffentliche Lesestellen:

- `amenity=library`

---

### Museum
Museen und Ausstellungen:

- `tourism=museum`
