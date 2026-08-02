from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent


def main():
    files = [
        path
        for path in ROOT.glob("**/index.html")
        if "gh-pages-build" not in path.parts
    ]
    missing = []
    modern_markers = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http", "#", "mailto:")) or href == "":
                continue
            target = (path.parent / href.split("#")[0]).resolve()
            if not target.exists():
                missing.append((str(path.relative_to(ROOT)), href))
        for marker in ["app-header", "side-panel", "kpi-grid"]:
            if marker in text:
                modern_markers += 1
    print(f"html_files={len(files)}")
    print(f"missing_links={missing}")
    print(f"modern_markers={modern_markers}")


if __name__ == "__main__":
    main()
