from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
# from symptom_matcher import get_matching_diseases


class RememberSymptoms(Action):

    def name(self) -> Text:
        return "action_remember_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("inside action_remember_symptoms ")
        diseases: list = list(tracker.get_latest_entity_values("DISEASE"))
        if diseases:
            diseases = [x.lower() for x in diseases]
            print("Newly added symptoms are :" + str(diseases))
            symptoms: list = tracker.get_slot("symptoms")
            if symptoms is None:
                symptoms = list()
            symptoms.extend(diseases)
            print(symptoms)
            return [SlotSet("disease", None), SlotSet("symptoms", symptoms)]
        print("I did not found any disease in the text")

        return []


class DetectDisease(Action):
    def name(self) -> Text:
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("inside action_predict_disease ")
        dispatcher.utter_message(text="utter_working_on_it")
        symptoms: list = tracker.get_slot("symptoms")
        potential_diseases = get_matching_diseases(symptoms)
        print(str(potential_diseases))
        if potential_diseases:
            dispatcher.utter_message(
                text="Your symptoms are matching with these diseases:" + str("\n".join(list(potential_diseases.keys()))))
        else:
            dispatcher.utter_message(
                text="I am unable to help you with the information you provided.")

        return []


############################
class ActionRememberSubjects(Action):

    def name(self) -> Text:
        return "action_remember_subjects"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("inside action_remember_subjects")
        new_subjects: list = list(tracker.get_latest_entity_values("subject"))
        if new_subjects:
            print("Newly added subjects are :" + str(new_subjects))
            subjects: list = tracker.get_slot("subjects")
            if subjects is None:
                subjects = list()
            subjects.extend(new_subjects)
            print(subjects)
            return [SlotSet("subject", None), SlotSet("subjects", subjects)]
        want_to_add_more_subjects = tracker.get_slot("want_to_add_more_subjects")
        if want_to_add_more_subjects:
            print("user want to add more subjects.")
            return [SlotSet("subject", None)]

        return []


class ActionSubjects(Action):

    def name(self) -> Text:
        return "action_iterate_for_subjects"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        want_to_add_more_subjects = tracker.get_slot("want_to_add_more_subjects")
        if want_to_add_more_subjects:
            print("user want to add more subjects.")
            return [SlotSet("subject", None)]

        return []


class ValidateAdmissionForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_admission_form"

    def validate_want_to_add_more_subjects(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_intent_of_latest_message() == "affirm":
            SlotSet("subject", None)
            return {"want_to_add_more_subjects": None}
        return {"want_to_add_more_subjects": False}

"""
This modul is used to match disease with provided symptom.

"""


def string_to_list(input_string: str):
    """
    Convert a string containing list to python list data type
    :param input_string:
    :return: list
    """
    import json
    if len(input_string.strip()) > 1:
        temp = input_string.replace("'", "\"").lower()
        list_result = json.loads(temp)
        return list(set(list_result))
    else:
        return []


def filter_fn(row, symptoms):
    """
    Filters pandas rows that contains symptoms
    :param row:
    :param symptoms:
    :return:
    """
    count = 0
    for s in symptoms:
        if s in row['symptom_list']:
            count = count + 1
    return count


def get_matching_diseases(symptom_list):
    print("inside get_matching_diseases")
    import os
    # to get the current working directory
    directory = os.getcwd()
    print(directory)
    import pandas as pd
    data = pd.read_excel('./db/df_diseases_processed.xlsx')

    # data[['name', 'symptom_list']]
    data['symptom_list'] = data['symptom_list'].apply(string_to_list)
    dis_sym = data[['symptom_list', 'name']]
    # dis_sym
    dis_sym["score"] = dis_sym.apply(filter_fn, symptoms=symptom_list, axis=1)
    result = dis_sym[dis_sym["score"] > 0]
    # result.sort_values(by=["score","name"],ascending=False)
    result = result[result['score'] == result['score'].max()].sort_values(by=["score", "name"])
    return result.set_index('name').to_dict('index')