from unittest import TestCase

from actions.actions import string_to_list, get_matching_diseases, filter_fn


class Test(TestCase):

    def test_string_to_list_unique(self):
        result = string_to_list("['itch', 'acanthosis nigricans']")
        expected = ['itch', 'acanthosis nigricans']
        self.assertListEqual(sorted(result), sorted(expected))

    def test_string_to_list_empty(self):
        result = string_to_list("")
        expected = []
        self.assertListEqual(sorted(result), sorted(expected))

    def test_string_to_list_duplicate(self):
        result = string_to_list("['itch','itch', 'acanthosis nigricans']")
        expected = ['itch', 'acanthosis nigricans']
        self.assertListEqual(sorted(result), sorted(expected))

    def test_string_to_list_upper(self):
        result = string_to_list("['ITCH', 'acanthosis nigricans']")
        expected = ['itch', 'acanthosis nigricans']
        self.assertListEqual(sorted(result), sorted(expected))

    def test_get_matching_disease(self):
        symptom_list = ['stomachache ', 'fever', 'skin discoloration', 'blisters']
        result = get_matching_diseases(symptom_list)
        self.assertEquals(len(result), 1)
        expected = {'Gangrene': {
            'symptom_list': ['sore', 'septic shock', 'gangrene', 'trauma', 'gangrenous', 'skin discoloration',
                             'blisters or lesions', 'shortness of breath confusion', 'blisters', 'bacterial infection',
                             'sudden pain', 'fever', 'numbness a foul-smelling', 'pain'], 'score': 3}}

        self.assertIn('Gangrene', result)
        self.assertListEqual(sorted(result['Gangrene']['symptom_list']), sorted(expected['Gangrene']['symptom_list']))
        self.assertEquals(result['Gangrene']['score'], expected['Gangrene']['score'])

    def test_filter_fu(self):
        row = {'symptom_list': ['itch', 'acanthosis nigricans'], 'name': 'Acanthosis nigricans'}
        symptoms = ['itch']

        result = filter_fn(row, symptoms)
        self.assertEqual(result, 1)
