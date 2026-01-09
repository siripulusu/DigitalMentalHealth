import uuid
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import SelfAssessment
from .utils import get_phq9_severity, get_gad7_severity
from .pdf_utils import generate_assessment_pdf

# Shared options for both tests
ASSESSMENT_OPTIONS = [
    (0, "Not at all"),
    (1, "Several days"),
    (2, "More than half the days"),
    (3, "Nearly every day")
]

def assessment_home(request):
    """Landing page for selecting an assessment."""
    return render(request, "assessments/index.html")

@login_required
def assessment_history(request):
    """Displays a list of all assessments taken by the logged-in user."""
    assessments = SelfAssessment.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'assessments/history.html', {
        'assessments': assessments
    })

@login_required
def download_assessment_pdf(request):
    """Generates and returns a PDF of the user's assessment history."""
    assessments = SelfAssessment.objects.filter(
        user=request.user
    ).order_by('-created_at')

    pdf_buffer = generate_assessment_pdf(request.user, assessments)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="assessment_report.pdf"'
    return response

def phq9_view(request):
    questions = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
        "Trouble concentrating on things, such as reading or watching television",
        "Moving or speaking so slowly that other people could have noticed, or being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead or of hurting yourself in some way"
    ]
    
    if request.method == 'POST':
        # Collect answers (defaulting to 0 if missed)
        answers = [int(request.POST.get(f'q{i}', 0)) for i in range(1, len(questions) + 1)]
        score = sum(answers)
        severity = get_phq9_severity(score)

        # Handle User Identification
        user = request.user if request.user.is_authenticated else None
        
        # Safe Anonymous ID retrieval
        anon_id = str(uuid.uuid4())
        if user and hasattr(user, 'anonymous_id') and user.anonymous_id:
            anon_id = str(user.anonymous_id)

        # SAVE TO DATABASE
        SelfAssessment.objects.create(
            user=user,
            anonymous_id=anon_id,
            test_type='PHQ9',
            score=score,
            severity=severity
        )

        return render(request, 'assessments/result.html', {
            'score': score,
            'severity': severity,
            'test': 'PHQ-9'
        })

    return render(request, 'assessments/phq9.html', {'questions': questions , 'options_list': ASSESSMENT_OPTIONS})

def gad7_view(request):
    questions = [
        "Feeling nervous, anxious, or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid as if something awful might happen"
    ]
    
    if request.method == 'POST':
        answers = [int(request.POST.get(f'q{i}', 0)) for i in range(1, len(questions) + 1)]
        score = sum(answers)
        severity = get_gad7_severity(score)

        user = request.user if request.user.is_authenticated else None
        
        anon_id = str(uuid.uuid4())
        if user and hasattr(user, 'anonymous_id') and user.anonymous_id:
            anon_id = str(user.anonymous_id)

        # SAVE TO DATABASE
        SelfAssessment.objects.create(
            user=user,
            anonymous_id=anon_id,
            test_type='GAD7',
            score=score,
            severity=severity
        )

        return render(request, 'assessments/result.html', {
            'score': score,
            'severity': severity,
            'test': 'GAD-7'
        })

    return render(request, 'assessments/gad7.html', {'questions': questions , 'options_list': ASSESSMENT_OPTIONS})