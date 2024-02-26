from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

from .forms import EditUserProfileForm, ProductForm
from .models import Banner_area, Category, Product, Review, Reply, Rating, Favorite
import json
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.shortcuts import render
from django.db.models import Q, Avg


# Create your views here.
def base(request):
    return render(request, "base.html")


def home(request):
    category = Category.objects.all()
    banner = Banner_area.objects.all()
    product = Product.objects.all()

    context = {'products': product, 'banner': banner, 'category': category}

    return render(request, "home.html", context)


def shop(request):
    category = Category.objects.all()
    banner = Banner_area.objects.all()
    product = Product.objects.all()
    context = {'products': product, 'banner': banner, 'category': category, }

    return render(request, "product_view.html", context)


def shop_filter(request):
    is_error = False
    data = None

    if request.method == 'POST':
        jsondata = json.loads(request.body.decode("utf-8"))
        req = jsondata.get('categories', [])  # default to an empty list if 'categories' key is missing
        if req:  # If 'categories' is not empty
            product = Product.objects.filter(categories__id__in=req).distinct()
        else:
            product = Product.objects.all()

        if not product.exists():  # Check if any products are found
            is_error = True

        context = {'products': product, 'is_error': is_error}
        data = render_to_string('includes/ajax/product_filter.html', context)

    return JsonResponse({"status": "Success", "data": data})


def filter_category(request):
    data = None  # Initialize data variable outside the if block

    if request.method == "POST":
        jsondata = json.loads(request.body.decode("utf-8"))
        req = jsondata.get('categories')
        product = Product.objects.filter(categories__id__in=req).distinct()
        context = {
            "products": product,
        }
        data = render_to_string('includes/ajax/product_filter.html', context)
        print(product)

    # Return the rendered HTML directly without wrapping it in a JSON response
    return JsonResponse({"status": "success", "data": data})


def product_details(request, id):
    product = Product.objects.get(id=id)
    reviews = Review.objects.all().order_by("-id")
    reply = Reply.objects.all().order_by("-id")
    ratings = Rating.objects.filter(prod_parent=product)
    avg_rating = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
    avg_rating = round(avg_rating, 1) if avg_rating is not None else 0.0

    product.avg_rating = avg_rating
    product.save()

    context = {'products': product, "reviews": reviews, "reply": reply, "rating": ratings, "avg": avg_rating}
    return render(request, "product_details.html", context)


from django.shortcuts import get_object_or_404


def product_details_slug(request, slug):
    # Retrieve the product with the given slug or return a 404 error if not found
    product = get_object_or_404(Product, slug=slug)

    # Prefetch related reviews and ratings to minimize database hits
    product_reviews = product.review_set.order_by("-id").all()
    product_ratings = product.rating_set.all()

    # Calculate average rating for the product
    avg_rating = product_ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
    avg_rating = round(avg_rating, 1) if avg_rating is not None else 0.0

    # Update average rating in the product instance
    product.avg_rating = avg_rating

    # Context data to pass to the template
    context = {
        'product': product,
        'reviews': product_reviews,
        'avg_rating': avg_rating,
    }

    # Render the template with the context data
    return render(request, "product_details.html", context)


def user_account(request):
    return render(request, "user_account.html")


from django.http import JsonResponse
from django.contrib.auth.models import User


def user_validate(request, username, field):
    if field == "username":
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            return JsonResponse({'status': 'error', 'message': 'Username already taken!'})
        else:
            return JsonResponse({'status': 'success', 'message': ''})
    elif field == "email":
        user_exists = User.objects.filter(email=username).exists()
        if user_exists:
            return JsonResponse({'status': 'error', 'message': 'this email is already registered, try logging in!'})
        else:
            return JsonResponse({'status': 'success', 'message': ''})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid field type specified.'})


def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("userpass")

        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            user = User.objects.create_user(username=username, first_name=fname, last_name=lname, email=email,
                                            password=password)
            messages.success(request, "User Credentials registered, glad to know u joined us !")
            return redirect("LogIn")  # Redirect to success page or any other page after successful registration

    return render(request, "user_account.html")  # Render the registration form page


