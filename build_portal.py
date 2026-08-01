from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
DASHBOARD = ROOT / "dashboard_zoit_pa_v1.html"

COMMUNES = [
    {
        "slug": "san-jose-de-maipo",
        "name": "San Jose de Maipo",
        "status": "Dashboard disponible",
        "description": "Monitoreo del Plan de Accion ZOIT Cajon del Maipo desde la hoja PA-V1.",
        "dashboard": True,
    },
    {
        "slug": "pirque",
        "name": "Pirque",
        "status": "Sitio preparado",
        "description": "Espacio listo para incorporar dashboard, mesa publico privada, actas y sugerencias.",
        "dashboard": False,
    },
    {
        "slug": "isla-de-maipo",
        "name": "Isla de Maipo",
        "status": "Sitio preparado",
        "description": "Espacio listo para incorporar dashboard, mesa publico privada, actas y sugerencias.",
        "dashboard": False,
    },
]

SECTIONS = [
    ("dashboard", "Dashboard", "Seguimiento de acciones, estados, ejecutores, trimestres y presupuesto."),
    ("mesa-publico-privada", "Mesa publico privada", "Integrantes, instituciones participantes y roles de coordinacion."),
    ("actas-publicaciones", "Actas y publicaciones", "Actas, reportes, documentos y publicaciones relevantes del proceso."),
    ("sugerencias", "Sugerencias", "Canal para recibir ideas, observaciones y propuestas ciudadanas."),
]


STYLE = """
    :root {
      --bg: #f4f6f1;
      --ink: #17211b;
      --muted: #63736a;
      --panel: #ffffff;
      --line: #dce3da;
      --green: #1f6f55;
      --green-dark: #163b31;
      --gold: #d6a64b;
      --blue: #315f89;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: var(--bg);
    }
    header {
      background: var(--green-dark);
      color: #fff;
      padding: 28px;
      border-bottom: 5px solid var(--gold);
    }
    header a { color: #f7e1aa; text-decoration: none; }
    .eyebrow {
      margin: 0 0 8px;
      color: #c8ddd3;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    h1 {
      margin: 0;
      font-size: clamp(28px, 4vw, 46px);
      line-height: 1.05;
      letter-spacing: 0;
    }
    header p {
      margin: 12px 0 0;
      max-width: 900px;
      color: #e4eee8;
      line-height: 1.5;
      font-size: 16px;
    }
    main {
      max-width: 1180px;
      margin: 0 auto;
      padding: 24px;
    }
    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 18px;
    }
    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 38px;
      padding: 9px 13px;
      border: 1px solid var(--line);
      border-radius: 6px;
      color: var(--ink);
      background: #fff;
      text-decoration: none;
      font-weight: 700;
      font-size: 14px;
    }
    .button.primary {
      background: var(--green);
      color: #fff;
      border-color: var(--green);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }
    .section-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }
    .card {
      display: block;
      min-height: 190px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      text-decoration: none;
      color: var(--ink);
    }
    .card:hover {
      border-color: #91aa9d;
      box-shadow: 0 8px 24px rgba(22, 59, 49, .08);
    }
    .card h2, .card h3 {
      margin: 0 0 10px;
      font-size: 22px;
      letter-spacing: 0;
    }
    .card p {
      margin: 0;
      color: var(--muted);
      line-height: 1.45;
    }
    .pill {
      display: inline-block;
      margin-bottom: 16px;
      padding: 5px 9px;
      border-radius: 999px;
      background: #e8f1ec;
      color: #1c6047;
      font-size: 12px;
      font-weight: 700;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 16px;
    }
    .panel h2 {
      margin: 0 0 10px;
      font-size: 22px;
    }
    .panel p, li {
      color: var(--muted);
      line-height: 1.5;
    }
    .empty {
      border-left: 4px solid var(--gold);
    }
    footer {
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 24px 32px;
      color: var(--muted);
      font-size: 13px;
    }
    @media (max-width: 900px) {
      .grid, .section-grid { grid-template-columns: 1fr; }
      header, main, footer { padding-left: 16px; padding-right: 16px; }
      .card { min-height: auto; }
    }
"""


