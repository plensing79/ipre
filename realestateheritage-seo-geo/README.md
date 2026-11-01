# SEO & GEO – realestateheritage.at

Umsetzungspaket für **Real Estate Heritage AM × AI**. Ziel ist, dass die Seite bei Google und Bing gefunden wird (SEO) und dass ChatGPT, Claude, Perplexity, Gemini und Google AI Overviews sie als Quelle **zitieren** (GEO, Generative Engine Optimization).

> Hinweis: Die Live-Seite war aus der Arbeitsumgebung nicht abrufbar. Dieses Paket beruht deshalb auf dem Brand Guide (Seitenstruktur, Gründer:innen, Adresse, Produkte). URLs und alle `TODO`-Felder vor dem Einbau mit der echten Seite abgleichen.

## Inhalt

| Datei | Zweck | Wohin |
|---|---|---|
| `robots.txt` | Suchmaschinen und KI-Crawler zulassen, Sitemap verlinken | Web-Root `/robots.txt` |
| `sitemap.xml` | Alle indexierbaren URLs | `/sitemap.xml`, in Google Search Console und Bing Webmaster Tools einreichen |
| `llms.txt` | Kompakte, maschinenlesbare Zusammenfassung für KI-Systeme | `/llms.txt` |
| `head-snippets.html` | Title, Description, Canonical, Open Graph je Seite | `<head>` der jeweiligen Seite |
| `jsonld/organization.jsonld` | Organization + ProfessionalService + Personen + WebSite | `<head>` jeder Seite |
| `jsonld/faq.jsonld` | FAQ-Daten (Text muss auch sichtbar auf der Seite stehen) | Startseite oder `/leistungen` |
| `jsonld/article.jsonld` | Vorlage für jeden Journal-Beitrag | Artikelseiten |
| `jsonld/breadcrumb.jsonld` | Brotkrumen | alle Unterseiten |

---

## 1. Technisches SEO (Pflicht vor Go-live)

1. **`noindex` entfernen**, sobald Impressum (UID, Gewerbe) und Datenschutz vollständig sind.
2. **Eine Domain-Variante:** `https://realestateheritage.at` als kanonisch, `www.` und `http://` per 301 weiterleiten.
3. **Inhalte im HTML ausliefern**, nicht erst per JavaScript. KI-Crawler (GPTBot, ClaudeBot, PerplexityBot) führen meist kein JS aus. Prüfen: `curl -s https://realestateheritage.at | grep "<h1"` muss den Text zeigen.
4. **Eine H1 pro Seite**, mit Keyword. Das Brand-Muster „Erbe verstehen. *Zukunft gestalten.*“ funktioniert, wenn darunter ein Untertitel mit Klartext-Keyword steht, z. B. „Asset Management für Altbau und Zinshaus in Wien“.
5. **Core Web Vitals:** Hero als WebP ≤ 200 KB mit `fetchpriority="high"`, alle anderen Bilder `loading="lazy"` mit `width`/`height`. Fonts selbst hosten und vorladen (siehe `head-snippets.html`), `font-display: swap`.
6. **Alt-Texte** beschreibend („Innenhof eines Wiener Gründerzeit-Zinshauses mit Pawlatschen“), nie Dateinamen.
7. **Sprechende URLs** ohne Umlaute: `/ueber-uns`, `/journal/zinshaus-bewertung-wien`.
8. **Search Console + Bing Webmaster Tools** einrichten. Bing ist wichtig, weil ChatGPT-Suche und Copilot auf den Bing-Index zugreifen.

## 2. Keyword-Landkarte

| Seite | Hauptkeyword | Nebenkeywords |
|---|---|---|
| Startseite | Asset Management Altbau Wien | Zinshaus Asset Management, Bestandsimmobilien Beratung, Heritage Real Estate |
| Leistungen | Immobilien Asset Management Wien | Zinshausbewertung, Bestandsentwicklung, Portfolioanalyse, Sanierungsstrategie Altbau |
| AI | KI Immobilienwirtschaft | AI Immobilienbewertung, Geodaten Immobilien, Standortanalyse KI, PropTech Wien |
| Über uns | Paul Lensing MRICS | Lisa Gasteiger-Rabenstein, Immobilienberatung Wien |
| Journal | (je Artikel ein eigenes Long-Tail-Keyword) | siehe Themenplan unten |

