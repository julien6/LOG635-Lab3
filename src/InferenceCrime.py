from aima.logic import *


class InferenceCrime:
    def __init__(self):
        self.Armes = ["Fusil", "Corde", "Couteau"]
        self.Pieces = ["Cuisine", "Bureau", "Garage", "Salon"]
        self.Personnes = ["Mustard", "Peacock", "Scarlet", "Plum", "White"]
        self.clauses = []
        self._cree_base_clauses()
        self._initilize_base_knowledge()
        self._combine_clauses()
        self.crime_kb = FolKB(self.clauses)

    def _cree_base_clauses(self):
        self.arme_clause = 'Arme({})'
        self.piece_clause = 'Piece({})'
        self.personne_clause = 'Personne({})'

        self.est_dans_clause = 'EstDans({},{})'
        self.est_dans_heure_clause = 'EstDansHeure({}, {}, {})'

        self.mort_clause = 'EstMort({})'
        self.vivant_clause = 'EstVivant({})'

        self.marque_corps_clause = 'MarqueCou({})'

        self.piece_differente_clause = 'Different({},{})'
        self.crime_heure_clause = 'HeureCrime({})'

        self.etait_avec_heure_clause = 'EtaitAvecHeure({},{},{})'

    def _initilize_base_knowledge(self):
        # Initialiser KB sur les pieces
        for i in range(len(self.Pieces)):
            for j in range(i + 1, len(self.Pieces)):
                if i != j:
                    self.clauses.append(expr(self.piece_differente_clause.format(self.Pieces[i], self.Pieces[j])))

        # Initialiser KB sur Armes, Pieces, Personnes
        for arme in self.Armes:
            self.clauses.append(expr(self.arme_clause.format(arme)))

        for piece in self.Pieces:
            self.clauses.append(expr(self.piece_clause.format(piece)))

        for personne in self.Personnes:
            self.clauses.append(expr(self.personne_clause.format(personne)))

    def _combine_clauses(self):
        # Determine piece crime
        self.clauses.append(expr('EstMort(x) & EstDansHeure(x, y, h) & HeureCrime(z) ==> PieceCrime(y)'))
        self.clauses.append(expr('EstMort(x) & EstDans(x, y) ==> PieceCrime(y)'))

        # Determiner l'arme du crime
        self.clauses.append(expr('PieceCrime(x) & Arme(y) & EstDans(y, x) ==> ArmeCrime(y)'))
        self.clauses.append(expr("EstMort(x) & MarqueCou(x) ==> ArmeCrime(Corde)"))

        # Si la personne est morte alors elle est innocente
        self.clauses.append(expr('EstMort(x) ==> Innocent(x)'))
        self.clauses.append(
            expr(
                "PieceCrime(r1) & Different(r1, r2) & EstVivant(p) & HeureCrime(h) & EstDansHeure(p,r2,h) ==> Innocent(p)"))

    def add_personne_vivante(self, personne):
        self.crime_kb.tell(expr(self.vivant_clause.format(personne)))

    def add_personne_morte(self, personne_morte):
        self.crime_kb.tell(expr(self.mort_clause.format(personne_morte)))

    def add_dans_piece(self, quelque_chose, piece):
        self.crime_kb.tell(expr(self.est_dans_clause.format(quelque_chose, piece)))

    def add_dans_piece_heure(self, quelque_chose, piece, heure):
        self.crime_kb.tell(expr(self.est_dans_heure_clause.format(quelque_chose, piece, heure)))

    def add_marque_corps(self, personne):
        self.crime_kb.tell(expr(self.marque_corps_clause.format(personne)))

    def add_crime_heure(self, heure):
        self.crime_kb.tell(expr(self.crime_heure_clause.format(heure)))

    def personne_etait_avec(self, personne1, personne2, heure):
        self.crime_kb.tell(expr(self.etait_avec_heure_clause.format(personne1, personne2, heure)))

    def get_piece_crime(self):
        result = self.crime_kb.ask(expr('PieceCrime(x)'))
        if result == False:
            return False
        else:
            return result[x]

    def get_arme_crime(self):
        result = self.crime_kb.ask(expr('ArmeCrime(x)'))
        if result == False:
            return result
        else:
            return result[x]

    def get_suspect(self):
        result = self.crime_kb.ask(expr('Suspect(suspect)'))
        return result

    def get_innocent(self):
        result = fol_fc_ask(self.crime_kb, expr('Innocent(innocent)'))
        return list(result)
