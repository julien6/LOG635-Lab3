from src import CrimeInference
import nltk

a = CrimeInference.CrimeInference()


def printResults(results):
    for result in results:
        for (synrep, semrep) in result:
            print(semrep)


# sents0 = ['Le fusil se trouve dans le salon']
# sents0 = ['Plum est dans la cuisine']
sents0 = ['White est vivante']
printResults(nltk.interpret_sents(sents0, '635/arme_piece.fcfg'))

# #####   step 0 :
#
# sents1 = ['Scarlet est morte']
# a.add_personne_morte("Scarlet")
#
# sents2 = ['Mustard est vivant']
# a.add_personne_vivante('Mustard')
#
# sents3 = ['Peacock est vivant']
# a.add_personne_vivante('Peacock')
#
# sents4 = ['Plum est vivant']
# a.add_personne_vivante('Plum')
#
# sents5 = ['White est vivant']
# a.add_personne_vivante('White')
#
# #####   step 1 : Bureau
#
# # Voit que Scarlet est morte par étranglement
# sents6 = ['Scarlet a des marques']
# a.add_marque_corps('Scarlet')
#
# sents7 = ['Scarlet est dans le bureau']
# a.add_personne_piece('Scarlet', 'Bureau')
#
# # Voit que Peacock est dans le bureau
# sents8 = ['Peacock est dans le bureau']
# a.add_personne_piece('Peacock', 'Bureau')
#
# # Demande à Peacock l'heure du decès -> Rep : 14h
# sents9 = ['Scarlet est morte à 14h']
# a.add_crime_heure(14)
#
# uneHeureApres = a.get_crime_heure_plusone()
#
# # Demande à Peacock dans quelle pièce il était une heure après le meurtre -> Rep : Peacock dans le Salon à 15h
# sents10 = ['Peacock etait dans le salon à ' + uneHeureApres]
# a.add_personne_piece_heure('Peacock', 'Salon', a.get_crime_heure_plusone())
#
# #####   step 2 : Salon
#
# # Voit qu'il y a un fusil et Plum dans le salon
# sents11 = ['Le fusil est dans le salon']
# a.add_arme_piece('Fusil', 'Salon')
# sents12 = ['Plum est dans le salon']
# a.add_personne_piece('Plum', 'Salon')
#
# # Demande à Plum dans quelle pièce il était une heure après le meurtre -> Rep : Plum dans le Salon à 15h
# sents13 = ['Plum etait dans le salon à ' + uneHeureApres]
# a.add_personne_piece_heure('Plum', 'Salon', a.get_crime_heure_plusone())
#
# #####   step 3 : Cuisine
#
# # Voit qu'il y a un couteau, White et Mustard dans la cuisine
# sents14 = ['Le couteau est dans la cuisine']
# a.add_arme_piece('Couteau', 'Cuisine')
# sents15 = ['White est dans la cuisine']
# a.add_personne_piece('White', 'Cuisine')
# sents16 = ['Mustard est dans la cuisine']
# a.add_personne_piece('Mustard', 'Cuisine')
#
# # Demande à White dans quelle pièce il était une heure après le meurtre -> Rep : White dans la Cuisine à 15h
# sents17 = ['White etait dans la cuisine à ' + uneHeureApres]
# a.add_personne_piece_heure('White', 'Salon', a.get_crime_heure_plusone())
#
# # Demande à Mustard dans quelle pièce il était une heure après le meurtre -> Rep : Mustard dans le Garage à 15h
# sents18 = ['Mustard etait dans le garage à ' + uneHeureApres]
# a.add_personne_piece_heure('Mustard', 'Garage', a.get_crime_heure_plusone())
#
# #####   step 4 : Garage
#
# # Voit qu'il y a une corde dans le garage
# sents19 = ['La corde est dans le garage']
# a.add_arme_piece('Corde', 'Garage')
#
# ## -> extract informations
# print("Pièce du crime : ", a.get_piece_crime())
# print("Arme du crime : ", a.get_arme_crime())
# print("Personne victime : ", a.get_victime())
# print("Heure du crime : ", a.get_crime_heure())
# print("Personnes suspectes : ", a.get_suspect())
# print("Personnes innocentes : ", a.get_innocent())
