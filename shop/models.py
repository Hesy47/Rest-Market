from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import os


class SingleImageHandler(models.Model):
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


class Category(SingleImageHandler):
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

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shop-categories"


class DesktopBanner(SingleImageHandler):
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

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shop-desktop-banners"


class MobileBanner(SingleImageHandler):
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

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shop-mobile-banners"


class Product(models.Model):
    """The Product database model"""

    title = models.CharField(
        max_length=60,
        unique=True,
        error_messages={"unique": "Product with this title is already exist"},
    )

    price = models.DecimalField(max_digits=12, decimal_places=0)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, models.CASCADE)
    owner = models.ForeignKey(get_user_model(), models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shop-products"
