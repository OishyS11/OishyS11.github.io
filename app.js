// Build publications dynamically from publications.json (dev mode)
async function buildPubs() {
  const container = document.querySelector(".pubs");
  if (!container) return;
  try {
    const resp = await fetch("publications.json", {cache: "no-store"});
    if (!resp.ok) return; // compiled version won't fetch
    const pubs = await resp.json();
    container.innerHTML = pubs.map(renderPub).join("");
  } catch (e) {
    // Ignore in compiled version
  }
}

// Render a single pub item to HTML
function esc(s){return String(s).replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;");}
function renderAuthor(a){
  if(a.url) return `<a href="${esc(a.url)}" target="_blank" rel="noopener">${esc(a.name)}</a>`;
  return esc(a.name);
}
function renderLinks(links){
  return links.map(l=>{
    if (l.action === "toggle") {
      return `<a class="pub-btn" data-action="toggle" data-target="${esc(l.target)}" href="#">${esc(l.label)}</a>`;
    } else if (l.url) {
      return `<a class="pub-btn" href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a>`;
    }
    return "";
  }).join("");
}
function renderPub(p){
  const authors = (p.authors||[]).map(renderAuthor).join(", ");
  const absId = p.links?.find(x=>x.action==="toggle" && x.target.startsWith("abs-"))?.target || "";
  const bibId = p.links?.find(x=>x.action==="toggle" && x.target.startsWith("bib-"))?.target || "";
  return `
  <article class="pub-item" id="${esc(p.id)}">
    <div><span class="pub-badge ${esc(p.badge_class||"")}">${esc(p.badge_label||"")}</span></div>
    <div class="pub-main">
      <h3><a href="${esc(p.title_url||"#")}" target="_blank" rel="noopener">${esc(p.title)}</a></h3>
      <p class="pub-authors">${authors}</p>
      <div class="pub-venue">${esc(p.venue)}, ${esc(p.year)}</div>
      <div class="pub-actions">${renderLinks(p.links||[])}</div>
      ${absId ? `<div id="${esc(absId)}" class="pub-box hidden"><strong>Abstract.</strong><p>${esc(p.abstract||"")}</p></div>` : ""}
      ${bibId ? `<div id="${esc(bibId)}" class="pub-box hidden"><strong>BibTeX.</strong><pre id="bibtex-${esc(p.id)}" class="bib">${esc(p.bibtex||"")}</pre><div class="pub-copy"><a class="pub-btn" data-action="copy" data-target="bibtex-${esc(p.id)}" href="#">Copy</a></div></div>` : ""}
    </div>
  </article>`;
}

document.addEventListener('click', function(e){
  const a = e.target.closest('a.pub-btn');
  if(!a) return;
  const action = a.dataset.action, target = a.dataset.target;
  if(action === 'toggle'){
    e.preventDefault();
    const box = document.getElementById(target);
    if(box) box.classList.toggle('hidden');
  }
  if(action === 'copy'){
    e.preventDefault();
    const pre = document.getElementById(target);
    if(pre){
      navigator.clipboard.writeText(pre.textContent.trim()).then(()=>{
        a.textContent = 'Copied!'; setTimeout(()=>a.textContent='Copy', 1000);
      }).catch(()=>{ alert('Copy failed.'); });
    }
  }
});
document.addEventListener('DOMContentLoaded', buildPubs);
