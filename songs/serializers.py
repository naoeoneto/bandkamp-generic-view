from rest_framework import serializers

from .models import Song
from albums.serializers import AlbumSerializer


# class SongSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=255)
#     duration = serializers.CharField(max_length=255)
# album_id = serializers.IntegerField(read_only=True)


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "duration", "album_id"]
        read_only_fields = ["id", "album_id"]
        extra_kwargs = {
            "title": {"required": True},
            "duration": {"required": True},
        }

    def create(self, validated_data):
        return Song.objects.create(**validated_data)
