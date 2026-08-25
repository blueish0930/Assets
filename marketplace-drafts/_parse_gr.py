import json, html, re
from pathlib import Path
p = Path(r"E:\Assets\marketplace-drafts\browser-logs\gumroad-before.html")
text = p.read_text(encoding="utf-8", errors="replace")
m = re.search(r'data-page="([^"]+)"', text)
if not m:
    m = re.search(r"data-page='([^']+)'", text)
raw = html.unescape(m.group(1))
data = json.loads(raw)
print("component", data.get("component"))
props = data.get("props", {})
print("prop keys", list(props.keys()))
for k in ("logged_in_user", "product", "native_product_types", "flash"):
    v = props.get(k)
    if isinstance(v, dict):
        print(k, {kk: v[kk] for kk in list(v)[:12]})
    else:
        print(k, str(v)[:300])
