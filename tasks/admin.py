from django.contrib import admin

from .models import BatchTask, Task, CorrectSeg,\
ReelDiff, DiffSeg, DiffSegText, DiffSegResult, ReelCorrectText, LQReelText,\
Punct, LQPunct, CorrectResultDiff, CorrectDiffSeg

admin.site.register(BatchTask)
admin.site.register(Task)
admin.site.register(CorrectSeg)
admin.site.register(ReelDiff)
admin.site.register(DiffSeg)
admin.site.register(DiffSegText)
admin.site.register(DiffSegResult)
admin.site.register(ReelCorrectText)
admin.site.register(LQReelText)
admin.site.register(Punct)
admin.site.register(LQPunct)
admin.site.register(CorrectResultDiff)
admin.site.register(CorrectDiffSeg)