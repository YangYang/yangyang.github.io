# Yang Yang · 杨洋

Academic homepage at https://yangyang.ai/, based on the [Minimal Light](https://github.com/yaoyao-liu/minimal-light) static template.

## Update content

- `data/profile.json`: biography, education, funding, honors, and academic service.
- `data/publications.json`: paper titles, authors, venues, and verified links. Keep accepted papers explicitly marked as accepted.
- `scripts/homepage.html`: page structure.
- `assets/css/homepage.css`: personal styling and responsive adjustments.

Run `python3 scripts/build.py` after changing content. Preview with `python3 -m http.server 8765`, then open http://localhost:8765/.

Commit the generated `index.html` together with the data and asset changes. GitHub Pages serves the static files from `master`; `.nojekyll` disables unnecessary processing. Keep `CNAME` set to `yangyang.ai`.

The earlier blog URLs remain available for existing links. They are not part of the academic homepage navigation.

Minimal Light's CC0 license is retained in `assets/MINIMAL-LIGHT-LICENSE.txt`. The homepage does not include the template's sample content or analytics.
