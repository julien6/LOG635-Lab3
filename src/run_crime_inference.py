from src import CrimeInference
import nltk

a = CrimeInference.CrimeInference()


def getStringResults(results):
    res = ''
    for result in results:
        for (synrep, semrep) in result:
            res += str(semrep)
    return res

#####   step 0 :

sents1 = ['Scarlet est morte']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents1, '635/personne_morte.fcfg')))

sents2 = ['Mustard est vivant']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents2, '635/personne_vivant.fcfg')))

sents3 = ['Peacock est vivant']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents3, '635/personne_vivant.fcfg')))

sents4 = ['Plum est vivant']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents4, '635/personne_vivant.fcfg')))

sents5 = ['White est vivant']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents5, '635/personne_vivant.fcfg')))

#####   step 1 : Bureau

# Voit que Scarlet est morte par étranglement
sents6 = ['Scarlet a des marques au cou']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents6, '635/personne_marque.fcfg')))

sents7 = ['Scarlet est dans le bureau']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents7, '635/personne_piece.fcfg')))

# Voit que Peacock est dans le bureau
sents8 = ['Peacock est dans le bureau']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents8, '635/personne_piece.fcfg')))

# Demande à Peacock l'heure du decès -> Rep : 14h
sents9 = ['Scarlet est morte à 14h']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents9, '635/personne_morte_heure.fcfg')))

uneHeureApres = a.get_crime_heure() + 1

a.add_any_clause('HeureCrimePlusOne({})'.format(uneHeureApres))

# Demande à Peacock dans quelle pièce il était une heure après le meurtre -> Rep : Peacock dans le Salon à 15h
sents10 = ['Peacock était dans le salon à ' + str(uneHeureApres) + 'h']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents10, '635/personne_piece_heure.fcfg')))

#####   step 2 : Salon

# Voit qu'il y a un fusil et Plum dans le salon
sents11 = ['Le fusil est dans le salon']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents11, '635/arme_piece.fcfg')))

sents12 = ['Plum est dans le salon']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents12, '635/personne_piece.fcfg')))

# Demande à Plum dans quelle pièce il était une heure après le meurtre -> Rep : Plum dans le Salon à 15h
sents13 = ['Plum était dans le salon à ' + str(uneHeureApres) + 'h']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents13, '635/personne_piece_heure.fcfg')))

#####   step 3 : Cuisine

# Voit qu'il y a un couteau, White et Mustard dans la cuisine
sents14 = ['Le couteau est dans la cuisine']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents14, '635/arme_piece.fcfg')))
sents15 = ['White est dans la cuisine']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents15, '635/personne_piece.fcfg')))
sents16 = ['Mustard est dans la cuisine']
print(getStringResults(nltk.interpret_sents(sents16, '635/personne_piece.fcfg')), " ------")
a.add_any_clause(getStringResults(nltk.interpret_sents(sents16, '635/personne_piece.fcfg')))

# Demande à White dans quelle pièce il était une heure après le meurtre -> Rep : White dans la Cuisine à 15h
sents17 = ['White était dans la cuisine à ' + str(uneHeureApres) + 'h']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents17, '635/personne_piece_heure.fcfg')))

# Demande à Mustard dans quelle pièce il était une heure après le meurtre -> Rep : Mustard dans le Garage à 15h
sents18 = ['Mustard était dans le garage à ' + str(uneHeureApres) + 'h']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents18, '635/personne_piece_heure.fcfg')))

#####   step 4 : Garage

# Voit qu'il y a une corde dans le garage
sents19 = ['La corde est dans le garage']
a.add_any_clause(getStringResults(nltk.interpret_sents(sents19, '635/arme_piece.fcfg')))

## -> extract informations
print("Pièce du crime : ", a.get_piece_crime())
print("Arme du crime : ", a.get_arme_crime())
print("Personne victime : ", a.get_victime())
print("Heure du crime : ", a.get_crime_heure())
print("Personne suspecte : ", a.get_suspect())
print("Personnes innocentes : ", a.get_innocent())