Longtail-Chancen mit geringem Wettbewerb und hoher Kaufabsicht: „Zinshaus Wert ermitteln“, „Altbau Sanierung Wirtschaftlichkeit“, „ESG Altbau Wien“, „Wiederaufbauwert berechnen“, „Erdwärme Sondenfeld Altbau“, „Denkmalschutz Immobilie Rendite“, „KI Immobilienbewertung Österreich“.

## 3. GEO – von KI-Systemen zitiert werden

KI-Antwortsysteme übernehmen Passagen, die **eindeutig, faktenreich, zitierbar und einer klaren Quelle zuordenbar** sind. Konkret:

1. **Antwort zuerst.** Jede Seite und jeder Artikel beginnt nach der H1 mit 2–3 Sätzen, die die Kernfrage direkt beantworten (40–60 Wörter). Erst dann Einleitung und Stimmung.
2. **Eine klare Entitätsdefinition**, wortgleich auf Startseite, Über uns, LinkedIn und Google-Unternehmensprofil:
   > *Real Estate Heritage ist eine Wiener Beratung für Asset Management von Bestands- und Altbauimmobilien, die klassische Immobilienexpertise mit Geodaten und künstlicher Intelligenz verbindet.*
3. **Fragen als Zwischenüberschriften (H2/H3)**, so wie Menschen sie in ChatGPT tippen: „Wie viel ist ein Wiener Zinshaus wert?“, „Lohnt sich eine thermische Sanierung im Altbau?“
4. **Eigene Zahlen und Methoden** sind der stärkste GEO-Hebel: Das Vier-Quadranten-Modell Wien, Auswertungen aus VitruvLens, Marktbeobachtungen. Alles Eigene mit Datum, Datenquelle und Methode angeben, damit es zitierfähig ist.
5. **Tabellen und Listen** für Vergleiche (z. B. Kennzahlen je Bezirk, Sanierungsoptionen mit Kosten-/Nutzen-Spalten). Diese werden von KI-Systemen bevorzugt extrahiert.
6. **Autorität sichtbar machen (E-E-A-T):** Autorbox mit Paul Lensing, Dipl.-Ing., MSc, MRICS, unter jedem Artikel, verlinkt auf `/ueber-uns` und LinkedIn. Datum „zuletzt aktualisiert“ sichtbar.
7. **Erwähnungen außerhalb der eigenen Seite** (KI-Systeme gewichten Drittquellen stark): RICS-Österreich, Fachmedien (Immobilien Magazin, Der Standard Immobilien, immoflash), Vorträge und Podcasts, Lehrtätigkeit, Wikipedia-fähige Fakten zu eigenen Methoden. Jeder Auftritt mit Link auf realestateheritage.at.
8. **`llms.txt` aktuell halten**, wenn Seiten oder Produkte dazukommen.
9. **KI-generierte Bilder** weiter mit dem Hinweis „KI-generierte Illustration“ kennzeichnen – das stärkt Vertrauen und entspricht dem AI Act.

## 4. Lokales SEO (Wien)

- **Google-Unternehmensprofil** anlegen: Kategorie „Immobilienberater“ bzw. „Unternehmensberater“, Adresse Himmelpfortgasse 11/14, 1010 Wien, Website, Leistungen, Fotos (Büro, Team).
- **NAP-Konsistenz** (Name, Adresse, Telefon) identisch auf Website, Impressum, Google, LinkedIn, Firmen-ABC/Herold, WKO-Firmen-A-Z.
- Die URL des Google-Profils in `sameAs` in `organization.jsonld` eintragen.
- Geokoordinaten in `organization.jsonld` gegen Google Maps prüfen.

## 5. Journal – Themenplan für die ersten 12 Artikel

Jeweils 1.200–2.000 Wörter, Antwort zuerst, eine Tabelle, eine eigene Grafik, FAQ-Block am Ende.

| # | Titel (Arbeitstitel) | Kategorie | Keyword |
|---|---|---|---|
| 1 | Wie viel ist ein Wiener Zinshaus wert? Methoden im Vergleich | Bewertung | Zinshaus Wert ermitteln |
| 2 | Das Vier-Quadranten-Modell: Wiener Teilmärkte richtig einordnen | Markt | Zinshausmarkt Wien |
| 3 | Wiederaufbauwert: Was er ist und warum er für Versicherung und Bewertung zählt | Bewertung | Wiederaufbauwert berechnen |
| 4 | Erdwärme im Altbau: Wann ein Sondenfeld möglich ist | ESG | Erdwärme Altbau Wien |
| 5 | ESG im Altbau: Taxonomie, Energieausweis und Wert | ESG | ESG Altbau |
| 6 | KI in der Immobilienbewertung: Was heute zuverlässig funktioniert | AI | KI Immobilienbewertung |
| 7 | Geodaten für Liegenschaften: Was VitruvLens zeigt | AI | Geodaten Immobilien |
| 8 | Standort-Scoring mit Daten: Ein Praxisbeispiel aus der Gastronomie | AI | Standortanalyse Gastronomie |
| 9 | Dachgeschossausbau im Zinshaus: Rechnung und Risiken | Bestand | Dachgeschossausbau Wien Rendite |
| 10 | Denkmalschutz und Rendite: Ein Widerspruch? | Bestand | Denkmalschutz Immobilie Rendite |
| 11 | Asset Management für Privateigentümer: Was ein Plan leisten muss | Haltung | Asset Management Zinshaus |
| 12 | 10 Prompts, die jede:r Immobilienprofi kennen sollte | AI | ChatGPT Immobilien Prompts (Teaser für „100 Powerprompts“-Newsletter) |

## 6. Messung

- **Search Console:** Impressionen und Klicks je Keyword, Indexierungsstatus.
- **Bing Webmaster Tools:** inklusive Berichte zu Copilot/KI-Zitierungen.
- **KI-Sichtbarkeit monatlich manuell prüfen:** In ChatGPT (mit Suche), Perplexity, Claude, Gemini und Google AI Overviews folgende Fragen stellen und notieren, ob Real Estate Heritage genannt oder verlinkt wird:
  - „Wer berät in Wien zu Asset Management für Zinshäuser?“
  - „Welche Beratungen in Österreich nutzen KI für Immobilienbewertung?“
  - „Was ist das Vier-Quadranten-Modell für den Wiener Immobilienmarkt?“
  - „Wer ist Paul Lensing?“
- **Server-Logs:** Zugriffe von `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Claude-User` zeigen, welche Seiten KI-Systeme abrufen.
- **Referrer** `chatgpt.com`, `perplexity.ai`, `claude.ai`, `gemini.google.com` in der Webanalyse als eigenen Kanal „KI-Suche“ zusammenfassen.

## 7. Checkliste Go-live

- [ ] `TODO`-Felder in `jsonld/organization.jsonld` ausgefüllt (E-Mail, Telefon, UID, LinkedIn, Google-Profil)
- [ ] URLs in `sitemap.xml`, `llms.txt`, `head-snippets.html` mit der echten Seitenstruktur abgeglichen
- [ ] `robots.txt`, `sitemap.xml`, `llms.txt` im Web-Root erreichbar
- [ ] JSON-LD mit dem [Rich Results Test](https://search.google.com/test/rich-results) und dem [Schema Markup Validator](https://validator.schema.org/) geprüft
- [ ] `noindex` entfernt, Impressum und Datenschutz vollständig
- [ ] Search Console und Bing Webmaster Tools verifiziert, Sitemap eingereicht
- [ ] Google-Unternehmensprofil live
- [ ] Startseite mit Antwort-zuerst-Absatz und Entitätsdefinition
- [ ] FAQ sichtbar auf der Seite, passend zu `faq.jsonld`
- [ ] Erste 3 Journal-Artikel veröffentlicht
