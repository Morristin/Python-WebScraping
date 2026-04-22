import unittest

from settings import settings


class SettingsTestCase(unittest.TestCase):
    def testSettings(self):
        settings.set('ollama_model', 'test_model')
        self.assertEqual(settings.ai_integrate.ollama_model, 'test_model')
        self.assertEqual(settings['ai_integrate']['ollama_model'], 'test_model')

        settings.set('ollama_model', None)
        self.assertEqual(settings.ai_integrate.ollama_model, None)
