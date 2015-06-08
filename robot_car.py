from math import *
import random

world_size = 100.0


landmarks = [[20.0,20.0],
             [80.0,80.0],
             [20.0,80.0],
             [80.0,20.0]]

class robot_car:

	# --------

	# init: 
	#	creates robot and initializes location/orientation 
	#

	def __init__(self, length = 10.0):
		self.x = random.random() * world_size # initial x position
		self.y = random.random() * world_size # initial y position
		self.orientation = random.random() * 2.0 * pi # initial orientation
		self.length = length # length of robot
		self.bearing_noise  = 0.0 # initialize bearing noise to zero
		self.steering_noise = 0.0 # initialize steering noise to zero
		self.distance_noise = 0.0 # initialize distance noise to zero

	def __repr__(self):
		return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
	# --------
	# set: 
	#	sets a robot coordinate
	#

	def set(self, new_x, new_y, new_orientation):

		if new_orientation < 0 or new_orientation >= 2 * pi:
			raise ValueError, 'Orientation must be in [0..2pi]'
		self.x = float(new_x)
		self.y = float(new_y)
		self.orientation = float(new_orientation)


	# --------
	# set_noise: 
	#	sets the noise parameters
	#

	def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
		# makes it possible to change the noise parameters
		# this is often useful in particle filters
		self.bearing_noise  = float(new_b_noise)
		self.steering_noise = float(new_s_noise)
		self.distance_noise = float(new_d_noise)

	############# ONLY ADD/MODIFY CODE BELOW HERE ###################

	# --------
	# move:
	#   move along a section of a circular path according to motion
	#

	def move(self, motion): # Do not change the name of this function
		result = robot_car(self.length)
		result.set_noise(self.bearing_noise, self.steering_noise, self.distance_noise)
		
		# basically a straight implementation of the equations for bicycle-based movement
		alpha = motion[0]
		d = motion[1]
		beta = d * tan(alpha) / self.length
		if abs(beta) < 0.001:
			# no movement
			result.x = self.x + d * cos(self.orientation)
			result.y = self.y + d * sin(self.orientation)
		else:
			R = d / beta
			cx = self.x - sin(self.orientation) * R
			cy = self.y + cos(self.orientation) * R
			result.x = cx + sin(self.orientation + beta) * R
			result.y = cy - cos(self.orientation + beta) * R
		result.orientation = (self.orientation + beta) % (2*pi)
		
		return result # make sure your move function returns an instance
					  # of the robot class with the correct coordinates.
        def sense(self): #do not change the name of this function
		Z = []

		for l in landmarks:
			direction = atan2(l[0] - self.y, l[1] - self.x)
			bearing = direction - self.orientation
			Z.append(bearing % (2 * pi))
		
		return Z #Leave this line here. Return vector Z of 4 bearings.

