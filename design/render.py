"""Re-render the profile images with headless Chrome: python design/render.py (from the repo root)."""
import pathlib
import subprocess

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = pathlib.Path(__file__).resolve().parent.parent
DESIGN, ASSETS = ROOT / "design", ROOT / "assets"
HEADERS = {"projects": "Featured projects", "tech": "Tech", "contact": "Contact"}

jobs = []
for theme in ("light", "dark"):
    jobs.append(("banner.html", "1280,360", f"banner-{theme}.png", f"theme={theme}", False))
    for key, title in HEADERS.items():
        jobs.append(("elements.html", "1000,70", f"h-{key}-{theme}.png",
                     f"kind=header&theme={theme}&title={title.replace(' ', '%20')}", True))

for i, (page, size, out, query, transparent) in enumerate(jobs):
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={size}",
            "--force-device-scale-factor=2", "--virtual-time-budget=8000",
            # A fresh profile per shot: reusing one makes Chrome hand off to the previous process and skip the shot.
            f"--user-data-dir={ROOT / '.chrome' / str(i)}",
            f"--screenshot={ASSETS / out}", f"{(DESIGN / page).as_uri()}?{query}"]
    if transparent:
        args.insert(4, "--default-background-color=00000000")
    result = subprocess.run(args, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    print(out, "ok" if "bytes written" in result.stderr + result.stdout else "FAILED")
