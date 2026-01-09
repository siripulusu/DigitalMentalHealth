from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment
from accounts.models import User

@login_required
def book_appointment(request):
    """
    Handles confidential booking and triggers Tri-party Email Notifications
    to the Student, Counsellor, and Admin.
    """
    counsellors = User.objects.filter(role='counsellor', is_approved=True)

    if request.method == 'POST':
        counsellor_id = request.POST.get('counsellor')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        counsellor = User.objects.get(id=counsellor_id)

        # 1. Create the Appointment Record
        Appointment.objects.create(
            student=request.user,
            counsellor=counsellor,
            date=date,
            time_slot=time_slot
        )

        # 2. Prepare the Tri-party Notification Details
        subject = 'Appointment Confirmation - DMH Support System'
        common_body = (
            f"Counsellor: {counsellor.username}\n"
            f"Student: {request.user.username}\n"
            f"Date: {date}\n"
            f"Time: {time_slot}\n\n"
            "Please log in to your dashboard for more details."
        )

        # 3. Trigger Tri-party Emails
        try:
            # Party A: Send to Student
            send_mail(
                subject,
                f"Hello {request.user.username},\nYour counselling appointment has been booked successfully.\n\n{common_body}",
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )

            # Party B: Send to Counsellor
            send_mail(
                subject,
                f"Hello {counsellor.username},\nA new counselling session has been booked with you.\n\n{common_body}",
                settings.DEFAULT_FROM_EMAIL,
                [counsellor.email],
                fail_silently=False,
            )

            # Party C: Send to Institutional Admins (System Audit)
            admin_emails = list(User.objects.filter(role='admin').values_list('email', flat=True))
            if admin_emails:
                send_mail(
                    'System Audit: New Appointment Booked',
                    f"A new appointment has been recorded in the DMH Portal.\n\n{common_body}",
                    settings.DEFAULT_FROM_EMAIL,
                    admin_emails,
                    fail_silently=False,
                )

        except Exception as e:
            # Prevent the app from crashing if the email server is down
            print(f"SMTP Error: {e}")

        messages.success(request, 'Appointment booked successfully. Confirmation emails have been sent.')
        return redirect('book_appointment')

    return render(request, 'appointments/book.html', {
        'counsellors': counsellors
    })

@login_required
def counsellor_appointments(request):
    if request.user.role != 'counsellor':
        return redirect('home')

    appointments = Appointment.objects.filter(counsellor=request.user)

    return render(request, 'appointments/counsellor_list.html', {
        'appointments': appointments
    })

@login_required
def view_appointments(request):
    if request.user.role == 'counsellor':
        # Counsellors see sessions assigned to them
        appointments = Appointment.objects.filter(counsellor=request.user).order_by('-date')
        return render(request, 'appointments/counsellor_list.html', {'appointments': appointments})
    else:
        # Students see their own bookings
        appointments = Appointment.objects.filter(student=request.user).order_by('-date')
        return render(request, 'appointments/student_list.html', {'appointments': appointments})

@login_required
def add_guidance(request, appointment_id):
    """
    Allows counsellors to add guidance messages to specific appointments.
    """
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        counsellor=request.user
    )

    if request.method == 'POST':
        appointment.guidance_message = request.POST.get('guidance')
        appointment.save()
        return redirect('view_appointments')

    return render(request, 'appointments/add_guidance.html', {
        'appointment': appointment
    })