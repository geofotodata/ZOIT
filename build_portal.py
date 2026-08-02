from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
DASHBOARD = ROOT / "dashboard_zoit_pa_v1.html"

COMMUNES = [
    {
        "slug": "san-jose-de-maipo",
        "name": "San Jose de Maipo",
        "status": "Dashboard disponible",
        "description": "Destino cordillerano orientado a naturaleza, aventura, patrimonio local y desarrollo turistico sustentable.",
        "plan": "Plan de Accion ZOIT San Jose de Maipo, octubre 2025.",
        "vision": "Al 2030 busca convertirse en referente turistico de los Andes Centrales, reconocido nacional e internacionalmente por su condicion cordillerana, oferta de actividades y servicios turisticos sustentables.",
        "focus": "Montana, senderismo, escalada, rafting, observacion de aves, cabalgatas, termas, embalses, patrimonio ferroviario y localidades cordilleranas.",
        "attractions": [
            "Parque y Monumento Natural El Morado",
            "Embalse El Yeso",
            "Volcan Tupungato",
            "Mirador de Condores",
            "Banos Morales y Termas Valle de Colina",
            "Casco historico de San Jose de Maipo",
        ],
        "governance": "El plan es gestionado, monitoreado e implementado por la Mesa Publico Privada de la ZOIT, con reglamento propio y gobernanza territorial.",
        "kpis": ["50 acciones ZOIT", "6 lineas operativas", "16 trimestres", "Dashboard activo"],
        "dashboard": True,
    },
    {
        "slug": "pirque",
        "name": "Pirque",
        "status": "Sitio preparado",
        "description": "Destino asociado al enoturismo, turismo de intereses especiales, naturaleza, cultura local y gastronomia.",
        "plan": "Plan de Accion ZOIT Pirque, septiembre 2025.",
        "vision": "Pirque sera al 2029 un destino turistico sustentable e innovador, reconocido como icono del enoturismo y el turismo de intereses especiales.",
        "focus": "Vinas, bodegas, turismo rural, Parque Nacional Rio Clarillo, gastronomia, artesania, patrimonio local y rutas de experiencias.",
        "attractions": [
            "Vinas Concha y Toro, El Principal, Haras de Pirque, Alyan, Santa Alicia, William Fevre y Apaltagua",
            "Parque Nacional Rio Clarillo",
            "Pueblito de artesanos",
            "Casas patrimoniales y parroquia historica",
            "Fiestas costumbristas",
        ],
        "governance": "El plan se implementa mediante Mesa Publico Privada, gobernanza territorial, nivel tecnico y coordinacion ejecutiva.",
        "kpis": ["Plan 2025", "5 lineas estrategicas", "Enoturismo", "Sitio preparado"],
        "dashboard": False,
    },
    {
        "slug": "isla-de-maipo",
        "name": "Isla de Maipo",
        "status": "Sitio preparado",
        "description": "Destino rural y vitivinicola con patrimonio cultural, actividades al aire libre, festividades y paisaje agricola.",
        "plan": "Plan de Accion ZOIT Isla de Maipo, septiembre 2025.",
        "vision": "Al 2030 sera reconocida como referente regional, nacional e internacional en turismo rural, enoturismo, deporte y patrimonio cultural, con desarrollo sostenible e identidad local.",
        "focus": "Enoturismo, turismo rural, cicloturismo, patrimonio religioso y cultural, fiestas tradicionales, naturaleza y borde del Rio Maipo.",
        "attractions": [
            "Humedal",
            "Rio Maipo",
            "Cerros de Naltagua",
            "Fiesta de la Vendimia",
            "Fiesta de la Virgen de la Merced",
            "Casco historico y rutas del vino",
        ],
        "governance": "El plan considera gestion participativa entre comunidad, sector publico y privado mediante Mesa Publico Privada y reglamento de funcionamiento.",
        "kpis": ["Plan 2025", "5 lineas estrategicas", "Turismo rural", "Sitio preparado"],
        "dashboard": False,
    },
]

