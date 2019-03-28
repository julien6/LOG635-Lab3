#!/usr/bin/env python3

import random
import time
import math
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.util import degrees, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

ROBOT: cozmo.robot.Robot = None
ORIGIN_X: int = None
ORIGIN_Y: int = None


def create_pose(x: float, y: float, angle: float) -> Pose:
    return Pose(x - ORIGIN_X, y - ORIGIN_Y, 0, angle_z=degrees(angle))


class RecognizableObject:
    def __init__(self):
        self.object: cozmo.world.objects.ObservableObject = None


class Cube(RecognizableObject):
    def __init__(self, id: int):
        self.id = id
        self.object = ROBOT.world.get_light_cube(id)


class Marker(RecognizableObject):
    def __init__(self, type: CustomObjectTypes, marker: CustomObjectMarkers):
        self.type = type
        self.marker = marker
        self.object = ROBOT.world.define_custom_wall(type, marker, 300.0, 300.0, 50.0, 30.0, True)


class Actor:
    def __init__(self):
        self.name: str = None


class Character(Actor):
    def __init__(self, name: str, recognizable_object: RecognizableObject):
        self.name = name
        self.recognizable_object = recognizable_object


class Weapon(Actor):
    def __init__(self, name: str, recognizable_object:RecognizableObject):
        self.name = name
        self.recognizable_object = recognizable_object


class Wall:
    HEIGHT = 100.0
    THICKNESS = 1.0

    def __init__(self, x: float, y: float, length: float, angle: float):
        self.x = x + math.cos(math.radians(angle)) * length / 2.0
        self.y = y + math.sin(math.radians(angle)) * length / 2.0
        self.length = length
        self.angle = angle

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

    def create_pose(self):
        self.pose = create_pose(self.center_x, self.center_y, 0.0)

class Map:
    def __init__(self):
        global ORIGIN_X, ORIGIN_Y

        # Markers
        self.markers = [
            Marker(CustomObjectTypes.CustomType00, CustomObjectMarkers.Circles2),
            Marker(CustomObjectTypes.CustomType01, CustomObjectMarkers.Circles3),
            Marker(CustomObjectTypes.CustomType04, CustomObjectMarkers.Diamonds2),
            Marker(CustomObjectTypes.CustomType05, CustomObjectMarkers.Diamonds3),
            Marker(CustomObjectTypes.CustomType08, CustomObjectMarkers.Hexagons2),
            Marker(CustomObjectTypes.CustomType09, CustomObjectMarkers.Hexagons3),
            Marker(CustomObjectTypes.CustomType12, CustomObjectMarkers.Triangles2),
            Marker(CustomObjectTypes.CustomType13, CustomObjectMarkers.Triangles3),
        ]

        # Characters
        self.scarlet = Character("Scarlet", Cube(LightCube1Id))
        self.plum = Character("Plum", self.markers[0])
        self.white = Character("White", self.markers[1])
        self.mustard = Character("Mustard", Cube(LightCube2Id))
        self.peacock = Character("Peacock", self.markers[2])
        self.characters = [self.scarlet, self.plum, self.white, self.mustard, self.peacock]

        # Weapons
        self.rope = Weapon("Rope", self.markers[3])
        self.knife = Weapon("Knife", self.markers[4])
        self.gun = Weapon("Gun", self.markers[5])
        self.weapons = [self.rope, self.knife, self.gun]

        # Communication cube
        self.communication_cube = Cube(LightCube3Id)

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

    def get_actor(self, object: cozmo.world.objects.ObservableObject) -> Actor:
        for c in self.characters:
            if c.recognizable_object.object is object:
                return c
        for w in self.weapons:
            if w.recognizable_object.object is object:
                return w

class Program:
    def __init__(self):
        self.map: Map = None
        self.current_actor: Actor = None
        self.cube_was_tapped = False

    def handle_object_appeared(self, evt, **kw):
        if isinstance(evt.obj, CustomObject):
            self.current_actor = self.map.get_actor(evt.obj)
            print("Cozmo started seeing a %s" % self.currentActor.name)

    def handle_object_disappeared(self, evt, **kw):
        if isinstance(evt.obj, CustomObject):
            print("Cozmo stopped seeing a %s" % self.map.get_actor(evt.obj).name)
            self.current_actor = None

    def handle_cube_tapped(self, evt, **kw):
        if isinstance(evt.obj, CustomObject):
            print("Communication cube was tapped")
            self.current_actor = None

    def start(self):
        # Create map
        self.map = Map()

        # Bind events
        ROBOT.add_event_handler(cozmo.objects.EvtObjectAppeared, self.handle_object_appeared)
        ROBOT.add_event_handler(cozmo.objects.EvtObjectDisappeared, self.handle_object_disappeared)
        self.map.communication_cube.add_event_handler(cozmo.objects.EvtObjectTapped, self.handle_object_disappeared)

        # Test navigation...
        while True:
            target_room: Room = random.choice(self.map.rooms)
            ROBOT.go_to_pose(target_room.pose).wait_for_completed()
            self.cube_was_tapped = False
            look_around = ROBOT.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            while not self.cube_was_tapped:
                if self.current_actor is not None:
                    #Send fact to inference engine...
                    pass
                time.sleep(10)
            look_around.stop()

def cozmo_program(robot: cozmo.robot.Robot):
    global ROBOT
    ROBOT = robot
    Program().start()


cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)