def rel_prefix(depth):
    return "../" * depth


def page(title, eyebrow, intro, body, depth=0):
    prefix = rel_prefix(depth)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{STYLE}</style>
</head>
<body>
  <header>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <p>{intro}</p>
  </header>
  <main>
    <nav class="toolbar">
      <a class="button" href="{prefix}index.html">Inicio</a>
      <a class="button" href="{prefix}san-jose-de-maipo/index.html">San Jose de Maipo</a>
      <a class="button" href="{prefix}pirque/index.html">Pirque</a>
      <a class="button" href="{prefix}isla-de-maipo/index.html">Isla de Maipo</a>
    </nav>
    {body}
  </main>
  <footer>Portal de seguimiento ZOIT. Version inicial para publicacion web.</footer>
</body>
</html>
"""


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_home():
    cards = "\n".join(
        f"""<a class="card" href="{commune['slug']}/index.html">
          <span class="pill">{commune['status']}</span>
          <h2>{commune['name']}</h2>
          <p>{commune['description']}</p>
        </a>"""
        for commune in COMMUNES
    )
    body = f"""
    <section class="panel">
      <h2>Seleccione un destino ZOIT</h2>
      <p>Este portal central organiza el monitoreo territorial, la gobernanza publico privada, las actas, publicaciones y canales de sugerencias para cada comuna.</p>
    </section>
    <section class="grid">{cards}</section>
"""
    write(
        ROOT / "index.html",
        page(
            "Portal ZOIT",
            "Monitoreo territorial",
            "Indice central para consultar dashboards, mesas publico privadas, actas, publicaciones y sugerencias de los destinos ZOIT.",
            body,
            depth=0,
        ),
    )


def build_commune(commune):
    links = "\n".join(
        f"""<a class="card" href="{slug}/index.html">
          <h3>{label}</h3>
          <p>{description}</p>
        </a>"""
        for slug, label, description in SECTIONS
    )
    body = f"""
    <section class="panel">
      <h2>{commune['name']}</h2>
      <p>{commune['description']}</p>
    </section>
    <section class="section-grid">{links}</section>
"""
    write(
        ROOT / commune["slug"] / "index.html",
        page(
            f"ZOIT {commune['name']}",
            "Destino ZOIT",
            "Seleccione una seccion para revisar el monitoreo, la gobernanza, documentos o sugerencias.",
            body,
            depth=1,
        ),
    )


def build_placeholder(commune, slug, label, description):
    body = f"""
    <section class="panel empty">
      <h2>{label}</h2>
      <p>{description}</p>
      <p>Esta seccion esta preparada para incorporar informacion oficial, listados, documentos, formularios o tableros especificos del destino.</p>
    </section>
    <section class="panel">
      <h2>Contenido sugerido</h2>
      <ul>
        <li>Responsables y fecha de ultima actualizacion.</li>
        <li>Documentos o enlaces oficiales asociados.</li>
        <li>Estado actual y proximos pasos.</li>
      </ul>
    </section>
"""
    write(
        ROOT / commune["slug"] / slug / "index.html",
        page(
            f"{label} - {commune['name']}",
            f"ZOIT {commune['name']}",
            description,
            body,
            depth=2,
        ),
    )


def build_dashboard(commune):
    target = ROOT / commune["slug"] / "dashboard" / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    if commune["dashboard"]:
        shutil.copy2(DASHBOARD, target)
        return
    build_placeholder(
        commune,
        "dashboard",
        "Dashboard",
        "Panel de monitoreo preparado para cargar acciones, indicadores, estados y responsables.",
    )


def main():
    build_home()
    for commune in COMMUNES:
        build_commune(commune)
        build_dashboard(commune)
        for slug, label, description in SECTIONS[1:]:
            build_placeholder(commune, slug, label, description)
    print("Portal creado")


if __name__ == "__main__":
    main()
