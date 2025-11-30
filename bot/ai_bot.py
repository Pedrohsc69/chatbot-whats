import os
from decouple import config
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')

class AIBot:

    def __init__(self):
        self.__chat = ChatGroq(model='llama-3.3-70b-versatile')

    def invoke(self, texto, idioma):
        prompt = PromptTemplate(
            input_variables=['texto', 'idioma'],
            template='''
            Você é um tradutor de textos profissional. Traduza o texto abaixo para o idioma: {idioma}. Sempre que possível utilize emojis nas suas respostas para torná-la mais divertida.
            <texto>
            {texto}
            </texto>
            '''
        )
        chain = prompt | self.__chat | StrOutputParser()
        response = chain.invoke({
            'texto': texto,
            'idioma': idioma,
        })
        return response
