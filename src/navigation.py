#!/usr/bin/env python3

import random
import time
import math
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes, LightCube
from cozmo.util import degrees, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id
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
        global ORIGIN_X, ORIGIN_Y

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

        # Communication cube
        self.communication_cube = ROBOT.world.get_light_cube(LightCube3Id)

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

        # Scenario
        self.victim = self.scarlet
        self.murderer = self.mustard
        self.murder_room = self.office
        self.murder_weapon = self.rope
        self.start_room = self.living_room

        # Origin
        ORIGIN_X = self.start_room.center_x
        ORIGIN_Y = self.start_room.center_y

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


class Program:
    def __init__(self):
        self.map: Map = None
        self.current_actor: Actor = None
        self.cube_was_tapped = False
        self.found_victim = None
        self.found_murderer = None
        self.found_weapon = None
        self.found_room = None

    def handle_cube_tapped(self, evt, **kw):
        if isinstance(evt.obj, CustomObject):
            actor = self.map.get_actor_from_object(evt.obj)
            if actor == self.map.communication_cube:
                print("Communication cube was tapped")

    def start(self):
        # Create map
        self.map = Map()

        # Bind events
        ROBOT.add_event_handler(cozmo.objects.EvtObjectTapped, self.handle_cube_tapped)

        current_room = self.map.start_room
        # Main loop
        while True:
            print("Current room: " + current_room.name)
            last_room = current_room
            while current_room is last_room:
                current_room = random.choice(self.map.rooms)
            print("Going to " + current_room.name + " room.")
            ROBOT.go_to_pose(current_room.pose).wait_for_completed()
            print("Arrived at " + current_room.name + " room.")
            look_around = ROBOT.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            observable_objects = ROBOT.world.wait_until_observe_num_objects(num=1, timeout=90)
            look_around.stop()
            print("Found " + str(len(observable_objects)) + " clues.")
            if len(observable_objects) != 1:
                break
            self.current_actor = self.map.get_actor_from_object(observable_objects[0])
            if self.current_actor:
                print("Cozmo observed a clue: %s" % self.current_actor.name)
                if isinstance(self.current_actor, Character):
                    was_present_crime_room = None
                    while was_present_crime_room:
                        answer = input(self.current_actor.name + ", were you in the " + self.map.murder_room.name + " at 3:00 PM (y/n)?")
                        if answer == "y":
                            was_present_crime_room = True
                        elif answer == "n":
                            was_present_crime_room = False
                    # Send fact to inference engine...
                    add_character_found_fact(self.current_actor.name, current_room.name, was_present_crime_room)
                if isinstance(self.current_actor, Weapon):
                    # Send fact to inference engine...
                    add_weapon_found_fact(self.current_actor.name, current_room.name)

            # Have we found the victim?
            victim_name = get_found_victim_name()
            if victim_name is not None:
                # React to victim found...
                print("Found victim is " + victim_name)
                self.found_victim = self.map.get_actor_from_name(victim_name)
                if self.found_victim is self.map.murderer:
                    print("Cozmo SUCCEEDED to find the VICTIM")
                else:
                    print("Cozmo FAILED to find the VICTIM")
                    break

            # Have we found the murderer?
            murderer_name = get_found_murderer_name()
            if murderer_name is not None:
                # React to murdered found...
                print("Found murdered is " + murderer_name)
                self.found_murderer = self.map.get_actor_from_name(murderer_name)
                if self.found_murderer is self.map.murderer:
                    print("Cozmo SUCCEEDED to find the MURDERER")
                else:
                    print("Cozmo FAILED to find the MURDERER")
                    break

            # Have we found the room?
            weapon_name = get_found_weapon_name()
            if weapon_name is not None:
                # React to weapon found...
                print("Found weapon is " + weapon_name)
                self.found_weapon = self.map.get_actor_from_name(weapon_name)
                if self.found_weapon is self.map.murder_weapon:
                    print("Cozmo SUCCEEDED to find the WEAPON")
                else:
                    print("Cozmo FAILED to find the WEAPON")
                    break

            # Have we found the weapon?
            room_name = get_found_room_name()
            if room_name is not None:
                # React to murdered found...
                print("Found room is " + room_name)
                self.found_room = self.map.get_room_from_name(room_name)
                if self.found_room is self.map.murder_room:
                    print("Cozmo SUCCEEDED to find the ROOM")
                else:
                    print("Cozmo FAILED to find the ROOM")
                    break

            if self.found_victim is not None and self.found_murderer is not None and self.found_room is not None and self.found_weapon is not None:
                print(self.found_murderer.name + " murdered " + self.found_victim.name + " in the " + self.found_room.name + " with the " + self.found_weapon.name)
                print("COZMO SUCCEEDED TO SOLVE THE CRIME!!!")
                break

        print("Investigation terminated!")


def cozmo_program(robot: cozmo.robot.Robot):
    global ROBOT
    ROBOT = robot
    Program().start()


cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)
