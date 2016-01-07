import os
import struct
from array import array
import numpy as np

size = 128 # input image length is size*size -- bunu classa gom ogrenince


class database(object):

        mnist = False
        count = 0
        numOfItems = 0
        images = []
        labels = []
        InOneHotShotFormLabels = []
        ImageArray = [] 

	def __init__(self, path='.'):
		self.path = path

	'''  	 @header 
	         item sayisi - 4 byte
		 reserved - 12 byte

		 @item
		image : sizexsize gray -- 64kb
		label : 1 byte 

	'''	
		
	def load(self, filepath):

		with open(filepath, 'rb') as file:
			numOfItems , dummy = struct.unpack("<II", file.read(8))
			if(numOfItems == 0) :
				print ' {} dosyasi bos, cikis..'.format(file)
				exit()

		self.numOfItems = numOfItems
		with open(filepath, 'rb') as file:
			db = array("B", file.read()) 
			
		items = []
		for i in range(numOfItems):
			items.append([0] * (size * size+1)) # 1 label icin

		for i in range(numOfItems):
			items[i][:] = db[16 + i * (size * size +1): 16 + (i + 1) * (size * size +1)] # 16 header dan geliyor


		self.images = []
		for i in range(numOfItems):
			self.images.append([0] * size * size)

		for i in range(numOfItems):
			self.images[i][:] = items[i][:-1]

		self.labels = []
		for i in range(numOfItems):
			self.labels.append(0)

		for i in range(numOfItems):
			self.labels[i] = items[i][size*size]
			
		labelsArray = np.array(self.labels)

		self.InOneHotShotFormLabels = np.ndarray(shape=[numOfItems,3], dtype=float)
		self.InOneHotShotFormLabels[:] = [0,0,0]
                for i in range (numOfItems):
                        if self.mnist is True:
                                self.InOneHotShotFormLabels[i][labelsArray[i]] = 1  
                        else:
                                self.InOneHotShotFormLabels[i][labelsArray[i]-1] = 1
                 
                self.ImageArray = np.array(self.images, dtype=float)       
                self.ImageArray[:][:] = self.ImageArray[:][:]/256.0

		return numOfItems, self.ImageArray, self.InOneHotShotFormLabels
		
	def loadmnist(self, filepath):
	        mnist = True;
	        global size 
	        mnist = True;
	        size = 28
	        return self.load(filepath)
	        
	def loadfare(self, filepath):
	        mnist = False;
	        global size
	        size = 128
	        return self.load(filepath)
	        
        def size(self):
                global size
                return size
 
        def NextBatch(self, batchSize):
                global size
                if self.count is self.numOfItems:
                        self.count = 0
	         
                self.count = self.count + batchSize
                return self.ImageArray[self.count :(self.count + batchSize)][:],  self.InOneHotShotFormLabels[self.count :(self.count + batchSize)][:] 
                
                
	        
	       
