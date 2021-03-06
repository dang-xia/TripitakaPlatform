from django.http import Http404
from django.conf import settings
from rest_framework import mixins, viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from tdata.models import *
from tasks.models import *
from rect.models import PageTask
from jkapi.serializers import *
from jkapi.permissions import *
from tasks.task_controller import correct_submit_async, correct_verify_submit_async, correct_difficult_submit_async

from tdata.lib.image_name_encipher import get_image_url
from ccapi.pagination import StandardPagination
import json, re
from operator import attrgetter, itemgetter

class CorrectTaskDetail(APIView):
    permission_classes = (IsTaskPickedByCurrentUser, )
    
    def get(self, request, task_id, format=None):
        image_url_prefix = self.task.reel.url_prefix()
        urls = []
        for vol_page in range(self.task.reel.start_vol_page, self.task.reel.end_vol_page + 1):
            url = get_image_url(self.task.reel, vol_page)
            urls.append(url)
        pagetask_numbers = [t.number for t in PageTask.objects.filter(
            pagerect__reel=self.task.reel).order_by('pagerect__page')]
        correct_task_count = 2
        if self.task.typ == Task.TYPE_CORRECT_VERIFY:
            correct_task_count = Task.objects.filter(reel=self.task.reel, \
            batchtask=self.task.batchtask, typ=Task.TYPE_CORRECT).count()
        bar_line_count = self.task.reel.sutra.tripitaka.bar_line_count
        if bar_line_count.isdigit():
            bar_line_count = int(bar_line_count)
        else:
            bar_line_count = json.loads(bar_line_count)
        response = {
            'task_id': task_id,
            'correct_task_count': correct_task_count,
            'task_typ': self.task.typ,
            'status': self.task.status,
            'result': self.task.result,
            'cur_focus': self.task.cur_focus,
            'image_urls': urls,
            'pagetask_numbers': pagetask_numbers,
            'bar_line_count': bar_line_count,
            }
        return Response(response)

class CorrectSegList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CorrectSegSerializer
    permission_classes = (IsTaskPickedByCurrentUser, )

    def get_queryset(self):
        queryset = CorrectSeg.objects.filter(
            task=self.task).order_by('id')
        return queryset

    def get(self, request, task_id, format=None):
        serializer = CorrectSegSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

class CorrectSegUpdate(mixins.UpdateModelMixin, generics.GenericAPIView):
    serializer_class = CorrectSegSerializer
    permission_classes = (IsTaskPickedByCurrentUser, )

    def get_object(self, pk):
        try:
            return CorrectSeg.objects.get(pk=pk)
        except CorrectSeg.DoesNotExist:
            raise Http404

    def put(self, request, task_id, pk, format=None):
        correctseg = self.get_object(pk)
        serializer = CorrectSegSerializer(correctseg, data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.task.cur_focus = pk
            self.task.save(update_fields=['cur_focus'])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoubtSegPagination(StandardPagination):       
       page_size = 100

class DoubtSegViewSet(viewsets.ModelViewSet):
    serializer_class = DoubtSegSerializer
    permission_classes = (IsTaskPickedByCurrentUser, )
    pagination_class = DoubtSegPagination
    filter_fields = ('task',)

    def get_queryset(self):
        task = self.request.query_params.get('task', None)
        # 为了应对DELETE方法
        task = task or self.request.parser_context['kwargs']['task_id']
        return DoubtSeg.objects.filter(task_id=task)

    def put(self, request, task_id, pk, format=None):
        doubtseg = DoubtSeg.objects.get(pk)
        serializer = DoubtSegSerializer(doubtseg, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinishCorrectTask(APIView):
    permission_classes = (IsTaskPickedByCurrentUser, )

    def post(self, request, task_id, format=None):
        if any([correctseg.selected_text is None for correctseg in CorrectSeg.objects.filter(task=self.task)]):
            return Response({'msg': '请校对完成'}, status=status.HTTP_400_BAD_REQUEST)
        if self.task.status >= Task.STATUS_FINISHED:
            correct_verify_task = Task.objects.filter(reel=self.task.reel, \
            batchtask=self.task.batchtask, typ=Task.TYPE_CORRECT_VERIFY).first()
            if correct_verify_task and correct_verify_task.status > Task.STATUS_READY:
                return Response({'status': self.task.status, 'msg': '此卷的文字校对审定任务已被领取，不能再重新提交'}, status=status.HTTP_400_BAD_REQUEST)
        update_fields=['status']
        if not self.task.finished_at:
            update_fields.append('finished_at')
            self.task.finished_at = timezone.now()
        self.task.status = Task.STATUS_FINISHED
        self.task.save(update_fields=update_fields)
        if self.task.typ == Task.TYPE_CORRECT:
            correct_submit_async(task_id)
        elif self.task.typ == Task.TYPE_CORRECT_VERIFY:
            correct_verify_submit_async(task_id)
        elif self.task.typ == Task.TYPE_CORRECT_DIFFICULT:
            correct_difficult_submit_async(task_id)
        return Response({'task_id': task_id, 'status': self.task.status})

class ReturnCorrectTask(APIView):
    permission_classes = (IsTaskPickedByCurrentUser, )

    def post(self, request, task_id, format=None):
        self.task.picker = None
        self.task.picked_at = None
        self.task.status = Task.STATUS_READY
        self.task.save(update_fields=['picker', 'picked_at', 'status'])
        return Response({'task_id': task_id, 'status': self.task.status})
