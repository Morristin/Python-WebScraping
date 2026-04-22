import logging

import ollama

from settings import settings

logging.getLogger(__name__)


class Ollama:
    """
    A class for ollama integrating.
    This class connect with the local ollama application, perform chat and handle exceptions.

    Visit https://ollama.com/ for more information.
    """

    _client = ollama.Client()

    class OllamaNotEnabledError(Exception):
        """
        Did not specific the name of ollama model in settings.json.
        In this situation ollama module cannot be used.
        """

    class OllamaError(Exception):
        """
        This exception is used to package the exception raised by ollama,
        so outer module can handle exception more easily.
        """

    def __init__(self, model: str = settings.ai_integrate.ollama_model):
        if model is None:
            raise self.OllamaNotEnabledError()
        else:
            self.model = model

            try:
                self._client.chat(model=self.model)
            except ollama.ResponseError as err:
                if err.status_code == 404:
                    logging.error(f'Cannot use {self.model} via ollama as the model does not exist.')
                else:
                    logging.warning(f'Cannot use {self.model} via ollama. Error message: {err.error}')
                raise self.OllamaError from err

    def chat(self, content: str, role: str = 'user') -> str:
        """
        Create chat via ollama and return the pure content ollama model responses.

        If the content given is not blank but cannot detect response,
        function will raise `Ollama.OllamaError` for exception handling.
        """
        response = self._client.chat(model=self.model, messages=[{'role': role, 'content': content}])
        logging.debug(f'Get chat response from ollama: {response}')
        if response.message.content is None:
            if len(content.strip()) != 0:
                raise self.OllamaError(f'Cannot detect response\'s content from ollama ChatResponse: {response}')
            else:
                return ''  # TODO: 此处实现可能需要之后根据调用者所需进行更改
        else:
            return response.message.content
