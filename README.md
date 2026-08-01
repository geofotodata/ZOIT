# Dashboard ZOIT San Jose de Maipo

Dashboard local para monitorear el Plan de Accion ZOIT San Jose de Maipo desde la hoja `PA-V1` del archivo Excel de seguimiento.

## Archivos principales

- `dashboard_zoit_pa_v1.html`: dashboard listo para abrir en el navegador.
- `build_dashboard_zoit.py`: generador del dashboard desde el Excel.

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
