
import json, html, os

ROOT = os.path.dirname(__file__)

def load(path):
  with open(os.path.join(ROOT, path), "r", encoding="utf-8") as f:
    return f.read()

def esc(s):
  return html.escape(str(s), quote=True)

def render_author(a):
  name = esc(a.get("name",""))
  url = a.get("url")
  if url:
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{name}</a>'
  return name

def render_links(links, pub_id):
  items = []
  for l in links or []:
    label = esc(l.get("label",""))
    action = l.get("action")
    if action == "toggle":
      target = esc(l.get("target",""))
      items.append(f'<a class="pub-btn" data-action="toggle" data-target="{target}" href="#">{label}</a>')
    else:
      url = esc(l.get("url","#"))
      items.append(f'<a class="pub-btn" href="{url}" target="_blank" rel="noopener">{label}</a>')
  return "".join(items)

def render_pub(p):
  authors = ", ".join(render_author(a) for a in p.get("authors",[]))
  venue = esc(p.get("venue",""))
  year = esc(p.get("year",""))
  title = esc(p.get("title",""))
  title_url = esc(p.get("title_url","#"))
  badge_class = esc(p.get("badge_class",""))
  badge_label = esc(p.get("badge_label",""))
  pid = esc(p.get("id","pub-item"))
  links_html = render_links(p.get("links"), pid)

  # find ids used for ABS and BIB
  abs_target = ""
  bib_target = ""
  for l in p.get("links",[]):
    if l.get("action") == "toggle":
      t = l.get("target","")
      if t.startswith("abs-"): abs_target = t
      if t.startswith("bib-"): bib_target = t

  abs_html = f'<div id="{esc(abs_target)}" class="pub-box hidden"><strong>Abstract.</strong><p>{esc(p.get("abstract",""))}</p></div>' if abs_target else ""
  bib_id = f"bibtex-{pid}"
  bib_html = f'<div id="{esc(bib_target)}" class="pub-box hidden"><strong>BibTeX.</strong><pre id="{esc(bib_id)}" class="bib">{esc(p.get("bibtex",""))}</pre><div class="pub-copy"><a class="pub-btn" data-action="copy" data-target="{esc(bib_id)}" href="#">Copy</a></div></div>' if bib_target else ""

  return (
    f'<article class="pub-item" id="{pid}">'
    f'  <div><span class="pub-badge {badge_class}">{badge_label}</span></div>'
    f'  <div class="pub-main">'
    f'    <h3><a href="{title_url}" target="_blank" rel="noopener">{title}</a></h3>'
    f'    <p class="pub-authors">{authors}</p>'
    f'    <div class="pub-venue">{venue}, {year}</div>'
    f'    <div class="pub-actions">{links_html}</div>'
    f'    {abs_html}'
    f'    {bib_html}'
    f'  </div>'
    f'</article>'
  )

def main():
  css = load("style.css")
  app_js = load("app.js")
  tpl = load("index.template.html")
  pubs = json.loads(load("publications.json"))
  pubs_html = "\n".join(render_pub(p) for p in pubs)

  # Inline CSS
  out = tpl.replace("<!--INLINE_CSS-->", f"<style>\n{css}\n</style>")
  # Insert rendered pubs
  out = out.replace("<!--PUBLICATIONS_RENDERED-->", pubs_html)
  # Inline JS (replace the external script tag)
  out = out.replace('<script src="app.js"></script>', f"<script>\n{app_js}\n</script>")

  # Write compiled output
  with open(os.path.join(ROOT, "index.compiled.html"), "w", encoding="utf-8") as f:
    f.write(out)

if __name__ == "__main__":
  main()
