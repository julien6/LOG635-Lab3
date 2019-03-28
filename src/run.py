import nltk
from nltk import load_parser

def printResults (results):
    for result in results:
        for (synrep, semrep) in result:
            print(semrep)

sents1 = ['La victime est moutarde']
sents1bis = ['Rose est la victime']

sents2 = ['Tu es dans la cuisine']
sents2bis = ['Tu te trouves dans le salon']

sents3 = ['L_heure du crime est 3h']

sents4 = ['Moutarde était avec prevenche à 4h']

#printResults(nltk.interpret_sents(sents3, '635/heure_crime.fcfg'))

printResults(nltk.interpret_sents(sents4, '635/etait_avec_qui.fcfg'))

#printResults(nltk.interpret_sents(sents1, '635/victime.fcfg'))
#printResults(nltk.interpret_sents(sents1bis, '635/victime.fcfg'))