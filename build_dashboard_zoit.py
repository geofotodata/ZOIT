import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "SEGUIMIENTO PLAN DE ACCIÓN ZOIT CAJÓN DEL MAIPO.xlsx"
OUTPUT = ROOT / "dashboard_zoit_pa_v1.html"
SHEET = "PA-V1"

EXECUTOR_COLUMNS = [
    "Muni SJM",
    "MOP",
    "SERNATUR",
    "CONAF RM",
    "MINVU",
    "SEREMI BBNN",
    "SEREMI MA",
    "Andes Santiago",
    "SERCOTEC",
    "Fund. Deporte Libre",
    "Fundación Sendero de Chile",
    "Fundeso",
    "Cámara de Turismo",
    "Coorporación",
    "UTEM",
    "Consultora",
    "Organizaciones",
    "Aguas Andinas",
    "Sociedad civil",
    "Academia",
    "Guías  de turismo",
]

DOCUMENTS = [
    {
        "title": "Ley 20.423",
        "file": "Ley-20423_12-FEB-2010.pdf",
        "type": "Marco legal",
    },
    {
        "title": "Decreto 30 procedimiento ZOIT",
        "file": "02-decreto-30-que-fija-procedimiento-zoit.pdf",
        "type": "Procedimiento",
    },
    {
        "title": "Decreto ZOIT San José de Maipo 2025",
        "file": "decretos-d-o-zoit-san-jose-de-maipo-2025.pdf",
        "type": "Declaratoria",
    },
    {
        "title": "Plan de acción ZOIT SJDM",
        "file": "plan-de-accion-zoit-sjdm-2025-2-0-octubre3.pdf",
        "type": "Plan de acción",
    },
]


def clean_value(value):
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return value


def is_marked(value):
    text = str(clean_value(value)).strip().upper()
    return text == "X"


def classify_status(observation):
    text = str(observation or "").lower()
    if "acción ya realizada" in text or "accion ya realizada" in text:
        if "falta" in text:
            return "Realizada sin verificador"
        return "Realizada"
    if "en ejecución" in text or "en ejecucion" in text:
        return "En ejecución"
    if "ajustes a realizar" in text:
        return "Requiere ajuste"
    if "hacer reunion" in text or "hacer reunión" in text or "ver con" in text:
        return "Requiere gestión"
    if "trabajar de manera interna" in text:
        return "Gestión interna"
    if "recopilar verificadores" in text:
        return "Requiere verificador"
    if text.strip():
        return "Con observación"
    return "Sin observación"


def parse_trimester_number(value):
    text = str(value or "")
    digits = "".join(ch for ch in text if ch.isdigit())
    if not digits:
        return None
    return int(digits)


def budget_to_number(value):
    if isinstance(value, (int, float)) and not math.isnan(value):
        return float(value)
    return 0.0


def build_records():
    df = pd.read_excel(SOURCE, sheet_name=SHEET, header=1)
    df = df[df["N°"].notna()].copy()

    records = []
    for _, row in df.iterrows():
        years = [year for year in ["AÑO 1", "AÑO 2", "AÑO 3", "AÑO 4"] if is_marked(row.get(year))]
        executors = [name for name in EXECUTOR_COLUMNS if is_marked(row.get(name))]
        start_q = parse_trimester_number(row.get("Inicio"))
        end_q = parse_trimester_number(row.get("Fin"))
        if not executors and str(row.get("TODOS LOS EJECUTORES") or "").strip():
            executors = [str(row.get("TODOS LOS EJECUTORES")).strip()]

        record = {
            "id": int(row["N°"]),
            "action": str(row.get("ACCIÓN") or "").strip(),
            "line": str(row.get("LÍNEA DE ACCIÓN") or "").strip(),
            "objective": str(row.get("Objetivo (definido en Ficha de Solicitud)") or "").strip(),
            "gap": str(row.get("Brecha (definido en Ficha de Solicitud)") or "").strip(),
            "indicator": str(row.get("Indicador") or "").strip(),
            "goal": str(row.get("Meta (en función de indicador)") or "").strip(),
            "verifier": str(row.get("Verificador") or "").strip(),
            "budget": budget_to_number(row.get("Presupuesto total ")),
            "budgetLabel": str(clean_value(row.get("Presupuesto total "))).strip(),
            "funding": str(row.get("Fuente de Financiamiento propuesto") or "").strip(),
            "years": years,
            "startQ": start_q,
            "endQ": end_q,
            "executors": executors,
            "allExecutors": str(row.get("TODOS LOS EJECUTORES") or "").strip(),
            "observation": str(row.get("OBSERVACIONES 1109") or "").strip(),
        }
        record["status"] = classify_status(record["observation"])
        records.append(record)
    return records


