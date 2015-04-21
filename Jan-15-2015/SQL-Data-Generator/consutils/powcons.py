import random;

class PowerConsumption:
	
	def __init__(self, powerMin, powerMax=None):
		if powerMax is None:
			self.__powerList = powerMin;
			self.__powerMin = -1;
			self.__powerMax = -1;
		else:
			self.__powerMin = powerMin;
			self.__powerMax = powerMax;
			self.__powerList = None;

	def getRandomPower(self):
		if self.__powerList is not None:
			return self.__getRandomPowerFromList();
		else:
			return self.__getRandomPowerFromRange();
	
	def __getRandomPowerFromList(self):
		maxIdx = len(self.__powerList) - 1;
		idx = random.randint(0, maxIdx);
		return self.__powerList[idx];

	def __getRandomPowerFromRange(self):
		return random.uniform(self.__powerMin, self.__powerMax + 1);
