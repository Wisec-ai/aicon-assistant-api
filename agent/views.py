import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .domain.entities.ChatDocumentoInfoRequest import ChatDocumentoInfoRequest
from .domain.repository.ai_retriver import AiRetriver
from .application.service.response_question import ResponseQuestion
from django.http import StreamingHttpResponse
from .domain.repository.transformer_si import TransformerSystemInstruction
from .domain.constants.prompts import DEFAULT_PROMPT

@method_decorator(csrf_exempt, name='dispatch')
class AgentConversationAPI(APIView):

    authentication_classes = []     
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        try:
            def generate_stream_response():
                try:

                    documents_info = ChatDocumentoInfoRequest(**request.data)

                    print("Estoy aqui")

                    ai_retriver = AiRetriver(max_documents=documents_info.max_documents)
                    few_examples = ai_retriver.get_few_examples(documents_info.question)

                    print("Fui al retriver")

                    response_question_service = ResponseQuestion()
                    template_system_instruction = DEFAULT_PROMPT

                    llm_system_instruction = TransformerSystemInstruction(
                         template_system_instruction,
                         few_examples
                    ).generate_system_instruction()

                    iterator_llm_response = response_question_service.generate_async_response_by_question(
                        llm_system_instruction,
                        documents_info.question
                    )
                    
                    for text_llm_response in iterator_llm_response:
                                yield json.dumps(
                                    {"raw_response": text_llm_response.text}
                                ) + "\n"

                except Exception as error:
                    yield json.dumps(
                                {"error": f"{str(error)}\n"}
                            ) + "\n"

            streaming_response = StreamingHttpResponse(generate_stream_response(), content_type='text/event-stream')
            streaming_response['Cache-Control'] = 'no-cache'
            
            return streaming_response

        except Exception as e:

            return Response(
                {
                    "error": "Error uploading file to cloud storage",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )