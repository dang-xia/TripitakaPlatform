from django.shortcuts import get_object_or_404, render, redirect

def index(request):
    return render(request, 'tasks/tripitaka.html')

def process_correctfeedback(request, correctfeedback_id):
    return render(request, 'tasks/correct_feedback.html', {'correctfeedback_id': correctfeedback_id})

def view_correctfeedback(request):
    return render(request, 'tasks/view_correct_feedback.html')
