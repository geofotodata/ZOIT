import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HTML = ROOT / "dashboard_zoit_pa_v1.html"
SERVER = ROOT / "dist" / "server" / "index.js"


def main():
    html = HTML.read_text(encoding="utf-8")
    SERVER.parent.mkdir(parents=True, exist_ok=True)
    SERVER.write_text(
        """
const html = __HTML__;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return new Response("ok", { status: 200 });
    }
    return new Response(html, {
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "public, max-age=300"
      }
    });
  }
};
""".replace("__HTML__", json.dumps(html)),
        encoding="utf-8",
    )
    print(f"Created {SERVER}")


if __name__ == "__main__":
    main()
