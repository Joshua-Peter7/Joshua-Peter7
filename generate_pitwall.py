import os
import urllib.request
import json
import re
import xml.etree.ElementTree as ET

USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER", "Joshua-Peter7")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def clean_text(text, max_len=46):
    if not text:
        return ""
    text = re.sub(r'[^\x20-\x7E]', '', str(text)).strip()
    if len(text) > max_len:
        text = text[:max_len - 3].rstrip() + "..."
    return text

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

# Build SVG strictly via ElementTree (Zero possibility of invalid XML tokens)
svg = ET.Element("svg", {
    "xmlns": "http://www.w3.org/2000/svg",
    "viewBox": "0 0 900 285",
    "width": "900",
    "height": "285"
})

defs = ET.SubElement(svg, "defs")

bg_grad = ET.SubElement(defs, "linearGradient", {"id": "ferrariRedBg", "x1": "0%", "y1": "0%", "x2": "100%", "y2": "100%"})
ET.SubElement(bg_grad, "stop", {"offset": "0%", "stop-color": "#4a0000"})
ET.SubElement(bg_grad, "stop", {"offset": "50%", "stop-color": "#800000"})
ET.SubElement(bg_grad, "stop", {"offset": "100%", "stop-color": "#380000"})

hdr_grad = ET.SubElement(defs, "linearGradient", {"id": "headerCrimson", "x1": "0%", "y1": "0%", "x2": "100%", "y2": "0%"})
ET.SubElement(hdr_grad, "stop", {"offset": "0%", "stop-color": "#b30000"})
ET.SubElement(hdr_grad, "stop", {"offset": "50%", "stop-color": "#DC0000"})
ET.SubElement(hdr_grad, "stop", {"offset": "100%", "stop-color": "#990000"})

pattern = ET.SubElement(defs, "pattern", {"id": "redCarbon", "width": "8", "height": "8", "patternUnits": "userSpaceOnUse"})
ET.SubElement(pattern, "rect", {"width": "8", "height": "8", "fill": "#000000", "fill-opacity": "0.12"})
ET.SubElement(pattern, "path", {"d": "M0 0h4v4H0zM4 4h4v4H4z", "fill": "#FF2800", "fill-opacity": "0.08"})

# Main Red Card & Carbon Overlay
ET.SubElement(svg, "rect", {"x": "2", "y": "2", "width": "896", "height": "281", "rx": "10", "fill": "url(#ferrariRedBg)", "stroke": "#FF2800", "stroke-width": "2"})
ET.SubElement(svg, "rect", {"x": "2", "y": "2", "width": "896", "height": "281", "rx": "10", "fill": "url(#redCarbon)"})

# Header Bar
ET.SubElement(svg, "path", {"d": "M 3 12 Q 3 3 12 3 L 888 3 Q 897 3 897 12 L 897 46 L 3 46 Z", "fill": "url(#headerCrimson)"})
ET.SubElement(svg, "line", {"x1": "3", "y1": "46", "x2": "897", "y2": "46", "stroke": "#FFB800", "stroke-width": "1.5"})

# Column Dividers
for x_pos in ("195", "445", "765"):
    ET.SubElement(svg, "line", {"x1": x_pos, "y1": "3", "x2": x_pos, "y2": "282", "stroke": "#FF2800", "stroke-opacity": "0.45", "stroke-width": "1"})

# Header Text
hdr_group = ET.SubElement(svg, "g", {"font-family": "Arial, sans-serif", "font-size": "12", "font-weight": "bold", "fill": "#ffffff", "letter-spacing": "1.5"})
for x, label, anchor in [
    ("20", "SECTOR", "start"),
    ("212", "NEWEST REPOSITORY", "start"),
    ("462", "DESCRIPTION & TELEMETRY", "start"),
    ("831", "STATUS", "middle")
]:
    t = ET.SubElement(hdr_group, "text", {"x": x, "y": "30", "text-anchor": anchor})
    t.text = label

sectors = [
    ("S1 // Latest", "Engine"),
    ("S2 // Recent", "Build"),
    ("S3 // Active", "Module"),
    ("S4 // Garage", "System")
]

for i, repo in enumerate(projects):
    y_top = 47 + (i * 59)
    y_line = y_top + 58

    if i % 2 == 0:
        ET.SubElement(svg, "rect", {"x": "3", "y": str(y_top), "width": "894", "height": "58", "fill": "#ffffff", "fill-opacity": "0.05"})
    if i < 3:
        ET.SubElement(svg, "line", {"x1": "3", "y1": str(y_line), "x2": "897", "y2": str(y_line), "stroke": "#FF2800", "stroke-opacity": "0.45", "stroke-width": "1"})

    sec_l1, sec_l2 = sectors[i]
    t_s1 = ET.SubElement(svg, "text", {"x": "20", "y": str(y_top + 26), "fill": "#FFB800", "font-family": "monospace", "font-size": "12.5", "font-weight": "bold"})
    t_s1.text = sec_l1
    t_s2 = ET.SubElement(svg, "text", {"x": "20", "y": str(y_top + 44), "fill": "#FFB800", "font-family": "monospace", "font-size": "12.5", "font-weight": "bold"})
    t_s2.text = sec_l2

    name = clean_text(repo.get("name", "Project"), max_len=26) or "New-Repository"
    desc = clean_text(repo.get("description") or "Active Scuderia Engineering Repository", max_len=46)
    lang = clean_text(repo.get("language") or "AI / Code", max_len=16)
    stars = int(repo.get("stargazers_count", 0))

    t_name = ET.SubElement(svg, "text", {"x": "212", "y": str(y_top + 34), "fill": "#ffffff", "font-family": "Arial, sans-serif", "font-size": "14", "font-weight": "bold"})
    t_name.text = name

    t_desc = ET.SubElement(svg, "text", {"x": "462", "y": str(y_top + 26), "fill": "#ffe5e5", "font-family": "monospace", "font-size": "12"})
    t_desc.text = desc

    t_tech = ET.SubElement(svg, "text", {"x": "462", "y": str(y_top + 44), "fill": "#ffb3b3", "font-family": "monospace", "font-size": "11"})
    t_tech.text = f"{lang}  |  Stars: {stars}  |  Auto-Synced"

    ET.SubElement(svg, "rect", {"x": "782", "y": str(y_top + 17), "width": "98", "height": "24", "rx": "12", "fill": "#1a0000", "stroke": "#00FF66", "stroke-width": "1"})
    dot = ET.SubElement(svg, "circle", {"cx": "798", "cy": str(y_top + 29), "r": "4.5", "fill": "#00FF66"})
    ET.SubElement(dot, "animate", {"attributeName": "opacity", "values": "1;0.3;1", "dur": "1.4s", "begin": f"{i * 0.3:.1f}s", "repeatCount": "indefinite"})

    t_live = ET.SubElement(svg, "text", {"x": "838", "y": str(y_top + 33), "text-anchor": "middle", "fill": "#00FF66", "font-family": "monospace", "font-size": "11", "font-weight": "bold"})
    t_live.text = "LIVE"

tree = ET.ElementTree(svg)
ET.indent(tree, space="  ")
tree.write("pitwall-console.svg", encoding="utf-8", xml_declaration=True)
print("Successfully generated valid XML pitwall-console.svg")
