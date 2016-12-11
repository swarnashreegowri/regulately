# # -*- coding: utf-8 -*-
# import json
# import requests
# from apikeys import IBMWatson
# from textstat.textstat import textstat

# from watson_developer_cloud import AlchemyLanguageV1

# API_KEY = IBMWatson

# alchemy_language = AlchemyLanguageV1(api_key=API_KEY)

# def getSentiment (text):
# 	score = json.loads(json.dumps(alchemy_language.sentiment(text=text),indent=2))["docSentiment"]["score"]
# 	if score:
# 		return score
# 	else:
# 		return 0 

# def getConcepts (text):
# 	return json.loads(json.dumps(alchemy_language.concepts(text=text),indent=2))

# def getKeywords (text):
# 	return json.loads(json.dumps(alchemy_language.keywords(text=text),indent=2))

# def getEmotion (text):
# 	return json.loads(json.dumps(alchemy_language.emotion(text=text),indent=2))

# def extractEntities (text):
# 	return json.loads(json.dumps(alchemy_language.entities(text = text),indent=2))

# def getSimilarity (textOne, textTwo):
# 	payload = {
# 	  "sentence1": textOne,
# 	  "sentence2": textTwo
# 	}

# 	headers = {
# 	  'content-type': "application/json",
# 	  'authorization': "Token 9697c0d6aff7433ec62fecc4a00cecc464fc732c",
# 	}

# 	status = requests.post('http://dev.neuronme.com/api/semanticrelatedness/', data=json.dumps(payload), headers=headers)
# 	return status.json()["Score"]

# def getComplexity ():
# 	test_data = """Playing games has always been thought to be important to the development of well-balanced and creative children; however, what part, if any, they should play in the lives of adults has never been researched that deeply. I believe that playing games is every bit as important for adults as for children. Not only is taking time out to play games with our children and other adults valuable to building interpersonal relationships but is also a wonderful way to release built up tension."""
# 	print textstat.flesch_reading_ease(test_data)
# 	print textstat.smog_index(test_data)
# 	print textstat.flesch_kincaid_grade(test_data)
# 	print textstat.coleman_liau_index(test_data)
# 	print textstat.automated_readability_index(test_data)
# 	print textstat.dale_chall_readability_score(test_data)
# 	print textstat.difficult_words(test_data)
# 	print textstat.linsear_write_formula(test_data)
# 	print textstat.gunning_fog(test_data)
# 	print textstat.text_standard(test_data)

