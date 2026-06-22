from django.db import models
from companies.models import Company

class PlantillaCarnet(models.Model):
    ORIENTACION_CHOICES = [
        ('H', 'Horizontal'),
        ('V', 'Vertical'),
    ]
    
    #company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='plantillas')
    company = models.ForeignKey(
            Company,
            on_delete=models.CASCADE,
            related_name='plantillas',
            null=True,  # Esto es clave
            blank=True
        )
    nombre = models.CharField(max_length=100)
    #empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    empresa = models.CharField(max_length=100, default='Mi Empresa')
    imagen_fondo = models.ImageField(upload_to='templates/', null=True, blank=True)
    orientacion = models.CharField(max_length=1, choices=ORIENTACION_CHOICES, default='H')
    ancho_mm = models.FloatField(default=85.6)  # CR80
    alto_mm = models.FloatField(default=54.0)

    def __str__(self):
        return f"{self.company.name} - {self.nombre}"

    def get_dimensiones_px(self, escala=10):
        """Escala 10 = 1mm = 10px para pantalla"""
        if self.orientacion == 'H':
            return {'w': self.ancho_mm * escala, 'h': self.alto_mm * escala}
        else:
            return {'w': self.alto_mm * escala, 'h': self.ancho_mm * escala}

    def __str__(self):
        return f"{self.nombre} - {self.empresa}"

class ElementoPlantilla(models.Model):
    TIPO_CHOICES = [
        ('nombre', 'Nombre'),
        ('cargo', 'Cargo'),
        ('empresa', 'Empresa'),
        ('codigo', 'Código'),
        ('qr', 'Código QR'),
        ('foto', 'Foto'),
        ('logo', 'Logo Empresa'),           # Nuevo
        ('barcode', 'Código de Barras'),    # Nuevo
        ('identificacion', 'DNI/ID'),       # Nuevo
        ('telefono', 'Teléfono'),           # Nuevo
        ('num_empleado', 'N° Empleado'),    # Nuevo
        ('texto', 'Texto libre'),           # Nuevo
    ]

    plantilla = models.ForeignKey(PlantillaCarnet, on_delete=models.CASCADE, related_name='elementos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    texto_fijo = models.CharField(max_length=200, blank=True, null=True)

    # Posición y tamaño
    x = models.FloatField(default=20)
    y = models.FloatField(default=20)
    width = models.FloatField(default=150)
    height = models.FloatField(default=30)

    #estilos nuevos
    font_size = models.IntegerField(default=16)
    font_family = models.CharField(max_length=50, default='Arial')
    color = models.CharField(max_length=7, default='#000000')
    background_color = models.CharField('Color fondo', max_length=7, default='', blank=True, help_text='Hex o vacío')
    font_weight = models.CharField('Grosor', max_length=10, default='normal', 
                                   choices=[('normal','Normal'), ('bold','Negrita')])
    text_align = models.CharField('Alineación', max_length=10, default='left',
                                  choices=[('left','Izquierda'), ('center','Centro'), ('right','Derecha')])
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.plantilla}"
