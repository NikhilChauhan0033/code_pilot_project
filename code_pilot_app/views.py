from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash  # Keeps user logged in after password change
from .models import Course, Instructor, Cart, Checkout, Favorite,ContactMessage,Subscriber # import your model
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q #for search functionality 


ADMIN_SECRET_KEY = 'superadmin123'  # Hardcoded secret key

# decoraters for unautorized access
def login_required_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please login or register to access this page.")
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('index')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            request.session['open_modal'] = 'register'
            return redirect('index')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            request.session['open_modal'] = 'register'
            return redirect('index')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            request.session['open_modal'] = 'register'
            return redirect('index')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful. Please log in.")
        request.session['open_modal'] = 'login'  # Open login modal after registration
        return redirect('index')

    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        identifier = request.POST['identifier'].strip()
        password = request.POST['password']

        user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()
        print(user)

        if user:
            user = authenticate(username=user.username, password=password)
            if user:
                auth_login(request, user)
                messages.success(request, f"Welcome, {user.username}!")

                # Check if the user is a superuser
                if user.is_superuser:
                    request.session['admin_verified'] = False
                    messages.info(request, "Please verify your admin key.")
                    return redirect('verify-admin')  # ask for admin key
                else:
                    request.session['admin_verified'] = True
                    request.session['open_modal'] = None
                    return redirect('index') #user redirects to index page
            else:
                messages.error(request, "Incorrect password.")
                request.session['open_modal'] = 'login'
        else:
            messages.error(request, "User not found.")
            request.session['open_modal'] = 'login'

        return redirect('index')

    return render(request, 'index.html')

@login_required_redirect
def verify_admin_key(request):
    if request.method == 'POST':
        key = request.POST.get('key', '').strip()
        if key == ADMIN_SECRET_KEY:
            request.session['admin_verified'] = True
            messages.success(request, "Admin verified successfully.")
            return redirect('index')  # or wherever you want
        else:
            messages.error(request, "Invalid admin key.")
            return redirect('verify-admin')

    return render(request, 'verify_admin.html')


def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')


@login_required_redirect
def profile(request):
    if request.user.is_superuser:
        messages.error(request, "Admins are not allowed to update their profile.")
        return redirect('index')

    if request.method == 'POST':
        new_username = request.POST['username'].strip()
        new_email = request.POST['email'].strip()
        old_password = request.POST.get('old_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not new_username or not new_email:
            messages.error(request, "Username and Email are required.")
            return redirect('profile')

        if User.objects.exclude(id=request.user.id).filter(username=new_username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('profile')
        if User.objects.exclude(id=request.user.id).filter(email=new_email).exists():
            messages.error(request, "Email is already used.")
            return redirect('profile')

        request.user.username = new_username
        request.user.email = new_email

        if new_password:
            if not old_password:
                messages.error(request, "Please enter your old password to set a new one.")
                return redirect('profile')

            if not request.user.check_password(old_password):
                messages.error(request, "Old password is incorrect.")
                return redirect('profile')

            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect('profile')

            request.user.set_password(new_password)
            update_session_auth_hash(request, request.user)  # Keep user logged in

        request.user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'profile.html')


def index(request): #we also use this [{% for course in courses|slice:":4" %} in templates for show only 4 courses]
    courses = Course.objects.all()[:4]  # fetch all courses 
    instructors = Instructor.objects.all()[:4]  # fetch all instructors
    return render(request, 'index.html', {'courses': courses, 'instructors': instructors})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

def instructor_detail(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'instructor_detail.html', {'instructor': instructor})

@login_required_redirect
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, course=course)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({'status': 'success', 'added': created, 'count': count})

    return redirect('course_detail', course_id=course.id)


@login_required_redirect
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.course.price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required_redirect
def remove_from_cart(request, item_id):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item = get_object_or_404(Cart, id=item_id, user=request.user)
        item.delete()
        count = Cart.objects.filter(user=request.user).count()

        total = sum(i.course.price for i in Cart.objects.filter(user=request.user))

        return JsonResponse({'status': 'success', 'count': count,'total': total})
    
    return redirect(request.META.get('HTTP_REFERER', 'view_cart'))

# created a seprate file for globally show the cart total inside code_pilot_app name context_processors.py and also add in setting.py


@login_required_redirect
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    course_id = request.GET.get('course_id')
    single_course = None

    if not cart_items and course_id:
        single_course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('checkout')

        if cart_items:
            for item in cart_items:
                Checkout.objects.create(
                    user=request.user,
                    course=item.course,
                    price=item.course.price,
                    payment_method=payment_method
                )
            cart_items.delete()
        elif single_course:
            Checkout.objects.create(
                user=request.user,
                course=single_course,
                price=single_course.price,
                payment_method=payment_method
            )

        messages.success(request, "Checkout successful!")
        return redirect('checkout_history')

    total = sum(item.course.price for item in cart_items) if cart_items else (single_course.price if single_course else 0)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'single_course': single_course,
        'total': total
    })

@login_required_redirect
def checkout_history(request):
    checkout_items = Checkout.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'checkout_history.html', {'checkout_items': checkout_items})


@login_required_redirect
def toggle_favorite(request, course_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        course = get_object_or_404(Course, id=course_id)
        fav, created = Favorite.objects.get_or_create(user=request.user, course=course)

        if not created:
            fav.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})

@login_required_redirect
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': favorites})


@login_required_redirect
def remove_from_favorites(request, course_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        fav = Favorite.objects.filter(user=request.user, course_id=course_id).first()
        if fav:
            fav.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'not_found'})
    return redirect('view_favorites')

def about_us(request):
    return render(request,'about_us.html')

# contact form
# @login_required_redirect
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, "✅ Thank you! We will connect with you shortly.")
            return redirect('contact_us')
        else:
            messages.error(request, "❌ Please fill all required fields.")

    return render(request, 'contact_us.html')

@login_required_redirect
def load_cart_snippet(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.course.price for item in cart_items)
    html = render_to_string("partials/cart_snippet.html", {
        "cart_items": cart_items,
        "cart_total": total,
    }, request=request)

    return JsonResponse({'html': html})

def search_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        courses = Course.objects.filter(course_name__icontains=query)
        data = [{'id': c.id, 'name': c.course_name} for c in courses]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def search_course_redirect(request):
    query = request.GET.get('q', '')
    if query:
        course = Course.objects.filter(course_name__icontains=query).first()
        if course:
            return redirect('course_detail', course_id=course.id)
    return redirect('index')

def instructors(request):
    all_instructors = Instructor.objects.all()
    return render(request,'instructors.html',{"all_instructors":all_instructors})

def courses(request):
    all_courses = Course.objects.all()
    return render(request,'courses.html',{"all_courses":all_courses})

def subscribe_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not Subscriber.objects.filter(email=email).exists():
                Subscriber.objects.create(email=email)
                messages.success(request, "✅ Subscribed successfully!")
            else:
                messages.info(request, "ℹ️ You are already subscribed.")
        else:
            messages.error(request, "❌ Please enter a valid email.")

        return redirect(request.META.get('HTTP_REFERER', '/'))
    

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)