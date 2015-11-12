from consutils.powcons import PowerConsumption;
from consutils.periods import PowerConsPeriod, SampleTime;
import copy, datetime;

#Any variables with the name "timeStamp" are datetime.datetime objects.
class PowerWithTimeGenerator:
	def __init__(self, limitedStartTime, limitedStopTime, minPeriod, maxPeriod, minSecondInterval, maxSecondInterval, startDate, endDate, minPower, maxPower=None):
		#If no maxPower passed, minPower acts as powerList.
		self.__pc = PowerConsumption(minPower, maxPower);
		self.__pcp = PowerConsPeriod(limitedStartTime, limitedStopTime, minPeriod, maxPeriod);
		start, stop = self.__pcp.getNextStartAndStopTimesNoLimit();
		self.__startDate = startDate; #datetime.datetime
		self.__endDate = endDate; #datetime.datetime
		self.__startTimeStamp = copy.deepcopy(self.__startDate);
		self.__startTimeStamp.replace(hour=start.hour, minute=start.minute);
		self.__stopTimeStamp = copy.deepcopy(self.__startDate);
		self.__stopTimeStamp = self.__stopTimeStamp.replace(hour=stop.hour, minute=stop.minute);
		self.__st = SampleTime(minSecondInterval, maxSecondInterval, self.__startTimeStamp, self.__stopTimeStamp);
		self.timeStamp = None;
		self.power = 0;
		self.__start = None;
		self.__stop = None;
		self.__lastStart = None;
		self.__lastStop = None;
		
	def getNextConsumption(self):
		if self.timeStamp is not None: #If it's not the first time
			if self.timeStamp > self.__stopTimeStamp:
				if self.__start is not None:
					self.__lastStart, self.__lastStop = self.__start, self.__stop;
				self.__start, self.__stop = self.__pcp.getNextStartAndStopTimesNoLimit();
				#print("start: "+str(self.__start)+", stop: "+str(self.__stop));
				self.__startTimeStamp = self.__startTimeStamp.replace(hour=self.__start.hour, minute=self.__start.minute);
				self.__stopTimeStamp = self.__stopTimeStamp.replace(hour=self.__stop.hour, minute=self.__stop.minute);
				if self.__lastStart is not None:
					oneDay = datetime.timedelta(days=1);
					if self.__lastStart > self.__start: #Going to a new day
						#print("\n\nlastStart: "+str(self.__lastStart) + ", start: "+str(self.__start)+"\n\n");
						#print("oneDay: " + str(oneDay) + "\n\n");
						self.__startTimeStamp = self.__startTimeStamp + oneDay;
						self.__stopTimeStamp = self.__stopTimeStamp + oneDay;
					elif self.__startTimeStamp > self.__stopTimeStamp:
						self.__stopTimeStamp = self.__stopTimeStamp + oneDay;
						
				self.__st.setNewLimitedTime(self.__startTimeStamp, self.__stopTimeStamp);
				#print("+++++startTimeStamp: "+str(self.__startTimeStamp)+", stopTimeStamp: "+str(self.__stopTimeStamp));
		else:
			self.power = self.__pc.getRandomPower(); #Assign a power for only the first time
		
		#print("timeStamp: "+str(self.timeStamp)+", stopTimeStamp: "+str(self.__stopTimeStamp));
		self.timeStamp = self.__st.getNextSampleTime();
		
		#print("=========timeStamp: "+str(self.timeStamp)+", endData: "+str(self.__endDate));
		if self.timeStamp < self.__endDate:
			if not(self.timeStamp.time() > self.__pcp.limitedStopTime or self.timeStamp.time() < self.__pcp.limitedStartTime):
				if self.timeStamp > self.__stopTimeStamp:
					self.power = self.__pc.getRandomPower();
			else:
				self.power = 0; #Set power = 0 when it passes the operating time (the limitedStopTime)
			return self.power, self.timeStamp;
		else:
			return None, None;
	