LINES = [
    "Equipamiento e infraestructura",
    "Promocion",
    "Sustentabilidad",
    "Desarrollo de productos y experiencias",
    "Capital humano",
]

SECTIONS = [
    ("dashboard", "Dashboard", "Seguimiento de acciones, estados, ejecutores, trimestres y presupuesto.", "dashboard"),
    ("mesa-publico-privada", "Mesa publico privada", "Integrantes, instituciones participantes y roles de coordinacion.", "groups"),
    ("actas-publicaciones", "Actas y publicaciones", "Actas, reportes, documentos y publicaciones relevantes del proceso.", "article"),
    ("sugerencias", "Sugerencias", "Canal para recibir ideas, observaciones y propuestas ciudadanas.", "rate_review"),
]


STYLE = """
    :root {
      --bg: #f6f9fc;
      --ink: #17212b;
      --muted: #5f6f7b;
      --panel: #ffffff;
      --line: #d9e3ea;
      --primary: #005A9C;
      --secondary: #0099CC;
      --success: #2E7D32;
      --warning: #F9A825;
      --error: #C62828;
      --shadow: 0 10px 28px rgba(22, 45, 70, .08);
      --radius: 12px;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      font-family: Inter, Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: var(--bg);
    }
    a { color: inherit; }
    a:focus-visible, button:focus-visible, input:focus-visible {
      outline: 3px solid rgba(0, 153, 204, .45);
      outline-offset: 2px;
    }
    .app-header {
      position: sticky;
      top: 0;
      z-index: 20;
      display: grid;
      grid-template-columns: auto minmax(180px, 1fr) minmax(220px, 460px) auto;
      gap: 14px;
      align-items: center;
      min-height: 72px;
      padding: 12px 24px;
      background: rgba(255, 255, 255, .96);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(12px);
    }
    .brand-mark {
      display: grid;
      place-items: center;
      width: 44px;
      height: 44px;
      border-radius: 12px;
      color: #fff;
      background: var(--primary);
      font-weight: 800;
    }
    .brand-title strong {
      display: block;
      font-size: 17px;
    }
    .brand-title span {
      display: block;
      font-size: 13px;
      color: var(--muted);
      margin-top: 2px;
    }
    .search {
      position: relative;
    }
    .search .material-symbols-outlined {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--muted);
      font-size: 21px;
    }
    .search input {
      width: 100%;
      min-height: 44px;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 10px 14px 10px 42px;
      background: #f9fbfd;
      color: var(--ink);
      font: inherit;
    }
    .header-actions {
      display: flex;
      gap: 8px;
      justify-content: flex-end;
    }
    .icon-button {
      display: inline-grid;
      place-items: center;
      width: 42px;
      height: 42px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: #fff;
      color: var(--primary);
      text-decoration: none;
    }
    .layout {
      display: grid;
      grid-template-columns: 248px minmax(0, 1fr);
      gap: 20px;
      max-width: 1440px;
      margin: 0 auto;
      padding: 20px;
    }
    .side-panel {
      position: sticky;
      top: 92px;
      align-self: start;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 10px;
    }
    .side-panel a {
      display: flex;
      align-items: center;
      gap: 10px;
      min-height: 42px;
      padding: 9px 10px;
      border-radius: 10px;
      color: var(--ink);
      text-decoration: none;
      font-weight: 700;
      font-size: 14px;
    }
    .side-panel a:hover {
      background: #eef7fb;
      color: var(--primary);
    }
    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(300px, .85fr);
      gap: 18px;
      align-items: stretch;
      margin-bottom: 18px;
    }
    .hero-copy {
      min-height: 310px;
      border-radius: var(--radius);
      padding: 32px;
      color: #fff;
      background: #073e67;
      box-shadow: var(--shadow);
    }
    .eyebrow {
      margin: 0 0 10px;
      color: #cceeff;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    h1 {
      margin: 0;
      font-size: clamp(32px, 5vw, 56px);
      line-height: 1.05;
      letter-spacing: 0;
    }
    .hero-copy p {
      margin: 12px 0 0;
      max-width: 900px;
      color: #e3f5ff;
      line-height: 1.5;
      font-size: 16px;
    }
    .map-preview {
      position: relative;
      overflow: hidden;
      min-height: 310px;
      border-radius: var(--radius);
      background:
        linear-gradient(90deg, rgba(0,90,156,.12) 1px, transparent 1px),
        linear-gradient(rgba(0,90,156,.12) 1px, transparent 1px),
        #edf7fb;
      background-size: 36px 36px;
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
    }
    .map-preview::before,
    .map-preview::after {
      content: "";
      position: absolute;
      border-radius: 999px;
      background: rgba(0, 153, 204, .22);
    }
    .map-preview::before {
      width: 250px;
      height: 250px;
      right: -70px;
      top: -50px;
    }
    .map-preview::after {
      width: 190px;
      height: 190px;
      left: -60px;
      bottom: -40px;
      background: rgba(46, 125, 50, .18);
    }
    .map-toolbar {
      position: absolute;
      right: 14px;
      top: 14px;
      display: grid;
      gap: 8px;
      z-index: 1;
    }
    .map-control {
      display: grid;
      place-items: center;
      width: 40px;
      height: 40px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: #fff;
      color: var(--primary);
      box-shadow: 0 4px 14px rgba(22, 45, 70, .08);
    }
    .map-card {
      position: absolute;
      left: 18px;
      right: 76px;
      bottom: 18px;
      z-index: 1;
      padding: 16px;
      background: rgba(255, 255, 255, .94);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }
    .map-card strong { display: block; margin-bottom: 4px; }
    .map-card span { color: var(--muted); font-size: 14px; line-height: 1.4; }
    main {
      min-width: 0;
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
      border-radius: 12px;
      color: var(--ink);
      background: #fff;
      text-decoration: none;
      font-weight: 700;
      font-size: 14px;
    }
    .button.primary {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }
    .kpi {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 16px;
      box-shadow: var(--shadow);
    }
    .kpi span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .kpi strong {
      display: block;
      margin-top: 7px;
      font-size: 20px;
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
    .info-grid {
      display: grid;
      grid-template-columns: 1.2fr .8fr;
      gap: 14px;
      align-items: start;
    }
    .detail-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 16px;
    }
    .card {
      display: block;
      min-height: 190px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 18px;
      text-decoration: none;
      color: var(--ink);
      box-shadow: 0 4px 18px rgba(22, 45, 70, .05);
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }
    .card:hover {
      transform: translateY(-2px);
      border-color: rgba(0, 90, 156, .35);
      box-shadow: var(--shadow);
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
      background: #e6f5fb;
      color: var(--primary);
      font-size: 12px;
      font-weight: 700;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: 0 4px 18px rgba(22, 45, 70, .05);
    }
    .panel h2 {
      margin: 0 0 10px;
      font-size: 22px;
    }
    .panel h3 {
      margin: 0 0 8px;
      font-size: 17px;
    }
    .panel p, li {
      color: var(--muted);
      line-height: 1.5;
    }
    .list {
      margin: 8px 0 0;
      padding-left: 18px;
    }
    .empty {
      border-left: 4px solid var(--warning);
    }
    .icon-heading {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .material-symbols-outlined {
      font-family: 'Material Symbols Outlined';
      font-weight: normal;
      font-style: normal;
      font-size: 24px;
      line-height: 1;
      letter-spacing: normal;
      text-transform: none;
      display: inline-block;
      white-space: nowrap;
      word-wrap: normal;
      direction: ltr;
      -webkit-font-feature-settings: 'liga';
      -webkit-font-smoothing: antialiased;
    }
    footer {
      max-width: 1440px;
      margin: 0 auto;
      padding: 0 20px 32px;
      color: var(--muted);
      font-size: 13px;
    }
    .bottom-nav {
      display: none;
    }
    @media (max-width: 900px) {
      .app-header {
        grid-template-columns: auto 1fr auto;
        padding: 10px 14px;
      }
      .search { grid-column: 1 / -1; }
      .header-actions .optional { display: none; }
      .layout { grid-template-columns: 1fr; padding: 12px; }
      .side-panel { display: none; }
      .hero, .grid, .section-grid, .info-grid, .detail-grid, .kpi-grid { grid-template-columns: 1fr; }
      .hero-copy { min-height: auto; padding: 24px; }
      .card { min-height: auto; }
      .bottom-nav {
        position: sticky;
        bottom: 0;
        z-index: 18;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        padding: 8px;
        background: rgba(255,255,255,.96);
        border-top: 1px solid var(--line);
        backdrop-filter: blur(12px);
      }
      .bottom-nav a {
        display: grid;
        place-items: center;
        gap: 2px;
        min-height: 50px;
        color: var(--primary);
        text-decoration: none;
        font-size: 11px;
        font-weight: 800;
      }
    }
"""


