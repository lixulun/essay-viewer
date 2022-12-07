from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from essay.models import Essay
from markdown import markdown


@login_required
def index(request):
    return render(
        request,
        "essay/index.html",
        context={"essays": Essay.objects.order_by("-publish_date").all()},
    )


@login_required
def detail(request, identity):
    essay = get_object_or_404(Essay, identity=identity)
    return render(
        request,
        "essay/detail.html",
        context={"essay": essay, "formatted_content": markdown(essay.content)},
    )
