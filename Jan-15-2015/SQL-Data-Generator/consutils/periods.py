import random;
import datetime;
import copy;

class PowerConsPeriod:
	#This class does not include date information, only time.
	def __init__(self, limitedStartTime, limitedStopTime, minPeriod, maxPeriod):
		self.limitedStartTime = limitedStartTime; #an object of datetime.time (includes hour, minute)
		self.limitedStopTime = limitedStopTime; #an object of datetime.time (includes hour, minute)
		self.__minPeriod = minPeriod; #an object of datetime.timedelta (minutes and/or hours)
		self.__maxPeriod = maxPeriod; #an object of datetime.timedelta (minutes and/or hours)
		self.__lastStartTime = None; #supposed to hold an object of datetime.time (hour, minute)
		self.__lastStopTime = None; #supposed to hold an object of datetime.time (hour, minute)
		
	def getNextStartAndStopTimesNoLimit(self):
		if self.__lastStartTime is None:
			self.__lastStartTime = self.limitedStartTime;
			self.__lastStopTime = self.__lastStartTime;
		else:
			delta = self.getRandomPeriod();
			self.__lastStartTime = self.__lastStopTime;
			self.__lastStopTime = (datetime.datetime.combine(datetime.date.today(), self.__lastStartTime) + delta).time();
		return self.__lastStartTime, self.__lastStopTime;

	def getNextStartAndStopTimes(self):
		if self.__lastStartTime is None:
			self.__lastStartTime = self.limitedStartTime;
			self.__lastStopTime = self.__lastStartTime;
		else:
			randPeriod = self.getRandomPeriod();
			delta = datetime.timedelta(minutes=randPeriod);
			self.__lastStartTime = self.__lastStopTime;
			self.__lastStopTime = (datetime.datetime.combine(datetime.date.today(), self.__lastStopTime) + delta).time();
			if not(self.__lastStopTime <= self.limitedStopTime and self.__lastStopTime >= self.limitedStartTime):
				self.__lastStopTime = self.limitedStopTime;
		return self.__lastStartTime, self.__lastStopTime;
		
	def getRandomPeriod(self):
		return datetime.timedelta(seconds=random.randint(self.__minPeriod.total_seconds(), self.__maxPeriod.total_seconds()));

class SampleTime:
	def __init__(self, minSecondInterval, maxSecondInterval, limitedStartTime, limitedStopTime):
		self.__minSecondInterval = minSecondInterval; #in seconds (integer)
		self.__maxSecondInterval = maxSecondInterval; #in seconds (integer)
		self.__limitedStartTime = limitedStartTime; #an object of datetime.datetime (year, month, day, hour, minute, second, tzinfo)
		self.__limitedStopTime = limitedStopTime; #an object of datetime.datetime (year, month, day, hour, minute, second, tzinfo)
		self.__currentTime = None; #supposed to hold an object of datetime.datetime (year, month, day, hour, minute, second, tzinfo)

	def setNewLimitedTime(self, limitedStartTime, limitedStopTime):
		self.__limitedStartTime = limitedStartTime;
		self.__limitedStopTime = limitedStopTime;
		self.__currentTime = None; #supposed to hold an object of datetime.datetime (year, month, day, hour, minute, second)

	def getNextSampleTime(self):
		if self.__currentTime is None:
			self.__currentTime = copy.deepcopy(self.__limitedStartTime);
		else:
			randInterval = self.__getRandomSecondInterval();
			delta = datetime.timedelta(seconds=randInterval);
			self.__currentTime = self.__currentTime + delta;
			if not(self.__currentTime < self.__limitedStopTime):
				self.__currentTime = self.__limitedStopTime + datetime.timedelta(seconds=1); #plus 1 second so it wouldn't resemble the start time of the next period.
		return self.__currentTime;

	def __getRandomSecondInterval(self):
		return random.randint(self.__minSecondInterval, self.__maxSecondInterval);
