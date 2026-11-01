#!/usr/bin/env python3
"""Erzeugt aus patch_site.py die Eingaben für Wix: je Seite SEO-Titel, Beschreibung
und bis zu 5 JSON-LD-Blöcke (Wix-Limit: 5 Blöcke à 7.000 Zeichen pro Seite)."""
import json, os, importlib.util, html
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("m", os.path.join(HERE, "patch_site.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
H1 = {  # Überschriften aus dem Export, für Artikel-Headline und Navigationspfad
 "journal/vibe-coding-evs": "EVS-Bewertungs-App: Vibe Coding und die größte Transformation seit Excel",
 "journal/powerprompts": "100 Powerprompts: Denkwerkzeuge für bessere Entscheidungen mit KI",
 "journal/standort-scoring-gastro-konzept": "Expansionstool für ein Fast-Casual-Gastro-Konzept: Standortentscheidungen mit Daten und KI",
 "journal/vier-quadranten-modell-wien": "Vier-Quadranten-Modell: Der Wiener Wohnungsmarkt als interaktives Szenario-Tool",
 "journal/vitruvlens": "VitruvLens: Kompaktheit, Sondenfeld und Wiederaufbauwert aus Geodaten",
 "journal/heritage-faktor": "Der „Heritage-Faktor“: Warum Altbau mehr als nur Nostalgie ist",
 "journal/drei-stufen-esg": "Die drei Stufen von ESG im Immobiliensektor: Von Pflicht zur Vision",
 "journal/kohlmarkt": "Der Kohlmarkt – seit Jahrhunderten die beste Adresse Wiens",
 "journal/humanistischer-kapitalismus": "Humanistischer Kapitalismus in der Immobilienbranche",
 "journal/entwicklung-bestandsimmobilien": "Die Entwicklung von Bestandsimmobilien: Ein systemischer Ansatz für nachhaltige Stadtentwicklung",
 "en/journal/vibe-coding-evs": "EVS valuation app: vibe coding and the biggest transformation since Excel",
}
def items(key, p):
    g = m.build_graph(key, p, H1.get(key, ""))["@graph"]
    out = []
    for node in g:
        if node.get("@type") in ("WebPage", "AboutPage", "CollectionPage"):
            continue  # erzeugt Wix selbst
        if node is m.ORG and p["type"] not in ("home", "about"):
            continue  # Organisation nur auf Start- und Über-uns-Seite vollständig
        out.append(dict({"@context": "https://schema.org"}, **node))
    return out
md = ["# Wix-Eingaben je Seite", "",
      "Pro Seite in Wix: Seiten & Menü → ⋯ → SEO-Grundlagen (Titel, Beschreibung) · Erweitertes SEO → Strukturierte Daten → je Block „Neue Markierung hinzufügen“ · Soziale Netzwerke (Titel, Beschreibung, Bild).", ""]
os.makedirs(os.path.join(HERE, "wix", "jsonld"), exist_ok=True)
for key, p in m.PAGES.items():
    its = items(key, p)
    assert len(its) <= 5, key
    md += [f"## {m.url_for(key)}", "", f"- **SEO-Titel:** {p['title']}", f"- **Meta-Beschreibung:** {p['desc']}",
           f"- **Social-Bild:** /img/{p['img']}.webp (besser als JPG 1200×630 hochladen)",
           f"- **Strukturierte Daten:** {len(its)} Block/Blöcke → `wix/jsonld/{(key or 'start').replace('/', '__')}-N.json`", ""]
    for i, it in enumerate(its, 1):
        s = json.dumps(it, ensure_ascii=False, indent=2)
        assert len(s) <= 7000, (key, len(s))
        open(os.path.join(HERE, "wix", "jsonld", f"{(key or 'start').replace('/', '__')}-{i}.json"), "w", encoding="utf-8").write(s + "\n")
open(os.path.join(HERE, "wix", "SEITEN.md"), "w", encoding="utf-8").write("\n".join(md))
print("ok")
