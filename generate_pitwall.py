import os
import urllib.request
import json
import html
import re
import xml.etree.ElementTree as ET

USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER", "Joshua-Peter7")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def clean_xml_text(text, max_len=46):
    if not text:
        return ""
    # Strip all non-ASCII characters (emojis, smart quotes, bullets) that break GitHub SVG sanitizer
    text = re.sub(r'[^\x20-\x7E]', '', str(text)).strip()
    if len(text) > max_len:
        text = text[:max_len - 3].rstrip() + "..."
    return html.escape(text, quote=True)

url = f"https://api.github.com/users/{USERNAME}/repos?sort=created&direction=desc&per_page=15"
headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Scuderia-Pitwall-Bot"
}
if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    repos = json.loads(resp.read().decode("utf-8"))

projects = [
    r for r in repos
    if not r.get("fork") and r.get("name", "").lower() != USERNAME.lower()
][:4]

while len(projects) < 4:
    projects.append({
        "name": f"Telemetry-Node-{len(projects)+1}",
        "description": "Standby Scuderia Engineering Module",
        "language": "Python",
        "stargazers_count": 0
    })

sectors = [
    ("S1 // Latest", "Engine"),
    ("S2 // Recent", "Build"),
    ("S3 // Active", "Module"),
    ("S4 // Garage", "System")
]

rows_svg = []
for i, repo in enumerate(projects):
    y_top = 47 + (i * 59)
    y_line = y_top + 58
    row_bg = f'<rect x="3" y="{y_top}" width="894" height="58" fill="#ffffff" fill-opacity="0.05"/>' if i % 2 == 0 else ""
    divider = f'<line x1="3" y1="{y_line}" x2="897" y2="{y_line}" stroke="#FF2800" stroke-opacity="0.45" stroke-width="1"/>' if i < 3 else ""

    name = clean_xml_text(repo.get("name", "Project"), max_len=26) or "New-Repository"
    desc = clean_xml_text(repo.get("description") or "Active Scuderia Engineering Repository", max_len=46)
    lang = clean_xml_text(repo.get("language") or "AI / Code", max_len=16)
    stars = int(repo.get("stargazers_count", 0))
    tech_line = f"{lang}  |  Stars: {stars}  |  Auto-Synced"

    sec_l1, sec_l2 = sectors[i]

    rows_svg.append(f'''
    {row_bg}
    {divider}
    <text x="20" y="{y_top + 26}" fill="#FFB800" font-family="monospace" font-size="12.5" font-weight="bold">{sec_l1}</text>
    <text x="20" y="{y_top + 44}" fill="#FFB800" font-family="monospace" font-size="12.5" font-weight="bold">{sec_l2}</text>

    <text x="212" y="{y_top + 34}" fill="#ffffff" font-family="Arial, sans-serif" font-size="14" font-weight="bold">{name}</text>

    <text x="462" y="{y_top + 26}" fill="#ffe5e5" font-family="monospace" font-size="12">{desc}</text>
    <text x="462" y="{y_top + 44}" fill="#ffb3b3" font-family="monospace" font-size="11">{tech_line}</text>

    <rect x="782" y="{y_top + 17}" width="98" height="24" rx="12" fill="#1a0000" stroke="#00FF66" stroke-width="1"/>
    <circle cx="798" cy="{y_top + 29}" r="4.5" fill="#00FF66">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.4s" begin="{i * 0.3:.1f}s" repeatCount="indefinite"/>
    </circle>
    <text x="838" y="{y_top + 33}" text-anchor="middle" fill="#00FF66" font-family="monospace" font-size="11" font-weight="bold">LIVE</text>
    ''')

svg_output = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 285" width="900" height="285">
  <defs>
    <linearGradient id="ferrariRedBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4a0000"/>
      <stop offset="50%" stop-color="#800000"/>
      <stop offset="100%" stop-color="#380000"/>
    </linearGradient>
    <linearGradient id="headerCrimson" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#b30000"/>
      <stop offset="50%" stop-color="#DC0000"/>
      <stop offset="100%" stop-color="#990000"/>
    </linearGradient>
    <pattern id="redCarbon" width="8" height="8" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#000000" fill-opacity="0.12"/>
      <path d="M0 0h4v4H0zM4 4h4v4H4z" fill="#FF2800" fill-opacity="0.08"/>
    </pattern>
  </defs>

  <rect x="2" y="2" width="896" height="281" rx="10" fill="url(#ferrariRedBg)" stroke="#FF2800" stroke-width="2"/>
  <rect x="2" y="2" width="896" height="281" rx="10" fill="url(#redCarbon)"/>

  <path d="M 3 12 Q 3 3 12 3 L 888 3 Q 897 3 897 12 L 897 46 L 3 46 Z" fill="url(#headerCrimson)"/>
  <line x1="3" y1="46" x2="897" y2="46" stroke="#FFB800" stroke-width="1.5"/>

  <line x1="195" y1="3" x2="195" y2="282" stroke="#FF2800" stroke-opacity="0.45" stroke-width="1"/>
  <line x1="445" y1="3" x2="445" y2="282" stroke="#FF2800" stroke-opacity="0.45" stroke-width="1"/>
  <line x1="765" y1="3" x2="765" y2="282" stroke="#FF2800" stroke-opacity="0.45" stroke-width="1"/>

  <g font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#ffffff" letter-spacing="1.5">
    <text x="20" y="30">SECTOR</text>
    <text x="212" y="30">NEWEST REPOSITORY</text>
    <text x="462" y="30">DESCRIPTION & TELEMETRY</text>
    <text x="831" y="30" text-anchor="middle">STATUS</text>
  </g>

  {"".join(rows_svg)}
</svg>'''

# Validate strict XML syntax before writing
ET.fromstring(svg_output)

with open("pitwall-console.svg", "w", encoding="utf-8") as f:
    f.write(svg_output)

print("Successfully validated and generated pitwall-console.svg")
