#!/usr/bin/env python3
"""SEO/GEO-Patch für den statischen Export von realestateheritage.at.

Aufruf:  python3 patch_site.py <export-ordner> [--golive]

- Ersetzt <title> und <meta name="description"> durch überarbeitete Fassungen.
- Fügt canonical, Open Graph, Twitter Card und JSON-LD (schema.org) ein.
- Kopiert robots.txt, sitemap.xml und llms.txt in den Export-Root.
- --golive entfernt zusätzlich <meta name="robots" content="noindex, nofollow">.
  Erst verwenden, wenn die Datenschutzerklärung vollständig ist.

Das Skript ist idempotent: Ein zweiter Lauf ersetzt den eingefügten Block, statt ihn zu verdoppeln.
"""
import html
import json
import os
import re
import shutil
import sys

BASE = "https://realestateheritage.at"
HERE = os.path.dirname(os.path.abspath(__file__))
MARK_START = "<!-- seo-geo:start -->"
MARK_END = "<!-- seo-geo:end -->"

ORG_ID = BASE + "/#organization"
PAUL_ID = BASE + "/#paul-lensing"
LISA_ID = BASE + "/#lisa-gasteiger-rabenstein"
SITE_ID = BASE + "/#website"

ORG = {
    "@type": ["Organization", "ProfessionalService"],
    "@id": ORG_ID,
    "name": "Real Estate Heritage",
    "alternateName": ["Real Estate Heritage AM × AI", "Heritage Real Estate Asset Management"],
    "slogan": "Tradition bewahren. Zukunft bauen.",
    "description": "Heritage Real Estate Asset Management aus Wien: strategisches Asset Management, "
                   "Architektur und Transaktion für historische und schutzwürdige Immobilien, "
                   "ergänzt um eigene datengestützte KI-Werkzeuge.",
    "url": BASE + "/",
    "logo": BASE + "/img/hero.webp",
    "image": BASE + "/img/hero.webp",
    "email": "mail@realestateheritage.at",
    "telephone": "+43 676 9196922",
    "vatID": "ATU66253608",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Himmelpfortgasse 11/14",
        "postalCode": "1010",
        "addressLocality": "Wien",
        "addressCountry": "AT",
    },
    "areaServed": [{"@type": "City", "name": "Wien"}, {"@type": "Country", "name": "Österreich"}],
    "knowsAbout": [
        "Heritage Real Estate Asset Management", "Bestandsimmobilien", "Historische und schutzwürdige Immobilien",
        "Immobilienbewertung", "ESG im Immobiliensektor", "Standortanalyse", "Geodaten",
        "Künstliche Intelligenz in der Immobilienwirtschaft",
    ],
    "founder": [{"@id": PAUL_ID}, {"@id": LISA_ID}],
    "sameAs": ["https://www.instagram.com/realestateheritage/"],
}

PAUL = {
    "@type": "Person",
    "@id": PAUL_ID,
    "name": "Paul Lensing",
    "honorificPrefix": "Dipl.-Ing.",
    "honorificSuffix": "MSc, MRICS",
    "jobTitle": "Gründer",
    "worksFor": {"@id": ORG_ID},
    "url": BASE + "/ueber-uns",
    "alumniOf": [
        {"@type": "CollegeOrUniversity", "name": "Technische Universität Wien"},
        {"@type": "CollegeOrUniversity", "name": "Donau-Universität Krems"},
    ],
    "memberOf": {"@type": "Organization", "name": "Royal Institution of Chartered Surveyors (RICS)"},
}

LISA = {
    "@type": "Person",
    "@id": LISA_ID,
    "name": "Lisa Gasteiger-Rabenstein",
    "jobTitle": "Gründerin",
    "worksFor": {"@id": ORG_ID},
    "url": BASE + "/ueber-uns",
}

WEBSITE = {
    "@type": "WebSite",
    "@id": SITE_ID,
    "url": BASE + "/",
    "name": "Real Estate Heritage",
    "inLanguage": ["de-AT", "en"],
    "publisher": {"@id": ORG_ID},
}