def rel_prefix(depth):
    return "../" * depth


def side_links(prefix):
    links = [
        ("Destino", "travel_explore", f"{prefix}index.html"),
        ("Atractivos", "landscape", "#atractivos"),
        ("Servicios", "room_service", "#servicios"),
        ("Infraestructura", "hub", "#indicadores"),
        ("Capas", "layers", "#capas"),
        ("Documentos", "folder_open", "#documentos"),
        ("Indicadores", "monitoring", "#indicadores"),
        ("Configuracion", "settings", "#configuracion"),
    ]
    return "\n".join(
        f"""<a href="{href}" aria-label="{label}">
          <span class="material-symbols-outlined" aria-hidden="true">{icon}</span>
          <span>{label}</span>
        </a>"""
        for label, icon, href in links
    )


def header_actions():
    return """
      <a class="icon-button optional" href="#" aria-label="Compartir">
        <span class="material-symbols-outlined" aria-hidden="true">share</span>
      </a>
      <a class="icon-button optional" href="#" aria-label="Pantalla completa">
        <span class="material-symbols-outlined" aria-hidden="true">fullscreen</span>
      </a>
      <a class="icon-button optional" href="#configuracion" aria-label="Configuracion">
        <span class="material-symbols-outlined" aria-hidden="true">settings</span>
      </a>
      <a class="icon-button" href="#ayuda" aria-label="Ayuda">
        <span class="material-symbols-outlined" aria-hidden="true">help</span>
      </a>
"""


