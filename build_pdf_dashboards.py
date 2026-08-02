import json
import math
import re
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent

PLANS = {
    "pirque": {
        "name": "Pirque",
        "source": Path(r"C:\Users\geofoto\Downloads\plan-de-accion-zoit-pirque.pdf"),
        "output": ROOT / "pirque" / "dashboard" / "index.html",
        "title": "Dashboard Plan de Acción ZOIT Pirque",
    },
    "isla-de-maipo": {
        "name": "Isla de Maipo",
        "source": Path(r"C:\Users\geofoto\Downloads\plan-de-accion-zoit-idm.pdf"),
        "output": ROOT / "isla-de-maipo" / "dashboard" / "index.html",
        "title": "Dashboard Plan de Acción ZOIT Isla de Maipo",
    },
}

LINE_MARKERS = [
    ("5.1", "Equipamiento e infraestructura"),
    ("5.2", "Promoción"),
    ("5.3", "Sustentabilidad"),
    ("5.4", "Desarrollo de productos"),
    ("5.5", "Capital humano"),
    ("5.6", "Gestión y planificación"),
]


def clean(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).replace("\n", " ")).strip()


def is_action_id(value):
    text = clean(value)
    return bool(re.fullmatch(r"\d{1,3}", text))


def parse_budget(value):
    text = clean(value).upper()
    if not text or text in {"S/P", "SP", "S/P.", "SFF", "S/F"}:
        return 0.0
    digits = re.sub(r"[^0-9]", "", text)
    return float(digits) if digits else 0.0


def parse_years(plazo):
    text = clean(plazo).lower()
    nums = [int(n) for n in re.findall(r"\d+", text)]
    if not nums:
        return []
    if len(nums) >= 2 and (" al " in text or "año" in text):
        start, end = min(nums[0], nums[1]), max(nums[0], nums[1])
        return [f"Año {n}" for n in range(start, end + 1) if 1 <= n <= 4]
    return [f"Año {n}" for n in nums if 1 <= n <= 4]


def status_from_years(years):
    if not years:
        return "Por programar"
    if "Año 1" in years and len(years) == 1:
        return "Corto plazo"
    if "Año 4" in years and len(years) >= 3:
        return "Plan plurianual"
    if "Año 4" in years:
        return "Largo plazo"
    return "Programada"


def line_for_page_text(text, current):
    upper = text.upper()
    for marker, line in LINE_MARKERS:
        if marker in upper:
            return line
    return current


def row_to_record(row, line):
    cells = [clean(cell) for cell in row]
    if not cells:
        return None
    id_index = None
    for idx in range(len(cells) - 1, -1, -1):
        if is_action_id(cells[idx]):
            id_index = idx
            break
    if id_index is None:
        return None

    action_id = cells[id_index]

    if len(cells) >= 17 and id_index >= 16:
        objective = cells[0]
        gap = cells[3]
        action = cells[4] or cells[5]
        executor = cells[7]
        deadline = cells[10]
        indicator = cells[11]
        goal = cells[12]
        verifier = cells[13]
        budget = cells[14]
        funding = cells[15]
    elif len(cells) >= 15 and id_index >= 14:
        objective = cells[0]
        gap = cells[1] or cells[3]
        action = cells[4] or cells[6]
        executor = cells[5] or cells[7]
        deadline = cells[8]
        indicator = cells[9]
        goal = cells[10]
        verifier = cells[11]
        budget = cells[12]
        funding = cells[13]
    elif len(cells) >= 13 and id_index >= 12:
        objective = cells[1] or cells[0]
        gap = cells[3] if len(cells) > 3 else ""
        action = cells[4]
        executor = cells[5]
        deadline = cells[6]
        indicator = cells[7]
        goal = cells[8]
        verifier = cells[9]
        budget = cells[10]
        funding = cells[11]
    elif len(cells) >= 11 and id_index >= 10:
        start = id_index - 10
        objective, gap, action, executor, deadline, indicator, goal, verifier, budget, funding, _ = cells[start : id_index + 1]
    else:
        return None

    if not action:
        return None
    years = parse_years(deadline)
    return {
        "id": int(action_id),
        "action": action,
        "line": line or "Sin línea identificada",
        "objective": objective,
        "gap": gap,
        "indicator": indicator,
        "goal": goal,
        "verifier": verifier,
        "budget": parse_budget(budget),
        "budgetLabel": budget,
        "funding": funding,
        "years": years,
        "startQ": None,
        "endQ": None,
        "executors": [executor] if executor else [],
        "allExecutors": executor,
        "observation": "Registro cargado desde el Plan de Acción PDF. Requiere seguimiento operativo y verificadores actualizados.",
        "status": status_from_years(years),
    }


