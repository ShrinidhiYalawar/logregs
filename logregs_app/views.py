from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings
import threading
from .models import CustomUser, Expense, CustomTitle, Title

User = get_user_model()

# ------------------ Forms ------------------
class RegisterForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# ------------------ Auth ------------------
def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('expense-list')
            else:
                error = "Invalid credentials"
    else:
        form = LoginForm()

    return render(request, 'logregs_app/login.html', {'form': form, 'error': error})












            # Thread class for sending mail
class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        super().__init__()
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list

    def run(self):
        send_mail(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
            fail_silently=False,
        )
        
@login_required
def register_user(request):
    if not request.user.is_admin:
        messages.error(request, "Only admins can register users.")
        return redirect('expense-list')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if CustomUser.objects.filter(email=email).exists():
            error = "Email already registered."
            return render(request, 'logregs_app/register_user.html', {'error': error})

        user = CustomUser.objects.create_user(
            name=name, email=email, phone=phone, password=password
        )
        user.admin = request.user
        user.save()

                # Send email using threading (non-blocking)
        subject = "Welcome to LogRegs"
        message = f"Hi {name},\n\nYour account has been created.\n\nLogin Credentials:\nName: {name}\nPhone: {phone}\nPassword: {password}\n\nKeep your credentials safe."
        EmailThread(subject, message, [email]).start()

        messages.success(request, f"{name} registered successfully under you.")
        return redirect('expense-list')

    return render(request, 'logregs_app/register_user.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        user = CustomUser.objects.create_user(
            name=name, email=email, phone=phone, password=password,
        )

        if request.user.is_authenticated and request.user.is_admin:
            user.admin = request.user
            user.save()

                # Send email using threading (non-blocking)
        subject = "Welcome to LogRegs"
        message = f"Hi {name},\n\nThank you for registering.\n\nYour login credentials are:\nName: {name}\nPhone: {phone}\nPassword: {password}\n\nKeep this information safe."
        EmailThread(subject, message, [email]).start()
        messages.success(request, 'User registered successfully')
        return redirect('login')

    return render(request, 'logregs_app/register.html')











def logout_view(request):
    logout(request)
    return redirect('login')

# ------------------ Titles ------------------
@login_required
def add_title(request):
    if not request.user.is_admin:
        messages.error(request, "Only admins can add custom titles.")
        return redirect('expense-list')

    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            return render(request, 'logregs_app/add_title.html', {
                'titles': CustomTitle.objects.filter(admin=request.user),
                'error': "Title cannot be empty."
            })

        if CustomTitle.objects.filter(admin=request.user, name=name).exists():
            return render(request, 'logregs_app/add_title.html', {
                'titles': CustomTitle.objects.filter(admin=request.user),
                'error': "Title already exists."
            })

        CustomTitle.objects.create(admin=request.user, name=name)
        return render(request, 'logregs_app/add_title.html', {
            'titles': CustomTitle.objects.filter(admin=request.user),
            'message': "Title added successfully!"
        })

    return render(request, 'logregs_app/add_title.html', {
        'titles': CustomTitle.objects.filter(admin=request.user)
    })

# ------------------ Expenses ------------------
@login_required
def expense_list(request):
    if request.user.is_admin:
        users = CustomUser.objects.filter(admin=request.user)
        expenses = Expense.objects.filter(user__in=users, is_delete=False)
    else:
        users = [request.user]
        expenses = Expense.objects.filter(user=request.user, is_delete=False)

    user_charts = []
    for user in users:
        grouped = Expense.objects.filter(user=user, is_delete=False).values('title').annotate(total=Sum('amount'))
        if grouped:
            user_charts.append({
                'user': user.name,
                'data': [{'title': g['title'], 'total': float(g['total'])} for g in grouped]
            })

    return render(request, 'logregs_app/expense_list.html', {
        'expenses': expenses,
        'user_charts': user_charts,
        'is_admin': request.user.is_admin,
    })

@login_required
def add_expense(request):
    users = None
    # Get titles for dropdown (filtered by admin)
    titles = CustomTitle.objects.filter(admin=request.user if request.user.is_admin else request.user.admin)
    if request.user.is_admin:
        users = CustomUser.objects.filter(admin=request.user)
    if request.method == 'POST':
        target_user = request.user
        if request.user.is_admin:
            user_id = request.POST.get('user')
            target_user = get_object_or_404(CustomUser, id=user_id, admin=request.user)
        title_name = request.POST.get('title')
        try:
            title_obj = CustomTitle.objects.get(
                name=title_name,
                admin=request.user if request.user.is_admin else request.user.admin
            )
        except CustomTitle.DoesNotExist:
            messages.error(request, "Selected title does not exist!")
            return redirect('add-expense')
        Expense.objects.create(
            user=target_user,
            title=title_obj,  # assign the instance, not string
            amount=request.POST['amount'],
            description=request.POST['description']
        )
        messages.success(request, "Expense added successfully!")
        return redirect('expense-list')
    return render(request, 'logregs_app/add_expense.html', {
        'users': users,
        'titles': titles,
    })

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.user != expense.user and (not request.user.is_admin or expense.user.admin != request.user):
        messages.error(request, "You cannot edit this expense.")
        return redirect('expense-list')

    users = CustomUser.objects.filter(admin=request.user) if request.user.is_admin else None
    titles = CustomTitle.objects.filter(admin=request.user if request.user.is_admin else request.user.admin)

    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.description = request.POST['description']
        if request.user.is_admin:
            user_id = request.POST.get('user')
            expense.user = get_object_or_404(CustomUser, id=user_id, admin=request.user)
        expense.save()
        return redirect('expense-list')

    return render(request, 'logregs_app/edit_expense.html', {
        'expense': expense,
        'users': users,
        'titles': titles
    })

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.user != expense.user and (not request.user.is_admin or expense.user.admin != request.user):
        messages.error(request, "You cannot delete this expense.")
        return redirect('expense-list')

    expense.is_delete = True
    expense.save()
    return redirect('expense-list')

# ------------------ Password ------------------
@login_required
def change_password_view(request):
    if request.method == 'POST':
        current = request.POST['current']
        new = request.POST['new']
        confirm = request.POST['confirm']

        if not request.user.check_password(current):
            return render(request, 'logregs_app/change_password.html', {'error': 'Wrong current password'})
        if new != confirm:
            return render(request, 'logregs_app/change_password.html', {'error': 'New passwords do not match'})

        request.user.set_password(new)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return render(request, 'logregs_app/change_password.html', {'success': 'Password changed successfully'})

    return render(request, 'logregs_app/change_password.html')

# ------------------ Forgot Password ------------------
def forgot_password_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        if otp != '1234':
            error = "Invalid OTP."
        else:
            try:
                user = get_user_model().objects.get(email=email)
                login(request, user)
                return redirect('expense-list')
            except get_user_model().DoesNotExist:
                error = "Email not found."

    return render(request, 'logregs_app/forgot_password.html', {'error': error})
