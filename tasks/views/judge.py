from django.shortcuts import get_object_or_404, render, redirect
from tdata.models import *
from tdata.lib.image_name_encipher import get_image_url
from tasks.models import *

def do_judge_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.typ == Task.TYPE_JUDGE:
        judge_task_ids = []
    elif task.typ in [Task.TYPE_JUDGE_VERIFY, Task.TYPE_JUDGE_DIFFICULT]:
        judge_task_ids = [ judge_task.id for judge_task in \
        Task.objects.filter(batchtask_id=task.batchtask_id, \
        lqreel_id=task.lqreel.id, typ=Task.TYPE_JUDGE).order_by('task_no') ]
    else:
        return redirect('/')
    judge_verify_task_id = 0
    if task.typ == Task.TYPE_JUDGE_DIFFICULT:
        try:
            judge_verify_task = Task.objects.get(batchtask_id=task.batchtask_id, \
            lqreel_id=task.lqreel.id, typ=Task.TYPE_JUDGE_VERIFY)
            judge_verify_task_id = judge_verify_task.id
        except:
            pass
    context = {
        'task': task,
        'judge_task_ids': judge_task_ids,
        'judge_verify_task_id': judge_verify_task_id,
        }
    return render(request, 'tasks/do_judge_task.html', context)

def sutra_page_detail(request, pid):
    page = get_object_or_404(Page, pid=pid)
    reel = page.reel
    vol_page = reel.start_vol_page + page.reel_page_no - 1
    image_url = get_image_url(reel, vol_page)
    char_pos = request.GET.get('char_pos', '')
    s = char_pos[-5:]
    try:
        line_no = int(s[0:2])
        char_no = int(s[3:])
    except:
        return redirect('/')
    context = {
        'page': page,
        'image_url': image_url,
        'line_no': line_no,
        'char_no': char_no,
    }
    return render(request, 'tasks/sutra_page_detail.html', context)
