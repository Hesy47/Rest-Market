from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files.base import ContentFile
import os


class Category(models.Model):
    """The category database model"""

    title = models.CharField(
        max_length=40,
        unique=True,
        error_messages={"unique": "Category with this title is already exist"},
    )

    image = models.ImageField(upload_to="images/category")

    def clean(self):
        if self.image and self.image.size() > 1 * 1024 * 1024:
            raise ValidationError("The Image size must be less than 1MB")

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)

                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")

                temp_img = BytesIO()
                img.save(temp_img, format="WEBP", quality=75, optimize=True)
                temp_img.seek(0)

                base_name = os.path.splitext(self.image_title.lower())[0]
                file_name = f"{base_name}.webp"

                self.image.save(file_name, ContentFile(temp_img.read()), save=False)

            except (OSError, UnidentifiedImageError) as e:
                raise ValueError(f"The uploaded file is not a valid image. -- {e}")

        super().save(*args, **kwargs)
