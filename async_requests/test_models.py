import unittest
import models

class TestFakeName(unittest.TestCase):

    def test_is_valid_name(self):

        valid_names = [
            'Kassulke', 'Glover', 'Kling', 'Heidenreich', 'Larson',
            'Palma', 'Abshire', 'Batz', 'Mills', 'Horacio' 
        ]

        invalid_names = [
            'PhD', 'MD', 'Prof.', 'Mr.', 'Dr.', 'Sr.', 'I', 
            'DDS', 'II', 'IV', 'DVM', 'Miss', 'Ms.', 'Mrs.'
        ]

        for name in valid_names:
            with self.subTest(name=name):
                self.assertTrue(models.FakeName.is_valid_name(name))

        for name in invalid_names:
            with self.subTest(name=name):
                self.assertFalse(models.FakeName.is_valid_name(name))


if __name__ == "__main__":
    unittest.main()