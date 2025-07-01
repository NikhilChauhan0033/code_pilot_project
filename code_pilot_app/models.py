# Create your models here.

# """
# 🧠 What happens during register:
# Django saves the username, email, password (hashed), and timestamps into the auth_user table.

# 🧠 What happens during login:
# Django checks the username or email and password against the entries in the same auth_user table.

# If successful, Django updates the last_login field.

# If you later add profile fields like bio, image, etc., you'll typically do it via a custom user model or UserProfile model linked with a OneToOneField — which would go into another table.

# Let me know if you want to create your own user profile model to store more custom fields!
# """


from django.db import models
from django.contrib.auth.models import User



class Instructor(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=200)
    about = models.TextField()
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    rating = models.FloatField()
    profile_image = models.ImageField(upload_to='instructors/', null=True, blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('full_stack', 'Full Stack Development'),
        ('mobile_app', 'Mobile App Development'),
        ('data_science', 'Data Science'),
        ('data_analytics', 'Data Analytics'),
        ('software_testing', 'Software Testing'),
        ('digital_marketing', 'Digital Marketing'),
        ('ux_ui', 'UX/UI Design'),
        ('cyber_security', 'Cyber Security'),
    ]

    SUBCATEGORY_CHOICES = [
        # Full Stack
        ('mern_stack', 'MERN Stack'),
        ('python_stack', 'Python Stack'),
        ('java_stack', 'Java Stack'),
        ('dotnet_stack', 'DotNet Stack'),

        # Mobile App
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('flutter_app', 'Flutter App'),
        ('flutter_app_development', 'Flutter App Development'),

        # Data Science
        ('data_science_training', 'Data Science Training'),
        ('machine_learning_training', 'Machine Learning Training'),

        # Data Analytics
        ('data_analytics_training', 'Data Analytics Training'),
        ('business_analytics_training', 'Business Analytics Training'),

        # Software Testing
        ('software_testing_training', 'Software Testing Training'),
        ('selenium_automation_training', 'Selenium Automation Training'),
        ('manual_testing_training', 'Manual Testing Training'),

        # Digital Marketing
        ('digital_marketing_training', 'Digital Marketing Training'),

        # UX/UI Design
        ('ux_ui_training', 'UX-UI Training'),

        # Cyber Security
        ('ethical_hacking_training', 'Ethical Hacking Training'),
    ]

    course_name = models.CharField(max_length=200)
    short_description = models.TextField()
    long_description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    learning_outcomes = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    duration = models.CharField(max_length=50)
    students_enrolled = models.PositiveIntegerField()
    language = models.CharField(max_length=50)
    certification = models.CharField(max_length=100)
    rating = models.FloatField()
    promo_video = models.FileField(upload_to='course_videos/', blank=True, null=True)  # FileField for manual upload
    technologies_covered = models.TextField()
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField()
    badge = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)  # e.g., Beginner, Intermediate, Advanced
    lessons_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course_name} ({self.get_category_display()})"

    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.course_name}"

class Checkout(models.Model):
    PAYMENT_CHOICES = (
        ('upi', 'UPI'),
        ('paytm', 'Paytm'),
        ('phonepe', 'PhonePe'),
        ('card', 'Credit/Debit Card'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES,default='upi')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.course_name} - {self.payment_method}"

    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')  # Prevent duplicates

# contact page 
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
# email subscription model in footer
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email