from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))


class Recipe(models.Model):
    """
    Model representing a recipe with all necessary fields
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    excerpt = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} | written by {self.author}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
