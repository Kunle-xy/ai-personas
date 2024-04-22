
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from .models import Document, CustomUser
# from transformers import T5ForConditionalGeneration, T5Tokenizer
import numpy as np
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

        query_str = request.data['query']
        query_embedding = np.array(embed_model.get_query_embedding(query_str))      
             
        # cater for em[ty databse and generalized answer
        if len(qs) == 0:
            prompt_template = """
                            Respond to the QUESTION below:
                            - If the QUESTION is a general greeting or an inquiry about personal welfare (e.g., "How are you?" or "Good day"),
                            reply in a friendly and jovial manner. These responses should be warm and engaging.
                            - If the QUESTION is too specific and lacks the necessary context or details for a comprehensive answer,
                            kindly request that the user provide more specific details or context to enable a more accurate response.
                            - If the QUESTION can be answered with general knowledge and the answer is known, provide a generalized,
                            honest, and harmless answer.
                            - If you are unable to answer the QUESTION due to a lack of information, either from the context provided
                            or within general knowledge parameters, clearly state "I DO NOT KNOW".

                            QUESTION:
                            {question}

                            ANSWER:
                    """
      
            text_input = prompt_template\
                .replace("{question}", query_str)
            
        else:
            corpus = np.array([item.vector for item in qs])
            prod = np.dot(corpus, query_embedding)
        
            norm = np.linalg.norm(corpus, axis=1) * np.linalg.norm(query_embedding)
            matrix_prod = prod / norm

            # FORGETFULLNESS: ADD PREVIOUS QUERY | RESPONSE TEXT TO CONTEXT IF DOT PRODUCT EXCEED A THRSHOLD

            #sample previous query and response
            prev_query = "where is the nearest grocery store?"
            prev_response = " I do not know. The information required to answer your question is not available in the provided context. The email exchange is focused on job application and paper writing, and does not provide any information about the location of grocery stores.\
                  You may want to try searching online or checking with local directories to find the nearest grocery store."

            prev_query = ""
            prev_response = ""
            prev_query_embedding = np.array(embed_model.get_query_embedding(f"PREVIOUS QUERY: {prev_query} \
                                                                           \n PREVIOUS RESPONSE :{prev_response}"))
            
            prev_prod = np.dot(query_embedding, prev_query_embedding)

            # Top 2 results
            try:
                top_k = np.argsort(matrix_prod)[-2:]
            except:
                top_k = np.argsort(matrix_prod)


            context = [qs[int(i)].text for i in top_k]
            context = '\n'.join(context)
            # print(context)

            
            # top guess if prev_prod is greater than 0.8, then add prev query and response to context
            if prev_prod > 0.83:
                print("prev_prod", prev_prod)
                context = f"PREVIOUS QUERY: {prev_query} \n PREVIOUS RESPONSE :{prev_response} \n {context}"


            prompt_template = """
                            Respond to the QUESTION below:
                            - If the QUESTION is a general greeting or an inquiry about welfare (e.g., "How are you?" or "Good day"),
                            reply in a friendly and jovial manner. Do not include the CONTEXT in your response.
                            - If the QUESTION requires specific information from the CONTEXT (provided below) and the answer can 
                            be determined from the CONTEXT, provide that answer.
                            - If the QUESTION pertains to general knowledge or topics not covered in the CONTEXT, such as current events or public information,
                            and if this information is readily available to the model, provide an informed response using general knowledge. 
                            Alternatively, suggest reliable sources where the user can verify the current information (e.g., "You might check the latest sports news outlets for the current heavyweight champion as this information changes frequently.").
                            - If the answer cannot be determined from the CONTEXT, is not within the general knowledge capabilities of the model, or requires updated information that the model cannot access,
                            explicitly state the limitations and respond with "I DO NOT KNOW. The information required to answer your question is not available in the provided context nor within my current dataset. For up-to-date information, please refer to relevant external sources."


                                CONTEXT:
                                {context}

                                QUESTION:
                                {question}

                                ANSWER:

                                """
        
            text_input = prompt_template.replace("{context}", context)\
                .replace("{question}", query_str)

        output = replicate.run(
            "meta/llama-2-70b-chat",
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
        # TRANSPARENCY
        # Print all retrieved contexts excluding previous query and response if added at some point.
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

