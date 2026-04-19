from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count, Sum, Case, When, IntegerField
from django.db.models.functions import TruncMonth
import requests
import json

from app.models import Profile, Restaurant, Comment
from .forms import RestaurantForm, CommentForm


def home(request):
    restaurants = Restaurant.objects.all().order_by('-created_at')

    city = request.GET.get('city')
    min_ratio = request.GET.get('min_ratio')

    if city:
        restaurants = restaurants.filter(city__icontains=city)

    restaurant_data = []

    for restaurant in restaurants:
        comments = Comment.objects.filter(restaurant=restaurant)
        total_comments = comments.count()
        positive_comments = comments.filter(sentiment=1).count()
        negative_comments = comments.filter(sentiment=0).count()

        ratio = 0
        if total_comments > 0:
            ratio = positive_comments / total_comments

        if min_ratio:
            try:
                if ratio < float(min_ratio):
                    continue
            except ValueError:
                pass

        restaurant_data.append({
            'restaurant': restaurant,
            'positive_comments': positive_comments,
            'negative_comments': negative_comments,
            'ratio': ratio,
        })

    return render(request, 'app/home.html', {
        'restaurant_data': restaurant_data
    })


@login_required
def add_restaurant(request):
    if request.user.profile.role != 'owner':
        return redirect('/')

    restaurant = Restaurant.objects.filter(owner=request.user).first()

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            return redirect('/')
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'app/add_restaurant.html', {'form': form})


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    comments = Comment.objects.filter(restaurant=restaurant).order_by('-created_at')

    total_comments = comments.count()
    positive_comments = comments.filter(sentiment=1).count()
    negative_comments = comments.filter(sentiment=0).count()

    ratio = 0
    if total_comments > 0:
        ratio = positive_comments / total_comments

    comment_form = CommentForm()

    return render(request, 'app/restaurant_detail.html', {
        'restaurant': restaurant,
        'comments': comments,
        'positive_comments': positive_comments,
        'negative_comments': negative_comments,
        'ratio': ratio,
        'comment_form': comment_form,
    })


@login_required
def add_comment(request, restaurant_id):
    if request.user.profile.role != 'visitor':
        return redirect('/')

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']

            response = requests.post(
                settings.AZURE_ENDPOINT_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.AZURE_ENDPOINT_KEY}"
                },
                json={"review": text}
            )

            result = response.json()
            sentiment = result["sentiment"]

            Comment.objects.create(
                restaurant=restaurant,
                user=request.user,
                text=text,
                sentiment=sentiment
            )

    return redirect(f'/restaurants/{restaurant.id}/')


@login_required
def owner_statistics(request):
    if request.user.profile.role != 'owner':
        return redirect('/')

    restaurant = Restaurant.objects.filter(owner=request.user).first()
    if not restaurant:
        return redirect('/restaurants/add/')

    comments = Comment.objects.filter(restaurant=restaurant)

    positive_comments = comments.filter(sentiment=1).count()
    negative_comments = comments.filter(sentiment=0).count()

    monthly_stats = (
        comments
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total=Count('id'),
            positive=Sum(
                Case(
                    When(sentiment=1, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        .order_by('month')
    )

    line_labels = []
    line_data = []
    bar_labels = []
    bar_data = []

    cumulative = 0

    for row in monthly_stats:
        month_label = row['month'].strftime('%Y-%m')
        total = row['total']
        positive = row['positive'] or 0

        cumulative += total
        positive_ratio = positive / total if total > 0 else 0

        line_labels.append(month_label)
        line_data.append(cumulative)

        bar_labels.append(month_label)
        bar_data.append(round(positive_ratio, 2))

    context = {
        'restaurant': restaurant,
        'positive_comments': positive_comments,
        'negative_comments': negative_comments,
        'line_labels': json.dumps(line_labels),
        'line_data': json.dumps(line_data),
        'bar_labels': json.dumps(bar_labels),
        'bar_data': json.dumps(bar_data),
    }

    return render(request, 'app/owner_statistics.html', context)