def render_html(records):
    data = json.dumps(records, ensure_ascii=False)
    docs = json.dumps(DOCUMENTS, ensure_ascii=False)
    source_name = SOURCE.name
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dashboard ZOIT San José de Maipo - PA-V1</title>
  <style>
    :root {{
      --bg: #f6f7f2;
      --ink: #17211b;
      --muted: #5f6f66;
      --line: #dbe1d8;
      --panel: #ffffff;
      --green: #2f7d5b;
      --blue: #366b9f;
      --amber: #c8872d;
      --red: #b8554b;
      --teal: #15827a;
      --gray: #68736c;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: var(--bg);
    }}
    header {{
      padding: 24px 28px 18px;
      background: #18392f;
      color: white;
      border-bottom: 5px solid #d8a64a;
    }}
    h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: 0; }}
    header p {{ margin: 0; color: #dce9df; max-width: 980px; line-height: 1.45; }}
    main {{ padding: 22px 28px 40px; max-width: 1500px; margin: 0 auto; }}
    .filters {{
      display: grid;
      grid-template-columns: 2fr repeat(4, minmax(160px, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }}
    input, select {{
      width: 100%;
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px 10px;
      background: white;
      color: var(--ink);
      font-size: 14px;
    }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(5, minmax(150px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .kpi {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }}
    .kpi .label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; }}
    .kpi .value {{ font-size: 26px; font-weight: 700; margin-top: 6px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      align-items: start;
    }}
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 14px;
    }}
    h2 {{ font-size: 18px; margin: 0 0 14px; }}
    .bar-row {{
      display: grid;
      grid-template-columns: minmax(130px, 230px) 1fr 54px;
      gap: 10px;
      align-items: center;
      margin: 9px 0;
      font-size: 14px;
    }}
    .bar-label {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .bar-track {{ background: #edf1ec; border-radius: 4px; height: 15px; overflow: hidden; }}
    .bar-fill {{ height: 100%; background: var(--green); }}
    .status-pill {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 999px;
      background: #edf1ec;
      font-size: 12px;
      white-space: nowrap;
    }}
    .s-realizada-sin-verificador {{ background: #fff1cf; color: #765000; }}
    .s-en-ejecucion {{ background: #d9edff; color: #17476f; }}
    .s-requiere-ajuste {{ background: #ffe0dc; color: #82322b; }}
    .s-requiere-gestion {{ background: #e1f1ea; color: #1e6548; }}
    .s-gestion-interna {{ background: #e8e3f8; color: #493a7a; }}
    .s-con-observacion {{ background: #eeeeee; color: #414141; }}
    .table-wrap {{ overflow: auto; max-height: 620px; border: 1px solid var(--line); border-radius: 6px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; min-width: 1050px; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ position: sticky; top: 0; background: #eef3ed; z-index: 1; }}
    tr:hover td {{ background: #fafbf7; }}
    .gantt {{ overflow: auto; }}
    .gantt-table {{ min-width: 980px; }}
    .q {{ width: 24px; text-align: center; padding: 5px 2px; }}
    .cell-active {{ background: #4b906e; border-radius: 2px; height: 14px; display: block; }}
    .docs {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }}
    .doc {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      color: var(--ink);
      text-decoration: none;
      background: #fbfcfa;
    }}
    .doc strong {{ display: block; margin-bottom: 5px; }}
    .doc span {{ color: var(--muted); font-size: 13px; }}
    .note {{ color: var(--muted); font-size: 13px; margin-top: 8px; }}
    @media (max-width: 1000px) {{
      .filters, .kpis, .grid, .docs {{ grid-template-columns: 1fr; }}
      header, main {{ padding-left: 16px; padding-right: 16px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Dashboard Plan de Acción ZOIT San José de Maipo</h1>
    <p>Monitoreo construido desde la hoja <strong>PA-V1</strong> del archivo {source_name}. Permite revisar acciones, líneas de acción, programación anual, trimestres, ejecutores y observaciones operativas.</p>
  </header>
  <main>
    <div class="filters">
      <input id="search" type="search" placeholder="Buscar acción, indicador, ejecutor u observación">
      <select id="lineFilter"><option value="">Todas las líneas</option></select>
      <select id="statusFilter"><option value="">Todos los estados</option></select>
      <select id="yearFilter"><option value="">Todos los años</option></select>
      <select id="executorFilter"><option value="">Todos los ejecutores</option></select>
    </div>

    <div class="kpis" id="kpis"></div>

    <div class="grid">
      <section>
        <h2>Acciones por estado</h2>
        <div id="statusChart"></div>
      </section>
      <section>
        <h2>Acciones por línea</h2>
        <div id="lineChart"></div>
      </section>
      <section>
        <h2>Programación por año</h2>
        <div id="yearChart"></div>
      </section>
      <section>
        <h2>Presupuesto por línea</h2>
        <div id="budgetChart"></div>
      </section>
    </div>

    <section>
      <h2>Carta Gantt por trimestres</h2>
      <div class="gantt" id="gantt"></div>
    </section>

    <section>
      <h2>Tabla de acciones</h2>
      <div class="table-wrap" id="table"></div>
    </section>

    <section>
      <h2>Normativa y documentos base</h2>
      <div class="docs" id="docs"></div>
      <div class="note">Los enlaces abren archivos locales ubicados en la misma carpeta del dashboard.</div>
    </section>
  </main>

  <script>
    const DATA = {data};
    const DOCUMENTS = {docs};

    const money = new Intl.NumberFormat('es-CL', {{ style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }});
    const byId = id => document.getElementById(id);
    const slug = value => 's-' + value.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

    function unique(values) {{
      return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, 'es'));
    }}

    function addOptions(id, values) {{
      const select = byId(id);
      unique(values).forEach(value => {{
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
      }});
    }}

    function filtered() {{
      const q = byId('search').value.trim().toLowerCase();
      const line = byId('lineFilter').value;
      const status = byId('statusFilter').value;
      const year = byId('yearFilter').value;
      const executor = byId('executorFilter').value;

      return DATA.filter(item => {{
        const haystack = [item.action, item.line, item.indicator, item.goal, item.verifier, item.observation, item.allExecutors, item.executors.join(' ')].join(' ').toLowerCase();
        return (!q || haystack.includes(q)) &&
          (!line || item.line === line) &&
          (!status || item.status === status) &&
          (!year || item.years.includes(year)) &&
          (!executor || item.executors.includes(executor) || item.allExecutors.includes(executor));
      }});
    }}

    function countBy(items, getter) {{
      const counts = {{}};
      items.forEach(item => {{
        const values = [].concat(getter(item)).filter(Boolean);
        values.forEach(value => counts[value] = (counts[value] || 0) + 1);
      }});
      return counts;
    }}

    function budgetBy(items, getter) {{
      const counts = {{}};
      items.forEach(item => {{
        const key = getter(item) || 'Sin clasificar';
        counts[key] = (counts[key] || 0) + item.budget;
      }});
      return counts;
    }}

    function renderBars(id, counts, formatter = value => value) {{
      const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);
      const max = Math.max(1, ...entries.map(entry => entry[1]));
      byId(id).innerHTML = entries.map(([label, value]) => `
        <div class="bar-row" title="${{label}}">
          <div class="bar-label">${{label}}</div>
          <div class="bar-track"><div class="bar-fill" style="width:${{Math.max(3, value / max * 100)}}%"></div></div>
          <div>${{formatter(value)}}</div>
        </div>
      `).join('') || '<p class="note">Sin datos para los filtros seleccionados.</p>';
    }}

    function renderKpis(items) {{
      const totalBudget = items.reduce((sum, item) => sum + item.budget, 0);
      const withBudget = items.filter(item => item.budget > 0).length;
      const verifierPending = items.filter(item => item.status.includes('verificador')).length;
      const activeExecutors = unique(items.flatMap(item => item.executors)).length;
      byId('kpis').innerHTML = [
        ['Acciones', items.length],
        ['Presupuesto identificado', money.format(totalBudget)],
        ['Con presupuesto', withBudget],
        ['Pendientes de verificador', verifierPending],
        ['Ejecutores activos', activeExecutors],
      ].map(([label, value]) => `<div class="kpi"><div class="label">${{label}}</div><div class="value">${{value}}</div></div>`).join('');
    }}

    function renderGantt(items) {{
      const quarters = Array.from({{length: 16}}, (_, index) => index + 1);
      byId('gantt').innerHTML = `
        <table class="gantt-table">
          <thead><tr><th>N°</th><th>Acción</th>${{quarters.map(q => `<th class="q">T${{q}}</th>`).join('')}}</tr></thead>
          <tbody>
          ${{items.map(item => `
            <tr>
              <td>${{item.id}}</td>
              <td>${{item.action}}</td>
              ${{quarters.map(q => `<td class="q">${{item.startQ && item.endQ && q >= item.startQ && q <= item.endQ ? '<span class="cell-active"></span>' : ''}}</td>`).join('')}}
            </tr>
          `).join('')}}
          </tbody>
        </table>`;
    }}

    function renderTable(items) {{
      byId('table').innerHTML = `
        <table>
          <thead>
            <tr>
              <th>N°</th><th>Acción</th><th>Línea</th><th>Estado lectura</th><th>Años</th><th>Trimestres</th><th>Ejecutores</th><th>Presupuesto</th><th>Observación</th>
            </tr>
          </thead>
          <tbody>
            ${{items.map(item => `
              <tr>
                <td>${{item.id}}</td>
                <td><strong>${{item.action}}</strong><br><span class="note">${{item.indicator}}</span></td>
                <td>${{item.line}}</td>
                <td><span class="status-pill ${{slug(item.status)}}">${{item.status}}</span></td>
                <td>${{item.years.join(', ')}}</td>
                <td>${{item.startQ && item.endQ ? `T${{item.startQ}} - T${{item.endQ}}` : ''}}</td>
                <td>${{item.allExecutors || item.executors.join(', ')}}</td>
                <td>${{item.budget ? money.format(item.budget) : item.budgetLabel}}</td>
                <td>${{item.observation}}</td>
              </tr>
            `).join('')}}
          </tbody>
        </table>`;
    }}

    function renderDocs() {{
      byId('docs').innerHTML = DOCUMENTS.map(doc => `
        <a class="doc" href="${{doc.file}}" target="_blank">
          <strong>${{doc.title}}</strong>
          <span>${{doc.type}}</span>
        </a>
      `).join('');
    }}

    function update() {{
      const items = filtered();
      renderKpis(items);
      renderBars('statusChart', countBy(items, item => item.status));
      renderBars('lineChart', countBy(items, item => item.line));
      renderBars('yearChart', countBy(items, item => item.years));
      renderBars('budgetChart', budgetBy(items, item => item.line), value => money.format(value));
      renderGantt(items);
      renderTable(items);
    }}

    addOptions('lineFilter', DATA.map(item => item.line));
    addOptions('statusFilter', DATA.map(item => item.status));
    addOptions('yearFilter', DATA.flatMap(item => item.years));
    addOptions('executorFilter', DATA.flatMap(item => item.executors));
    ['search', 'lineFilter', 'statusFilter', 'yearFilter', 'executorFilter'].forEach(id => byId(id).addEventListener('input', update));
    renderDocs();
    update();
  </script>
</body>
</html>
"""


def main():
    records = build_records()
    OUTPUT.write_text(render_html(records), encoding="utf-8")
    print(f"Dashboard creado: {OUTPUT}")
    print(f"Acciones cargadas: {len(records)}")


if __name__ == "__main__":
    main()
