# -*- coding: utf-8 -*-
import json

from textstat.textstat import textstat
from watson_developer_cloud import AlchemyLanguageV1

from lib.external_services import IBMWatson

API_KEY = IBMWatson

alchemy_language = AlchemyLanguageV1(api_key=API_KEY)

def getSentiment (text):
    if not text.strip():
        return 0
    try: 
        docSentiment = json.loads(json.dumps(alchemy_language.sentiment(text=text),indent=2))["docSentiment"]
        return float(docSentiment.get("score", 0))
    except:
        return 0

def getConcepts (text):
    concepts = []
    conceptsJson = json.loads(json.dumps(alchemy_language.concepts(text=text),indent=2))["concepts"]
    for newConcept in conceptsJson:
        concept = {"relevance": newConcept["relevance"], "text": newConcept["text"]}
        concepts.append(concept)
    return concepts

<<<<<<< Updated upstream
def getKeywords (text):
    keywords = []
    keywordsJson = json.loads(json.dumps(alchemy_language.keywords(text=text),indent=2))["keywords"]
=======

def getKeywords(text):
    keywords = []
    keywordsJson = json.loads(json.dumps(alchemy_language.keywords(text=text), indent=2))["keywords"]
>>>>>>> Stashed changes
    for newKeyword in keywordsJson:
        keyword = {"relevance": newKeyword["relevance"], "text": newKeyword["text"]}
        keywords.append(keyword)
    return keywords

<<<<<<< Updated upstream
def getEmotions (text):
    return json.loads(json.dumps(alchemy_language.emotion(text=text),indent=2))["docEmotions"]

def extractEntities (text):
    return json.loads(json.dumps(alchemy_language.entities(text = text),indent=2))["entities"]
=======

def getEmotions(text):
    return json.loads(json.dumps(alchemy_language.emotion(text=text), indent=2))["docEmotions"]


def extractEntities(text):
    return json.loads(json.dumps(alchemy_language.entities(text=text), indent=2))["entities"]

>>>>>>> Stashed changes

# def getSimilarity (textOne, textTwo):
#     payload = {
#       "sentence1": textOne,
#       "sentence2": textTwo
#     }

#     headers = {
#       'content-type': "application/json",
#       'authorization': "Token 9697c0d6aff7433ec62fecc4a00cecc464fc732c",
#     }

#     status = requests.post('http://dev.neuronme.com/api/semanticrelatedness/', data=json.dumps(payload), headers=headers)
#     return status.json()["Score"]

<<<<<<< Updated upstream
def getComplexity (text):
    '''
    90-100 : Very Easy 
    80-89 : Easy 
    70-79 : Fairly Easy 
    60-69 : Standard 
    50-59 : Fairly Difficult 
    30-49 : Difficult 
    0-29 : Very Confusing
    '''
=======

def get_complexity(text):
    """
    0-100 : Very Easy
    80-89 : Easy
    0-79 : Fairly Easy
    60-69 : Standard
    50-59 : Fairly Difficult
    30-49 : Difficult
    0-29 : Very Confusing
    :param text:
    :return:
    """
>>>>>>> Stashed changes
    return textstat.flesch_reading_ease(text)
