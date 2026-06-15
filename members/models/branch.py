from django.db import models

class Branch(models.Model):
    Cities = [
        ("tanta", "Tanta"),
        ("cairo", "Cairo"),
        ("alexandria", "Alexandria"),
        ("mansura", "Mansura"),
        ("suez", "Suez"),
        ("north_sinai", "North_Sinai"),
        ("boston", "Boston"),
        ("london", "London"),
        ("berlin", "Berlin"),
        ("barcelona", "Barcelona"),
        ("moscow", "Moscow"),
        ("stockholm", "Stockholm")
    ]
    branch_name = models.CharField(max_length=100, unique=True, default="cario")
    city = models.CharField(max_length=100, blank=False, null=False, choices=Cities)

    def __str__(self):
        return f"{self.branch_name} in {self.city} city"