def bottom_nav(prefix):
    return f"""
  <nav class="bottom-nav" aria-label="Navegacion movil">
    <a href="{prefix}index.html"><span class="material-symbols-outlined" aria-hidden="true">home</span>Inicio</a>
    <a href="#indicadores"><span class="material-symbols-outlined" aria-hidden="true">monitoring</span>Datos</a>
    <a href="#capas"><span class="material-symbols-outlined" aria-hidden="true">layers</span>Capas</a>
    <a href="#ayuda"><span class="material-symbols-outlined" aria-hidden="true">help</span>Ayuda</a>
  </nav>
"""


def map_preview(title):
    return f"""
      <aside class="map-preview" aria-label="Vista cartografica referencial">
        <div class="map-toolbar" aria-label="Herramientas del mapa">
          <span class="map-control material-symbols-outlined" title="Mi ubicacion">my_location</span>
          <span class="map-control material-symbols-outlined" title="Mapa base">map</span>
          <span class="map-control material-symbols-outlined" title="Medicion">straighten</span>
          <span class="map-control material-symbols-outlined" title="Compartir ubicacion">ios_share</span>
        </div>
        <div class="map-card">
          <strong>{title}</strong>
          <span>Area de exploracion territorial preparada para integrar capas, atractivos, servicios, indicadores y documentos.</span>
        </div>
      </aside>
"""


