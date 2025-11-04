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
    15263084726064999534: "ML5x6_P8",
    15097471866278510330: "ML8x8A_P1",
    11535125626094346362: "ML8x8A_P2",
    6452297899005257711: "ML8x8A_P5",
    5490173546682757697: "ML8x8A_P6",
    4921689318145816336: "ML8x8A_P7",
    13216233204279948118: "ML8x8A_P8",
    11594946222317542084: "ML8x8B_P1",
    9124646931138146095: "ML8x8B_P2",
    5518858394087590314: "ML8x8B_P3",
    10896492889213851004: "ML8x8B_P4",
    15465253359017123427: "ML8x8B_P5",
    16685760148458881893: "ML8x8B_P6",
    3870238836580099975: "ML8x8B_P7",
    9980314963354335980: "ML8x8B_P8",
    4725453185355724302: "ML8x8C_P1",
    1801953957812695826: "ML8x8C_P2",
    17160810651532576232: "ML8x8C_P5",
    6508136573949847879: "ML8x8C_P6",
    11568821048590478697: "ML8x8C_P7",
    11933378158293264201: "ML8x8C_P8",
    10474192284955317446: "ML8x10A_P1",
    10222473504939829718: "ML8x10A_P2",
    3606802512401401718: "ML8x10A_P3",
    12474779193059015998: "ML8x10A_P4",
    12838808419137821065: "ML8x10A_P5",
    5495067936295135376: "ML8x10A_P6",
    8038744665186670970: "ML8x10A_P7",
    11036692542366098368: "ML8x10A_P8",
    11597920225838351244: "ML8x10B_P1",
    10800384262694920107: "ML8x10B_P2",
    2518945348337807477: "ML8x10B_P3",
    523621255692931928: "ML8x10B_P4",
    6798907268149512164: "ML8x10B_P5",
    10341464001017669547: "ML8x10B_P6",
    16489621341873135010: "ML8x10B_P7",
    8907641049415570721: "ML8x10B_P8",
}
