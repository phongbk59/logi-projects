

import numpy
import time
import math
import matplotlib.pyplot as plt


class EuclidianPoint():
	
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		

class PurePursuit():
	
	look_ahead_dist = 10.0

	def __init__(self):
		self.curv = 0.0
	
	def computeSteering(self, point_A, point_B, pos, heading):	
		toRad = math.pi/180.0		
		eq_path = [0, 0]	
		# compute path equation
		eq_path[0] = (point_A.y - point_B.y)/(point_A.x - point_B.x)
		eq_path[1] = point_B.y - (point_B.x*eq_path[0])
		#compute equation of line orthogonal to path and passing by current position		
		eq_orth = [(-1/eq_path[0]), 0]
		eq_orth[1] = pos.y - (eq_orth[0]*pos.x)
		cross_x = (eq_orth[1] - eq_path[1])/(eq_path[0] - eq_orth[0])
		cross_y = cross_x * eq_path[0] + eq_path[1]		
		#compute coordinates of lookahead point
		
		tetha = math.atan(eq_path[0]) # compute line angle
		look_ahead_point_y = (self.look_ahead_dist * math.sin(tetha)) + cross_y
		look_ahead_point_x = (self.look_ahead_dist * math.cos(tetha)) + cross_x
		
		# should check that the look_ahead point is not further that the target waypoint
				
		# now translating and rotating to center on robot
		look_ahead_point_x_rob = look_ahead_point_x - pos.x
		look_ahead_point_y_rob = look_ahead_point_y - pos.y

		#rotation to align on robot reference frame, heading pointing 90
		rotation_tetha = 90.0 - heading
		look_ahead_point_x_rob = look_ahead_point_x_rob * math.cos(toRad*rotation_tetha) + look_ahead_point_y_rob * math.sin(toRad*rotation_tetha)
		look_ahead_point_y_rob = look_ahead_point_x_rob * -math.sin(toRad*rotation_tetha) + look_ahead_point_y_rob * math.cos(toRad*rotation_tetha)
		
		# following is based on 
		# http://www8.cs.umu.se/kurser/TDBD17/VT06/utdelat/Assignment%20Papers/Path%20Tracking%20for%20a%20Miniature%20Robot.pdf
		
		print look_ahead_point_x_rob
		print look_ahead_point_y_rob
		D_square = pow(look_ahead_point_x_rob, 2) + pow(look_ahead_point_y_rob, 2)
		r = D_square/(2.0*look_ahead_point_x_rob)
		curvature = 1.0/r


		
		plt.subplot(211)
		plt.plot(point_A.x, point_A.y, '+r')
		plt.plot(point_B.x, point_B.y, '+g' )
		plt.plot(pos.x,  pos.y, '+b')
		plt.plot(cross_x, cross_y, '+k')
		plt.plot(look_ahead_point_x, look_ahead_point_y, '+c')
		
		path_x = numpy.linspace(point_A.x,point_B.x,100) # 100 linearly spaced numbers
		path_y = eq_path[0]*path_x + eq_path[1]
		plt.plot(path_x, path_y)
		equ_x = numpy.linspace(cross_x, pos.x, 100) # 100 linearly spaced numbers
		equ_y = eq_orth[0]*equ_x + eq_orth[1]
		plt.plot(equ_x, equ_y, 'r')
		#plt.axis([0.0, 25, 0.0, 25])


		
		plt.subplot(212)
		circ = plt.Circle((0,r),r,color='r', fill=False)
		plt.plot(0.0, 0.0, '+r')
		plt.plot(look_ahead_point_x_rob, look_ahead_point_y_rob, '+b')
		plt.plot(r, 0.0, '+k')
		
		plt.gca().add_artist(circ)
		plt.show()

		return curvature


if __name__ == "__main__":	
	path = PurePursuit()
	curv = path.computeSteering(EuclidianPoint(3.0, 4.0), EuclidianPoint(25.0, 2.0), EuclidianPoint(10.0, 4.5), 90.0)
	print curv
		
		

		
		
		
