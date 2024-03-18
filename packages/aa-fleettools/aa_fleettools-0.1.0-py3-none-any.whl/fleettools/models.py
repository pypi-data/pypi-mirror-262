from django.db import models


class ResetButton(models.Model):
    wing_name = models.CharField(max_length=255)
    squad_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.wing_name} - {self.squad_name}"

    class Meta:
        default_permissions = ()
        constraints = [
            models.UniqueConstraint(
                fields=['wing_name', 'squad_name'],
                name='unique_wing_squad'
            ),
        ]
