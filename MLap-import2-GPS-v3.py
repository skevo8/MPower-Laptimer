##distance.far:           8bytes version hex
##                        entries:
##                        8bytes float time
##                        8bytes float distance in meters

import struct
import pandas as pd
import plotly.express as px
import time

# SETTINGS 
##adresar="C:/Users/mhata/Documents/auto-moto/BMW-DIAG/MHDLogs/MLapTimer/Dunajská-Lužná-10-10-2020-164252.mpower/"
##adresar="C:/Users/mhata/Documents/auto-moto/BMW-DIAG/MHDLogs/MLapTimer/Orechová-Potôň-14-06-2020-120024.mpower/"
##adresar="C:/Users/mhata/Documents/auto-moto/BMW-DIAG/MHDLogs/MLapTimer/Driving-Experience-DE-1-06-05-2019-170409.mpower/"
adresar="C:/Users/mhata/Documents/auto-moto/BMW-DIAG/MHDLogs/MLapTimer/Tureň-27-12-2020-112347.mpower/"

SpdSmooth = 6   # smoothing parameter for Speed as it is only refreshing 2x sec
gLatSign = 1  # with -1 swap left/right accel
gLongSign = -1   # with -1 swap front/rear accel
DateAdjust = 978307200 # adjustment due to mac and unix timestamp https://stackoverflow.com/questions/16901279/convert-mac-timestamps-with-python

# ------------------
df = pd.DataFrame(columns=['Time','Distance'])

filename="Distance.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu
print("Time Stamp orig : "+ time.asctime(time.localtime(StartTime)))
print("Corrected Time  : "+ time.asctime(time.localtime(StartTime+DateAdjust)))
 
initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 16  # dlzka 2x8byte  Time, Distance
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@dd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    df.loc[x] = driveData

df["LogTime"]=df["Time"]-StartTime

##fig = px.line(df, x = "LogTime", y = "Distance", title="Distance (m)");
##
##fig.show()

#  RPM file
##rpm.far:                8bytes version hex
##                        entries:
##                        8bytes float time
##                        8bytes float rpm

filename="RPM.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu

initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 16  
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@dd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    df.loc[x,"RPM"] = driveData[1]


##Speed.far
##8bytes version hex
##entries:
##8bytes float time
##8bytes float speed in m/s

filename="Speed.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu

initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 16  # dlzka 2x8byte  Time, Distance
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@dd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    df.loc[x,"Speed"] = driveData[1]*3.6

df["SpeedSmooth"] = df["Speed"].rolling(SpdSmooth).mean()

##acceleratorPedal.far:   8bytes version hex
##                        entries:
##                        8bytes float time
##                        8bytes float (0-100)? pedal state
    
filename="AcceleratorPedal.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu

initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 16
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@dd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    df.loc[x,"AccPedal"] = driveData[1] 


##brakeContact.far:       8bytes version hex
##                        entries:
##                        8bytes float time
##                        8bytes (hex?) brakestate [0,1]
filename="BrakeContact.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu

initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 16   
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@dd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    df.loc[x,"Brake"] = driveData[1]

##gear.far:               8bytes version hex
##                        entries:
##                        8bytes float time
##                        8bytes hex gear number - nejake cudne treba odpocitat 4
filename="Gear.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu

initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 16   
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@dd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    df.loc[x,"Gear"] = driveData[1]-4

##acceleration.far:       8bytes version hex
##                        entries:
##                        8bytes float time
##                        8bytes float acceleration ?
filename="AccelerationLateral.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu

initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 16   
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@dd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    df.loc[x,"gLat"] = gLatSign * driveData[1]

filename="AccelerationLongitudinal.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu

initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 16   
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@dd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    df.loc[x,"gLong"] = gLongSign * driveData[1]

fig = px.line(df, x = "LogTime", y = ["RPM","Speed","SpeedSmooth","Gear","AccPedal","Brake","gLat","gLong"], title="Graf 1 - "+adresar); fig.show()

df.to_csv(adresar+"MLapExport1.csv",index=False)

##
##location.far:           8bytes version hex
##                        entries:
##                        8bytes float time
##                        8bytes float latitude
##                        8bytes float longitude

filename="Location.far"
data = open(adresar+filename, "rb").read()
initialData = struct.unpack("@dddd", data[:32])
print(filename)
print(initialData)
StartTime=initialData[1]  # read time prveho zaznamu

dfGPS = pd.DataFrame(columns=['Time','PosLat','PosLong'])

initbytelen=8  # dlzka uvodu vo file - nie su tam data
dataWord = 24   
driveData = [0] * ((len(data) - initbytelen) // dataWord)
print(len(driveData))

for x in range(0, (len(data) - initbytelen) // dataWord):
    driveData = struct.unpack("@ddd", data[(initbytelen + dataWord * x):(initbytelen + dataWord + dataWord * x)])
    dfGPS.loc[x,"Time"] = pd.to_numeric(driveData[0])
    dfGPS.loc[x,"PosLat"] = driveData[1]
    dfGPS.loc[x,"PosLong"] = driveData[2]
##    print(driveData)

dfGPS["Time"]=pd.to_numeric(dfGPS.Time, errors="coerce")  # skontvertuj Time na type float
dfGPS["PosLat"]=pd.to_numeric(dfGPS.PosLat, errors="coerce")
dfGPS["PosLong"]=pd.to_numeric(dfGPS.PosLong, errors="coerce")

dfmerged=pd.merge_ordered(df, dfGPS, on="Time")
##dfmerged.to_csv(adresar+"MLapExport2-GPS-beforeInterpolate.csv",index=False)
dfmerged.interpolate(method='linear', axis=0, limit=20, inplace=True)
##dfmerged.interpolate(method='pad', axis=0, inplace=True)  # methoda "pad" vyplni Nan hodnotou - ale neurobi linear

dfmerged.to_csv(adresar+"MLapExport2-GPS.csv",index=False)
