# -*- coding: utf-8 -*-
"""
Módulo: plotter.py
------------------
Procesa y grafica datos de velocidad obtenidos en formato JSON desde Bluzone.
Convierte las fechas de UTC (GMT 0) a hora local (GMT -5) y genera gráficos
de velocidades (X, Y, Z) con escala ajustada automáticamente.
Incluye líneas de referencia diarias y cada 2 horas.
"""

from datetime import datetime, timezone, timedelta
from pathlib import Path
import matplotlib

# Forzar backend no interactivo (necesario si no hay GUI, ej. ejecución automática)
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Configuración de zona horaria local (GMT -5) ---
TZ_OFFSET = timedelta(hours=-5)


def process_metric_data(json_data):
    """
    Procesa el JSON descargado de los datos de velocidad.
    Convierte las marcas de tiempo desde GMT 0 a GMT -5.
    Devuelve una lista de tuplas (datetime_local, valor).

    Parámetros:
        json_data (list): lista de registros JSON con campos:
            - "keyAsString": fecha/hora en UTC (str)
            - "rmsPeak": valor de velocidad RMS (float)
            - "sum": suma de valores (float)

    Retorna:
        list[tuple(datetime, float)]: lista ordenada de (fecha_local, valor)
    """
    data = []
    for item in json_data:
        try:
            # Convertir string a datetime (UTC)
            timestamp_utc = datetime.strptime(item["keyAsString"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timestamp_utc = timestamp_utc.replace(tzinfo=timezone.utc)

            # Convertir a hora local (GMT -5)
            timestamp_local = timestamp_utc.astimezone(timezone(TZ_OFFSET))

            # Filtrar datos válidos (sum != 0)
            if item.get("sum", 0.0) != 0.0:
                # Convertir de pulgadas/segundo a mm/segundo
                data.append((timestamp_local, item["rmsPeak"] * 25.4))
        except Exception:
            continue

    # Ordenar cronológicamente
    data.sort(key=lambda x: x[0])
    return data


def plot_velocity_graph(data_x, data_y, data_z, name, output_file):
    """
    Genera el gráfico de velocidad (X, Y, Z) en función del tiempo local (GMT-5).

    - Escala vertical: [0, max + 5]
    - Líneas verticales sólidas grises al inicio de cada día (medianoche local GMT-5)
    - Líneas punteadas más suaves cada 2 horas
    - Guarda automáticamente el PNG en la ruta especificada

    Parámetros:
        data_x, data_y, data_z (list[tuple]): datos por eje [(datetime, valor), ...]
        name (str): nombre descriptivo del sensor/beacon
        output_file (str | Path): ruta donde se guardará el PNG
    """

    # Asegurar carpeta destino
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Combinar todos los datos para definir escala
    all_values = [v for _, v in data_x + data_y + data_z]
    if not all_values:
        print(f"⚠️ No hay datos válidos para {name}")
        return

    max_value = max(all_values)
    y_min = 0
    y_max = max_value + 5  # margen superior

    # Crear figura
    fig, ax = plt.subplots(figsize=(16, 8), dpi=200)

    # Graficar cada eje si tiene datos
    if data_x:
        ax.plot([d[0] for d in data_x], [d[1] for d in data_x], label="X", linewidth=1.2)
    if data_y:
        ax.plot([d[0] for d in data_y], [d[1] for d in data_y], label="Y", linewidth=1.2)
    if data_z:
        ax.plot([d[0] for d in data_z], [d[1] for d in data_z], label="Z", linewidth=1.2)

    # Configurar ejes
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("Tiempo (GMT-5)")
    ax.set_ylabel("Velocidad (mm/s)")
    ax.set_title(f"Velocidades para {name}")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()

    # --- Formato del eje X (fechas en hora local GMT-5) ---
    tzinfo_local = timezone(TZ_OFFSET)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M", tz=tzinfo_local))
    plt.xticks(rotation=45)

    # --- Líneas verticales al inicio de cada día local (medianoche GMT-5) ---
    all_datetimes = [d[0] for d in (data_x + data_y + data_z)]
    if all_datetimes:
        local_dates = sorted(set(dt.astimezone(tzinfo_local).date() for dt in all_datetimes))
        for day in local_dates:
            midnight_local = datetime.combine(day, datetime.min.time(), tzinfo=tzinfo_local)
            # Línea principal en medianoche
            ax.axvline(midnight_local, color="gray", linestyle="--", linewidth=0.9, alpha=0.5)

            # --- Líneas punteadas cada 2 horas ---
            for hour in range(2, 24, 2):
                tick_time = midnight_local + timedelta(hours=hour)
                ax.axvline(tick_time, color="gray", linestyle=":", linewidth=0.6, alpha=0.25)

    plt.tight_layout()

    # Guardar figura
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"✅ PNG guardado: {out_path.resolve()}")
