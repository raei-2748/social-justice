import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. hero gap 48px
text = re.sub(r'(\.hero-strip\{[^}]+?)gap:0;', r'\g<1>gap:48px;', text)

# 2. chart-wrap min-height and tog padding
text = re.sub(r'(\.chart-wrap\{[^}]*?height:)320px;', r'\g<1>320px;min-height:320px;', text)
text = re.sub(r'(\.tog\{padding:)7px 20px', r'\g<1>8px 20px', text)

# 3. growth story grid
text = re.sub(r'(\.main\{[^}]*?grid-template-columns:)1fr 380px', r'\g<1>1fr 300px', text)
if ".main > *" not in text:
    text = re.sub(r'(\.main\s*\{[^\}]+\})', r'\1\n.main > * { min-width: 0; }', text, count=1)

# 4. community portrait canvas min height 400px
text = re.sub(r'(#portraitCanvas\s*\{[^\}]*)(\})', r'\g<1>  min-height: 400px;\n\2', text)

# 5. follow the dollar
text = re.sub(r'(\.page-wrap\s*\{[^}]*?grid-template-columns:\s*)1fr 400px', r'\g<1>1fr 360px', text)
text = re.sub(r'(\.sticky-calc\s*\{[^}]*?top:\s*)64px([^}]*?height:\s*)calc\(100vh - 64px\)', r'\g<1>0\g<2>100vh', text)
if "@media (max-width: 1024px) {\n  .page-wrap { display: flex;" not in text:
    text = re.sub(r'(\.sticky-calc\s*\{[^\}]+\})', r'\1\n@media (max-width: 1024px) {\n  .page-wrap { display: flex; flex-direction: column; }\n  .sticky-calc { position: relative; height: auto; top: 0; }\n}', text, count=1)

# 6. charity radar eff-grid
if ".eff-grid > *" not in text:
    text = re.sub(r'(\.eff-grid\s*\{[^\}]+\})', r'\1\n.eff-grid > * { min-width: 0; }\n.eff-grid canvas { width: 100% !important; height: auto !important; }\n', text, count=1)

# 7. Replace 1280px with 1200px and 72px padding with 48px horizontal
text = re.sub(r'max-width:\s*1280px', 'max-width:1200px', text)
text = re.sub(r'max-width:1280px', 'max-width:1200px', text)

text = re.sub(r'(padding:\s*(?:\d+px|0)\s+)72px', r'\g<1>48px', text)
text = re.sub(r'padding-left:\s*72px', 'padding-left:48px', text)
text = re.sub(r'padding-right:\s*72px', 'padding-right:48px', text)
text = re.sub(r'(padding:\s*(?:\d+px|0)\s+)48px(\s+\d+px)', r'\g<1>48px\2', text)

# Wait, if there was padding: 80px 72px 48px, the first regex made it padding: 80px 48px 48px
# And in my old script I had a separate match. Let's make sure it handles generic 72px paddings safely:
text = text.replace(" 72px;", " 48px;")
text = text.replace(" 72px ", " 48px ")

# 8. Box sizing border-box grid children
if "box-sizing: border-box" not in ".main > *":
   text = text.replace('/* --- PRES STYLES --- */', '/* --- PRES STYLES --- */\n.main > *, .eff-grid > *, .hero-strip > *, .page-wrap > *, .tk-grid > * { box-sizing: border-box; }')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Done index.html updates.")
