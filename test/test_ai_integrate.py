import unittest

from ai_integrate.ollama_integrate import Ollama


class OllamaIntegrateTestCase(unittest.TestCase):
    def testOllamaBasicOperations(self):
        self.assertHasAttr(Ollama(model='gemma4:31b-cloud'), 'model')
