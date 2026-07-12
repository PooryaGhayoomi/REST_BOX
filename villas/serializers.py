from rest_framework import serializers
from .models import Villa


class VillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Villa
        fields = "__all__"
        read_only_fields = ("host", "created_at")