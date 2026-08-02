# Portal ZOIT

Portal web para organizar informacion, dashboard, mesa publico privada, actas, publicaciones y sugerencias de tres Zonas de Interes Turistico: San Jose de Maipo, Pirque e Isla de Maipo.

## Archivos principales

- `index.html`: portada central del portal.
- `dashboard_zoit_pa_v1.html`: dashboard de San Jose de Maipo listo para abrir en el navegador.
- `build_dashboard_zoit.py`: generador del dashboard desde el Excel.
- `build_portal.py`: generador de la estructura central del portal.

El Excel fuente y los documentos PDF se mantienen fuera del repositorio. Para regenerar el dashboard, deben estar disponibles en la carpeta local del proyecto con los nombres esperados por el script.

## Como usar

Abrir `dashboard_zoit_pa_v1.html` en un navegador.

Version publicada en GitHub Pages:

https://geofotodata.github.io/ZOIT/

## Como regenerar el dashboard

Si se actualiza el Excel, ejecutar:

```bash
python build_dashboard_zoit.py
```

El script vuelve a crear `dashboard_zoit_pa_v1.html` usando la hoja `PA-V1`.

## Contenido del dashboard

- Indicadores generales del plan.
- Filtros por linea de accion, estado, anio y ejecutor.
- Graficos de acciones por estado, linea, anio y presupuesto.
- Carta Gantt por trimestres.
- Tabla completa de acciones.
- Enlaces a normativa y documentos base.

## Mejoras UX/UI del portal

- Header fijo con buscador y acciones rapidas.
- Panel lateral de categorias con iconos.
- Navegacion inferior para celulares.
- Tarjetas KPI y accesos por destino.
- Estructura preparada para capas, documentos, indicadores y herramientas GIS.
- Estilos responsive con foco en accesibilidad visual y navegacion clara.
