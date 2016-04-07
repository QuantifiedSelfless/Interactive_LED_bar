class panel:

	def __init__(self, number, addr, flipped):
		#inputs:
		self.number = number    # panel number
		self.addr = addr		# panel I2C address
		self.flipped = flipped	# panel flipped 180 degrees?
		self.IRmap = []			# IR sensor map
		self.animap = []		# Animation map
        
	def set_IRmap(self, IRmap):
		self.IRmap = IRmap

	def set_animap(self, animap):
		self.animap = animap

class barmodule:
	
	def __init__(self):
		self.panels=[]
		self.rowsPerPanel = 7
		self.colsPerPanel = 7
		self.unusedLEDsPerPanel = 1
		self.lednobyxy=[]
		self.ledxbyno=[]
		self.ledybyno=[]
		
	def add_panel(self, panel):
		self.panels.append(panel)
		
	#this function allows us to translate x,y locations to LED numbers
	def populateGrids(self):
		self.lednobyxy = []
		#Go through each panel
		for pan in range(len(self.panels)):
			start = self.panels[pan].number*self.colsPerPanel;
			stop = start+self.colsPerPanel;
			#fill cols/rows
			for i in range(start,stop):
				self.lednobyxy.append([])
				for j in range(self.rowsPerPanel):
					#Different pending if wire btw panels is flipped
					k = i;
					if (self.panels[pan].flipped):
						k = i + 1
					if (k%2 == 0):
						self.lednobyxy[i].append((i * self.rowsPerPanel) + j + self.unusedLEDsPerPanel*pan)
					else:
						self.lednobyxy[i].append((i * self.rowsPerPanel) + (self.rowsPerPanel-1 - j) + self.unusedLEDsPerPanel*pan)
		

#readNodes wants (addr,panelno)
#I suggest defining an array to look up the addr as well as corresponding registers
#then, we just call readNodes() to populate arrays nodeResults and nodeDiffs
#to check for trigger, we can then go through nodeDiffs and check if elements are > threshold