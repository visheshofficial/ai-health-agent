from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class RepeatInformation(Action):
    '''
    Custom action to repeat information to the user
    '''
    def name(self) -> Text:
        return "action_repeat_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("inside action_repeat_information ")
        symptoms: list = list(set(tracker.get_slot("symptoms")))
        if symptoms:
            text = "As i could understand, you have entered following symptoms: \n\n" + "\n\n".join(symptoms)
        else:
            text = "As i could not understand the symptoms entered"
        dispatcher.utter_message(text=text)
        print("I did not found any disease in the text")
        return []


class RememberSymptoms(Action):
    '''
    Custom action for symptoms slot filling
    '''

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
            symptoms = list(set(symptoms))
            print(symptoms)
            return [SlotSet("disease", None), SlotSet("symptoms", symptoms)]
        print("I did not found any disease in the text")

        return []


class DetectDisease(Action):
    '''
    Custom action for calling get_matching_diseases service
    '''
    def name(self) -> Text:
        return "action_predict_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("inside action_predict_disease ")
        dispatcher.utter_message(text="Checking for diseases corresponding to the entered symptoms.")
        symptoms: list = tracker.get_slot("symptoms")
        potential_diseases = get_matching_diseases(symptoms)
        print(str(potential_diseases))
        if potential_diseases:
            dispatcher.utter_message(
                text="Your symptoms are matching with these diseases: \n\n" + str(
                    "\n\n".join(list(potential_diseases.keys()))))
        else:
            dispatcher.utter_message(
                text="I am unable to help you with the information you provided.")

        return []


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
    :param row: pandas row
    :param symptoms: symptom list
    :return:
    """
    count = 0
    for s in symptoms:
        if s in row['symptom_list']:
            count = count + 1
    return count


def get_matching_diseases(symptom_list):
    '''

    :param symptom_list: list of symptoms
    :return: dictionary of disease name and score
    '''
    print("inside get_matching_diseases")
    import os
    # to get the current working directory
    directory = os.getcwd()
    print(directory)
    import pandas as pd
    data = pd.read_csv('./db/df_diseases_processed.csv')

    # data[['name', 'symptom_list']]
    data['symptom_list'] = data['symptom_list'].apply(string_to_list)
    dis_sym = data[['symptom_list', 'name']]
    # dis_sym
    dis_sym["score"] = dis_sym.apply(filter_fn, symptoms=symptom_list, axis=1)
    result = dis_sym[dis_sym["score"] > 0]
    # result.sort_values(by=["score","name"],ascending=False)
    result = result[result['score'] == result['score'].max()].sort_values(by=["score", "name"])
    return result.head(10).set_index('name').to_dict('index')
