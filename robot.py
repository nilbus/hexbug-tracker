from math import *
from box_world import *
import random

class robot:
    def __init__(self, x = 0.0, y = 0.0, heading = 0.0, distance = 1.0):
        """This function is called when you create a new robot. It sets some of
        the attributes of the robot, either to their default values or to the values
        specified when it is created."""
        self.x = x
        self.y = y
        self.heading = heading
        self.distance = distance # only applies to target bot, who always moves at same speed.
        self.distance_noise    = 0.0
        self.measurement_noise = 0.0


    def set_noise(self, new_d_noise, new_m_noise):
        """This lets us change the noise parameters, which can be very
        helpful when using particle filters."""
        self.distance_noise    = float(new_d_noise)
        self.measurement_noise = float(new_m_noise)


    def move(self, distance, tolerance = 0.001):
        """This function turns the robot and then moves it forward."""
        distance = random.gauss(distance, self.distance_noise)

        # truncate to fit physical limitations
        distance = max(0.0, distance)

        # Naive bounce model based on angle to reflection
        bounds = box_bounds()
        #Top Edge
        if self.x < bounds['min_x']:
            self.heading = pi - self.heading
        #Right Edge
        elif self.y < bounds['min_y']:
            self.heading = -1 * self.heading
        #Bottom Edge
        if self.x > bounds['max_x']:
            self.heading = pi - self.heading
        #Left Edge
        if self.y > bounds['max_y']:
            self.heading = -1 * self.heading

        # Execute motion
        self.heading = angle_trunc(self.heading)
        self.x += distance * cos(self.heading)
        self.y += distance * sin(self.heading)

    def advance(self):
        """This function is used to advance the bot."""
        self.move(self.distance)
        return self.sense()

    def sense(self):
        """This function represents the robot sensing its location. When
        measurements are noisy, this will return a value that is close to,
        but not necessarily equal to, the robot's (x, y) position."""
        return (random.gauss(self.x, self.measurement_noise),
                random.gauss(self.y, self.measurement_noise))

    def __repr__(self):
        """This allows us to print a robot's position"""
        return '[%.5f, %.5f]'  % (self.x, self.y)
