# -*- coding: utf-8 -*-
"""
Módulo: pdf_exporter.py
-----------------------
Combina múltiples archivos PNG en un único documento PDF,
donde cada imagen corresponde a una página.
Incluye una portada automática con título, fecha y cantidad de gráficos.
"""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from datetime import datetime
from PIL import Image
from config_time import START_TIME, END_TIME  # ← fechas originales GMT-5



def add_cover_page(c, title, num_images, logo_path=None,
                   start_time_str=None, end_time_str=None):
    """
    Dibuja una portada con título, fecha y logotipo (si existe).
    """
    width, height = landscape(A4)
    margin = 50

    # Fondo suave
    c.setFillColorRGB(0.96, 0.96, 0.96)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # Título principal
    c.setFillColor(colors.darkblue)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 180, title)

    # 🔹 Formato de fechas con mes en letras
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    def formato_humano(fecha_str, incluir_hora=False):
        """
        Convierte 'YYYY-MM-DD HH:MM' en 'DD mes YYYY' o 'DD mes YYYY HH:MM'
        """
        try:
            dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                dt = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
            except Exception:
                return fecha_str

        mes = meses[dt.month - 1]
        if incluir_hora:
            return f"{dt.day:02d} {mes} {dt.year} {dt.strftime('%H:%M')}"
        return f"{dt.day:02d} {mes} {dt.year}"

    # 🔹 Fecha de generación (legible)
    fecha_generacion = formato_humano(datetime.now().strftime("%Y-%m-%d %H:%M"), incluir_hora=True)
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 230, f"Generado el {fecha_generacion}")

    # 🔹 Rango de análisis
    start_humano = formato_humano(start_time_str, incluir_hora=True)
    end_humano = formato_humano(end_time_str, incluir_hora=True)

    c.setFont("Helvetica", 13)
    c.drawCentredString(
        width / 2,
        height - 260,
        f"Período analizado: {start_humano} — {end_humano} (GMT-5)"
    )

    # Cantidad de gráficos
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 290, f"Gráficos incluidos: {num_images}")

    # Logotipo (opcional)
    if logo_path and Path(logo_path).exists():
        try:
            logo = ImageReader(logo_path)
            logo_width = 200
            logo_height = 200
            c.drawImage(
                logo,
                (width - logo_width) / 2,
                height / 2 - 100,
                width=logo_width,
                height=logo_height,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception as e:
            print(f"⚠️ No se pudo insertar el logo: {e}")

    # Pie de página
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.gray)
    c.drawCentredString(width / 2, margin, "Generado automáticamente")

    c.showPage()


def combine_pngs_to_pdf(
    png_folder,
    pdf_filename="reporte_velocidades.pdf",
    logo_path=None,
    start_time_str=None,
    end_time_str=None
):
    """
    Combina todos los archivos PNG de una carpeta en un único PDF con portada.

    Parámetros:
        png_folder (str | Path): carpeta donde se guardan los PNG.
        output_pdf_name (str): nombre del PDF final (por defecto "report_velocities.pdf").
        logo_filename (str): nombre del archivo de logotipo opcional (por defecto "logo.png").

    Retorna:
        Path: ruta completa del PDF generado.
    """
    png_folder = Path(png_folder)
    output_path = png_folder / pdf_filename


    # Buscar imágenes PNG
    png_files = sorted(png_folder.glob("*.png"))
    if not png_files:
        print(f"⚠️ No se encontraron imágenes PNG en {png_folder}")
        return None

    a4_width, a4_height = landscape(A4)
    c = canvas.Canvas(str(output_path), pagesize=landscape(A4))

    # Agregar portada
    add_cover_page(
        c,
        title="Reporte de Velocidades",
        num_images=len(png_files),
        logo_path=logo_path,
        start_time_str=start_time_str,
        end_time_str=end_time_str
    )
    
    for png_path in png_files:
        try:
            with Image.open(png_path) as img:
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height

                # Ajustar imagen manteniendo proporción
                max_width, max_height = a4_width - 40, a4_height - 40
                if aspect_ratio > (max_width / max_height):
                    new_width = max_width
                    new_height = max_width / aspect_ratio
                else:
                    new_height = max_height
                    new_width = max_height * aspect_ratio

                x = (a4_width - new_width) / 2
                y = (a4_height - new_height) / 2

                c.drawImage(
                    ImageReader(png_path),
                    x,
                    y,
                    width=new_width,
                    height=new_height,
                    preserveAspectRatio=True,
                    mask="auto",
                )

            c.showPage()
            print(f"🖼️ Añadido al PDF: {png_path.name}")

        except Exception as e:
            print(f"⚠️ Error al procesar {png_path.name}: {e}")

    c.save()
    print(f"✅ PDF generado: {output_path.resolve()}")
    return output_path
