import json
import os
import urllib.request
import html
import hashlib

USERNAME = "sahitikilaru"
TOKEN = os.environ["GITHUB_TOKEN"]

with open("projects.json", encoding="utf-8") as f:
    projects = json.load(f)["projects"]

def get_repo(path):
    url = f"https://api.github.com/repos/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    })
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def pixel_icon(name, x, y, color):
    digest = hashlib.sha256(name.encode()).digest()
    rects = []
    for row in range(8):
        for col in range(8):
            if digest[(row * 8 + col) % len(digest)] & 1:
                rects.append(
                    f'<rect x="{x+col*10}" y="{y+row*10}" '
                    f'width="10" height="10" fill="{color}"/>'
                )
    return "".join(rects)

colors = ["#f04b2b", "#f4df54", "#f4df54", "#f4df54"]

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'width="920" height="370" viewBox="0 0 920 370">',
    '<rect width="920" height="370" fill="#0d1117"/>',
    '<style>'
    '.heading{font:bold 27px monospace;fill:#3fb950}'
    '.name{font:bold 15px monospace;fill:#e6edf3}'
    '.desc{font:13px Arial;fill:#8b949e}'
    '.meta{font:12px monospace;fill:#8b949e}'
    '.star{font:15px monospace;fill:#3fb950}'
    '</style>',
    '<text x="0" y="31" class="heading">› PROJECTS</text>',
    '<path d="M190 20 H920" stroke="#30363d" '
    'stroke-dasharray="5 6"/>'
]

for i, path in enumerate(projects):
    repo = get_repo(path)

    col = i % 2
    row = i // 2

    x = col * 464
    y = 52 + row * 160

    name = html.escape(repo["name"])
    desc = html.escape(
        repo.get("description") or "A project in progress."
    )
    language = html.escape(repo.get("language") or "Other")
    stars = repo["stargazers_count"]
    url = html.escape(repo["html_url"], quote=True)

    color = colors[i % len(colors)]

    svg.append(f'''
    <a href="{url}">
      <rect x="{x}" y="{y}" width="450" height="148"
        rx="13" fill="#161b22" stroke="#30363d"/>

      <rect x="{x+14}" y="{y+33}" width="100" height="100"
        rx="9" fill="{color}" opacity=".35"/>

      {pixel_icon(name, x+24, y+43, color)}

      <text x="{x+132}" y="{y+43}" class="name">{name}</text>
      <text x="{x+132}" y="{y+68}" class="desc">{desc[:43]}</text>

      <text x="{x+132}" y="{y+119}" class="star">
        ★ {stars}
      </text>

      <text x="{x+350}" y="{y+119}" class="meta">
        {language[:13]}
      </text>
    </a>
    ''')

svg.append("</svg>")

os.makedirs("assets", exist_ok=True)

with open("assets/projects.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print("Project cards updated successfully!")
