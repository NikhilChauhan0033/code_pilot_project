from django.contrib import admin
from django.urls import path
from code_pilot_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('verify-admin/', views.verify_admin_key, name='verify-admin'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('instructor/<int:instructor_id>/', views.instructor_detail, name='instructor_detail'),
    path('instructors', views.instructors, name='instructors'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("cart/load_snippet/", views.load_cart_snippet, name="load_cart_snippet"),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout-history/', views.checkout_history, name='checkout_history'),
    path('favorite/toggle/<int:course_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites/remove/<int:course_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('about_us/',views.about_us,name='about_us'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('search_course/', views.search_course_redirect, name='search_course_redirect'),
    path('courses/', views.courses, name='courses'),
    path('subscribe/', views.subscribe_email, name='subscribe_email'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
