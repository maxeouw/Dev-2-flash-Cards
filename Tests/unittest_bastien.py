import unittest
from core.audio_manager import AudioManager

class TestAudioManagerRate(unittest.TestCase):    
    def setUp(self):
        self.manager = AudioManager()
    
    
    def test_rate_valid_minimum(self):
        self.manager.rate = 50
        self.assertEqual(self.manager.rate, 50)
    
    def test_rate_valid_maximum(self):
        self.manager.rate = 300
        self.assertEqual(self.manager.rate, 300)
    
    def test_rate_valid_middle(self):
        self.manager.rate = 150
        self.assertEqual(self.manager.rate, 150)
    
    def test_rate_invalid_below_minimum(self):
        with self.assertRaises(ValueError) as context:
            self.manager.rate = 49
        self.assertIn("entre 50 et 300", str(context.exception))
    
    def test_rate_invalid_above_maximum(self):
        with self.assertRaises(ValueError) as context:
            self.manager.rate = 301
        self.assertIn("entre 50 et 300", str(context.exception))


class TestAudioManagerActif(unittest.TestCase):
    
    def setUp(self):
        self.manager = AudioManager()

    
    def test_actif_true(self):
        self.manager.actif = True
        self.assertTrue(self.manager.actif)
    
    def test_actif_false(self):
        self.manager.actif = False
        self.assertFalse(self.manager.actif)
    
    def test_actif_invalid_string(self):
        with self.assertRaises(ValueError) as context:
            self.manager.actif = "true"
        self.assertIn("booléen", str(context.exception))
    
    def test_actif_invalid_integer(self):
        with self.assertRaises(ValueError) as context:
            self.manager.actif = 1
        self.assertIn("booléen", str(context.exception))
    
    def test_actif_invalid_none(self):
        with self.assertRaises(ValueError) as context:
            self.manager.actif = None
        self.assertIn("booléen", str(context.exception))


if __name__ == '__main__':
    unittest.main()
