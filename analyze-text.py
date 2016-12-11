# -*- coding: utf-8 -*-
import json
import requests
from watson_developer_cloud import AlchemyLanguageV1

with open('apikeys.json') as data_file:    
    API_KEY = json.load(data_file)["IBMWatson"]

alchemy_language = AlchemyLanguageV1(api_key=API_KEY)

def getSentiment (text):
	score = json.loads(json.dumps(alchemy_language.sentiment(text=text),indent=2))["docSentiment"]["score"]
	if score:
		return score
	else:
		return 0 

def getConcepts (text):
	return json.loads(json.dumps(alchemy_language.concepts(text=text),indent=2))

def getKeywords (text):
	return json.loads(json.dumps(alchemy_language.keywords(text=text),indent=2))

def getEmotion (text):
	return json.loads(json.dumps(alchemy_language.emotion(text=text),indent=2))

def extractEntities (text):
	return json.loads(json.dumps(alchemy_language.entities(text = text),indent=2))

def getSimilarity (textOne, textTwo):
	payload = {
	  "sentence1": textOne,
	  "sentence2": textTwo
	}

	headers = {
	  'content-type': "application/json",
	  'authorization': "Token 9697c0d6aff7433ec62fecc4a00cecc464fc732c",
	}

	status = requests.post('http://dev.neuronme.com/api/semanticrelatedness/', data=json.dumps(payload), headers=headers)
	return status.json()["Score"]