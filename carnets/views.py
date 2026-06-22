from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from barcode import Code128
from barcode.writer import ImageWriter
import json
from .models import PlantillaCarnet, ElementoPlantilla

def editar_plantilla(request, pk):
    plantilla = get_object_or_404(PlantillaCarnet, pk=pk)
    dims = plantilla.get_dimensiones_px()
    return render(request, 'carnets/editor_plantilla.html', {
        'plantilla': plantilla,
        'canvas_w': dims['w'],
        'canvas_h': dims['h']
    })

@require_POST
def cambiar_orientacion(request, pk):
    plantilla = get_object_or_404(PlantillaCarnet, pk=pk)
    plantilla.orientacion = request.POST.get('orientacion', 'H')
    plantilla.save()
    return redirect('editar_plantilla', pk=pk)

@require_POST
def crear_elemento(request):
    data = json.loads(request.body)
    elemento = ElementoPlantilla.objects.create(
        plantilla_id=data['plantilla_id'],
        tipo=data['tipo'],
        x=float(data['x']),
        y=float(data['y']),
        width=float(data.get('width', 150)),
        height=float(data.get('height', 30))
    )
    return JsonResponse({
        'status': 'ok',
        'id': elemento.id,
        'tipo': elemento.tipo,
        'get_tipo_display': elemento.get_tipo_display()
    })

@csrf_exempt
def guardar_plantilla(request, pk):
    if request.method == 'POST':
        plantilla = PlantillaCarnet.objects.get(pk=pk)
        data = json.loads(request.body)
        
        # Borra elementos que ya no están
        ids_enviados = [e.get('id') for e in data['elementos'] if e.get('id')]
        plantilla.elementos.exclude(id__in=ids_enviados).delete()
        
        for elem_data in data['elementos']:
            elem_id = elem_data.get('id')
            defaults = {
                'tipo': elem_data['tipo'],
                'texto_fijo': elem_data['texto_fijo'],
                'x': elem_data['x'],
                'y': elem_data['y'],
                'width': elem_data['width'],
                'height': elem_data['height'],
                'font_size': elem_data['font_size'],
                'color': elem_data.get('color', '#000000'),
                'background_color': elem_data.get('background_color', ''),
                'font_weight': elem_data.get('font_weight', 'normal'),
                'text_align': elem_data.get('text_align', 'left'),
            }
            if elem_id:
                ElementoPlantilla.objects.filter(id=elem_id).update(**defaults)
            else:
                ElementoPlantilla.objects.create(plantilla=plantilla, **defaults)
        
        return JsonResponse({'status': 'ok'})
    
@require_POST
def actualizar_elemento(request):
    data = json.loads(request.body)
    ElementoPlantilla.objects.filter(id=data['id']).update(
        x=float(data['x']),
        y=float(data['y']),
        width=float(data['width']),
        height=float(data['height'])
    )
    return JsonResponse({'status': 'ok'})

@require_POST
def eliminar_elemento(request):
    data = json.loads(request.body)
    ElementoPlantilla.objects.filter(id=data['id']).delete()
    return JsonResponse({'status': 'ok'})


## PDF

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from django.http import FileResponse
import io
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter

def generar_pdf_plantilla(request, pk):
    plantilla = PlantillaCarnet.objects.get(pk=pk)

    w, h = (85.6*mm, 54*mm) if plantilla.orientacion == 'H' else (54*mm, 85.6*mm)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=(w, h))

    # Fondo
    if plantilla.imagen_fondo:
        p.drawImage(plantilla.imagen_fondo.path, 0, 0, width=w, height=h)

    # Datos de ejemplo - aquí después jalas del empleado real
    datos_empleado = {
        'nombre': 'JUAN PÉREZ GARCÍA',
        'cargo': 'Desarrollador Senior',
        'empresa': plantilla.company.name if plantilla.company else 'Mi Empresa',
        'identificacion': '12345678',
        'telefono': '999-888-777',
        'num_empleado': 'EMP-001',
        'codigo': '123456789'
    }

    for elem in plantilla.elementos.all():
        x = (elem.x / 10) * mm
        y = h - ((elem.y / 10) * mm) - ((elem.height / 10) * mm)  # height, no alto
        ancho = (elem.width / 10) * mm  # width, no ancho
        alto = (elem.height / 10) * mm  # height, no alto

        # Color de fondo
        if elem.background_color:
            p.setFillColor(HexColor(elem.background_color))
            p.rect(x, y, ancho, alto, fill=1, stroke=0)

        # Color de texto
        p.setFillColor(HexColor(elem.color or '#000000'))

        # Fuente
        font = "Helvetica-Bold" if elem.font_weight == 'bold' else "Helvetica"
        p.setFont(font, elem.font_size)

        # Texto a mostrar según el tipo
        texto = elem.texto_fijo or ""
        if elem.tipo in datos_empleado:
            texto = datos_empleado[elem.tipo]
        elif elem.tipo == 'texto':
            texto = elem.texto_fijo or "Texto"

        if elem.tipo == 'logo' and plantilla.company.logo:
            p.drawImage(plantilla.company.logo.path, x, y, width=ancho, height=alto, preserveAspectRatio=True)

        elif elem.tipo == 'barcode':
            code = Code128(texto or datos_empleado['codigo'], writer=ImageWriter())
            img_buf = io.BytesIO()
            code.write(img_buf)
            img_buf.seek(0)
            p.drawImage(ImageReader(img_buf), x, y, width=ancho, height=alto)

        elif elem.tipo == 'qr':
            qr = qrcode.QRCode(box_size=2, border=1)
            qr.add_data(texto or datos_empleado['codigo'])
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_buf = io.BytesIO()
            img.save(img_buf, format='PNG')
            img_buf.seek(0)
            p.drawImage(ImageReader(img_buf), x, y, width=ancho, height=alto)

        elif elem.tipo == 'foto':
            p.setStrokeColor(colors.grey)
            p.setLineWidth(1)
            p.rect(x, y, ancho, alto, stroke=1, fill=0)
            p.setFillColor(HexColor('#999999'))
            p.drawCentredString(x + ancho/2, y + alto/2, "FOTO")

        else:  # Textos: nombre, cargo, dni, telefono, empresa, etc
            p.setFillColor(HexColor(elem.color or '#000000'))
            if elem.text_align == 'center':
                p.drawCentredString(x + ancho/2, y + alto/2 - 2, texto)
            elif elem.text_align == 'right':
                p.drawRightString(x + ancho - 2, y + alto/2 - 2, texto)
            else:
                p.drawString(x + 2, y + alto/2 - 2, texto)

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, filename=f'carnet_{plantilla.id}.pdf')