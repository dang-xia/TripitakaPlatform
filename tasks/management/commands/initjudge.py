from django.core.management.base import BaseCommand, CommandError
from jwt_auth.models import Staff
from tdata.models import *
from tasks.models import *
from tasks.common import *
from tasks.reeldiff_processor import *
from tasks.task_controller import *
from tasks.utils.text_align import *
from .init import save_reel, get_reel

import TripitakaPlatform.settings

from difflib import SequenceMatcher
import os, sys
from os.path import isfile, join
import traceback

import re, json

def save_reel_with_correct_text(lqsutra, sid, reel_no, start_vol, start_vol_page, end_vol_page,
    path1='', path2='', path3=''):
    reel, reel_ocr_text = save_reel(lqsutra, sid, reel_no, start_vol, start_vol_page, end_vol_page, \
    path1, path2, path3)
    try:
        reel_correct_text = ReelCorrectText.get(reel=reel)
    except:
        filename = os.path.join(settings.BASE_DIR, 'data/sutra_text/%s_%03d_fixed.txt' % (sid, reel_no))
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            reel_correct_text = ReelCorrectText(reel=reel)
            reel_correct_text.set_text(text)
            reel_correct_text.save()

    # 得到精确的切分数据
    try:
        compute_accurate_cut(reel)
    except Exception:
        traceback.print_exc()

def create_data(lqsutra):
    save_reel_with_correct_text(lqsutra, 'QL000870', 1, 24, 1, 17, '24')
    save_reel_with_correct_text(lqsutra, 'ZH000860', 1, 12, 1, 12, '12')
    save_reel_with_correct_text(lqsutra, 'GL000790', 1, 0, 1, 21, '79', '1')
    save_reel_with_correct_text(lqsutra, 'QS000810', 1, 21, 449, 461, '21')
    save_reel_with_correct_text(lqsutra, 'ZC000780', 1, 10, 21, 48, '10')
    save_reel_with_correct_text(lqsutra, 'SX000770', 1, 956, 2, 38, '956')
    save_reel_with_correct_text(lqsutra, 'PL000810', 1, 1114, 2, 25, '1114')
    save_reel_with_correct_text(lqsutra, 'YB000860', 1, 27, 1, 23, '27')
    save_reel_with_correct_text(lqsutra, 'QL000870', 2, 24, 18, 31, '24')
    save_reel_with_correct_text(lqsutra, 'ZH000860', 2, 12, 13, 24, '12')
    save_reel_with_correct_text(lqsutra, 'QS000810', 2, 21, 461, 472, '21')
    save_reel_with_correct_text(lqsutra, 'SX000770', 2, 957, 2, 36, '957')
    save_reel_with_correct_text(lqsutra, 'YB000860', 2, 27, 25, 45, '27')

class Command(BaseCommand):
    def handle(self, *args, **options):
        BASE_DIR = settings.BASE_DIR
        try:
            admin = Staff.objects.get(username='admin')
        except:
            admin = Staff(email='admin@example.com', username='admin')
            admin.set_password('admin')
            admin.is_admin = True
            admin.save()

        # get LQSutra
        lqsutra = LQSutra.objects.get(sid='LQ003100') #大方廣佛華嚴經60卷
        create_data(lqsutra)
        # create BatchTask
        batch_task = BatchTask(priority=2, publisher=admin)
        batch_task.save()

        CB = Tripitaka.objects.get(code='CB')
        try:
            base_sutra = Sutra.objects.get(lqsutra=lqsutra, tripitaka=CB)
        except:
            print('please run ./manage.py import_cbeta_huayan60')
            return
        for reel_no in range(1, 3):
            base_reel = Reel.objects.get(sutra=base_sutra, reel_no=reel_no)
            lqreel = LQReel.objects.get(lqsutra=lqsutra, reel_no=reel_no)
            create_judge_tasks(batch_task, lqreel, base_reel, 2, 1)
        judge_tasks = create_data_for_judge_tasks(batch_task, lqsutra, base_sutra, 2)

        set_result = True
        if set_result:
            for task in judge_tasks:
                for diffseg in task.reeldiff.diffseg_set.all():
                    diffsegtexts = list(DiffSegText.objects.filter(diffseg=diffseg, tripitaka=CB))
                    if len(diffsegtexts) == 1:
                        diffsegresult = DiffSegResult.objects.get(task=task, diffseg=diffseg)
                        diffsegresult.selected_text = diffsegtexts[0].text
                        diffsegresult.selected = 1
                        diffsegresult.save()
