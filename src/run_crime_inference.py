from src import CrimeInference

a = CrimeInference.CrimeInference()

#####   step 0 :
a.add_personne_morte("Scarlet")
a.add_personne_vivante('Mustard')
a.add_personne_vivante('Peacock')
a.add_personne_vivante('Plum')
a.add_personne_vivante('White')

#####   step 1 : Bureau

# Voit que Scarlet est morte par étranglement
a.add_marque_corps('Scarlet')
a.add_personne_piece('Scarlet', 'Bureau')

# Voit que Peacock est dans le bureau
a.add_personne_piece('Peacock', 'Bureau')

# Demande à Peacock l'heure du decès -> Rep : 14h
a.add_crime_heure(14)

# Demande à Peacock dans quelle pièce il était une heure après le meurtre -> Rep : Peacock dans le Salon à 15h
a.add_personne_piece_heure('Peacock', 'Salon', a.get_crime_heure_plusone())

#####   step 2 : Salon

# Voit qu'il y a un fusil et Plum dans le salon
a.add_arme_piece('Fusil', 'Salon')
a.add_personne_piece('Plum', 'Salon')

# Demande à Plum dans quelle pièce il était une heure après le meurtre -> Rep : Plum dans le Salon à 15h
a.add_personne_piece_heure('Plum', 'Salon', a.get_crime_heure_plusone())

#####   step 3 : Cuisine

# Voit qu'il y a un couteau, White et Mustard dans la cuisine
a.add_arme_piece('Couteau', 'Cuisine')
a.add_personne_piece('White', 'Cuisine')
a.add_personne_piece('Mustard', 'Cuisine')

# Demande à White dans quelle pièce il était une heure après le meurtre -> Rep : White dans le Salon et la Cuisine à 15h
a.add_personne_piece_heure('White', 'Salon', a.get_crime_heure_plusone())
a.add_personne_piece_heure('White', 'Cuisine', a.get_crime_heure_plusone())

# Demande à Mustard dans quelle pièce il était une heure après le meurtre -> Rep : Mustard dans le Garage à 15h
a.add_personne_piece_heure('Mustard', 'Garage', a.get_crime_heure_plusone())

#####   step 4 : Garage

# Voit qu'il y a une corde dans le garage
a.add_arme_piece('Corde', 'Garage')

## -> extract informations
print("Pièce du crime : ", a.get_piece_crime())
print("Arme du crime : ", a.get_arme_crime())
print("Personne victime : ", a.get_victime())
print("Heure du crime : ", a.get_crime_heure())
print("Personnes suspectes : ", a.get_suspect())
print("Personnes innocentes : ", a.get_innocent())
