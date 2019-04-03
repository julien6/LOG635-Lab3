from aima.logic import *


# Permet d'inferer qui est le meurtrier, quand, comment, où il a tué.
class CrimeInference:
    def __init__(self):
        self.Armes = ["Corde", "Fusil", "Couteau"]
        self.Pieces = ["Cuisine", "Bureau", "Garage", "Salon"]
        self.Personnes = ["Mustard", "Peacock", "Scarlet", "Plum", "White"]
        self.clauses = []
        self._cree_base_clauses()
        self._initialize_base_knowledge()
        self._combine_clauses()
        self.crime_kb = FolKB(self.clauses)

    def _cree_base_clauses(self):
        self.arme_clause = 'Arme({})'
        self.piece_clause = 'Piece({})'
        self.personne_clause = 'Personne({})'

        # paramètre 1 : arme; paramètre 2 : piece
        self.arme_piece_clause = 'Arme_Piece({},{})'

        # paramètre 1 : personne; paramètre 2 : piece; paramètre 3 : heure
        self.personne_piece_heure_clause = 'Personne_Piece_Heure({}, {}, {})'

        # paramètre 1 : personne; paramètre 2 : piece
        self.personne_piece_clause = 'Personne_Piece({}, {})'

        # paramète 1 : personne
        self.mort_clause = 'EstMort({})'
        # paramète 1 : personne
        self.vivant_clause = 'EstVivant({})'

        # paramètre 1 : personne
        self.victime_clause = 'Victime({})'

        # paramètre 1 : personne
        self.marque_corps_clause = 'MarqueCou({})'

        # paramètre 1 : piece; paramètre 2 : piece
        self.piece_differente_clause = 'DifferentPiece({},{})'

        # paramètre 1 : piece; paramètre 2 : piece
        self.arme_differente_clause = 'DifferentArme({},{})'

        # paramètre 1 : heure
        self.crime_heure_clause = 'HeureCrime({})'

        # paramètre 1 : heure
        self.crime_heure_plusone_clause = 'HeureCrimePlusOne({})'

    def _initialize_base_knowledge(self):

        # Initialiser KB sur les pieces
        for i in range(len(self.Pieces)):
            for j in range(len(self.Pieces)):
                if i != j:
                    self.clauses.append(expr(self.piece_differente_clause.format(self.Pieces[i], self.Pieces[j])))

        # Initialiser KB sur les armes
        for i in range(len(self.Armes)):
            for j in range(len(self.Armes)):
                if i != j:
                    self.clauses.append(expr(self.arme_differente_clause.format(self.Armes[i], self.Armes[j])))

        # Initialiser KB sur Armes, Pieces, Personnes
        for arme in self.Armes:
            self.clauses.append(expr(self.arme_clause.format(arme)))

        for piece in self.Pieces:
            self.clauses.append(expr(self.piece_clause.format(piece)))

        for personne in self.Personnes:
            self.clauses.append(expr(self.personne_clause.format(personne)))

    def _combine_clauses(self):
        # Determine la piece du crime
        self.clauses.append(expr('EstMort(x) & Personne_Piece_Heure(x, y, h) & HeureCrime(z) ==> PieceCrime(y)'))
        self.clauses.append(expr('EstMort(x) & Personne_Piece(x, y) ==> PieceCrime(y)'))

        # Determiner l'arme du crime
        self.clauses.append(expr('PieceCrime(x) & Arme(y) & Piece_Arme(y, x) ==> ArmeCrime(y)'))
        self.clauses.append(expr("EstMort(x) & MarqueCou(x) ==> ArmeCrime(Corde)"))

        # Si la personne est morte alors elle est la victime
        self.clauses.append(expr('EstMort(x) ==> Victime(x)'))

        # Si la personne est morte alors elle est innocente
        self.clauses.append(expr('EstMort(x) ==> Innocent(x)'))

        # Si la personne est vivante et était dans une pièce
        # qui ne contient pas l'arme du crime, alors elle est innocente
        self.clauses.append(expr(
            'EstVivant(p) & HeureCrimePlusOne(h1) & Personne_Piece_Heure(p,r2,h1) & PieceCrime(r1)'
            ' & DifferentPiece(r1,r2) & ArmeCrime(a1) & Arme_Piece(a2,r2) & DifferentArme(a1,a2) ==> Innocent(p)'))

        # Si la personne se trouvait dans une piece qui contient l'arme
        # qui a tué la victime une heure après le meurtre alors elle est suspecte
        self.clauses.append(expr(
            'EstVivant(p) & HeureCrimePlusOne(h1) & Personne_Piece_Heure(p,r2,h1) & PieceCrime(r1)'
            ' & DifferentPiece(r1,r2) & ArmeCrime(a) & Arme_Piece(a,r2) ==> Suspect(p)'))

    def add_any_clause(self, clause_string):
        self.crime_kb.tell(expr(clause_string))

    def get_victime(self):
        result = self.crime_kb.ask(expr('Victime(x)'))
        if not result:
            return False
        else:
            return result[x]

    def get_piece_crime(self):
        result = self.crime_kb.ask(expr('PieceCrime(x)'))
        if not result:
            return False
        else:
            return result[x]

    def get_arme_crime(self):
        result = self.crime_kb.ask(expr('ArmeCrime(x)'))
        if not result:
            return result
        else:
            return result[x]

    def get_crime_heure(self):
        result = self.crime_kb.ask(expr('HeureCrime(x)'))
        if not result:
            return result
        else:
            return result[x]

    def get_crime_heure_plusone(self):
        result = self.crime_kb.ask(expr('HeureCrimePlusOne(x)'))
        if not result:
            return result
        else:
            return result[x]

    def get_suspect(self):
        result = self.crime_kb.ask(expr('Suspect(x)'))
        if not result:
            return result
        else:
            return result[x]

    def get_innocent(self):
        result = list(fol_bc_ask(self.crime_kb, expr('Innocent(x)')))
        res = []

        for elt in result:
            if not res.__contains__(elt[x]):
                res.append(elt[x])

        return res
