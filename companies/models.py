from django.db import models
from django.utils.text import slugify

class Company(models.Model):
    SUBSCRIPTION_PLANS = [
        ('free', 'Gratuito (100 tarjetas)'),
        ('basic', 'Básico (1,000 tarjetas)'),
        ('premium', 'Premium (10,000 tarjetas)'),
        ('enterprise', 'Enterprise (Ilimitado)'),
    ]

    name = models.CharField('Nombre', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True, blank=True)
    contact_email = models.EmailField('Email de contacto', blank=True, null=True)
    contact_phone = models.CharField('Teléfono', max_length=50, blank=True, null=True)
    contact_person = models.CharField('Persona de contacto', max_length=200, blank=True, null=True)
    tax_id = models.CharField('RUC / Tax ID', max_length=50, blank=True, null=True)
    address = models.CharField('Dirección', max_length=255, blank=True, null=True)
    city = models.CharField('Ciudad', max_length=100, blank=True, null=True)
    country = models.CharField('País', max_length=100, default='Perú', blank=True)
    logo = models.ImageField('Logo', upload_to='companies/logos/', blank=True, null=True)
    primary_color = models.CharField('Color primario', max_length=7, default='#000000', help_text='Hex: #RRGGBB')
    secondary_color = models.CharField(max_length=7, default='#1E40AF', verbose_name="Color secundario")


    # Suscripción
    subscription_plan = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_PLANS,
        default='free',
        verbose_name="Plan de suscripción"
    )
    subscription_start = models.DateField(auto_now_add=True, verbose_name="Inicio de suscripción")
    subscription_end = models.DateField(null=True, blank=True, verbose_name="Fin de suscripción")

    is_active = models.BooleanField('Activa', default=True)
    is_verified = models.BooleanField('Verificada', default=False)
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['subscription_plan']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name