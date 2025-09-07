from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files.base import ContentFile
import os


class ApplicationImageHandler(models.Model):
    """The base abstract model to handel application image processing"""

    class Meta:
        abstract = True

    image_field = "image"
    image_name_field = "image_name"

    def clean(self):
        image = getattr(self, self.image_field, None)
        if image and image.size > 1 * 1024 * 1024:
            raise ValidationError("The image size must be less than 1MB")

    def save(self, *args, **kwargs):
        image = getattr(self, self.image_field, None)
        image_name = getattr(self, self.image_name_field, None)

        if image:
            try:
                img = Image.open(image)

                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")

                temp_img = BytesIO()
                img.save(temp_img, format="WEBP", quality=80, optimize=True)
                temp_img.seek(0)

                base_name = os.path.splitext(image_name.lower())[0]
                file_name = f"{base_name}.webp"

                image.save(file_name, ContentFile(temp_img.read()), save=False)

            except (OSError, UnidentifiedImageError) as e:
                raise ValueError(f"The uploaded file is not a valid image,\nerror: {e}")

        super().save(*args, **kwargs)


class Category(ApplicationImageHandler):
    """The category database model"""

    title = models.CharField(
        max_length=40,
        unique=True,
        error_messages={"unique": "Category with this title is already exist"},
    )

    image_name = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"unique": "Category with this title is already exist"},
    )

    image = models.ImageField(upload_to="images/categories")

    class Meta:
        db_table = "shop-categories"


class DesktopBanner(ApplicationImageHandler):
    """The desktop banner database model"""

    title = models.CharField(
        max_length=40,
        unique=True,
        error_messages={"unique": "Desktop Banner with this title is already exist"},
    )

    image_name = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"unique": "Desktop Banner with this title is already exist"},
    )

    image = models.ImageField(upload_to="images/DesktopBanners")

    def clean(self):
        if self.image and self.image.size > 4 * 1024 * 1024:
            raise ValidationError("The image size must be less than 4MB")

        if self.image and self.image.width < 1600:
            raise ValidationError("Image width must between 1600 and 1603")

        if self.image and self.image.width > 1603:
            raise ValidationError("Image width must between 1600 and 1603")

        if self.image and self.image.height < 400:
            raise ValidationError("Image height must between 400 and 403")

        if self.image and self.image.height > 403:
            raise ValidationError("Image height must between 400 and 403")

    class Meta:
        db_table = "shop-desktop-banners"


class MobileBanner(ApplicationImageHandler):
    """The Mobile banner database model"""

    title = models.CharField(
        max_length=40,
        unique=True,
        error_messages={"unique": "Desktop Banner with this title is already exist"},
    )

    image_name = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"unique": "Desktop Banner with this title is already exist"},
    )

    image = models.ImageField(upload_to="images/DesktopBanners")

    def clean(self):
        super().clean()

        if self.image and self.image.width < 720:
            raise ValidationError("Image width must between 720 and 723")

        if self.image and self.image.width > 723:
            raise ValidationError("Image width must between 720 and 723")

        if self.image and self.image.height < 180:
            raise ValidationError("Image height must between 180 and 183")

        if self.image and self.image.height > 183:
            raise ValidationError("Image height must between 180 and 183")

    class Meta:
        db_table = "shop-mobile-banners"
