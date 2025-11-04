# -*- coding: utf-8 -*-
"""
Archivo: config_time.py
-----------------------
Define los tiempos de inicio y fin en hora local (GMT -5).
Estos serán convertidos automáticamente a GMT 0 por el programa principal.
"""
from datetime import datetime, timedelta, timezone

# Definir zona horaria GMT-5
GMT_MINUS_5 = timezone(timedelta(hours=-5))

# Fecha y hora actuales (fin del período)
END_TIME_PY = datetime.now(GMT_MINUS_5)

# Fecha 30 días antes (inicio del período)
START_TIME_PY = END_TIME_PY - timedelta(days=30)

# Formatos legibles (para mostrar en el PDF)
START_TIME = START_TIME_PY.strftime("%Y-%m-%d %H:%M")
END_TIME = END_TIME_PY.strftime("%Y-%m-%d %H:%M")


# Escribe los horarios de manera humana (zona local GMT -5)
#START_TIME = "2025-10-20 00:00"  # inicio (hora local)
#END_TIME   = "2025-11-04 23:59"  # fin (hora local)
