import nltk

class CrimeSentenceAnalyzer: 

    def __init__(self):
        self._victim_grammar_file = '635/victime.fcfg'
        self._location_grammar_file = '635/emplacement.fcfg'
        self._crime_hour_grammar_file = '635/heure_crime.fcfg'
        self._location_hour_grammar_file = '635/emplacement_heure.fcfg'
        self._location_person_grammar = '635/emplacement_personnage.fcfg'
        self.was_with_who_grammar = '635/etait_avec_qui.fcfg'

    def who_is_the_victime(self, sentence):
        return str(nltk.interpret_sents(sentence, self._victim_grammar_file)[0][0][1])

    def where_am_i(self, sentence):
        return str(nltk.interpret_sents(sentence, self._location_grammar_file)[0][0][1])

    #Moutarde est dans la cuisine
    def where_is_person(self, sentence):
        result = str(nltk.interpret_sents(sentence, self._location_person_grammar)[0][0][1])
        return self.parse_result_person_location(result)

    #L_heure du crime est 22h
    #La victime est morte à 22h
    #La victime a été tuée à 22h
    def what_is_the_crime_hour(self, sentence):
        return 'H' + str(nltk.interpret_sents(sentence, self._crime_hour_grammar_file)[0][0][1])

    #Moutarde était dans le salon à 22h
    def where_in_room_in_hour(self, sentence):
        result = str(nltk.interpret_sents(sentence, self._location_hour_grammar_file)[0][0][1])
        return self.parse_result_room_hour(result)

    def who_was_with_who(self, sentence):
        result = str(nltk.interpret_sents(sentence, self.was_with_who_grammar)[0][0][1])
        return self.parse_result_was_with(result)

    def parse_result_room_hour(self, result):
        response = {}
        response['name'] = result.split(',')[0].split('(')[1]
        response['room'] = result.split(',')[1]
        response['hour'] = 'H' + result.split(',')[2].split(')')[0]
        return response

    def parse_result_person_location(self, result):
        response = {}
        response['name'] = result.split(',')[0].split('(')[1]
        response['room'] = result.split(',')[1].split(')')[0]
        return response

    def parse_result_was_with(self, result):
        response = {}
        response['name1'] = result.split(',')[0].split('(')[1]
        response['name2'] = result.split(',')[1]
        response['hour'] = 'H' + result.split(',')[2].split(')')[0]
        return response