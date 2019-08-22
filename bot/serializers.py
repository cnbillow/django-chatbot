# -*- coding:utf-8 -*-
from rest_framework import serializers
from chatbot.chatbot import ChatBot
from django.conf import settings


chatbot = ChatBot(
    'django',
    # storage={
    #     'import_path': 'chatbot.storage.SQLStorage',
    #     'database_uri': 'mysql+pymysql://root:123456@127.0.0.1:3306/chatbot'
    # },
)


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)


class LearnSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    answer = serializers.CharField(max_length=1000)
    category = serializers.CharField(max_length=100, default='其他')
    type_ = serializers.IntegerField(default=0)
    parameters = serializers.CharField(max_length=255, allow_blank=True, required=False)
    extractor = serializers.CharField(max_length=255, allow_blank=True, required=False)

    def learn(self):
        return chatbot.learn(**self.validated_data)

    def validate_type_(self, value):
        if value not in (0, 1):
            raise serializers.ValidationError('the type must be 0 or 1')
        return value
