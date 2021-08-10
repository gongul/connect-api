from rest_framework import serializers
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from PIL import Image
from io import BytesIO

import os

from image.utils import is_allow_max_size, is_allow_mime_type


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    path = serializers.CharField()
    name = serializers.CharField()

    def validate_image(self, value):
        if not is_allow_max_size(value):
            raise serializers.ValidationError('이미지의 크기가 너무 큽니다(5mb 이하만 가능합니다)')
        elif not is_allow_mime_type(value):
            raise serializers.ValidationError('이미지는 jpeg, jpg, png 포맷만 가능합니다.')

    def save(self):
        validated_data = self.validated_data
        site = get_current_site(self.context['request'])
        protocol = 'http://' if settings.DEBUG else 'https://'
        url = ''.join([protocol, site.domain, settings.MEDIA_URL, validated_data['path'], validated_data['name']])
        storage_root = os.path.join(settings.MEDIA_ROOT, validated_data['path'])
        save_path = os.path.join(storage_root, validated_data['name'])

        if not os.path.exists(storage_root):
            os.makedirs(storage_root)

        validated_data['image'].open()
        image = Image.open(BytesIO(validated_data['image'].read()))
        image.save(save_path)

        return {'url': url}
