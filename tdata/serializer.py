from rest_framework import serializers
from tdata.models import Page, LQSutra, LQReel, Sutra,Reel

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class LQReelSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LQReel
        fields = ('id', 'reel_no', 'text_ready')

class LQSutraSerializer(serializers.ModelSerializer):
    lqreel_set = LQReelSimpleSerializer(many=True)

    class Meta:
        model = LQSutra
        fields = ('id', 'sid', 'name', 'total_reels', 'lqreel_set')
#================
#new code 0411 
class ReelSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reel
        fields = ('id', 'reel_no','ocr_ready')

class SutraSerializer(serializers.ModelSerializer):
    reel_set = ReelSimpleSerializer(many=True)
        read_only_fields = ('id', 'sid', 'name', 'total_reels', 'lqreel_set')