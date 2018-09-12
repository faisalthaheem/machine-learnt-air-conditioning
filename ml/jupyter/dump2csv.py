import shared
import time

df = shared.getData(90, False)
filename = "data-{}.csv".format(int(time.time()))
print("Dumping frame to ", filename)

df.to_csv(filename)
