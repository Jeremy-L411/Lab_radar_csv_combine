import csv
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import fnmatch
import os

trk_path = 'LBR/SR0028/TRK'
trk_len = len(fnmatch.filter(os.listdir(trk_path), '*.csv'))  # Will be used to control loop

def variables(path):
    """
    Finds Velocity and Distance variable in first record in TRK folder
    the remaining files will be the same unit
    """
    tmp = []
    units_file = os.path.join(path, 'Shot0001 Track.csv')
    with open(units_file, 'r') as e:
        mycsv = csv.reader(e, delimiter=';')
        for line in itertools.islice(mycsv, 6):
            tmp.append(line)
    vel = tmp[5][1]
    distance = tmp[5][2]
    print("Velocity Units: {}, Distance Units {}.".format(vel, distance))
    return vel, distance


cur_vel, cur_dist = variables(trk_path)  #

trk_list = []  # creating variables for DF loop

for i in range(trk_len):
    trk_list.append("shot_" + str(i))

cur_shot = 0  # Looping through the DF variable list
df_list = []  # List to add DF for the plot

for root, dirs, files in os.walk(trk_path, topdown=True):  # make sure in TRK
    for file in files:
        read_file = os.path.join(root, file)

        trk_list[cur_shot] = pd.DataFrame(pd.read_csv(read_file, usecols=[cur_vel, cur_dist], skiprows=5, sep=';'))
        df_list.append(trk_list[cur_shot])

        if cur_shot == trk_len:
            break
        else:
            cur_shot += 1

vel = [cur_vel]
dist = [cur_dist]

for frame in df_list:
    print("frame", frame)
    plt.plot(frame[cur_vel], frame[cur_dist])

plt.show()

# todo Labels
# todo create trend line
# todo create whole function