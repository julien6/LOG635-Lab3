#!/usr/bin/env python3

import math
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes, LightCube
from cozmo.util import degrees, Pose
from cozmo.objects import LightCube1Id, LightCube2Id
from src.inference import add_character_found_fact, add_weapon_found_fact, get_found_victim_name, get_found_murderer_name, get_found_weapon_name, get_found_room_name

ROBOT: cozmo.robot.Robot = None
ORIGIN_X: int = None
ORIGIN_Y: int = None


def create_pose(x: float, y: float, angle: float) -> Pose:
    return Pose(x - ORIGIN_X, y - ORIGIN_Y, 0, angle_z=degrees(angle))


class Actor:
    def __init__(self, name: str, observable_object: cozmo.world.objects.ObservableObject):
        self.name = name
        self.observable_object = observable_object

    def is_represented_by(self, other_object):
        if isinstance(self.observable_object, CustomObject):
            return isinstance(other_object, CustomObject) and other_object.object_type == self.observable_object.object_type
        elif isinstance(self.observable_object, LightCube):
            return isinstance(other_object, LightCube) and other_object.object_id == self.observable_object.object_id


class Character(Actor):
    def __init__(self, name: str, observable_object: cozmo.world.objects.ObservableObject):
        super().__init__(name, observable_object)


class Weapon(Actor):
    def __init__(self, name: str, observable_object: cozmo.world.objects.ObservableObject):
        super().__init__(name, observable_object)


class Wall:
    HEIGHT = 100.0
    THICKNESS = 1.0

    def __init__(self, x: float, y: float, length: float, angle: float):
        self.x = x + math.cos(math.radians(angle)) * length / 2.0
        self.y = y + math.sin(math.radians(angle)) * length / 2.0
        self.length = length
        self.angle = angle
        self.pose: Pose = None
        self.object: cozmo.world.objects.FixedCustomObject = None

    def create_pose(self):
        self.pose = create_pose(self.x, self.y, self.angle)
        self.object = ROBOT.world.create_custom_fixed_object(self.pose, self.length, Wall.THICKNESS, Wall.HEIGHT, relative_to_robot=True)


class Room:
    def __init__(self, name: str, center_x: float, center_y: float):
        self.name = name
        self.center_x = center_x
        self.center_y = center_y
        self.walls = list()
        self.characters = list()
        self.weapons = list()
        self.pose: Pose = None

    def create_pose(self):
        self.pose = create_pose(self.center_x, self.center_y, 0.0)


