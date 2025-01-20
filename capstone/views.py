import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Show, Rating, Review
from .forms import ReviewForm

def index(request, showpage=None, query=None):
    if showpage == 'favorites':
        shows = request.user.favorites.all().order_by('title')
    elif showpage == 'recommendations':
        # top 10 highest avg rating
        shows = Show.objects.all().order_by('-average_rating')[:10]
    elif showpage == 'search_results':
        query = request.GET.get('q')
        shows = Show.objects.filter(title__icontains=query).order_by('title')
    else:
        shows = Show.objects.all().order_by('title')
        
    for show in shows:
        show.update_average_rating()
        show.total_ratings = show.ratings.count()
        
    paginator = Paginator(shows, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "capstone/index.html", {"shows": shows, "showpage": showpage, "page_obj": page_obj, "query": query})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")
    
def profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    # Retrieve the user's posts in reverse chronological order
    user_shows = Show.objects.filter(creator=user_profile).order_by('title')

    return render(request, "capstone/profile.html", {
        "user_profile": user_profile,
        "user_shows": user_shows,
    })

@login_required
def new_show(request):
    if request.method == "POST":
        # form submission
        creator = request.user
        title = request.POST.get("add-show-title")
        description = request.POST.get("add-show-description")
        genre = request.POST.get("add-show-genre")
        image_url = request.POST.get("add-show-image")
        new_show = Show(creator=creator,title=title,description=description,genre=genre, image_url=image_url)
        new_show.save()
        return HttpResponseRedirect(reverse("show_view", args=[new_show.id]))
    else:
        return render(request, "capstone/new_show.html")
    
def show_view(request, show_id):
    show =  Show.objects.get(pk=show_id)
    reviews = Review.objects.filter(show=show).order_by("-created_at")

    review_form = ReviewForm()
    if request.method == "POST":
        if "review_form_submit" in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                text = review_form.cleaned_data["text"]
                review = Review(show=show, user=request.user, text=text)
                review.save()
                return HttpResponseRedirect(reverse("show_view", args=[show_id]))
        elif "favorites_submit" in request.POST:
            if request.user.is_authenticated:
                if show in request.user.favorites.all():
                    request.user.favorites.remove(show)
                    show.favorites.remove(request.user)
                else:
                    request.user.favorites.add(show)
                    show.favorites.add(request.user)
            return HttpResponseRedirect(reverse("show_view", args=[show_id]))
    
    is_in_favorites = show in request.user.favorites.all() if request.user.is_authenticated else False

    show.update_average_rating()
    total_ratings = show.ratings.count()

    return render(request, "capstone/show_page.html", {
        "show": show,
        "reviews": reviews,
        "review_form": review_form,
        "is_in_favorites": is_in_favorites,
        "average_rating": show.average_rating,
        "total_ratings": total_ratings
    })

@login_required
def remove_from_favorites(request, show_id):
    show = Show.objects.get(pk=show_id)
    request.user.favorites.remove(show)
    return HttpResponseRedirect(reverse("favorites"))

@login_required
def edit_show(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    show_id = data.get("show_id")
    edited_description = data.get("description")

    show = Show.objects.get(id=show_id)

    show.description = edited_description
    show.save()

    return JsonResponse({"success": True})

@login_required
def rate_show(request, show_id):
    if request.method == 'POST':
        show = Show.objects.get(pk=show_id)
        data = json.loads(request.body)
        stars = data.get('stars')

        if stars:
            stars = int(stars)
            # Check if the user has already rated this show
            existing_rating = Rating.objects.filter(user=request.user, rated_show=show).first()

            if existing_rating:
                # If there's an existing rating, update it with the new stars
                existing_rating.stars = stars
                existing_rating.save()
            else:
                # If no existing rating, create a new one
                new_rating = Rating(user=request.user, rated_show=show, stars=stars)
                new_rating.save()

            show.update_average_rating()
            print(type(show.average_rating))
            total_ratings = show.ratings.count()

            return JsonResponse({
                "success": True,
                "average_rating": show.average_rating,
                "total_ratings": total_ratings
            })
        else:
            return JsonResponse({"error": "Stars field is missing in the request."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)


# def search(request):
#     query_title = request.GET.get("q")
#     if query_title:
#         exact_show = util.get_show(query)
#         if exact_show:
#             return redirect(reverse("show", args=[query]))
#         else:
#             matching_entries = [
#                 show for show in util.list_entries() if query.lower() in show.titlelower()]
#             return render(request, "capstone/index.html", {
#                 "search_results": matching_entries
#             })
#     else:
#         return redirect("index")