from rest_framework import serializers
from .models import CornYieldModel


class CornYieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = CornYieldModel
        fields = "__all__"


class CornYieldFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = "__all__"