# page key (relative path without .html / index.html) -> settings
# img: Bild für Social-Vorschau. date: Veröffentlichungsdatum (nur Artikel).
PAGES = {
    "": dict(lang="de", type="home", img="hero",
             title="Real Estate Heritage – Asset Management für Altbau in Wien",
             desc="Asset Management für historische und schutzwürdige Immobilien in Wien – verbunden mit eigenen KI-Werkzeugen für Bewertung, Markt und Standort."),
    "leistungen": dict(lang="de", type="services", img="ai-facade",
             title="Leistungen: Asset Management, Architektur & Transaktion",
             desc="Strategisches Asset Management und ESG, Architektur und Vermarktung, Transaktion und Standortberatung für historische Immobilien – ergänzt um KI."),
    "ai": dict(lang="de", type="page", img="hof",
             title="KI im Immobilienbestand: Werkzeuge & Fallstudien",
             desc="VitruvLens, Vier-Quadranten-Modell Wien, Standort-Scoring und EVS-Bewertungs-App: eigene KI-Werkzeuge für Bewertung, Markt und Standortwahl."),
    "ueber-uns": dict(lang="de", type="about", img="seite",
             title="Über uns: Paul Lensing & Lisa Gasteiger-Rabenstein",
             desc="Paul Lensing (Dipl.-Ing., MSc, MRICS) und Lisa Gasteiger-Rabenstein: Heritage Real Estate Asset Management aus Wien, hervorgegangen aus Schlossseiten."),
    "journal": dict(lang="de", type="blog", img="leitsatz",
             title="Journal: Bestand, Markt, ESG & KI – Real Estate Heritage",
             desc="Fachbeiträge zu Bestandsimmobilien, Wiener Markt, ESG, Bewertung und künstlicher Intelligenz in der Immobilienwirtschaft."),
    "impressum": dict(lang="de", type="page", img="hero",
             title="Impressum – Real Estate Heritage",
             desc="Impressum von Real Estate Heritage, Himmelpfortgasse 11/14, 1010 Wien: Angaben gemäß § 5 ECG und § 25 MedienG."),
    "datenschutz": dict(lang="de", type="page", img="hero",
             title="Datenschutz – Real Estate Heritage",
             desc="Datenschutzerklärung von Real Estate Heritage: Hosting, lokal geladene Schriften, lokale Speicherung und Kontakt zum Datenschutz."),
    "nutzungsbedingungen": dict(lang="de", type="page", img="hero",
             title="Nutzungsbedingungen – Real Estate Heritage",
             desc="Nutzungsbedingungen der Website von Real Estate Heritage AM × AI, Wien."),
    "journal/vibe-coding-evs": dict(lang="de", type="article", img="ai-evs", date="2026-10-18", section="AI",
             title="EVS-Bewertungs-App: Vibe Coding in der Bewertung",
             desc="Wie ein Gutachter mit Vibe Coding eine Bewertungs-App nach den European Valuation Standards baut – live gezeigt auf der TEGoVA-Konferenz in Wien."),
    "journal/powerprompts": dict(lang="de", type="article", img="werkzeuge", date="2026-10-18", section="AI",
             title="100 Powerprompts: Bessere Entscheidungen mit KI",
             desc="Red Team, Premortem, Steelman und 97 weitere Denkwerkzeuge: wie Sie KI als Sparringspartner für Entscheidungen nutzen statt als Suchmaschine."),
    "journal/standort-scoring-gastro-konzept": dict(lang="de", type="article", img="ai-map", date="2026-10-18", section="AI",
             title="Standort-Scoring mit KI für ein Fast-Casual-Gastro-Konzept",
             desc="Wo zuerst eröffnen, wo danach? Gewichtetes Scoring für fünf Kandidaten in Wien, gestaffelte Eröffnungsreihenfolge und Zehn-Jahres-Modell."),
    "journal/vier-quadranten-modell-wien": dict(lang="de", type="article", img="ai-quad", date="2026-10-17", section="Markt",
             title="Vier-Quadranten-Modell: Szenarien für Wiens Wohnungsmarkt",
             desc="Was passiert mit Mieten, Preisen und Neubau in Wien, wenn Bauen teurer wird? Ein interaktives Modell nach DiPasquale und Wheaton."),
    "journal/vitruvlens": dict(lang="de", type="article", img="ai-lc", date="2026-10-17", section="AI",
             title="VitruvLens: Kompaktheit, Sondenfeld & Wiederaufbauwert",
             desc="VitruvLens berechnet aus Geodaten die Kompaktheit eines Gebäudes, die Eignung für Erdwärmesonden und den Wiederaufbauwert – zuerst für Wien."),
    "journal/heritage-faktor": dict(lang="de", type="article", img="heritage-faktor", date="2026-02-09", section="Bewertung",
             title="Der Heritage-Faktor: Was Altbau wertvoll macht",
             desc="Warum Altbau mehr als Nostalgie ist: wie Lage und Balkon zusammenwirken und warum der Preis nicht linear mit der Wohnungsgröße steigt."),
    "journal/drei-stufen-esg": dict(lang="de", type="article", img="esg", date="2025-08-11", section="ESG",
             title="Die drei Stufen von ESG im Immobiliensektor",
             desc="Light, Transitional und Deep ESG: drei Stufen der Nachhaltigkeit bei Immobilien – von der gesetzlichen Pflicht bis zum ganzheitlichen Anspruch."),
    "journal/kohlmarkt": dict(lang="de", type="article", img="kohlmarkt", date="2025-07-01", section="Markt",
             title="Der Kohlmarkt: Geschichte der besten Adresse Wiens",
             desc="Vom Kohle- und Gemüsehandel zur Luxusmeile: wie sich der Wiener Kohlmarkt in den letzten 150 Jahren zu einer der besten Adressen der Stadt entwickelt hat."),
    "journal/humanistischer-kapitalismus": dict(lang="de", type="article", img="humanismus", date="2025-07-01", section="Haltung",
             title="Humanistischer Kapitalismus in der Immobilienbranche",
             desc="Wie Immobilien wirtschaftliche, soziale und ökologische Ziele verbinden: Sanierung, Wohnmodelle, Beteiligung und Impact Investing."),
    "journal/entwicklung-bestandsimmobilien": dict(lang="de", type="article", img="bestand", date="2025-02-04", section="Bestand",
             title="Bestandsimmobilien entwickeln: ein systemischer Ansatz",
             desc="Bestandsimmobilien in sechs Schritten entwickeln: Standort, Bauordnung und Denkmalschutz, Bestandsaufnahme, Nutzungskonzept, Stakeholder, Umsetzung."),
    "en": dict(lang="en", type="home", img="hero",
             title="Real Estate Heritage – Heritage Asset Management, Vienna",
             desc="Asset management for historic and listed real estate in Vienna, combined with our own AI tools for valuation, market analysis and site selection."),
    "en/ai": dict(lang="en", type="page", img="hof",
             title="AI for Existing Buildings: Tools & Case Studies",
             desc="VitruvLens, the Vienna four-quadrant model, site scoring and an EVS valuation app: our own AI tools for valuation, markets and site selection."),
    "en/about": dict(lang="en", type="about", img="seite",
             title="About Us: Paul Lensing & Lisa Gasteiger-Rabenstein",
             desc="Paul Lensing (Dipl.-Ing., MSc, MRICS) and Lisa Gasteiger-Rabenstein: heritage real estate asset management from Vienna."),
    "en/journal/vibe-coding-evs": dict(lang="en", type="article", img="ai-evs", date="2026-10-18", section="AI",
             title="EVS Valuation App: Vibe Coding in Valuation",
             desc="How a valuer uses vibe coding to build a valuation app based on the European Valuation Standards – shown live at the TEGoVA conference in Vienna."),
}

