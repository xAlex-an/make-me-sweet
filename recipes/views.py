from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Recipe

# Create your views here.
class RecipeList(generic.ListView):
    """Generic class-based view for a list of recipes."""
    queryset = Recipe.objects.filter(status=1)
    template_name = "recipes/index.html"
    paginate_by = 6

def recipes_detail(request, slug):
    """
    Display an individual :model:`recipes.Recipe` instance.

    Context:
        recipe -- An instance of :model:`recipes.Recipe`

    Template:
        recipes/recipes_detail.html
    """
    queryset = Recipe.objects.filter(status=1)  
    recipe = get_object_or_404(queryset, slug=slug)  
    return render(request, "recipes/recipes_detail.html", {"recipe": recipe})

