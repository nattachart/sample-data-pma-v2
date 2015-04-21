from consutils.powtime import PowerWithTimeGenerator;
import datetime, math;

db = "pma_sp2014_db";

powerList = [0, 277, 277*2, 277*3, 277*4, 277*5, 277*6];
limitedStartTime = datetime.time(hour=8, minute=0);
limitedStopTime = datetime.time(hour=18, minute=0);
minPeriod = datetime.timedelta(hours=10);
maxPeriod = datetime.timedelta(hours=10);
minSecondInterval = 2;
maxSecondInterval = 5;
startDate = datetime.datetime(year=2014, month=10, day=20);
endDate = datetime.datetime(year=2014, month=10, day=21);
godID = 9;

#dataID = 0;
vrms = 230; #Actually it's not constant like this, just assume for the sake of simplicity
vpp = round(230*math.sqrt(2), 2); #Actually it's not constant like this, just assume for the sake of simplicity
irms = 0; #Will be a derived value
ipp = 0; #Will be a derived value
pf = 0.8; #Actually it's not constant like this, just assume for the sake of simplicity
updateAt = "null";
modBy = "null";
desc = "null";
power = 0;
timeStamp = None;
tmpSQL = "";

initial = "insert ignore into data(`date`, month, year, hh, mm, ss, vrms, vpp, irms, ipp, `power`, power_factor, update_at, group_of_device_id, modified_by, `desc`) values";

pwtg = PowerWithTimeGenerator(limitedStartTime, limitedStopTime, minPeriod, maxPeriod, minSecondInterval, maxSecondInterval, startDate, endDate, powerList, None);

print("use " + db + ";\n");
while power is not None:
	power, timeStamp = pwtg.getNextConsumption();
	#print("power: "+str(power)+", timeStamp: "+str(timeStamp));
	if timeStamp is not None:
		#dataID = dataID + 1;
		irms=round(power/(vrms*pf), 2);
		ipp=round(irms*math.sqrt(2), 2);
		pfUsed = pf;
		if power == 0:
			pfUsed = 0;
		tmpSQL = ''.join([initial, "(", str(timeStamp.day), ", ", str(timeStamp.month), ", ", 
		str(timeStamp.year), ", ", str(timeStamp.hour), ", ", str(timeStamp.minute), ", ", str(timeStamp.second), ", ",
		str(vrms), ", ", str(vpp), ", ", str(irms), ", ", str(ipp), ", ",
		str(power), ", ", str(pfUsed), ", ", updateAt, ", ", str(godID), ", ", modBy, ", ", desc, ");"]);
		print(tmpSQL);