class Map:
    def __init__(self):
        # Markers
        self.markers = [
            ROBOT.world.define_custom_wall(CustomObjectTypes.CustomType00, CustomObjectMarkers.Circles2, 300.0, 300.0, 50.0, 30.0, True),
            ROBOT.world.define_custom_wall(CustomObjectTypes.CustomType01, CustomObjectMarkers.Circles3, 300.0, 300.0, 50.0, 30.0, True),
            ROBOT.world.define_custom_wall(CustomObjectTypes.CustomType04, CustomObjectMarkers.Diamonds2, 300.0, 300.0, 50.0, 30.0, True),
            ROBOT.world.define_custom_wall(CustomObjectTypes.CustomType05, CustomObjectMarkers.Diamonds3, 300.0, 300.0, 50.0, 30.0, True),
            ROBOT.world.define_custom_wall(CustomObjectTypes.CustomType08, CustomObjectMarkers.Hexagons2, 300.0, 300.0, 50.0, 30.0, True),
            ROBOT.world.define_custom_wall(CustomObjectTypes.CustomType09, CustomObjectMarkers.Hexagons3, 300.0, 300.0, 50.0, 30.0, True),
            ROBOT.world.define_custom_wall(CustomObjectTypes.CustomType12, CustomObjectMarkers.Triangles2, 300.0, 300.0, 50.0, 30.0, True),
            ROBOT.world.define_custom_wall(CustomObjectTypes.CustomType13, CustomObjectMarkers.Triangles3, 300.0, 300.0, 50.0, 30.0, True)
        ]

        # Characters
        self.scarlet = Character("Scarlet", ROBOT.world.get_light_cube(LightCube1Id))
        self.plum = Character("Plum", self.markers[0])
        self.white = Character("White", self.markers[1])
        self.mustard = Character("Mustard", ROBOT.world.get_light_cube(LightCube2Id))
        self.peacock = Character("Peacock", self.markers[2])
        self.characters = [self.scarlet, self.plum, self.white, self.mustard, self.peacock]

        # Weapons
        self.rope = Weapon("Rope", self.markers[3])
        self.knife = Weapon("Knife", self.markers[4])
        self.gun = Weapon("Gun", self.markers[5])
        self.weapons = [self.rope, self.knife, self.gun]

        # Toilet
        self.toilet = Room("Toilet", center_x=150, center_y=200)
        self.toilet.walls.append(Wall(x=0, y=0, length=300, angle=0))
        self.toilet.walls.append(Wall(x=0, y=0, length=400, angle=90))
        self.toilet.walls.append(Wall(x=0, y=400, length=300, angle=0))
        self.toilet.walls.append(Wall(x=300, y=0, length=100, angle=90))
        self.toilet.walls.append(Wall(x=300, y=200, length=200, angle=90))
        self.toilet.characters.append(self.mustard)

        # Kitchen
        self.kitchen = Room("Kitchen", center_x=450, center_y=50)
        self.kitchen.walls.append(Wall(x=300, y=0, length=300, angle=0))
        self.kitchen.walls.append(Wall(x=300, y=0, length=100, angle=90))
        self.kitchen.walls.append(Wall(x=300, y=100, length=200, angle=0))
        self.kitchen.walls.append(Wall(x=600, y=0, length=100, angle=90))
        self.kitchen.weapons.append(self.knife)

        # DiningRoom
        self.dining_room = Room("DiningRoom", center_x=450, center_y=250)
        self.dining_room.walls.append(Wall(x=300, y=100, length=200, angle=0))
        self.dining_room.walls.append(Wall(x=300, y=200, length=200, angle=90))
        self.dining_room.walls.append(Wall(x=300, y=400, length=100, angle=0))
        self.dining_room.walls.append(Wall(x=500, y=400, length=100, angle=0))
        self.dining_room.walls.append(Wall(x=600, y=100, length=100, angle=90))
        self.dining_room.walls.append(Wall(x=600, y=300, length=100, angle=90))
        self.dining_room.characters.append(self.white)

        # LivingRoom
        self.living_room = Room("LivingRoom", center_x=800, center_y=200)
        self.living_room.walls.append(Wall(x=600, y=0, length=400, angle=0))
        self.living_room.walls.append(Wall(x=600, y=0, length=200, angle=90))
        self.living_room.walls.append(Wall(x=600, y=300, length=100, angle=90))
        self.living_room.walls.append(Wall(x=600, y=400, length=100, angle=0))
        self.living_room.walls.append(Wall(x=800, y=400, length=200, angle=0))
        self.living_room.walls.append(Wall(x=1000, y=0, length=400, angle=90))
        self.living_room.characters.append(self.plum)
        self.living_room.weapons.append(self.gun)

        # Office
        self.office = Room("Office", center_x=800, center_y=600)
        self.office.walls.append(Wall(x=600, y=400, length=100, angle=0))
        self.office.walls.append(Wall(x=800, y=400, length=200, angle=0))
        self.office.walls.append(Wall(x=600, y=400, length=300, angle=90))
        self.office.walls.append(Wall(x=600, y=800, length=400, angle=0))
        self.office.walls.append(Wall(x=1000, y=400, length=400, angle=90))
        self.office.walls.append(Wall(x=800, y=400, length=200, angle=0))
        self.office.characters.append(self.scarlet)
        self.office.characters.append(self.peacock)

        # Garage
        self.garage = Room("Garage", center_x=300, center_y=600)
        self.garage.walls.append(Wall(x=0, y=400, length=400, angle=0))
        self.garage.walls.append(Wall(x=0, y=400, length=400, angle=90))
        self.garage.walls.append(Wall(x=0, y=800, length=600, angle=0))
        self.garage.walls.append(Wall(x=500, y=400, length=100, angle=0))
        self.garage.walls.append(Wall(x=600, y=400, length=300, angle=90))
        self.garage.weapons.append(self.rope)

        # Add rooms
        self.rooms = [self.toilet, self.kitchen, self.dining_room,self.living_room, self.office, self.garage]

    def set_walls_poses(self, start_room: Room):
        global ORIGIN_X, ORIGIN_Y

        # Origin
        ORIGIN_X = start_room.center_x
        ORIGIN_Y = start_room.center_y

        # Poses
        for r in self.rooms:
            r.create_pose()
            for w in r.walls:
                w.create_pose()

    def get_actor_from_object(self, object: cozmo.world.objects.ObservableObject) -> Actor:
        for c in self.characters:
            if c.is_represented_by(object):
                return c
        for w in self.weapons:
            if w.is_represented_by(object):
                return w

    def get_actor_from_name(self, name: str) -> Actor:
        for c in self.characters:
            if c.name == name:
                return c
        for w in self.weapons:
            if w.name == name:
                return w

    def get_room_from_name(self, name: str) -> Room:
        for r in self.rooms:
            if r.name == name:
                return r


class VisitedRoom:
    def __init__(self, room: Room, actors_to_find: set):
        self.room = room
        self.actors_to_find = actors_to_find


class Scenario:
    def __init__(self, map: Map):
        self.map = map

        self.doctor = self.map.peacock
        self.victim = self.map.scarlet
        self.murderer = self.map.mustard
        self.murder_room = self.map.office
        self.murder_weapon = self.map.rope


