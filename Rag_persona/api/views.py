
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from .models import Document, CustomUser
from transformers import AutoModelForCausalLM, AutoTokenizer
# from transformers import T5ForConditionalGeneration, T5Tokenizer
import numpy as np
import torch
from transformers import BitsAndBytesConfig
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import Settings


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import DocumentSerializer, CreateUserSerializer,\
      UpdateUserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
# from llama_index.core.schema import TextNode

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.core.query_engine import RetrieverQueryEngine

device = "cuda"
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

import replicate
from dotenv import load_dotenv
import os
load_dotenv()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PromptView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        qs = Document.objects.filter(user=user.id).order_by('-uploaded_at')
        # print(qs)

        corpus = np.array([item.vector for item in qs])
        query_str = request.data['query']
        query_embedding = np.array(embed_model.get_query_embedding(query_str))

        prod = np.dot(corpus, query_embedding)
        norm = np.linalg.norm(corpus, axis=1) * np.linalg.norm(query_embedding)

        matrix_prod = prod / norm
        # print(matrix_prod)

        # Top 5 results
        try:
            top_k = np.argsort(matrix_prod)[-2:]
        except:
            top_k = np.argsort(matrix_prod)

   
        # print(top_k)
        # if len(qs) > 5:
        #     top_k = np.argsort(matrix_prod, axis=0)[-5:]

        # else:
        #     top_k = np.argsort(matrix_prod, axis=0)

        context = [qs[int(i)].text for i in top_k]
        context = '\n'.join(context)

        prompt_template = """Answer the following QUESTION based on the CONTEXT
                            given. If you do not know the answer and the CONTEXT doesn't
                            contain the answer truthfully and return "I DO NOT KNOW".

                            CONTEXT:
                            {context}

                            QUESTION:
                            {question}

                            ANSWER:
                            """
      
        text_input = prompt_template.replace("{context}", context)\
            .replace("{question}", query_str)

        output = replicate.run(
            "meta/llama-2-13b-chat",
            input={
                "debug": False,
                "top_k": -1,
                "top_p": 1,
                "prompt": text_input,
                "temperature": 0.05,
                "system_prompt": "You are a helpful and truthful assistant, answer only if you know the answer. If you do not know the answer, truthfully say 'I do not know'.",
                "max_new_tokens": 800,
                "min_new_tokens": -1,
                "repetition_penalty": 1
            }
        )

        print("".join(output))
        return Response('123')

prompt = PromptView.as_view()



class DocumentList(ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        """
        This view should return a list of all the documents
        for the currently authenticated user.
        """
        user = self.request.user
        print(Document.objects.filter(user=user.id))
        return Document.objects.filter(user=user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class DocumentList(ListCreateAPIView):
#     serializer_class = DocumentSerializer
#     queryset = Document.objects.all()

#     def perform_create(self, serializer):
#         serializer.save()

documentlist = DocumentList.as_view()


class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)
createuser = CreateUserAPI.as_view()


class UpdateUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
updateuser = UpdateUserAPI.as_view()