SECTION_NAMES = {"de": {"journal": "Journal"}, "en": {"journal": "Journal"}}


def page_key(rel):
    rel = rel.replace(os.sep, "/")
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[: -len("/index.html")]
    return rel[: -len(".html")]


def url_for(key):
    if key == "":
        return BASE + "/"
    if key == "en":
        return BASE + "/en/"
    return BASE + "/" + key


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def build_graph(key, p, h1):
    url = url_for(key)
    lang = "de-AT" if p["lang"] == "de" else "en"
    graph = [ORG]
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"],
            "description": p["desc"], "inLanguage": lang, "isPartOf": {"@id": SITE_ID},
            "about": {"@id": ORG_ID}}
    if p["type"] == "home":
        graph += [WEBSITE, PAUL, LISA]
    elif p["type"] == "about":
        page["@type"] = "AboutPage"
        graph += [PAUL, LISA]
    elif p["type"] == "blog":
        page["@type"] = "CollectionPage"
    elif p["type"] == "services":
        graph.append({
            "@type": "ItemList", "name": "Leistungen",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "item": {"@type": "Service", "name": n, "provider": {"@id": ORG_ID}, "areaServed": "Wien"}}
                for i, n in enumerate([
                    "Strategisches Asset Management & ESG",
                    "Architektur & Immobilienmarketing",
                    "Wirtschaftliche Steuerung & Transaktion",
                    "Standortberatung mit datengestütztem Scoring",
                    "KI-Werkzeuge nach Maß",
                    "AI-Leadership & Workshops",
                ])
            ],
        })
    elif p["type"] == "article":
        img = f"{BASE}/img/{p['img']}.webp"
        graph.append({
            "@type": "BlogPosting", "@id": url + "#article", "headline": h1[:110] or p["title"],
            "description": p["desc"], "image": [img], "datePublished": p["date"], "dateModified": p["date"],
            "inLanguage": lang, "articleSection": p["section"], "author": {"@id": PAUL_ID},
            "publisher": {"@id": ORG_ID}, "mainEntityOfPage": url + "#webpage",
        })
        graph.append(PAUL)
        home = BASE + ("/en/" if p["lang"] == "en" else "/")
        crumbs = [("Real Estate Heritage", home)]
        if p["lang"] == "de":
            crumbs.append(("Journal", BASE + "/journal"))
        crumbs.append((h1 or p["title"], url))
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    graph.insert(1, page)
    return {"@context": "https://schema.org", "@graph": graph}