def extract_records(pdf_path):
    records = []
    seen = set()
    current_line = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            current_line = line_for_page_text(text, current_line)
            for table in page.extract_tables() or []:
                for row in table:
                    rec = row_to_record(row, current_line)
                    if rec and rec["id"] not in seen:
                        records.append(rec)
                        seen.add(rec["id"])
    return sorted(records, key=lambda item: item["id"])


def review_record(action_id, line, action, executor="", budget="S/P", funding="Sin dato extraido"):
    return {
        "id": action_id,
        "action": action,
        "line": line,
        "objective": "",
        "gap": "",
        "indicator": "",
        "goal": "",
        "verifier": "",
        "budget": parse_budget(budget),
        "budgetLabel": budget,
        "funding": funding,
        "years": [],
        "startQ": None,
        "endQ": None,
        "executors": [executor] if executor else [],
        "allExecutors": executor,
        "observation": "Fila no extraida de forma completa desde el PDF; requiere revision manual del plan de accion.",
        "status": "Requiere revision",
    }


def fill_missing_records(slug, records):
    by_id = {record["id"]: record for record in records}
    if slug == "pirque" and 44 not in by_id:
        records.append(
            review_record(
                44,
                "Gestion y planificacion",
                "Accion 44 segun matriz PDF",
            )
        )
    if slug == "isla-de-maipo" and 6 not in by_id:
        records.append(
            review_record(
                6,
                "Equipamiento e infraestructura",
                "Accion 6 segun matriz PDF",
                "Minvu, Equipo PPL, Turismo",
                "S/P",
                "SFF",
            )
        )
    return sorted(records, key=lambda item: item["id"])


