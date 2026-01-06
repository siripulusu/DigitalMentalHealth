from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from assessments.models import SelfAssessment
from appointments.models import Appointment
from resources.models import Resource
from django.db.models import Count
from django.http import HttpResponse
from .pdf_utils import generate_admin_pdf

@staff_member_required
def download_admin_pdf(request):
    context = {
        'total_assessments': SelfAssessment.objects.count(),
    }

    pdf = generate_admin_pdf(context)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admin_summary.pdf"'
    return response

@staff_member_required
def admin_dashboard(request):
    total_assessments = SelfAssessment.objects.count()

    severity_data = (
        SelfAssessment.objects
        .values('severity')
        .annotate(count=Count('id'))
    )

    appointment_stats = {
        'total': Appointment.objects.count(),
        'completed': Appointment.objects.filter(status='COMPLETED').count(),
        'booked': Appointment.objects.filter(status='BOOKED').count(),
    }

    resource_usage = Resource.objects.values(
        'title'
    ).annotate(count=Count('usage_count'))

    return render(request, 'dashboard/admin_dashboard.html', {
        'total_assessments': total_assessments,
        'severity_data': severity_data,
        'appointment_stats': appointment_stats,
        'resource_usage': resource_usage,
    })
