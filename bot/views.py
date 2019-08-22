from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import json
from .serializers import QuestionSerializer, LearnSerializer, chatbot
from urllib.parse import quote, unquote


if hasattr(settings, 'COOKIE_MAX_AGE'):
    COOKIE_MAX_AGE = settings.COOKIE_MAX_AGE
else:
    COOKIE_MAX_AGE = 120


# Create your views here.
class QuestionView(generics.GenericAPIView):
    """
    """
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.validated_data['question']
        context_data = unquote(request.COOKIES.get('context', ''))
        try:
            if context_data and json.loads(context_data).get('domain'):
                answer = chatbot.get_response(question, context=json.loads(context_data))
            else:
                answer = chatbot.get_response(question)
        except Exception as e:
            chatbot.logger.error(str(e))
            answer = {'text': '机器人接口发生了错误，错误信息是:{}'.format(str(e))}

        # response
        response = Response(
            {'text': answer.get('text', '')},
            status=status.HTTP_200_OK
        )

        # set cookie
        context_data = answer.get('context')
        if context_data:
            response.set_cookie('context', quote(json.dumps(context_data)), max_age=COOKIE_MAX_AGE)
        return response


class LearnView(generics.GenericAPIView):
    serializer_class = LearnSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.learn(),
            status=status.HTTP_200_OK
        )
