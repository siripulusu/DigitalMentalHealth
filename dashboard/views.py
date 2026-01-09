import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

# Model Imports
from assessments.models import SelfAssessment
from appointments.models import Appointment
from resources.models import Resource, CommunityLink
from accounts.models import DailyMood, Notification, User

# Utility Imports
from .pdf_utils import generate_admin_pdf

# ==========================================
# --- STUDENT VIEWS ---
# ==========================================

@login_required
def student_dashboard(request):
    """Main dashboard for students featuring mood tracking and activity."""
    if request.user.role != 'student':
        return redirect('home')

    # LOGIN COUNT LOGIC: Increments once per browser session
    if not request.session.get('has_counted_login', False):
        request.user.login_count += 1
        request.user.save()
        request.session['has_counted_login'] = True

    # 1. Fetch user's mood history (last 7 entries for the Chart)
    mood_history_data = DailyMood.objects.filter(user=request.user).order_by('created_at')[:7]
    
    # 2. Extract labels and scores for Chart.js
    chart_labels = [m.created_at.strftime("%d %b") for m in mood_history_data]
    chart_scores = [m.mood_score for m in mood_history_data]

    # 3. Handle empty state for graph
    if not chart_scores:
        chart_labels = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
        chart_scores = [0, 0, 0, 0, 0, 0, 0] 

    # 4. Fetch history for the "Recent Activity" list
    recent_moods = DailyMood.objects.filter(user=request.user).order_by('-created_at')[:3]

    context = {
        'chart_labels': json.dumps(chart_labels),
        'chart_scores': json.dumps(chart_scores),
        'recent_moods': recent_moods,
    }
    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def log_mood(request):
    """Handles saving the quick emoji check-in."""
    if request.method == 'POST':
        score = request.POST.get('mood_score')
        labels = {"20": "Sad", "50": "Okay", "80": "Good", "100": "Great"}
        
        if score:
            DailyMood.objects.create(
                user=request.user,
                mood_score=int(score),
                mood_label=labels.get(str(score), "Neutral")
            )
    return redirect('student_dashboard')


# ==========================================
# --- ADMIN VIEWS ---
# ==========================================

@login_required
def admin_dashboard(request):
    """High-Level System Overview and Stats."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')

    # System Activity Logs
    recent_assessments = SelfAssessment.objects.all().order_by('-created_at')[:3]
    recent_appointments = Appointment.objects.all().order_by('-created_at')[:3]
    recent_users = User.objects.all().order_by('-date_joined')[:5]

    context = {
        'total_users': User.objects.count(),
        'pending_approvals': User.objects.filter(is_approved=False).count(),
        'total_assessments': SelfAssessment.objects.count(),
        'appointment_stats': {
            'total': Appointment.objects.count(),
            'completed': Appointment.objects.filter(status='COMPLETED').count(),
            'booked': Appointment.objects.filter(status='BOOKED').count(),
        },
        'recent_users': recent_users,
        'recent_assessments': recent_assessments,
        'recent_appointments': recent_appointments,
        'severity_data': SelfAssessment.objects.values('severity').annotate(count=Count('id')),
        'resource_usage': Resource.objects.values('title').annotate(count=Count('id')),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def admin_user_management(request):
    """Full CRUD for Users including Adding, Approving, and Deleting."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "add_user":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                User.objects.create_user(
                    username=username, email=email, 
                    password=password, role=role, is_approved=True
                )
                messages.success(request, f"User {username} created successfully.")
        
        elif action == "approve":
            target = get_object_or_404(User, id=request.POST.get('user_id'))
            target.is_approved = True
            target.save()
            Notification.objects.create(
                user=target, 
                title="Access Granted", 
                message="Your professional portal is now active.", 
                link="/dashboard/"
            )
            messages.success(request, f"Approved {target.username}")
        
        elif action == "delete":
            User.objects.filter(id=request.POST.get('user_id')).delete()
            messages.warning(request, "User account removed.")
            
        return redirect('admin_user_management')

    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/admin_users.html', {'users': users})

@login_required
def admin_edit_user(request, user_id):
    """Modify User Data (Names, Emails, Roles)."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')
        
    target = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        target.username = request.POST.get('username')
        target.email = request.POST.get('email')
        target.role = request.POST.get('role')
        target.save()
        messages.success(request, f"Profile for {target.username} updated.")
        return redirect('admin_user_management')
        
    return render(request, 'dashboard/admin_edit_user.html', {'target': target})

@login_required
def admin_resource_management(request):
    """Manage Global Resources (Music, Yoga, Exercise, etc.) for Admins."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == "add":
            title = request.POST.get('title')
            link = request.POST.get('link')
            category = request.POST.get('category', 'General')
            description = request.POST.get('description', '')
            if title and link:
                Resource.objects.create(title=title, link=link, category=category, description=description)
                messages.success(request, "Resource published successfully.")
        
        elif action == "delete":
            resource_id = request.POST.get('res_id')
            Resource.objects.filter(id=resource_id).delete()
            messages.warning(request, "Resource removed from system.")
            
        return redirect('admin_resource_management')
    
    resources = Resource.objects.all().order_by('-id')
    return render(request, 'dashboard/admin_resources.html', {'resources': resources})

