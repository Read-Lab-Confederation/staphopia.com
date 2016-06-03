""" . """
from rest_framework import serializers
from sample.models import (
    Sample,
    Publication,
    Tag,
    ToTag,
    Resistance,
    ToResistance
)


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class ToTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToTag


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication


class ResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resistance


class ToResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToResistance
