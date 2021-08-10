from rest_framework import serializers


from .models import Feed


class FeedSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user

        return super().update(instance, validated_data)

    class Meta:
        model = Feed
        read_only_fields = ['registration_date', 'user']
        fields = '__all__'
