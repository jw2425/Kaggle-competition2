import numpy as np
import pandas as pd
import csv

#adjust these parameters to change computation time and accuracy of results
#smaller tolerances shorten computation time but may reduce accuracy
#the initial tolerance has to be more strict to filter out as many of the 600,000 labeled entries as possible
#otherwise computation time explodes
initial_tolerance = 0.004
iteration_tolerance = 0.05


names = [ "step_" + str(n+1) for n in range(1000)]
obs = pd.read_csv('Observations.csv', names=names)
nobs = obs[:6000].copy()
delta_x = 1.4629
delta_y = 1.4499

nm = ['run', 'step', 'x', 'y']
lbl = pd.read_csv('Label.csv', names=nm)
lbl['x'] = lbl['x'] + delta_x
lbl['y'] = lbl['y'] + delta_y
lbl['angle']= lbl.apply(lambda row: np.arctan((row.y) / (row.x)), axis=1)

lbl['step'] =  lbl['step'].astype(int)
lbl['run'] =  lbl['run'].astype(int)

def get_single_prev_angle(i, row):
    c_step = int(row.step) - 1 - i
    if c_step < 1:
        return 0
    else:
        return nobs.iloc[int(row.run-1)]['step_'+str(c_step)]
#add generate the extended label table - takes 30-60min to run
print "Generating angle history columns for label table..."
for i in range(50):
    lbl['prev_angle_'+ str(i)] = lbl.apply(lambda row: get_single_prev_angle(i, row), axis=1)
    print '{}/{} columns generated'.format(i+1,50)

soltable = []
indices = [ x+6000 for x in range(4000)]


# this step is the bulk of computation. Choose a label for each of the 4000 samples by
# picking the known label which has the most similar history of angles as the 1000th angle of each sample
# this step can take a few or more hours increasing on the size of the tolerances
# at 0.02 and 0.001 for iteration and initial tolerance respectively, this takes about 2 hours
print "Generating predictions..."
iters = 0
for i in indices:
    if i % 200 == 0:
        print "Labeled {}/{} points".format(i-indices[0],len(indices)) 
    def filter_by_prev_angle_table(j, row):
        c_step = int(row.step) - 1 - j
        if c_step < 1:
            return False
        else:
            prev_angle = row['prev_angle_'+str(j)]
            return abs(prev_angle - obs.iloc[i][999-j]) < iteration_tolerance
    filtered = lbl.copy()
    filtered = filtered.drop(filtered[abs(obs.iloc[i][999] - filtered['prev_angle_0']) > initial_tolerance].index)
    idx = 0
    while idx < 50:
        filtered['keep'] = filtered.apply(lambda row: filter_by_prev_angle_table(idx, row), axis=1)
        refiltered = filtered[filtered['keep']==True].copy()
        if len(refiltered) == 0:
            break
        idx += 1
        filtered = refiltered
    iters += idx
    soltable.append([i+1,filtered.iloc[0]['x'],filtered.iloc[0]['y']])
print("Predictions completed. Average number of iterations per data point: {}").format(iters / float(len(indices)))
print "Saving predictions..."
predictions = []
predictions.append(['id', 'value'])

for sol in soltable:
    predictions.append([str(sol[0])+"x", '{:.5f}'.format(round( sol[1]-delta_x, 5))])
    predictions.append([str(sol[0])+"y", '{:.5f}'.format(round( sol[2]-delta_y, 5))])

with open("submission.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(predictions)

print "Predictions saved to submission.csv"