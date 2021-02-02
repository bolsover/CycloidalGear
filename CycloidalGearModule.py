from __future__ import division

import math


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return self.x == other.get_x() & self.x == other.get_y()

    def __str__(self):
        return "" + str(round(self.x, 3)) + "," + str(round(self.y, 3))


class CycloidalGear:

    def __init__(self, values):
        """Utility to develop Cycloidal Gear sketches using Alibre Design
        :param values is an array  [None, module, wheel_count, pinion_count, wheel_center_hole, pinion_center_hole,
        custom_slop, custom_slop_enabled, plane, sketch]"""
        self.wheel_add_factor = 0.0
        self.wheel_practical_addendum_factor = 0.0
        self.pinion_add_factor = 0.0
        self.pinion_practical_addendum_factor = 0.0
        self.gear_ratio = 0.0
        self.wheel_circular_pitch = 0.0
        self.wheel_dedendum = 0.0
        self.pinion_dedendum = 0.0
        self.wheel_pitch_diameter = 0.0
        self.pinion_pitch_diameter = 0.0
        self.wheel_center_hole = values[4]
        self.pinion_center_hole = values[5]
        self.custom_slop = values[6]
        self.custom_slop_enabled = values[7]
        self.wheel_addendum = 0.0
        self.pinion_addendum = 0.0
        self.wheel_addendum_radius = 0.0
        self.pinion_addendum_radius = 0.0
        self.wheel_count = values[2]
        self.pinion_count = values[3]
        self.module = values[1]
        self.sketch = values[9]
        self.pinion_half_tooth_angle = 0.0

        self.build_gear_set()  # builds the gears

    def __getattribute__(self, item):
        """Returns the value of the attribute name """
        # what no switch!!**??
        if item == 'wheel_add_factor':
            return self.wheel_add_factor
        elif item == 'wheel_practical_addendum_factor':
            return self.wheel_practical_addendum_factor
        elif item == 'pinion_add_factor':
            return self.pinion_add_factor
        elif item == 'pinion_practical_addendum_factor':
            return self.pinion_practical_addendum_factor
        elif item == 'gear_ratio':
            return self.gear_ratio
        elif item == 'circular_pitch':
            return self.wheel_circular_pitch
        elif item == 'wheel_dedendum':
            return self.wheel_dedendum
        elif item == 'pinion_dedendum':
            return self.pinion_dedendum
        elif item == 'wheel_pitch_diameter':
            return self.wheel_pitch_diameter
        elif item == 'pinion_pitch_diameter':
            return self.pinion_pitch_diameter
        elif item == 'pinion_addendum':
            return self.pinion_addendum
        elif item == 'wheel_addendum':
            return self.wheel_addendum
        elif item == 'addendum_radius':
            return self.wheel_addendum_radius
        elif item == 'wheel_count':
            return self.wheel_count
        elif item == 'pinion_count':
            return self.pinion_count
        elif item == 'module':
            return self.module
        elif item == 'wheel_center_hole':
            return self.wheel_center_hole
        elif item == 'pinion_center_hole':
            return self.pinion_center_hole
        elif item == 'custom_slop':
            return self.custom_slop
        elif item == 'custom_slop_enabled':
            return self.custom_slop_enabled
        else:
            return "error"

    def __str__(self):
        """Returns a string representation of the class"""
        r = "".join(["CycloidalGear:",
                     # "\nwheel_add_factor = ", str(self.wheel_add_factor),
                     # "\nwheel_practical_addendum_factor = ", str(self.wheel_practical_addendum_factor),
                     # "\npinion_add_factor = ", str(self.pinion_add_factor),
                     # "\npinion_practical_addendum_factor = ", str(self.pinion_practical_addendum_factor),
                     "\nwheel_count = ", str(self.wheel_count),
                     "\nwheel_pitch_diameter = ", str(self.wheel_pitch_diameter),
                     "\nwheel_circular_pitch = ", str(self.wheel_circular_pitch),
                     "\nwheel_addendum = ", str(self.wheel_addendum),
                     "\nwheel_addendum_radius = ", str(self.wheel_addendum_radius),
                     "\nwheel_dedendum = ", str(self.wheel_dedendum),
                     "\npinion_count = ", str(self.pinion_count),
                     "\npinion_pitch_diameter = ", str(self.pinion_pitch_diameter),
                     "\npinion_addendum = ", str(self.pinion_addendum),
                     "\npinion_addendum_radius = ", str(self.pinion_addendum_radius),
                     "\npinion_dedendum = ", str(self.pinion_dedendum),
                     "\ngear_ratio = ", str(self.gear_ratio),
                     "\nmodule = ", str(self.module),
                     "\nwheel_center_hole = ", str(self.wheel_center_hole),
                     "\npinion_center_hole = ", str(self.pinion_center_hole),
                     "\ncustom_slop = ", str(self.custom_slop),
                     "\ncustom_slop_enabled = ", str(self.custom_slop_enabled)])

        return r

    def addendum_factor(self):
        """returns the calculated addendum factor for the given wheel pinion pair
    The calculation is iterative and completes when the result reaches an acceptable error limit"""
        error_limit = 0.000001

        t0 = 1.0
        t1 = 0.0
        r2 = 2.0 * self.wheel_count / self.pinion_count
        while abs(t1 - t0) > error_limit:
            t0 = t1
            b = math.atan2(math.sin(t0), (1.0 + r2 - math.cos(t0)))
            t1 = math.pi / self.pinion_count + r2 * b
        k = 1.0 + r2
        d = math.sqrt(1.0 + k * k - 2.0 * k * math.cos(t1))
        result = 0.25 * self.pinion_count * (1.0 - k + d)
        return result

    def compute_wheel(self):
        """Computes values for critical dimensions of the wheel"""
        self.wheel_add_factor = self.addendum_factor()
        self.wheel_practical_addendum_factor = self.wheel_add_factor * 0.95
        self.gear_ratio = self.wheel_count / self.pinion_count
        self.wheel_circular_pitch = self.module * math.pi
        self.wheel_dedendum = self.module * math.pi / 2
        self.wheel_pitch_diameter = self.module * self.wheel_count
        self.pinion_pitch_diameter = self.module * self.pinion_count
        self.wheel_addendum = self.module * 0.95 * self.wheel_add_factor
        self.wheel_addendum_radius = self.module * 1.40 * self.wheel_add_factor

    @staticmethod
    def is_point_within_wheel(wheel_centre, test_point, wheel_radius):
        """Returns True if the test_point is within the diameter of a circle of given radius at the specified centre"""
        d_x = test_point.x - wheel_centre.x
        d_y = test_point.y - wheel_centre.y
        px = math.sqrt((d_x * d_x) + (d_y * d_y))
        return px <= wheel_radius

    def addendum_radius_centre(self, radius, point_a, point_b, center_x, center_y):
        """returns a Point representing the centre location of addendum radius
        radius is the radius of the addendum
        point_a and point_b are endpoints of addendum arc
        :rtype: Point representing location of addendum radius centre"""

        q = math.sqrt(math.pow((point_b.x - point_a.x), 2) + math.pow((point_b.y - point_a.y), 2))
        y3 = (point_a.y + point_b.y) / 2
        x3 = (point_a.x + point_b.x) / 2
        basex = math.sqrt(math.pow(radius, 2) - math.pow((q / 2), 2)) * (point_a.y - point_b.y) / q
        basey = math.sqrt(math.pow(radius, 2) - math.pow((q / 2), 2)) * (point_b.x - point_a.x) / q
        centerx1 = x3 + basex
        centery1 = y3 + basey
        centerx2 = x3 - basex
        centery2 = y3 - basey

        radius_centre = Point(centerx1, centery1)

        # todo change so circle_centre can be anywhere rather than fixed zero pont
        gear_centre = Point(center_x, center_y)

        if self.is_point_within_wheel(gear_centre, radius_centre, self.wheel_pitch_diameter):
            return radius_centre
        else:
            radius_centre.x = centerx2
            radius_centre.y = centery2
            return radius_centre

    def build_wheel_sketch_lines(self):
        """Draws the sketch elements for the wheel - should only be called after compute_wheel()"""
        wheel_centre_x = 0.0
        wheel_centre_y = 0.0
        outer_diameter = self.wheel_pitch_diameter + (self.wheel_addendum * 2)
        inner_diameter = self.wheel_pitch_diameter - (self.wheel_dedendum * 2)
        outer_radius = outer_diameter / 2
        inner_radius = inner_diameter / 2
        wheel_pitch_radius = self.wheel_pitch_diameter / 2
        tooth_angle = 360.0 / self.wheel_count
        for t in range(0, self.wheel_count):
            ref_angle_apex = tooth_angle * t
            next_ref_angle_apex = tooth_angle * (t + 1)

            point_1_x = outer_radius * (math.cos(math.radians(ref_angle_apex)))
            point_1_y = outer_radius * (math.sin(math.radians(ref_angle_apex)))

            point_2_x = wheel_pitch_radius * (math.cos(math.radians(ref_angle_apex + (tooth_angle / 4))))
            point_2_y = wheel_pitch_radius * (math.sin(math.radians(ref_angle_apex + (tooth_angle / 4))))

            point_3_x = inner_radius * (math.cos(math.radians(ref_angle_apex + (tooth_angle / 4))))
            point_3_y = inner_radius * (math.sin(math.radians(ref_angle_apex + (tooth_angle / 4))))

            point_4_x = inner_radius * (math.cos(math.radians(ref_angle_apex - (tooth_angle / 4))))
            point_4_y = inner_radius * (math.sin(math.radians(ref_angle_apex - (tooth_angle / 4))))

            point_5_x = wheel_pitch_radius * (math.cos(math.radians(ref_angle_apex - (tooth_angle / 4))))
            point_5_y = wheel_pitch_radius * (math.sin(math.radians(ref_angle_apex - (tooth_angle / 4))))

            point_6_x = inner_radius * (math.cos(math.radians(next_ref_angle_apex - (tooth_angle / 4))))
            point_6_y = inner_radius * (math.sin(math.radians(next_ref_angle_apex - (tooth_angle / 4))))

            point_a = Point(point_1_x, point_1_y)

            point_b = Point(point_2_x, point_2_y)

            point_c = Point(point_5_x, point_5_y)

            rad_center = self.addendum_radius_centre(self.wheel_addendum_radius, point_a, point_b, wheel_centre_x,
                                                     wheel_centre_y)

            self.sketch.AddArcCenterStartEnd(rad_center.x, rad_center.y, point_1_x, point_1_y, point_2_x,
                                             point_2_y, False)
            rad_center = self.addendum_radius_centre(self.wheel_addendum_radius, point_c, point_a, wheel_centre_x,
                                                     wheel_centre_y)

            self.sketch.AddArcCenterStartEnd(rad_center.x, rad_center.y, point_5_x, point_5_y, point_1_x,
                                             point_1_y, False)

            self.sketch.AddLine(point_2_x, point_2_y, point_3_x, point_3_y, False)
            self.sketch.AddLine(point_4_x, point_4_y, point_5_x, point_5_y, False)
            self.sketch.AddArcCenterStartEnd(wheel_centre_x, wheel_centre_y, point_3_x, point_3_y, point_6_x, point_6_y,
                                             False)

        # add center hole
        self.sketch.AddCircle(wheel_centre_x, wheel_centre_y, self.wheel_center_hole, False)

        # diameter reference lines
        self.sketch.AddCircle(wheel_centre_x, wheel_centre_y, self.wheel_pitch_diameter, True)
        self.sketch.AddCircle(wheel_centre_x, wheel_centre_y, outer_diameter, True)
        self.sketch.AddCircle(wheel_centre_x, wheel_centre_y, inner_diameter, True)

    def build_wheel(self):
        self.compute_wheel()
        self.build_wheel_sketch_lines()

    def initialize_pinion_tooth_width(self):
        """ From http://www.csparks.com/watchmaking/CycloidalGears/index.jhtml:
        The nominal width of a tooth or a space when they are equally spaced is just pi/2, or about 1.57.
        For pinions, we will reduce the width of the tooth a bit. For pinions with 6-10 leaves, the tooth
        width at the pitch circle is 1.05. For pinions with 11 or more teeth the tooth width is 1.25."""

        if self.pinion_count <= 10:
            factor = 1.05
        else:
            factor = 1.25
        self.pinion_half_tooth_angle = factor * self.module / self.pinion_pitch_diameter

    def initialize_pinion_addendum(self):
        """For details see the Profile - Leaves tables in
        http://www.csparks.com/watchmaking/CycloidalGears/index.jhtml"""
        if self.pinion_count <= 7:
            # high ogival
            self.pinion_addendum = 0.855 * self.module
            self.pinion_addendum_radius = 1.050 * self.module
        elif self.pinion_count == 8 | self.pinion_count == 9:
            # medium ogival
            self.pinion_addendum = 0.670 * self.module
            self.pinion_addendum_radius = 0.7 * self.module

        elif self.pinion_count == 10:
            # round top for small tooth
            self.pinion_addendum = 0.525 * self.module
            self.pinion_addendum_radius = 0.525 * self.module
        else:
            # 11+ teeth, round top for wider tooth
            self.pinion_addendum = 0.625 * self.module
            self.pinion_addendum_radius = 0.625 * self.module

    def build_pinion_sketch_lines(self):
        """Draws the sketch elements for the pinion"""
        pinion_centre_x = (self.wheel_pitch_diameter + self.pinion_pitch_diameter)
        pinion_centre_y = 0.0
        outer_diameter = self.pinion_pitch_diameter + (self.pinion_addendum * 2)
        inner_diameter = self.pinion_pitch_diameter - (self.pinion_dedendum * 2)
        outer_radius = outer_diameter / 2
        inner_radius = inner_diameter / 2
        pinion_pitch_radius = self.pinion_pitch_diameter / 2
        tooth_angle = 360.0 / self.pinion_count
        half_tooth_angle = self.pinion_half_tooth_angle

        for t in range(0, self.pinion_count):
            ref_angle_apex = tooth_angle * t

            next_ref_angle_apex = tooth_angle * (t + 1)

            point_1_x = (outer_radius * (math.cos(math.radians(ref_angle_apex)))) + pinion_centre_x
            point_1_y = outer_radius * (math.sin(math.radians(ref_angle_apex)))

            point_2_x = (pinion_pitch_radius * (
                math.cos(math.radians(ref_angle_apex) + half_tooth_angle))) + pinion_centre_x
            point_2_y = pinion_pitch_radius * (math.sin(math.radians(ref_angle_apex) + half_tooth_angle))

            point_3_x = (inner_radius * (math.cos(math.radians(ref_angle_apex) + half_tooth_angle))) + pinion_centre_x
            point_3_y = inner_radius * (math.sin(math.radians(ref_angle_apex) + half_tooth_angle))

            point_4_x = (inner_radius * (math.cos(math.radians(ref_angle_apex) - half_tooth_angle))) + pinion_centre_x
            point_4_y = inner_radius * (math.sin(math.radians(ref_angle_apex) - half_tooth_angle))

            point_5_x = (pinion_pitch_radius * (
                math.cos(math.radians(ref_angle_apex) - half_tooth_angle))) + pinion_centre_x
            point_5_y = pinion_pitch_radius * (math.sin(math.radians(ref_angle_apex) - half_tooth_angle))

            point_6_x = (inner_radius * (
                math.cos(math.radians(next_ref_angle_apex) - half_tooth_angle))) + pinion_centre_x
            point_6_y = inner_radius * (math.sin(math.radians(next_ref_angle_apex) - half_tooth_angle))

            point_a = Point(point_1_x, point_1_y)

            point_b = Point(point_2_x, point_2_y)

            point_c = Point(point_5_x, point_5_y)

            rad_center = self.addendum_radius_centre(self.pinion_addendum_radius, point_a, point_b, pinion_centre_x,
                                                     pinion_centre_y)

            self.sketch.AddArcCenterStartEnd(rad_center.x, rad_center.y, point_1_x, point_1_y, point_2_x,
                                             point_2_y, False)

            rad_center = self.addendum_radius_centre(self.pinion_addendum_radius, point_c, point_a, pinion_centre_x,
                                                     pinion_centre_y)

            self.sketch.AddArcCenterStartEnd(rad_center.x, rad_center.y, point_5_x, point_5_y, point_1_x,
                                             point_1_y, False)

            self.sketch.AddLine(point_2_x, point_2_y, point_3_x, point_3_y, False)
            self.sketch.AddLine(point_4_x, point_4_y, point_5_x, point_5_y, False)
            self.sketch.AddArcCenterStartEnd(pinion_centre_x, pinion_centre_y, point_3_x, point_3_y, point_6_x,
                                             point_6_y, False)

        # add center hole
        self.sketch.AddCircle(pinion_centre_x, pinion_centre_y, self.pinion_center_hole, False)

        # diameter reference lines
        self.sketch.AddCircle(pinion_centre_x, pinion_centre_y, self.pinion_pitch_diameter, True)
        self.sketch.AddCircle(pinion_centre_x, pinion_centre_y, outer_diameter, True)
        self.sketch.AddCircle(pinion_centre_x, pinion_centre_y, inner_diameter, True)

    def build_pinion(self):
        self.pinion_pitch_diameter = self.module * self.pinion_count
        if self.custom_slop_enabled:
            self.pinion_dedendum = self.wheel_addendum + self.custom_slop
        else:
            self.pinion_dedendum = self.module * (self.wheel_practical_addendum_factor + 0.4)
        self.initialize_pinion_tooth_width()
        self.initialize_pinion_addendum()
        self.build_pinion_sketch_lines()

    def build_gear_set(self):
        self.build_wheel()
        self.build_pinion()