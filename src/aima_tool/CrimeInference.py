from utils import *
from logic import *

class CrimeInference:
	def __init__(self):
		self.Weapons = ["Poignard", "Corde", "Revolver", "FerCheval", "Matraque", "Poison"]
		self.Rooms = ["Cuisine", "Bureau", "Garage", "SalleDeBain", "Salon"]
		self.Persons = ["Moutarde", "Pervenche", "Rose", "Olive", "Leblanc", "Violet", "Black"]
		self.clauses = []
		self._create_base_clauses()
		self._initilize_base_knowledge()
		self._combine_clauses()
		self.crime_kb = FolKB(self.clauses)

	def _create_base_clauses(self):
		self.weapon_clause = 'Weapon({})' #Parameter is a weapon
		self.room_clause = 'Room({})' #Parameter is a room
		self.person_clause = 'Person({})' #Parameter is a person

		self.is_in_clause = 'IsIn({},{})' #Parameter 1 is in parameter 2
		self.is_in_hour_clause = 'IsInHour({}, {}, {})'

		self.dead_clause = 'IsDead({})' #Parameter is dead
		self.alive_clause = 'Alive({})' #Parameter is alive

		self.wound_clause = 'Wound({})' #Parameter has a wound
		self.fracture_clause = 'Fracture({})' #Parameter has a fracture
		self.burn_clause = 'Burn({})' #Parameter has a burn
		self.body_mark_clause = 'BodyMark({})' #Parameter has a body mark (FerCheval)
		self.bullet_clause = 'Bullet({})' #Parameter has a bullet

		self.room_different_clause = 'Different({},{})' # Room 1 is different from room 2
		self.crime_hour_clause = 'CrimeHour({})' # Parameter is the crime hour

	def _initilize_base_knowledge(self):
		# Initialize knowledge about room difference
		for i in range(len(self.Rooms)):
			for j in range(i+1, len(self.Rooms)):
				if i != j:
					self.clauses.append(expr(self.room_different_clause.format(self.Rooms[i], self.Rooms[j])))
		
		# Initialize knowledge about weapons
		for weapon in self.Weapons:
			self.clauses.append(expr(self.weapon_clause.format(weapon)))

		# Initialize knowledge about room
		for room in self.Rooms:
			self.clauses.append(expr(self.room_clause.format(room)))

		# Initialize knowledge about persons
		for person in self.Persons:
			self.clauses.append(expr(self.person_clause.format(person)))
		
	def _combine_clauses(self):
		# Determine crime room
		self.clauses.append(expr('IsDead(x) & IsInHour(x, y, h) & CrimeHour(z) ==> CrimeRoom(y)'))

		# Determine crime weapon
		self.clauses.append(expr('CrimeRoom(x) & Weapon(y) & IsIn(y, x) ==> CrimeWeapon(y)'))
		self.clauses.append(expr("IsDead(x) & Wound(x) & Balle(x)  ==> CrimeWeapon(Revolver)"))
		self.clauses.append(expr("IsDead(x) & Wound(x) ==> CrimeWeapon(Poignard)"))
		self.clauses.append(expr("IsDead(x) & Fracture(x) & BodyMark(x) ==> CrimeWeapon(FerCheval)"))
		self.clauses.append(expr("IsDead(x) & Fracture(x) ==> CrimeWeapon(Matraque)"))
		self.clauses.append(expr("IsDead(x) & Burn(x) ==> CrimeWeapon(Corde)"))

		self.clauses.append(expr('CrimeRoom(x) & IsIn(y, x) & Alive(y) ==> Suspect(y)'))

		self.clauses.append(expr('IsDead(x) ==> Innocent(x)'))
		self.clauses.append(expr("CrimeRoom(r1) & Different(r1, r2) & CrimeHour(h) & IsInHour(p,r2,h) ==> Innocent(p)"))

	def add_alive_person(self, person):
		self.crime_kb.tell(expr(self.alive_clause.format(person)))

	def add_dead_person(self, dead_person):
		self.crime_kb.tell(expr(self.dead_clause.format(dead_person)))

	def add_in_room(self, something, room):
		self.crime_kb.tell(expr(self.is_in_clause.format(something, room)))

	def add_in_room_hour(self, something, room, hour):
		self.crime_kb.tell(expr(self.is_in_hour_clause.format(something, room, hour)))

	def add_wound_on_person(self, person):
		self.crime_kb.tell(expr(self.wound_clause.format(person)))
	
	def add_burn_on_person(self, person):
		self.crime_kb.tell(expr(self.burn_clause.format(person)))

	def add_fracture_on_person(self, person):
		self.crime_kb.tell(expr(self.fracture_clause.format(person)))

	def add_body_mark_on_person(self, person):
		self.crime_kb.tell(expr(self.body_mark_clause.format(person)))

	def add_bullet_on_person(self, person):
		self.crime_kb.tell(expr(self.bullet_clause.format(person)))

	def add_crime_hour(self, hour):
		self.crime_kb.tell(expr(self.crime_hour_clause.format(hour)))

	def get_crime_room(self):
		result = self.crime_kb.ask(expr('CrimeRoom(x)'))
		if result == False:
			return False
		else :
			return result[x]

	def get_crime_weapon(self):
		result = self.crime_kb.ask(expr('CrimeWeapon(x)'))
		if result == False:
			return result
		else:
			return result[x]

	def get_suspect(self):
		result = self.crime_kb.ask(expr('Suspect(x)'))
		print(result)

	def get_innocent(self):
		result = fol_fc_ask(self.crime_kb, expr('Innocent(x)'))
		print(list(result))


crime = CrimeInference()

crime.add_crime_hour('H2')
crime.add_dead_person('Black')
crime.add_in_room_hour('Black', 'Cuisine', 'H2')
crime.add_burn_on_person('Black')
crime.add_alive_person('Violet')
crime.add_in_room_hour('Violet', 'Bureau', 'H2')

print(crime.get_crime_room())
print(crime.get_crime_weapon())
crime.get_innocent()
