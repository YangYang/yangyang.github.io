#!/usr/bin/env python3
"""Build the static Minimal Light homepage using only Python's standard library."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
profile = json.loads((ROOT / 'data/profile.json').read_text())
papers = json.loads((ROOT / 'data/publications.json').read_text())

def esc(value):
    return html.escape(str(value), quote=True)

def link(url, text, css=''):
    if not url.startswith(('https://', 'http://', 'mailto:', '#')):
        raise ValueError(f'Unsupported link: {url}')
    return f'<a href="{esc(url)}"' + (f' class="{esc(css)}"' if css else '') + f'>{text}</a>'

def entries(items):
    return '\n'.join(f'<li><span class="entry-date">{esc(i["date"])}</span><div><h3>{esc(i["title"])}</h3><p>{esc(i["detail"])}</p></div></li>' for i in items)

def publication(p):
    authors = []
    for name in p['authors']:
        author = f'<strong>{esc(name)}</strong>' if name == profile['name'] else esc(name)
        if name in p.get('equal_contribution', []):
            author += '<sup>†</sup>'
        authors.append(author)
    title = link(p['url'], esc(p['title'])) if p.get('url') else esc(p['title'])
    links = ' '.join(link(u, esc(label), 'paper-link') for label, u in p.get('links', {}).items() if u)
    status = ' <span class="accepted">Accepted</span>' if p.get('status') == 'accepted' else ''
    return f'''<li class="publication"><div class="venue-label">{esc(p['short_venue'])}</div><div class="paper-body"><h3>{title}</h3><p class="authors">{', '.join(authors)}</p><p class="venue">{esc(p['venue'])}, {esc(p['year'])}.{status}</p><div class="paper-links">{links}</div></div></li>'''

groups = []
for year in sorted({p['year'] for p in papers}, reverse=True):
    rows = '\n'.join(publication(p) for p in papers if p['year'] == year)
    groups.append(f'<h3 class="year">{year}</h3><ol class="bibliography">{rows}</ol>')

social = [link('mailto:'+profile['email'], 'Email'), link(profile['github_url'], 'GitHub'), link(profile['faculty_url'], 'Faculty profile')]
if profile['scholar_url']:
    social.insert(0, link(profile['scholar_url'], 'Google Scholar'))
scholar_note = link(profile['scholar_url'], 'View Google Scholar') if profile['scholar_url'] else ''
values = {
    'name': esc(profile['name']), 'name_zh': esc(profile['name_zh']),
    'role': esc(profile['role']), 'department': esc(profile['department']),
    'university': esc(profile['university']), 'email': esc(profile['email']),
    'faculty_url': esc(profile['faculty_url']), 'updated': esc(profile['updated']),
    'social': '\n'.join(social),
    'about': '\n'.join(f'<p>{esc(p)}</p>' for p in profile['about']),
    'research': '\n'.join(f'<li><strong>{esc(t)}.</strong> {esc(d)}</li>' for t,d in profile['research']),
    'publications': '\n'.join(groups), 'scholar_note': scholar_note,
    'education': entries(profile['education']), 'funding': entries(profile['funding']),
    'awards': '\n'.join(f'<li><span class="award-date">{esc(y)}</span><span>{esc(t)}</span></li>' for y,t in profile['awards']),
    'service': '\n'.join(f'<li><strong>{esc(t)}.</strong> {esc(d)}</li>' for t,d in profile['service'])
}
page = (ROOT / 'scripts/homepage.html').read_text()
for name, value in values.items():
    page = page.replace('{{'+name+'}}', value)
if '{{' in page:
    raise ValueError('Unexpanded template field')
(ROOT / 'index.html').write_text(page)
print(f'Built homepage with {len(papers)} publications.')
