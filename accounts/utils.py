from django.shortcuts import redirect

def redirect_user_dashboard(user):
    if user.is_superuser or user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'student':
        return redirect('student_dashboard')
    elif user.role == 'counsellor':
        return redirect('counsellor_dashboard')
    elif user.role == 'peer':
        return redirect('volunteer_dashboard')
    return redirect('home')