@login_required
def admin_analytics(request):
    """Deep Analytics with Scatterplots & Mood Trend Data."""
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('home')

    mood_data = DailyMood.objects.all().order_by('created_at')
    mood_labels = [m.created_at.strftime("%d %b") for m in mood_data]
    mood_values = [m.mood_score for m in mood_data]

    assessments = SelfAssessment.objects.all()
    scatter_data = [{'x': a.created_at.hour, 'y': a.score} for a in assessments]

    context = {
        'mood_labels': json.dumps(mood_labels),
        'mood_values': json.dumps(mood_values),
        'scatter_data': json.dumps(scatter_data),
        'resource_usage': Resource.objects.values('title').annotate(count=Count('id')),
    }
    return render(request, 'dashboard/admin_analytics.html', context)

@login_required
def download_admin_pdf(request):
    """Generates Admin system report PDF."""
    if not (request.user.is_superuser or getattr(request.user, 'role', None) == 'admin'):
        return redirect('home')

    context = {'total_assessments': SelfAssessment.objects.count()}
    pdf = generate_admin_pdf(context)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admin_summary.pdf"'
    return response


# ==========================================
# --- COUNSELLOR VIEWS ---
# ==========================================

@login_required
def counsellor_dashboard(request):
    if request.user.role != 'counsellor':
        return redirect('home')
    return render(request, 'dashboard/counsellor_dashboard.html')

@login_required
def counsellor_assessments(request):
    """View Student Assessment Reports with student details."""
    if request.user.role != 'counsellor':
        return redirect('home')

    reports = SelfAssessment.objects.all().select_related('user').order_by('-created_at')
    return render(request, 'dashboard/counsellor_assessments.html', {'reports': reports})

@login_required
def manage_resources(request):
    """Counsellor Resource Management."""
    if request.user.role != 'counsellor':
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        if title and link:
            Resource.objects.create(title=title, link=link)
            return redirect('manage_resources')
    
    resources = Resource.objects.all().order_by('-id')
    return render(request, 'dashboard/counsellor_resources.html', {'resources': resources})

@login_required
def counsellor_messages(request):
    """Post feedback/guidance for student appointments."""
    if request.user.role != 'counsellor':
        return redirect('home')
    
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        guidance_text = request.POST.get('guidance')
        
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.guidance_message = guidance_text
        appointment.save()
        
        Notification.objects.create(
            user=appointment.user,
            title="New Guidance Message",
            message=f"Dr. {request.user.username} has posted new feedback for you.",
            link="/appointments/"
        )
        return redirect('counsellor_messages')
    return render(request, 'dashboard/counsellor_messages.html')

@login_required
def counsellor_ethics(request):
    if request.user.role != 'counsellor':
        return redirect('home')
    return render(request, 'dashboard/counsellor_ethics.html')


# ==========================================
# --- PEER / VOLUNTEER VIEWS ---
# ==========================================

@login_required
def volunteer_dashboard(request):
    if request.user.role != 'peer':
        return redirect('home')
    return render(request, 'dashboard/volunteer_dashboard.html')

def community_view(request):
    """Public/Peer Community View (Handles posting new links)."""
    if request.method == 'POST':
        if request.user.is_authenticated and (request.user.role in ['peer', 'admin'] or request.user.is_staff):
            title = request.POST.get('title')
            description = request.POST.get('description')
            form_link = request.POST.get('form_link')
            if title and form_link:
                CommunityLink.objects.create(title=title, description=description, form_link=form_link)
                return redirect('community_view')
    links = CommunityLink.objects.all().order_by('-created_at')
    return render(request, 'resources/community.html', {'links': links})

@login_required
def manage_communities(request):
    """Admin/Peer control over Community links."""
    if not (request.user.role in ['peer', 'admin'] or request.user.is_staff):
        return redirect('home')

    if request.method == "POST":
        action = request.POST.get('action')
        if action == "add":
            CommunityLink.objects.create(
                title=request.POST.get('title'),
                form_link=request.POST.get('form_link'),
                description=request.POST.get('description')
            )
        elif action == "delete":
            CommunityLink.objects.filter(id=request.POST.get('link_id')).delete()
        return redirect('manage_communities')

    links = CommunityLink.objects.all().order_by('-created_at')
    return render(request, 'dashboard/admin_communities.html', {'links': links})

@login_required
def peer_communities(request):
    if request.user.role != 'peer':
        return redirect('home')
    links = CommunityLink.objects.all().order_by('-created_at')
    return render(request, 'dashboard/peer_communities.html', {'links': links})

@login_required
def peer_conversations(request):
    if request.user.role != 'peer': return redirect('home')
    return render(request, 'dashboard/peer_conversations.html')

@login_required
def peer_guidelines(request):
    if request.user.role != 'peer': return redirect('home')
    return render(request, 'dashboard/peer_guidelines.html')

@login_required
def peer_escalation(request):
    if request.user.role != 'peer': return redirect('home')
    return render(request, 'dashboard/peer_escalation.html')


# ==========================================
# --- GENERAL UTILITIES ---
# ==========================================

@login_required
def mark_all_notifications_read(request):
    """AJAX endpoint to clear notifications."""
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)