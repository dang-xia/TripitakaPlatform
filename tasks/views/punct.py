from django.shortcuts import get_object_or_404, render, redirect
from tdata.models import *
from tasks.models import *

def do_punct_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.typ != Task.TYPE_PUNCT:
        return redirect('/')
    return render(request, 'tasks/do_punct_task.html', {'task_id': task_id})