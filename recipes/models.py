from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))

# Tag choices for recipe badges
TAG_CHOICES = [
    ('autumn', '🍂 Autumn Special'),
    ('winter', '❄️ Winter Warmth'),
    ('spring', '🌸 Spring Fresh'),
    ('summer', '☀️ Summer Delight'),
    ('holiday', '🎄 Holiday Favorite'),
    ('quick', '⚡ Quick & Easy'),
    ('healthy', '🥗 Healthy Choice'),
    ('decadent', '💎 Indulgent Treat'),
    ('classic', '👑 Classic Recipe'),
    ('new', '✨ New Recipe'),
    ('popular', '🔥 Popular Choice'),
    ('', 'No Tag'),  # Option for no tag
]


class Recipe(models.Model):
    """
    Model representing a recipe with all necessary fields
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    excerpt = models.TextField(blank=True)
    tag = models.CharField(
        max_length=20,
        choices=TAG_CHOICES,
        blank=True,
        default='',
        help_text="Choose a tag to display as a badge on the recipe"
    )
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"{self.title} | written by {self.author}"


class Comment(models.Model):
    """
    Model representing a comment on a recipe
    """
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"