class Investigation:
    def __init__(self, scenario: Scenario):
        self.scenario = scenario

        self.found_victim: Character = None
        self.found_murderer: Character = None
        self.found_weapon: Weapon = None
        self.found_room: Room = None
        self.observed_actor: Actor = None
        self.visited_room: VisitedRoom = None
        self.hour_victim_died: int = None

        self.rooms_to_visit = list()
        self.rooms_to_visit.append(VisitedRoom(self.scenario.map.office, {self.scenario.map.peacock}))
        self.rooms_to_visit.append(VisitedRoom(self.scenario.map.living_room, {self.scenario.map.plum, self.scenario.map.gun}))
        self.rooms_to_visit.append(VisitedRoom(self.scenario.map.kitchen, {self.scenario.map.white, self.scenario.map.mustard, self.scenario.map.knife}))
        self.rooms_to_visit.append(VisitedRoom(self.scenario.map.garage, {self.scenario.map.rope}))

        self.scenario.map.set_walls_poses(self.rooms_to_visit[0].room)

    def check_has_all_proofs(self) -> bool:
        victim_name = get_found_victim_name()
        if victim_name:
            self.found_victim = self.scenario.map.get_actor_from_name(victim_name)
            print("Cozmo found the victim to be: " + victim_name)

        murderer_name = get_found_murderer_name()
        if murderer_name:
            self.found_murderer = self.scenario.map.get_actor_from_name(murderer_name)
            print("Cozmo found the murderer to be: " + murderer_name)

        weapon_name = get_found_weapon_name()
        if weapon_name:
            self.found_weapon = self.scenario.map.get_actor_from_name(weapon_name)
            print("Cozmo found the crime weapon to be: " + weapon_name)

        room_name = get_found_room_name()
        if room_name:
            self.found_room = self.scenario.map.get_actor_from_name(room_name)
            print("Cozmo found the crime room to be: " + room_name)

        if self.found_victim and self.found_murderer and self.found_room and self.found_weapon:
            print("Solution: " + self.found_murderer.name + " murdered " + self.found_victim.name + " in the " + self.found_room.name + " with the " + self.found_weapon.name + " at " + self.hour_victim_died + ":00.")
            return True
        else:
            return False

    def ask_was_present_crime_room(self) -> bool:
        while True:
            answer = input(self.observed_actor.name + ", were you in the " + self.scenario.murder_room.name + " at 3:00 PM (y/n)?")
            if answer == "y":
                return True
            elif answer == "n":
                return False

    def ask_at_what_hour_victim_died(self) -> int:
        while True:
            answer = input(self.observed_actor.name + ", you're a doctor. At what hour did " + self.scenario.victim.name + " died (ex: 15)?")
            try:
                return int(answer)
            except ValueError:
                continue

    def find_all_actors_in_visited_room(self):
        print("Searching for clues...")
        while len(self.visited_room.actors_to_find) > 0:
            look_around = ROBOT.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            observable_objects = ROBOT.world.wait_until_observe_num_objects(num=1)
            look_around.stop()
            self.observed_actor = self.scenario.map.get_actor_from_object(observable_objects[0])
            if self.observed_actor in self.visited_room.actors_to_find:
                self.visited_room.actors_to_find.remove(self.observed_actor)
                print("Cozmo found a %s : %s" % type(self.observed_actor).__name__, self.observed_actor.name)
                if isinstance(self.observed_actor, Character):
                    # Ask questions
                    if self.observed_actor is self.scenario.doctor:
                        self.hour_victim_died = self.ask_at_what_hour_victim_died()
                    was_present_crime_room = self.ask_was_present_crime_room()

                    # Send fact to inference engine
                    add_character_found_fact(self.observed_actor.name, self.visited_room.room.name, was_present_crime_room)
                if isinstance(self.observed_actor, Weapon):
                    # Send fact to inference engine
                    add_weapon_found_fact(self.observed_actor.name, self.visited_room.room.name)

    def solve(self) -> bool:
        self.visited_room = self.rooms_to_visit.pop(0)
        while self.visited_room:
            print("Current room: " + self.visited_room.room.name)
            self.find_all_actors_in_visited_room()
            self.visited_room = self.rooms_to_visit.pop(0)
            if self.visited_room:
                print("Going to room: " + self.visited_room.room.name)
                ROBOT.go_to_pose(self.visited_room.room.pose).wait_for_completed()
        return self.check_has_all_proofs()


def cozmo_program(robot: cozmo.robot.Robot):
    global ROBOT

    ROBOT = robot

    map = Map()
    scenario = Scenario(map)
    investigation = Investigation(scenario)

    if investigation.solve():
        print("Investigation succeeded!")
    else:
        print("Investigation failed!")


cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)
