#!/usr/bin/env python3

import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.util import degrees, distance_mm, speed_mmps
import os
import sys
import time
import asyncio
import datetime

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")


class ActionMarker:

    def __init__(self, rob: cozmo.robot.Robot):
        self.robot = rob
        self.move_action = None
        self.currentObjectName = ""
        self.switcher = {
            "CustomObjectTypes.CustomType00": "Circles2",
            "CustomObjectTypes.CustomType01": "Circles3",
            "CustomObjectTypes.CustomType02": "Circles4",
            "CustomObjectTypes.CustomType03": "Circles5",
            "CustomObjectTypes.CustomType04": "Diamonds2",
            "CustomObjectTypes.CustomType05": "Diamonds3",
            "CustomObjectTypes.CustomType06": "Diamonds4",
            "CustomObjectTypes.CustomType07": "Diamonds5",
            "CustomObjectTypes.CustomType08": "Hexagons2",
            "CustomObjectTypes.CustomType09": "Hexagons3",
            "CustomObjectTypes.CustomType10": "Hexagons4",
            "CustomObjectTypes.CustomType11": "Hexagons5",
            "CustomObjectTypes.CustomType12": "Triangles2",
            "CustomObjectTypes.CustomType13": "Triangles3",
            "CustomObjectTypes.CustomType14": "Triangles4",
            "CustomObjectTypes.CustomType15": "Triangles5"
        }
        self.currentDate = 0
        self.currentImageIndex = 0

    def handle_object_appeared(self, evt, **kw):
        # This will be called whenever an EvtObjectAppeared is dispatched -
        # whenever an Object comes into view.
        if isinstance(evt.obj, CustomObject):
            print("Cozmo started seeing a %s" % self.switcher.get(str(evt.obj.object_type), ""))
            self.currentObjectName = self.switcher.get(str(evt.obj.object_type), "");
            # image = self.robot.world.latest_image.raw_image
            # img_io = BytesIO()
            # image.save(img_io, 'JPEG', quality=jpeg_quality)
            # img_io.seek(0)
            self.currentDate = (datetime.datetime.now().minute * 60) + (datetime.datetime.now().second)
            self.move_action.abort(log_abort_messages=True)
            self.lastCaturedImage.save("CapturedImage" + self.currentImageIndex + ".bmp")
            self.currentImageIndex += 1
            print("Cozmo saved an screenshot.")

    def handle_object_disappeared(self, evt, **kw):
        # This will be called whenever an EvtObjectDisappeared is dispatched -
        # whenever an Object goes out of view.
        if isinstance(evt.obj, CustomObject):
            print("Cozmo stopped seeing a %s" % self.switcher.get(str(evt.obj.object_type), ""))

    def handle_new_camera_image(self, evt, **kw):
        self.lastCaturedImage = evt.image.raw_image

    def set_custom_objects(self):

        global currentObjectName

        # Add event handlers for whenever Cozmo sees a new object
        self.robot.add_event_handler(cozmo.objects.EvtObjectAppeared, self.handle_object_appeared)
        self.robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, self.handle_object_disappeared)

        self.robot.add_event_handler(cozmo.world.EvtNewCameraImage, self.handle_new_camera_image)

        # CustomObjects array to save CustomObject creation results
        wall_obj = [None] * 16

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[0] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType00,
                                                          CustomObjectMarkers.Circles2,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[1] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType01,
                                                          CustomObjectMarkers.Circles3,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[2] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType02,
                                                          CustomObjectMarkers.Circles4,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[3] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType03,
                                                          CustomObjectMarkers.Circles5,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[4] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType04,
                                                          CustomObjectMarkers.Diamonds2,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[5] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType05,
                                                          CustomObjectMarkers.Diamonds3,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[6] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType06,
                                                          CustomObjectMarkers.Diamonds4,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[7] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType07,
                                                          CustomObjectMarkers.Diamonds5,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[8] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType08,
                                                          CustomObjectMarkers.Hexagons2,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[9] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType09,
                                                          CustomObjectMarkers.Hexagons3,
                                                          300, 300,
                                                          50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[10] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType10,
                                                           CustomObjectMarkers.Hexagons4,
                                                           300, 300,
                                                           50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[11] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType11,
                                                           CustomObjectMarkers.Hexagons5,
                                                           300, 300,
                                                           50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[12] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType12,
                                                           CustomObjectMarkers.Triangles2,
                                                           300, 300,
                                                           50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[13] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType13,
                                                           CustomObjectMarkers.Triangles3,
                                                           300, 300,
                                                           50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[14] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType14,
                                                           CustomObjectMarkers.Triangles4,
                                                           300, 300,
                                                           50, 30, True)

        # define a unique wall (150mm x 120mm (x10mm thick for all walls)
        # with a 50mm x 30mm Circles2 image on front and back
        wall_obj[15] = self.robot.world.define_custom_wall(CustomObjectTypes.CustomType15,
                                                           CustomObjectMarkers.Triangles5,
                                                           300, 300,
                                                           50, 30, True)

        # Just checking each creation result
        for i in range(0, 16):

            if ((wall_obj[i] is not None) is not None):
                print("Object %d defined successfully!" % i)

            else:
                print("One or more object definitions failed!")
                return

    def doMatchingAction(self):

        if (self.currentObjectName == "Circles2"):

            # say stupid things

            self.robot.say_text("Salut tout le monde").wait_for_completed()

            for i in range(5):
                self.robot.say_text(str(i + 1)).wait_for_completed()

        if (self.currentObjectName == "Circles3"):
            self.robot.play_anim_trigger(cozmo.anim.Triggers.FrustratedByFailure).wait_for_completed()
            self.robot.play_anim_trigger(cozmo.anim.Triggers.Sleeping).wait_for_completed()
            self.robot.play_anim_trigger(cozmo.anim.Triggers.CozmoSaysBadWord).wait_for_completed()

        if (self.currentObjectName == "Diamonds5"):

            # Attempt to stack 2 cubes

            # Lookaround until Cozmo knows where at least 2 cubes are:
            lookaround = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            cubes = self.robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube,
                                                                    timeout=60)
            lookaround.stop()

            if len(cubes) < 2:
                print("Error: need 2 Cubes but only found", len(cubes), "Cube(s)")
            else:
                # Try and pickup the 1st cube
                current_action = self.robot.pickup_object(cubes[0], num_retries=3)
                current_action.wait_for_completed()
                if current_action.has_failed:
                    code, reason = current_action.failure_reason
                    result = current_action.result
                    print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                    return

                # Now try to place that cube on the 2nd one
                current_action = self.robot.place_on_object(cubes[1], num_retries=3)
                current_action.wait_for_completed()
                if current_action.has_failed:
                    code, reason = current_action.failure_reason
                    result = current_action.result
                    print("Place On Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                    return

                print("Cozmo successfully stacked 2 blocks!")

        if (self.currentObjectName == "Circles5"):

            # square drive
            for _ in range(4):
                self.robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
                self.robot.turn_in_place(degrees(90)).wait_for_completed()

        if (self.currentObjectName == "Diamonds2"):

            # sing Do,Re,Mi,Fa,Sol,La,Si,Do

            scales = ["Doe", "Ray", "Mi", "Fa", "So", "La", "Si", "Doe"]
            voice_pitch = -1.0
            voice_pitch_delta = 2.0 / (len(scales) - 1)

            for note in scales:
                self.robot.say_text(note, voice_pitch=voice_pitch, duration_scalar=0.3).wait_for_completed()
                voice_pitch += voice_pitch_delta

        if (self.currentObjectName == "Triangles3"):
            # move head down and up
            self.robot.set_head_angle(degrees(25.0)).wait_for_completed()

            self.robot.set_head_angle(degrees(-25.0)).wait_for_completed()

        if (self.currentObjectName == "Diamonds4"):

            # display a picture on Cozmo's oled screen face

            current_directory = os.path.dirname(os.path.realpath(__file__))

            if (self.robot.lift_height.distance_mm > 45) or (self.robot.head_angle.degrees < 40):
                with self.robot.perform_off_charger():
                    lift_action = self.robot.set_lift_height(0.0, in_parallel=True)
                    head_action = self.robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE,
                                                            in_parallel=True)
                    lift_action.wait_for_completed()
                    head_action.wait_for_completed()

            hello_png = os.path.join(current_directory, "hello_world.png")

            # load some images and convert them for display cozmo's face
            image_settings = [(hello_png, Image.NEAREST)]
            face_images = []
            for image_name, resampling_mode in image_settings:
                image = Image.open(image_name)

                # resize to fit on Cozmo's face screen
                resized_image = image.resize(cozmo.oled_face.dimensions(), resampling_mode)

                # convert the image to the format used by the oled screen
                face_image = cozmo.oled_face.convert_image_to_screen_data(resized_image, invert_image=True)
                face_images.append(face_image)

            duration_s = 2.0

            for image in face_images:
                self.robot.display_oled_face_image(image, duration_s * 1000.0)
                time.sleep(duration_s)

        if (self.currentObjectName == "Triangles2"):

            # Attempt to unstack 2 cubes

            self.robot.set_head_angle(degrees(7)).wait_for_completed()

            # Lookaround until Cozmo knows where at least 2 cubes are:
            lookaround = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            cubes = self.robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube,
                                                                    timeout=60)
            lookaround.stop()

            if len(cubes) < 2:
                print("Error: need 2 Cubes but only found", len(cubes), "Cube(s)")
            else:
                max_y, max_targ_ = -1000, None
                min_y, min_targ_ = 1000, None
                for cube in cubes:
                    translation = self.robot.pose - cube.pose
                    print(translation.position.y)
                    if translation.position.y > max_y:
                        max_y, max_targ_ = translation.position.y, cube
                    if translation.position.y < min_y:
                        min_y, min_targ_ = translation.position.y, cube

                # Try and pickup the highest cube
                current_action = self.robot.pickup_object(max_targ_, num_retries=3)
                current_action.wait_for_completed()
                if current_action.has_failed:
                    code, reason = current_action.failure_reason
                    result = current_action.result
                    print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                    return

                # Place on ground here
                self.robot.drive_straight(distance_mm(-150), speed_mmps(50)).wait_for_completed()
                self.robot.place_object_on_ground_here(max_targ_, 0)

                print("Cozmo successfully unstacked 2 blocks!")

        if (self.currentObjectName == "Hexagons4"):

            self.robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

            face_to_follow = None

            while True:
                turn_action = None
                if face_to_follow:
                    # start turning towards the face
                    turn_action = self.robot.turn_towards_face(face_to_follow)

                if not (face_to_follow and face_to_follow.is_visible):
                    # find a visible face, timeout if nothing found after a short while
                    try:
                        face_to_follow = self.robot.world.wait_for_observed_face(timeout=30)
                    except asyncio.TimeoutError:
                        print("Didn't find a face - exiting!")
                        return

                if turn_action:
                    # Complete the turn action if one was in progress
                    turn_action.wait_for_completed()
                    self.robot.say_text("Hello").wait_for_completed()
                    self.robot.set_head_angle(degrees(-20)).wait_for_completed()
                    return

                time.sleep(.1)

    def start(self):

        self.set_custom_objects()

        print("Press CTRL-C to quit")
        print("-----------------------------")

        count = 0;

        giveDirection = {
            0: 0,
            1: -135,
            2: 135,
            3: -135,
            4: -135,
            5: 135,
            6: -135
        }

        giveDistance = {
            0: 4,
            1: 2,
            2: 5,
            3: 8,
            4: 5,
            5: 2,
            6: 3.8
        }

        coefficient = 70
        speed = 30
        traveledDistance = 0
        currentDistance = 0
        traveledDistance = 0

        while (count < 7):

            currentDistance = giveDistance.get(count, 0) * coefficient
            dateBegin = (datetime.datetime.now().minute * 60) + (datetime.datetime.now().second)

            self.move_action = self.robot.drive_straight(distance_mm(currentDistance), speed_mmps(speed),
                                                         should_play_anim=True, in_parallel=True)
            headAction = self.robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE, duration=4, in_parallel=True)
            headAction.wait_for_completed()

            self.move_action.wait_for_completed()

            while (True):

                if (self.currentObjectName != ""):
                    traveledDistance = (self.currentDate - dateBegin) * speed
                    self.doMatchingAction()
                    self.currentObjectName = ""
                    break

                self.currentDate = (datetime.datetime.now().minute * 60) + (datetime.datetime.now().second)
                traveledDistance = (self.currentDate - dateBegin) * speed

                """
                if(traveledDistance > (currentDistance / 2)):
                    headAction1 = self.robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE, duration=4, in_parallel=True)
                    headAction1.wait_for_completed()
                """

                if (traveledDistance > currentDistance):
                    break

                time.sleep(0.01)

            if (traveledDistance < currentDistance):
                self.move_action = self.robot.drive_straight(distance_mm(currentDistance - traveledDistance + 5),
                                                             speed_mmps(50), should_play_anim=True, in_parallel=True)
                self.move_action.wait_for_completed()

            count += 1

            self.robot.turn_in_place(degrees(giveDirection.get(count, 0))).wait_for_completed()

        self.robot.turn_in_place(degrees(-90)).wait_for_completed()


def cozmo_program(robot: cozmo.robot.Robot):
    am = ActionMarker(robot)
    am.start();


cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)