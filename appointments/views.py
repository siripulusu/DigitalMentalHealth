from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment
from accounts.models import User

@login_required
def book_appointment(request):
    counsellors = User.objects.filter(role='counsellor', is_approved=True)

    if request.method == 'POST':
        counsellor_id = request.POST.get('counsellor')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        counsellor = User.objects.get(id=counsellor_id)

        Appointment.objects.create(
            student=request.user,
            counsellor=counsellor,
            date=date,
            time_slot=time_slot
        )

        send_mail(
            subject='Appointment Confirmation',
            message=(
                f"Your counselling appointment has been booked.\n\n"
                f"Counsellor: {counsellor.username}\n"
                f"Date: {date}\n"
                f"Time: {time_slot}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        messages.success(request, 'Appointment booked successfully.')
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
def add_guidance(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        counsellor=request.user
    )

    if request.method == 'POST':
        appointment.guidance_message = request.POST.get('guidance')
        appointment.save()
        return redirect('counsellor_appointments')

    return render(request, 'appointments/add_guidance.html', {
        'appointment': appointment
    })


