# -*- coding: UTF-8 -*-
"""
Configuración general del proyecto: rutas, tiempos, tipos y mapeo de beacons.
Detecta automáticamente la carpeta del ejecutable (.py o .exe)
y guarda los resultados allí.
"""

from datetime import datetime, timedelta
from pathlib import Path
import sys
import os
import pytz

# Importar los tiempos definidos por el usuario (en GMT -5)
from config_time import START_TIME, END_TIME

# === Conversión automática de GMT -5 → GMT 0 (UTC) ===
def to_utc_from_gmt_minus5(local_str):
    """
    Convierte una fecha local (GMT-5) a UTC (GMT 0).
    Espera formato: 'YYYY-MM-DD HH:MM'
    """
    local_tz = pytz.timezone("Etc/GMT+5")  # GMT-5 → +5 por convención pytz
    dt_local = local_tz.localize(datetime.strptime(local_str, "%Y-%m-%d %H:%M"))
    dt_utc = dt_local.astimezone(pytz.utc)
    return dt_utc

# Fechas convertidas a UTC para descarga
START_TIME_UTC = to_utc_from_gmt_minus5(START_TIME)
END_TIME_UTC   = to_utc_from_gmt_minus5(END_TIME)

# Fechas en string ISO (para API o curl)
START_TIME_STR = START_TIME_UTC.strftime("%Y-%m-%dT%H:%M:%SZ")
END_TIME_STR   = END_TIME_UTC.strftime("%Y-%m-%dT%H:%M:%SZ")

# --- Tiempos locales (GMT-5) para uso humano ---
tz_minus5 = pytz.timezone("Etc/GMT+5")
START_TIME_LOCAL = tz_minus5.localize(datetime.strptime(START_TIME, "%Y-%m-%d %H:%M"))
END_TIME_LOCAL   = tz_minus5.localize(datetime.strptime(END_TIME, "%Y-%m-%d %H:%M"))

# Formatos para uso humano (para portada del PDF)
START_TIME_HUMAN = START_TIME_LOCAL.strftime("%Y-%m-%d %H:%M")
END_TIME_HUMAN = END_TIME_LOCAL.strftime("%Y-%m-%d %H:%M")

# --- Detección automática del directorio del script o ejecutable ---
if getattr(sys, 'frozen', False):
    # Si está compilado con PyInstaller (ejecutable .exe)
    BASE_PATH = Path(sys.executable).parent
else:
    # Si se ejecuta como script .py
    BASE_PATH = Path(os.path.abspath(__file__)).parent

# --- Carpeta de salida dentro del mismo directorio ---
FOLDER = "VELOCITY"
PATH = BASE_PATH / FOLDER

# Tipos de datos
TYPE = "VELOCITY"
TYPE_X = "X_VELOCITY"
TYPE_Y = "Y_VELOCITY"
TYPE_Z = "Z_VELOCITY"

# Fechas locales para graficar (convertidas de vuelta a GMT-5)
tz_minus5 = pytz.timezone("Etc/GMT+5")
START_TIME_PLOT = START_TIME_UTC.astimezone(tz_minus5)
END_TIME_PLOT   = END_TIME_UTC.astimezone(tz_minus5)

# Diccionario reducido de beacons (puedes agregar los tuyos aquí)
BEACONS = {
    8337288246588878388: "ML5x6_P2",
    8654335862333516267: "ML5x6_P6",
    3513830231309335651: "ML5x6_P7",
}
