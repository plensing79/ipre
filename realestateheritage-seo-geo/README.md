# SEO & KI-Sichtbarkeit – realestateheritage.at

Grundlage: statischer Export `reh-wix.zip` (22 Seiten, DE/EN, Hosting Vercel), geprüft am 1. November 2026.

## Dateien

| Datei | Zweck |
|---|---|
| `patch_site.py` | Patcht den Export: neue Titel und Beschreibungen, Canonical, Open Graph, JSON-LD je Seite; kopiert robots.txt, sitemap.xml, llms.txt in den Root. Idempotent. |
| `robots.txt` | Erlaubt Suchmaschinen, KI-Suche und (abschaltbar) KI-Training |
| `sitemap.xml` | 20 URLs inkl. hreflang-Paare DE/EN |
| `llms.txt` | Faktenblatt für KI-Systeme, nur Angaben von der eigenen Website |

## Anwendung

```bash
unzip reh-wix.zip -d reh
python3 patch_site.py reh            # noindex bleibt (vor Launch)
python3 patch_site.py reh --golive   # erst wenn die Datenschutzerklärung vollständig ist
```

Neue Seiten oder Artikel: Eintrag in `PAGES` in `patch_site.py` ergänzen (Titel ≤ 60 Zeichen, Beschreibung ≤ 155 Zeichen, Bild, Datum), in `sitemap.xml` und `llms.txt` nachtragen.

## Die fünf wichtigsten Befunde

1. **Alle Seiten `noindex, nofollow`, Datenschutz ist Platzhalter** – vor Launch korrekt; `--golive` erst nach vollständiger Datenschutzerklärung.
2. **Keine robots.txt / sitemap.xml** – erstellt.
3. **Keine strukturierten Daten** – Organization/ProfessionalService, Personen, Leistungen, BlogPosting, BreadcrumbList eingefügt.
4. **Drei Firmennamen** (Real Estate Heritage AM × AI / Heritage Real Estate Asset Management / SCHLOSSSEITEN Österreich) und keine Einträge außerhalb der Seite – einen Namen festlegen, Google-Unternehmensprofil, LinkedIn, WKO, RICS-Verzeichnis.
5. **Titel/Beschreibungen ohne Suchbegriffe, keine Canonicals, kein Open Graph** – neu geschrieben und eingefügt.

Weitere Punkte: EVS-Artikel spricht vom 23.10.2026 in der Zukunft; Gewerbebehörde 3. Bezirk vs. Adresse 1010 prüfen; Bilder bis 600 KB; WebP als Vorschaubild für LinkedIn ungünstig; kein sichtbarer FAQ-Block.
