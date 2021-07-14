from django.db import models


class ProductTypes(models.TextChoices):
    """
        different types of products
    """
    JPEG = 'JPEG', 'Picture With Normal Quality'
    PSD = 'PSD', 'Photoshop File'
    AI = 'AI', 'Illustrator File'
    TEXT = 'TEXT', 'A Word File'
    PRINT = 'PRINT', 'Print On Paper'
