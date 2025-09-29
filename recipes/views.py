from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Recipe, Comment
from .forms import CommentForm


# Create your views here.
class RecipeList(generic.ListView):
    """Generic class-based view for a list of recipes."""
    queryset = Recipe.objects.filter(status=1)
    paginate_by = 6
    
    def get_template_names(self):
        """
        Return different templates based on page number.
        First page shows full index.html with all sections,
        subsequent pages show only recipes_list.html
        """
        page = self.request.GET.get('page', '1')
        try:
            page_num = int(page)
        except (ValueError, TypeError):
            page_num = 1
            
        if page_num == 1:
            return ["recipes/index.html"]
        else:
            return ["recipes/recipes_list.html"]


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
    comments = recipe.comments.all().order_by("-created_on")
    comment_count = recipe.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.recipe = recipe
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'We’ve got your comment — it’ll be visible once approved ✨'
            )
            comment_form = CommentForm()
        else:
            comment_form = CommentForm(data=request.POST)
    else:
        comment_form = CommentForm()

    return render(
        request,
        "recipes/recipes_detail.html",
        {
            "recipe": recipe,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    Context:
        comment -- An instance of :model:`recipes.Comment`
    Template:
        recipes/recipes_detail.html

    """
    if request.method == "POST":

        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been updated successfully!')
        else:
            messages.add_message(request, messages.ERROR, 'Oops! There was a problem updating your comment.')

    return HttpResponseRedirect(reverse('recipes_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Recipe.objects.filter(status=1)
    recipe = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('recipes_detail', args=[slug]))