def LogIn(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        if '@' in username:
            user = authenticate(email=username, password=password)
        else:
            user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return render(request, 'admin_panel.html')
            else:
                login(request, user)
                messages.success(request, "Successfully logged in ! ")
                return redirect("home")


        else:
            # Authentication failed, handle error (e.g., display error message)
            error_message = "Invalid credentials, try again ..."
            return render(request, "login.html", {'error_message': error_message})

    return render(request, "login.html")


def LogOut(request):
    logout(request)
    messages.success(request, "Successfully Logged Out ! ,take care , see u later !")
    return redirect("index")


def index(request):
    user = request.user
    category = Category.objects.all()
    banner = Banner_area.objects.all()
    product = Product.objects.all()

    context = {'banner': banner, 'category': category, 'products': product}
    if user.is_authenticated:
        return redirect('home')
    else:
        return render(request, "index.html", context)


def review(request):
    if request.method == "POST":
        name = request.user
        prod_id = request.POST.get("prod_id")
        reviews = request.POST.get("reviews")

        rev = Review(name=name, prod_parent=prod_id, review=reviews)
        rev.save()
        messages.success(request, "review successfully added")

    return redirect(f"product_details/{prod_id}")


def replies(request, id):
    rev = Review.objects.get(id=id)
    if request.method == "POST":
        name = request.user
        rev_id = request.POST.get("rev_id")
        review_parent_id = request.POST.get("review_parent_id")  # Assuming this is the ID of the parent review
        reply_text = request.POST.get("reply")  # Assuming this is the reply text

        # Create a new Reply object with the provided data
        rep = Reply(name=name, review_parent_id=review_parent_id, reply=reply_text)
        rep.save()
        messages.success(request, "Comment successfully added")

    return redirect(f"product/{rev_id}")


def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request, "user profile updated successfully")
        else:
            fm = EditUserProfileForm(instance=request.user)
        return render(request, "profile.html", {"name": request.user, "form": fm})
    else:
        return redirect('LogIn')


from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render


def changepass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, "User password changed successfully")
                return redirect('LogIn')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, "profile.html", {"name": request.user, "form": fm})
    else:
        return redirect('LogIn')


def rating(request):
    if request.method == 'POST':
        user = request.user
        prod_id = request.POST.get('rate_id')
        rating_value = request.POST.get('rate')
        product = Product.objects.get(id=prod_id)
        data = Rating(user=user, prod_parent=product, rating=rating_value)
        messages.success(request, "rated movie successfully !")
        data.save()

    return redirect(f"product_details/{prod_id}")


# Create your views here.


def search(request):
    products = None
    query = None
    if 'q' in request.POST:
        query = request.POST.get('q')
        products = Product.objects.all().filter(Q(title__contains=query) | Q(description__contains=query))
        print(products)
    return render(request, 'search.html', {'query': query, 'products': products})


from django.shortcuts import get_object_or_404


def favorites(request):
    if request.method == "POST":
        user_id = request.user.id
        rev = request.POST.get("fav_id")

        print(rev, user_id)

        # Check if a favorite entry already exists for this user and product combination
        existing_favorite = Favorite.objects.filter(user=user_id, product=rev).exists()

        if not existing_favorite:
            fav = Favorite(user=user_id, product=rev)
            fav.save()
            messages.success(request, "movie added to Favorites")

    return redirect(f"product_details/{rev}")


def fav_view(request):
    fav = Favorite.objects.all()
    products = Product.objects.all()
    context = {
        "fav": fav, "products": products
    }
    return render(request, "favorites.html", context)


# views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Favorite


def delete_favorite(request):
    if request.method == 'POST':
        favorite_id = request.POST.get('fav_id')
        favorite = Favorite.objects.get(id=favorite_id)
        favorite.delete()
        messages.success(request, " movie removed from favorites !")
        return redirect('fav_view')  # Redirect to the user's profile page or wherever you want
    return redirect(f"fav_view")


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # If you have a logged-in user and want to set it as the creator, you can do so here
            if request.user.is_authenticated:
                product.creator = request.user.id
            product.save()
            form.save_m2m()
            messages.success(request, " movie model created successfully ")  # Save the many-to-many relationships
            return redirect('my_product_view')  # Redirect to a success page
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def my_product_view(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "my_product.html", context)


# views.py

def delete_product(request):
    if request.method == 'POST':
        favorite_id = request.POST.get('fav_id')
        favorite = Product.objects.get(id=favorite_id)
        favorite.delete()
        messages.success(request, "one movie deleted")
        return redirect('my_product_view')  # Redirect to the user's profile page or wherever you want
    return redirect(f"my_product_view")


def delete_product_all(request):
    if request.method == 'POST':
        favorite_id = request.POST.get('fav_id')
        favorite = Product.objects.get(id=favorite_id)
        favorite.delete()
        messages.success(request, "one movie deleted")
        return redirect('all_product_view')  # Redirect to the user's profile page or wherever you want
    return redirect(f"all_product_view")


def cat_add(request):
    cat = Category.objects.all()
    if request.method == "POST":

        cat_name = request.POST.get('cat_name')
        cat_slug = request.POST.get('cat_slug')

        category = Category(name=cat_name, slug=cat_slug)
        if category:
            category.save()
    context = {
        "category": cat,
    }
    return render(request, "add_category.html", context)


def cat_del(request, id):
    cat = Category.objects.all()

    categories = Category.objects.get(id=id)
    if categories:
        categories.delete()
        return redirect(f'cat_add')

    context = {
        "category": cat,
    }
    return render(request, "add_category.html", context)


def all_product_view(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "all_movie.html", context)


def user_view(request):
    users = User.objects.all().order_by("-id")
    context ={
        "users":users,
    }
    return render(request, "all_users.html", context)


def user_delete(request,id):
    usr = User.objects.get(id=id)
    if usr:
        usr.delete()
        return redirect('user_view')

    return redirect('user_view')


def admin_home(request):
    return render(request,"admin_panel.html")

