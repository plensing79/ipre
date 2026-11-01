# Umsetzung in Wix

Wix erzeugt Sitemap, Canonical-Tags und hreflang (Wix Multilingual) selbst. `patch_site.py` und `sitemap.xml` sind für Wix nicht nötig.

| Schritt | Wo in Wix | Was |
|---|---|---|
| 1 | Einstellungen → SEO → „Suchmaschinen erlauben, Ihre Website zu indexieren“ | Erst einschalten, wenn die Datenschutzerklärung fertig ist. Auf jeder Seite unter Erweitertes SEO prüfen, dass „noindex“ nicht gesetzt ist. |
| 2 | Einstellungen → SEO → Robots.txt-Editor | Block aus `robots-ergaenzung.txt` **anfügen**, Wix-Zeilen stehen lassen. |
| 3 | Seiten & Menü → ⋯ → SEO-Grundlagen | Titel und Beschreibung je Seite aus `SEITEN.md`. |
| 4 | Seiten & Menü → ⋯ → Erweitertes SEO → Strukturierte Daten | Je JSON-Datei aus `jsonld/` ein Block (max. 5 pro Seite, je 7.000 Zeichen – eingehalten). |
| 5 | Seiten & Menü → ⋯ → Soziale Netzwerke | Social-Titel, -Beschreibung und Bild (JPG 1200 × 630). |
| 6 | SEO-Dashboard → llms.txt (falls angezeigt) | Inhalt aus `../llms.txt` einsetzen. Wix bietet die Datei nicht in jedem Tarif an. Fehlt sie, entfällt der Schritt. |
| 7 | Einstellungen → SEO → Google Search Console verbinden; Bing Webmaster Tools per Meta-Tag | Sitemap `https://realestateheritage.at/sitemap.xml` einreichen. |

Ist das Journal ein Wix Blog, erzeugt Wix die BlogPosting-Daten selbst; dann nur den Navigationspfad-Block (`…-3.json`) ergänzen oder den eigenen Block bewusst als Ersatz einsetzen.

Wichtig: Wenn die Seiten als HTML-Einbettung (iframe/„Code einbetten“) in Wix stecken, sehen Google und KI-Crawler den Text nicht als Teil der Seite. Dann müssen die Texte als echte Wix-Textelemente angelegt werden.

Die Datenschutzerklärung im Export nennt Vercel als Hoster. Bei Wix-Hosting auf Wix.com Ltd. (inkl. Cookies und Datenübermittlung) umstellen.
