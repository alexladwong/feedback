# feedback/views.py

from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg, Count




def is_admin(user):
    return user.groups.filter(name='Admin').exists()



# @user_passes_test(is_admin)
def feedback_analytics(request):
    total_feedback = Feedback.objects.count()
    average_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
    feedback_by_product = Feedback.objects.values('product_service').annotate(count=Count('id'))

    return render(request, 'feedback/feedback_analytics.html', {
        'total_feedback': total_feedback,
        'average_rating': average_rating,
        'feedback_by_product': feedback_by_product,
    })




def send_notification_email(user_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feedback_list')  # Redirect after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'feedback/register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('feedback_list')


def feedback_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'created_at')  # Default sorting by date
    feedbacks = Feedback.objects.filter(comment__icontains=query).order_by(sort_by)

    paginator = Paginator(feedbacks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'feedback/feedback_list.html', {
        'page_obj': page_obj,
        'query': query,
        'sort_by': sort_by,
    })

@login_required
def user_feedback_history(request):
    feedbacks = Feedback.objects.filter(user_name=request.user.username)
    return render(request, 'feedback/user_feedback_history.html', {'feedbacks': feedbacks})


def submit_feedback(request):
    if request.method == 'POST':
        product_service_id = request.POST['product_service']
        user_name = request.POST['user_name']
        comment = request.POST['comment']
        rating = request.POST['rating']
        file_upload = request.FILES.get('file_upload')  # Get the uploaded file
        Feedback.objects.create(product_service_id=product_service_id, user_name=user_name, comment=comment, rating=rating, file_upload=file_upload)
        
        # Send email notification for feedback
        user_email = request.user.email
        send_notification_email(user_email, 'Feedback Received', 'Thank you for your feedback!')
        
        return redirect('feedback_list')
    return render(request, 'feedback/submit_feedback.html')


def subscribe(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        Subscription.objects.create(user_name=user_name)
        
        # Send email notification
        subject = 'Subscription Confirmation'
        message = f'Thank you for subscribing, {user_name}!'
        send_notification_email(user_name, subject, message)
        
        return redirect('feedback_list')
    return render(request, 'feedback/subscribe.html')


@login_required
def manage_subscription(request, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    subscription.is_active = not subscription.is_active
    subscription.save()
    return redirect('profile')

@login_required
def profile(request):
    subscriptions = Subscription.objects.filter(user_name=request.user.username)
    return render(request, 'feedback/profile.html', {'subscriptions': subscriptions})




@login_required
def user_dashboard(request):
    feedbacks = Feedback.objects.filter(user_name=request.user.username)
    subscriptions = Subscription.objects.filter(user_name=request.user.username)

    return render(request, 'feedback/user_dashboard.html', {
        'feedbacks': feedbacks,
        'subscriptions': subscriptions,
    })
    
    
@login_required
def edit_feedback(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)

    if request.method == 'POST':
        feedback.comment = request.POST['comment']
        feedback.rating = request.POST['rating']
        feedback.save()
        return redirect('user_dashboard')

    return render(request, 'feedback/edit_feedback.html', {'feedback': feedback})
    
@login_required
def delete_feedback(request, feedback_id):
    feedback = Feedback.objects.get(id=feedback_id)
    if request.method == 'POST':
        feedback.delete()
        return redirect('user_dashboard')
    return render(request, 'feedback/delete_feedback.html', {'feedback': feedback})