def render_dashboard(records, title, source_name):
    data = json.dumps(records, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f6f7f2;
      --ink: #17211b;
      --muted: #5f6f66;
      --line: #dbe1d8;
      --panel: #ffffff;
      --green: #2f7d5b;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: var(--ink); background: var(--bg); }}
    header {{ padding: 24px 28px 18px; background: #18392f; color: white; border-bottom: 5px solid #d8a64a; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: 0; }}
    header p {{ margin: 0; color: #dce9df; max-width: 980px; line-height: 1.45; }}
    main {{ padding: 22px 28px 40px; max-width: 1500px; margin: 0 auto; }}
    .filters {{ display: grid; grid-template-columns: 2fr repeat(4, minmax(160px, 1fr)); gap: 10px; margin-bottom: 16px; }}
    input, select {{ width: 100%; min-height: 38px; border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; background: white; color: var(--ink); font-size: 14px; }}
    .kpis {{ display: grid; grid-template-columns: repeat(5, minmax(150px, 1fr)); gap: 12px; margin-bottom: 16px; }}
    .kpi {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }}
    .kpi .label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; }}
    .kpi .value {{ font-size: 26px; font-weight: 700; margin-top: 6px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; align-items: start; }}
    section {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 16px; margin-bottom: 14px; }}
    h2 {{ font-size: 18px; margin: 0 0 14px; }}
    .bar-row {{ display: grid; grid-template-columns: minmax(130px, 230px) 1fr 70px; gap: 10px; align-items: center; margin: 9px 0; font-size: 14px; }}
    .bar-label {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .bar-track {{ background: #edf1ec; border-radius: 4px; height: 15px; overflow: hidden; }}
    .bar-fill {{ height: 100%; background: var(--green); }}
    .status-pill {{ display: inline-block; padding: 4px 8px; border-radius: 999px; background: #edf1ec; font-size: 12px; white-space: nowrap; }}
    .table-wrap {{ overflow: auto; max-height: 650px; border: 1px solid var(--line); border-radius: 6px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; min-width: 1050px; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ position: sticky; top: 0; background: #eef3ed; z-index: 1; }}
    tr:hover td {{ background: #fafbf7; }}
    .note {{ color: var(--muted); font-size: 13px; margin-top: 8px; }}
    @media (max-width: 1000px) {{ .filters, .kpis, .grid {{ grid-template-columns: 1fr; }} header, main {{ padding-left: 16px; padding-right: 16px; }} }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p>Monitoreo construido desde el plan de acción <strong>{source_name}</strong>. Los datos base provienen de la matriz del PDF y quedan listos para seguimiento operativo, verificadores y actualización de avance.</p>
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
      <section><h2>Acciones por estado</h2><div id="statusChart"></div></section>
      <section><h2>Acciones por línea</h2><div id="lineChart"></div></section>
      <section><h2>Programación por año</h2><div id="yearChart"></div></section>
      <section><h2>Presupuesto por línea</h2><div id="budgetChart"></div></section>
    </div>
    <section>
      <h2>Tabla de acciones</h2>
      <div class="table-wrap" id="table"></div>
      <div class="note">Nota: estos dashboards usan la planificación del PDF. Para monitoreo público fino conviene agregar % avance, fecha de actualización y links a evidencias.</div>
    </section>
  </main>
  <script>
    const DATA = {data};
    const money = new Intl.NumberFormat('es-CL', {{ style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }});
    const byId = id => document.getElementById(id);
    function unique(values) {{ return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, 'es')); }}
    function addOptions(id, values) {{
      const select = byId(id);
      unique(values).forEach(value => {{ const option = document.createElement('option'); option.value = value; option.textContent = value; select.appendChild(option); }});
    }}
    function filtered() {{
      const q = byId('search').value.trim().toLowerCase();
      const line = byId('lineFilter').value;
      const status = byId('statusFilter').value;
      const year = byId('yearFilter').value;
      const executor = byId('executorFilter').value;
      return DATA.filter(item => {{
        const haystack = [item.action, item.line, item.indicator, item.goal, item.verifier, item.observation, item.allExecutors, item.executors.join(' ')].join(' ').toLowerCase();
        return (!q || haystack.includes(q)) && (!line || item.line === line) && (!status || item.status === status) && (!year || item.years.includes(year)) && (!executor || item.executors.includes(executor) || item.allExecutors.includes(executor));
      }});
    }}
    function countBy(items, getter) {{
      const counts = {{}};
      items.forEach(item => {{ [].concat(getter(item)).filter(Boolean).forEach(value => counts[value] = (counts[value] || 0) + 1); }});
      return counts;
    }}
    function budgetBy(items, getter) {{
      const counts = {{}};
      items.forEach(item => {{ const key = getter(item) || 'Sin clasificar'; counts[key] = (counts[key] || 0) + item.budget; }});
      return counts;
    }}
    function renderBars(id, counts, formatter = value => value) {{
      const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);
      const max = Math.max(1, ...entries.map(entry => entry[1]));
      byId(id).innerHTML = entries.map(([label, value]) => `<div class="bar-row" title="${{label}}"><div class="bar-label">${{label}}</div><div class="bar-track"><div class="bar-fill" style="width:${{Math.max(3, value / max * 100)}}%"></div></div><div>${{formatter(value)}}</div></div>`).join('') || '<p class="note">Sin datos para los filtros seleccionados.</p>';
    }}
    function renderKpis(items) {{
      const totalBudget = items.reduce((sum, item) => sum + item.budget, 0);
      const withBudget = items.filter(item => item.budget > 0).length;
      const activeExecutors = unique(items.flatMap(item => item.executors)).length;
      byId('kpis').innerHTML = [
        ['Acciones', items.length],
        ['Presupuesto identificado', money.format(totalBudget)],
        ['Con presupuesto', withBudget],
        ['Líneas de acción', unique(items.map(item => item.line)).length],
        ['Ejecutores activos', activeExecutors],
      ].map(([label, value]) => `<div class="kpi"><div class="label">${{label}}</div><div class="value">${{value}}</div></div>`).join('');
    }}
    function renderTable(items) {{
      byId('table').innerHTML = `<table><thead><tr><th>N°</th><th>Acción</th><th>Línea</th><th>Estado lectura</th><th>Años</th><th>Ejecutores</th><th>Presupuesto</th><th>Meta</th><th>Verificador</th></tr></thead><tbody>${{items.map(item => `<tr><td>${{item.id}}</td><td><strong>${{item.action}}</strong><br><span class="note">${{item.indicator}}</span></td><td>${{item.line}}</td><td><span class="status-pill">${{item.status}}</span></td><td>${{item.years.join(', ')}}</td><td>${{item.allExecutors || item.executors.join(', ')}}</td><td>${{item.budget ? money.format(item.budget) : item.budgetLabel}}</td><td>${{item.goal}}</td><td>${{item.verifier}}</td></tr>`).join('')}}</tbody></table>`;
    }}
    function update() {{
      const items = filtered();
      renderKpis(items);
      renderBars('statusChart', countBy(items, item => item.status));
      renderBars('lineChart', countBy(items, item => item.line));
      renderBars('yearChart', countBy(items, item => item.years));
      renderBars('budgetChart', budgetBy(items, item => item.line), value => money.format(value));
      renderTable(items);
    }}
    addOptions('lineFilter', DATA.map(item => item.line));
    addOptions('statusFilter', DATA.map(item => item.status));
    addOptions('yearFilter', DATA.flatMap(item => item.years));
    addOptions('executorFilter', DATA.flatMap(item => item.executors));
    ['search', 'lineFilter', 'statusFilter', 'yearFilter', 'executorFilter'].forEach(id => byId(id).addEventListener('input', update));
    update();
  </script>
</body>
</html>
"""


def main():
    for slug, plan in PLANS.items():
        records = extract_records(plan["source"])
        records = fill_missing_records(slug, records)
        plan["output"].parent.mkdir(parents=True, exist_ok=True)
        plan["output"].write_text(
            render_dashboard(records, plan["title"], plan["source"].name),
            encoding="utf-8",
        )
        print(f"{plan['name']}: {len(records)} acciones -> {plan['output']}")


if __name__ == "__main__":
    main()
