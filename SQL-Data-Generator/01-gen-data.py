import subprocess;

dataDir = "data";
groupNo = 1;
cmdPart1 = "python G";
cmdPart2 = "-data-gen.py > " + dataDir + "/";
cmdPart3 = "-G";
cmdPart4 = "-data.sql";

subprocess.call("mkdir " + dataDir, shell=True);

while groupNo <= 42:
	cmd = ''.join([cmdPart1, str(groupNo), cmdPart2, str(groupNo+1), cmdPart3, str(groupNo), cmdPart4]);
	print(cmd);
	subprocess.call(cmd, shell=True);
	groupNo = groupNo + 1;