def head_block(key, p, h1):
    url = url_for(key)
    img = f"{BASE}/img/{p['img']}.webp"
    e = lambda s: html.escape(s, quote=True)
    og_type = "article" if p["type"] == "article" else "website"
    lines = [
        MARK_START,
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:type" content="{og_type}">',
        '<meta property="og:site_name" content="Real Estate Heritage">',
        f'<meta property="og:locale" content="{"de_AT" if p["lang"] == "de" else "en_GB"}">',
        f'<meta property="og:title" content="{e(p["title"])}">',
        f'<meta property="og:description" content="{e(p["desc"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{img}">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    if p["type"] == "article":
        lines.append(f'<meta property="article:published_time" content="{p["date"]}">')
        lines.append('<meta name="author" content="Paul Lensing">')
    lines.append(jsonld(build_graph(key, p, h1)))
    lines.append(MARK_END)
    return "\n".join(lines)


def patch_file(path, key, golive):
    p = PAGES[key]
    s = open(path, encoding="utf-8").read()
    s = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END) + r"\n?", "", s, flags=re.S)
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, flags=re.S | re.I)
    h1 = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip() if m else ""
    s = re.sub(r"<title>.*?</title>", "<title>" + html.escape(p["title"], quote=False) + "</title>", s, count=1, flags=re.S)
    desc_tag = '<meta name="description" content="' + html.escape(p["desc"], quote=True) + '">'
    s, n = re.subn(r'<meta name="description"[^>]*>', lambda _: desc_tag, s, count=1)
    if n == 0:
        s = s.replace("</title>", "</title>\n" + desc_tag, 1)
    if golive:
        s = re.sub(r'<meta name="robots" content="noindex, nofollow">\n?', "", s)
    block = head_block(key, p, h1)
    s = s.replace("</head>", block + "\n</head>", 1)
    open(path, "w", encoding="utf-8").write(s)
    return h1


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    golive = "--golive" in sys.argv
    seen = set()
    for dp, _, files in os.walk(root):
        for f in files:
            if not f.endswith(".html"):
                continue
            path = os.path.join(dp, f)
            key = page_key(os.path.relpath(path, root))
            if key not in PAGES:
                print("ÜBERSPRUNGEN (keine Daten):", key)
                continue
            patch_file(path, key, golive)
            seen.add(key)
    for k in PAGES:
        if k not in seen:
            print("NICHT GEFUNDEN:", k)
    for f in ("robots.txt", "sitemap.xml", "llms.txt"):
        shutil.copy(os.path.join(HERE, f), os.path.join(root, f))
    print(f"{len(seen)} Seiten gepatcht{' (go-live: noindex entfernt)' if golive else ' (noindex bleibt)'}")


if __name__ == "__main__":
    main()
