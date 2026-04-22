import unittest

from settings.settings import settings


class SettingsTestCase(unittest.TestCase):
    def testBasicSettings(self):
        settings.set('ollama_model', 'test_model')
        self.assertEqual(settings.ai_integrate.ollama_model, 'test_model')
        self.assertEqual(settings['ai_integrate']['ollama_model'], 'test_model')

        settings.set('ollama_model', None)
        self.assertEqual(settings.ai_integrate.ollama_model, None)

    def testExternalSettings(self):
        self.assertIs(type(settings.get_text_prompt), str)
