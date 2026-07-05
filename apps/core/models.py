from django.db import models

class Lead(models.Model):
    ESTADO_CHOICES = [
        ("nuevo", "Nuevo"),
        ("contactado", "Contactado"),
        ("en_proceso", "En proceso"),
        ("cerrado", "Cerrado"),
    ]

    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    empresa = models.CharField(max_length=255)
    mensaje = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="nuevo",
    )
    ip_origen = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.nombre} - {self.empresa} ({self.estado})"
