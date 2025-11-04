from config import PATH, FOLDER, BEACONS, TYPE, TYPE_X, TYPE_Y, TYPE_Z,START_TIME_HUMAN,END_TIME_HUMAN
from utils.data_fetcher import run_curl_command, load_json_file
from utils.plotter import process_metric_data, plot_velocity_graph
from utils.pdf_exporter import combine_pngs_to_pdf
from pathlib import Path
import os

# Crear carpeta destino (en la misma ubicación del script o ejecutable)
os.makedirs(PATH, exist_ok=True)

print("DEBUG: EMAIL_USER set?", "EMAIL_USER" in os.environ)
print("DEBUG: EMAIL_PASS set?", "EMAIL_PASS" in os.environ)

for beacon_id, name in BEACONS.items():
    print(f"Procesando beacon {name} ({beacon_id})")

    base_filename = PATH / f"{TYPE}_{name}_{beacon_id}"
    file_x = base_filename.with_name(f"{base_filename.name}_X.dat")
    file_y = base_filename.with_name(f"{base_filename.name}_Y.dat")
    file_z = base_filename.with_name(f"{base_filename.name}_Z.dat")
    file_png = base_filename.with_suffix(".png")

    try:
        run_curl_command(beacon_id, TYPE_X, file_x)
        run_curl_command(beacon_id, TYPE_Y, file_y)
        run_curl_command(beacon_id, TYPE_Z, file_z)
    except Exception as e:
        print(f"❌ Error al descargar datos del beacon {name}: {e}")
        continue

    try:
        json_x = load_json_file(file_x)
        json_y = load_json_file(file_y)
        json_z = load_json_file(file_z)

        data_x = process_metric_data(json_x)
        data_y = process_metric_data(json_y)
        data_z = process_metric_data(json_z)

        plot_velocity_graph(data_x, data_y, data_z, name, str(file_png))
        print(f"✅ Gráfico generado: {file_png}")
    except Exception as e:
        print(f"❌ Error al procesar datos del beacon {name}: {e}")

output_folder = Path(__file__).parent / "VELOCITY"

# 🧩 Generar el PDF y guardar la ruta
output_pdf_path = combine_pngs_to_pdf(
    PATH,
    "informe_velocidades.pdf",
    start_time_str=START_TIME_HUMAN,
    end_time_str=END_TIME_HUMAN
)

# === Enviar PDF por correo ===
from utils.email_sender import send_report_email

if output_pdf_path and output_pdf_path.exists():
    send_report_email(
        subject="Reporte de Velocidades Semanal",
        body="Adjunto el reporte semanal de velocidades (últimos 30 días).",
        recipients=["daniel.akamine@gmail.com"],  # lista de destinatarios
        attachment_path=output_pdf_path
    )
    print("📧 Reporte enviado correctamente.")
else:
    print("⚠️ No se encontró el PDF generado. No se enviará el correo.")
