# figure out a way to use intersect_by_area if shapes have different constructors
class Shape:
	def intersect_by_area(self, other):
		return bool(set(self.area()) & set(other.area()))

class Rect(Shape):
	#a rectangle on the map. used to characterize a room.
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return center_x, center_y

	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
						self.y1 <= other.y2 and self.y2 >= other.y1)

	# Return a list of x,y coords that represents this shape
	def area(self):
		area = []
		for y in range(self.y1, self.y2 + 1):
			for x in range(self.x1, self.x2 + 1):
				area.append((x,y))
		return area

class Circle(Shape):
	def __init__(self, x, y, r):
		self.x = x
		self.y = y
		self.r = r

	def center(self):
		return self.x, self.y

	# TODO
	def area(self):
		area = []
		for y in range(self.y - self.r, self.y + self.r):
			for x in range(self.x - self.r, self.x + self.r):
				if abs(y - self.y) <= self.r and abs(x - self.x) <= self.r:
					area.append((x,y))
		return area