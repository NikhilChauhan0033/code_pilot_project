# code_pilot_app/context_processors.py

# created a seprate file for globally show the cart total inside code_pilot_app name context_processors.py and also add in setting.py

# we here define the cart total to globally so we can use it anywehere where we want to use 
# use only this <p>Total: ₹{{ cart_total|floatformat:2 }}</p>

# we define here over globally uses data

from .models import Cart,Course, Instructor

def cart_total_processor(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.course.price for item in cart_items)
        return {'cart_total': total}
    return {'cart_total': 0}

# define globally all the courses and instruvtors details

def global_data(request):
    return {
        'courses': Course.objects.all()[:4],
        'instructors': Instructor.objects.all()[:4],
        'allcourses': Course.objects.all(),
    }