def page(title, eyebrow, intro, body, depth=0):
    prefix = rel_prefix(depth)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
  <style>{STYLE}</style>
</head>
<body>
  <header class="app-header">
    <a class="brand-mark" href="{prefix}index.html" aria-label="Inicio Portal ZOIT">Z</a>
    <div class="brand-title">
      <strong>{title}</strong>
      <span>{eyebrow}</span>
    </div>
    <label class="search" aria-label="Buscar en el geoportal">
      <span class="material-symbols-outlined" aria-hidden="true">search</span>
      <input type="search" placeholder="Buscar destino, atractivo, servicio o documento">
    </label>
    <nav class="header-actions" aria-label="Acciones rapidas">
      {header_actions()}
    </nav>
  </header>
  <div class="layout">
    <aside class="side-panel" aria-label="Categorias del geoportal">
      {side_links(prefix)}
    </aside>
    <main>
      <section class="hero">
        <div class="hero-copy">
          <p class="eyebrow">{eyebrow}</p>
          <h1>{title}</h1>
          <p>{intro}</p>
          <div class="toolbar">
            <a class="button primary" href="{prefix}san-jose-de-maipo/index.html">Explorar destinos</a>
            <a class="button" href="#indicadores">Ver indicadores</a>
            <a class="button" href="#documentos">Documentos</a>
          </div>
        </div>
        {map_preview(title)}
      </section>
      {body}
    </main>
  </div>
  <footer>Portal de seguimiento ZOIT. Version inicial para publicacion web.</footer>
  {bottom_nav(prefix)}
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
          <p><strong>Vision:</strong> {commune['vision']}</p>
        </a>"""
        for commune in COMMUNES
    )
    lines = "".join(f"<li>{line}</li>" for line in LINES)
    kpis = [
        ("Destinos ZOIT", "3"),
        ("Lineas comunes", "5"),
        ("Accesos por destino", "4"),
        ("Dashboard activo", "1"),
    ]
    kpi_cards = "".join(f"""<div class="kpi"><span>{label}</span><strong>{value}</strong></div>""" for label, value in kpis)
    body = f"""
    <section class="kpi-grid" id="indicadores">{kpi_cards}</section>
    <section class="panel" id="atractivos">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">travel_explore</span>Seleccione un destino ZOIT</h2>
      <p>Este portal central organiza la informacion base de tres Zonas de Interes Turistico y permite ingresar a sus dashboards, mesas publico privadas, actas, publicaciones y canales de sugerencias.</p>
    </section>
    <section class="info-grid">
      <div class="panel" id="servicios">
        <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">dashboard</span>Que se monitorea</h2>
        <p>Cada plan de accion funciona como carta de navegacion para cuatro anos de gestion, con compromisos, brechas, indicadores, responsables y medios de verificacion.</p>
      </div>
      <div class="panel" id="capas">
        <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">layers</span>Lineas estrategicas comunes</h2>
        <ul class="list">{lines}</ul>
      </div>
    </section>
    <section class="grid">{cards}</section>
    <section class="panel" id="documentos">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">folder_open</span>Documentos y publicaciones</h2>
      <p>Los planes de accion se mantienen como fuente local de trabajo. En una segunda etapa se pueden publicar versiones oficiales, actas, resoluciones y verificadores por destino.</p>
    </section>
    <section class="panel" id="configuracion">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">settings</span>Configuracion del geoportal</h2>
      <p>La interfaz queda preparada para selector de mapa base, capas, busqueda avanzada, accesibilidad y herramientas de medicion.</p>
    </section>
    <section class="panel" id="ayuda">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">help</span>Ayuda</h2>
      <p>Use el buscador superior para ubicar destinos o ingrese a cada comuna para revisar dashboard, gobernanza, actas y sugerencias.</p>
    </section>
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
          <span class="material-symbols-outlined" aria-hidden="true">{icon}</span>
          <h3>{label}</h3>
          <p>{description}</p>
        </a>"""
        for slug, label, description, icon in SECTIONS
    )
    attraction_items = "".join(f"<li>{item}</li>" for item in commune["attractions"])
    line_items = "".join(f"<li>{line}</li>" for line in LINES)
    kpi_cards = "".join(f"""<div class="kpi"><span>{commune['name']}</span><strong>{item}</strong></div>""" for item in commune["kpis"])
    body = f"""
    <section class="kpi-grid" id="indicadores">{kpi_cards}</section>
    <section class="info-grid">
      <div class="panel">
        <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">travel_explore</span>Descripcion de la ZOIT</h2>
        <p>{commune['description']}</p>
        <p><strong>Vision:</strong> {commune['vision']}</p>
        <p><strong>Foco turistico:</strong> {commune['focus']}</p>
      </div>
      <div class="panel" id="documentos">
        <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">article</span>Plan de accion</h2>
        <p>{commune['plan']}</p>
        <p>{commune['governance']}</p>
      </div>
    </section>
    <section class="detail-grid">
      <div class="panel" id="atractivos">
        <h3 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">landscape</span>Atractivos y recursos</h3>
        <ul class="list">{attraction_items}</ul>
      </div>
      <div class="panel" id="capas">
        <h3 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">layers</span>Lineas de accion</h3>
        <ul class="list">{line_items}</ul>
      </div>
      <div class="panel" id="servicios">
        <h3 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">apps</span>Accesos del sitio</h3>
        <p>Ingrese a la seccion correspondiente para revisar seguimiento, integrantes, documentos o sugerencias.</p>
      </div>
    </section>
    <section class="section-grid">{links}</section>
    <section class="panel" id="configuracion">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">settings</span>Herramientas preparadas</h2>
      <p>La pagina queda lista para incorporar selector de mapa base, capas turisticas, medicion, compartir ubicacion, coordenadas y busqueda inteligente.</p>
    </section>
    <section class="panel" id="ayuda">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">help</span>Ayuda</h2>
      <p>Use los accesos de esta pagina para revisar dashboard, mesa publico privada, actas, publicaciones y sugerencias de {commune['name']}.</p>
    </section>
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
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">info</span>{label}</h2>
      <p>{description}</p>
      <p>Esta seccion esta preparada para incorporar informacion oficial, listados, documentos, formularios o tableros especificos del destino.</p>
    </section>
    <section class="panel">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">checklist</span>Contenido sugerido</h2>
      <ul>
        <li>Responsables y fecha de ultima actualizacion.</li>
        <li>Documentos o enlaces oficiales asociados.</li>
        <li>Estado actual y proximos pasos.</li>
      </ul>
    </section>
    <section class="panel" id="capas">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">layers</span>Capas y datos asociados</h2>
      <p>Espacio preparado para agrupar informacion por Turismo, Naturaleza, Infraestructura, Seguridad, Patrimonio y Movilidad.</p>
    </section>
    <section class="panel" id="configuracion">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">settings</span>Configuracion</h2>
      <p>Se mantiene compatibilidad con la estructura estatica actual y se deja preparada la integracion de formularios o visores especificos.</p>
    </section>
    <section class="panel" id="ayuda">
      <h2 class="icon-heading"><span class="material-symbols-outlined" aria-hidden="true">help</span>Ayuda</h2>
      <p>Vuelva al destino para navegar a otra seccion o al inicio para cambiar de ZOIT.</p>
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
        for slug, label, description, _icon in SECTIONS[1:]:
            build_placeholder(commune, slug, label, description)
    print("Portal creado")


if __name__ == "__main__":
    main()
