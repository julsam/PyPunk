from PySFML import sf
from Graphic import Graphic

#Reference to colour
Color = sf.Color

class Rectangle:
	def __init__(self, x, y, width, height):
		self.x = x; self.y = y;
		self.width = width; self.height = height;

class Image(Graphic, sf.Sprite):
	def __init__(self, loc, rect=None):
		"""Create new Image
		Args:
		loc: location of image"""
		Graphic.__init__(self)
		if type(loc) == str:
			self.img = GetImage(loc)
		elif type(loc) == sf.Image:
			self.img = loc
		else:
			raise TypeError("Please pass the path to an image or a sf.Image instance")
		sf.Sprite.__init__(self, self.img)

		#Sprite.SetSubRect(sf::IntRect(10, 10, 20, 20));
		if rect:
			self.SetSubRect(sf.IntRect(rect.x, rect.y, rect.x+rect.width, rect.y+rect.height))

		# Rotation of the image, in degrees.
		self.angle = 0

		# Scale of the image, affects both x and y scale.
		self.scale = 1

		# X scale of the image.
		self.scaleX = 1

		# Y scale of the image.
		self.scaleY = 1

		# X origin of the image, determines transformation point.
		self.originX = 0

		# Y origin of the image, determines transformation point.
		self.originY = 0

		self._alpha = 1.0

	def render(self, App, pos=(0, 0)):
		"""Render the image to App"""
		self.SetPosition(int(self.x+pos[0]), int(self.y+pos[1]))
		if self.visible:
			App.Draw(self)
	
	def set_alpha(self, value):
		if value > 1: value = 1
		self._alpha = value
		self.SetColor(sf.Color(255, 255, 255, int(value*255)))
	alpha = property(lambda self: self._alpha, set_alpha)


class Spritemap(Image):
	def __init__(self, source, frameWidth=0, frameHeight=0, callback=None):
		Image.__init__(self, loc)

class Shape(sf.Shape):
	def __init__(self):
		"""Create a shape"""
		sf.Shape.__init__(self)
		self.x = 0
		self.y = 0
		self._alpha = 1.0
	
	def createRect(self, width, height, colour):
		"""Predefined rectangle shape"""
		self.AddPoint(0, 0, colour)
		self.AddPoint(width, 0, colour)
		self.AddPoint(width, height, colour)
		self.AddPoint(0, height, colour)
	
	def render(self, App, pos=(0, 0)):
		self.SetPosition(int(self.x+pos[0]), int(self.y+pos[1]))
		App.Draw(self)
	
	def set_alpha(self, value):
		if value > 1: value = 1
		self._alpha = value
		self.SetColor(sf.Color(255, 255, 255, int(value*255)))
	alpha = property(lambda self: self._alpha, set_alpha)

class Text(sf.String):
	def __init__(self, loc, text="", size=16):
		"""Create text graphic
		Args:
		loc: location of font
		text: text to display
		size: font size"""
		self.fnt = GetFont(loc, size)

		self.x = 0
		self.y = 0
		self._alpha = 1.0

		sf.String.__init__(self)
		self.SetText(text)
		self.SetFont(self.fnt)
		self.SetSize(size)
	
	def set_color(self, value):
		self.SetColor(sf.Color(value[0], value[1], value[2]))
	def get_color(self):
		"""Get/Set the color of the text"""
		clr = self.GetColor()
		return (clr.r, clr.g, clr.b)
	color = property(get_color, set_color)

	def set_text(self, value): self.SetText(value)
	text = property(lambda self: self.GetText(), set_text)

	def set_size(self, value): self.SetSize(value)
	size = property(lambda self: self.GetSize(), set_size)

	def set_alpha(self, value):
		if value > 1: value = 1
		self._alpha = value
		self.SetColor(sf.Color(255, 255, 255, int(value*255)))
	alpha = property(lambda self: self._alpha, set_alpha)
	
	def render(self, App, pos=(0, 0)):
		self.SetPosition(int(self.x+pos[0]), int(self.y+pos[1]))
		App.Draw(self)

class Graphiclist(object):
	def __init__(self, *args):
		"""List of graphics to render"""
		self.list = args
	
	def add(self, toAdd):
		self.list.append(toAdd)
	def remove(self, toRem):
		self.list.remove(toRem)
	
	def render(self, App, pos=(0,0)):
		for obj in self.list:
			obj.render(App, pos)

#Caches
imageCache = {}
def GetImage(loc):
	try: #Will only run if already loaded
		return imageCache[loc]
	except KeyError:
		Image = sf.Image()
		Image.SetSmooth(False)
		if not Image.LoadFromFile(loc):
			return None
		imageCache[loc] = Image
		return Image

fontCache = {}
def GetFont(loc, size):
	try:
		fnt = fontCache[loc]
		old_size = fnt.GetCharacterSize()
		if size < old_size:
			return fnt
	except KeyError: pass
	Font = sf.Font()
	if not Font.LoadFromFile(loc, size):
		return None
	fontCache[loc] = Font
	return Font
