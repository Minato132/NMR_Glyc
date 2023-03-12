import numpy as np
import pandas as pd
import scipy.optimize as py
import matplotlib.pyplot as plt


#Fit function for T1
def T1(t, a, b, c, d):
	y =  1 - np.exp(-1/b * t + c) + d 
	return y

#Fit function for T2'
def T2p(t, a, b, c, d):
	y = np.exp(-1/b *t + c) + d 
	return y


#Fit function for T2
def T2(t, a, b, c, d):
	y = np.exp(-1/b * t + c) + d
	return y


def parameter_get(ar1, ar2, func, err):
	a, b = py.curve_fit(func, ar1, ar2, sigma = err, method = 'trf')
	return a, b




#_____________________________________________________________________________________________________________________________

#Measurements of T1 for Glycerin

with open('/home/minato132/Documents/Data/glyc/glyc_t1') as file:
	data = pd.read_csv(file)
	data = data.rename(columns = {'Delay time (ms)': 'dtime', 'Max Amp (V)' : 'amp'})
	data.loc[:22, 'amp'] = -1 * data.loc[:22,:'amp']

error = []
for i in data['amp']:
	if i < 0:
		i *= -.1
	else:
		i *= .1
	error.append(i)



def t1_glyc(ar1, ar2, ar3):
	a, b = parameter_get(ar1, ar2, T1, ar3)

	plt.figure()
	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'green', label = 'Error')
	plt.scatter(data['dtime'], data['amp'], marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T1(ar1, *a), color = 'red', label = 'Fitted Curve')
	plt.xlabel('Delay Time (ms)')
	plt.ylabel('Maximum Amplitude (V)')
	plt.title('T1 of Glycerin')
	plt.legend()

	print(*a, f'\n Error of b is {b[1, 1]}')
	plt.show()
	return 0


#print(t1_glyc(data['dtime'], data['amp'], error))



#_________________________________________________________________________________________________________________________________

#Measurements for T2' for Glycerin

with open('/home/minato132/Documents/Data/glyc/glyct2p_ne.csv') as file:
	data = pd.read_csv(file)
	data['CH1'] = pd.to_numeric(data.loc[1:, 'CH1'])

time = []
x = data.iat[0, 2]
i = 0
while i < len(data['X']) - 1:
	time.append(x)
	x += data.iat[0, 3]
	i += 1 

time = pd.Series(time, index = np.arange(1, 1201))

err = []
for i in data['CH1']:
	i *= .1
	err.append(i)

d = {'time' : time, 'amp' : data['CH1'], 'err' : err}

data = pd.DataFrame(d)
data.drop(0, axis = 0, inplace = True)
data = data.loc[data['amp'] > .45]

pd.set_option('display.max_row', None)

data = data.loc[[130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450, 470, 490, 510, 530, 550, 570, 590, 610, 630, 650, 670, 690, 710, 730, 750, 770, 810, 830, 850, 870, 890, 910, 930, 950, 970, 990], :]


def t2p(ar1, ar2, ar3):
	a, b = parameter_get(ar1, ar2, T2p, ar3)
	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'blue', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T2p(ar1, *a), color = 'red', label = 'Fitted Curve')
	plt.xlabel('Time (ms)')
	plt.ylabel('Voltage (V)')
	plt.title("T2' of Glycerin")
	plt.legend()

	print(*a, f'\n Error of b is {b[1,1]}')
	plt.show()
	return 0

data['time'] = data['time'] * 1000

#print(t2p(data['time'], data['amp'], data['err']))






#_________________________________________________________________________________________________________________________________

#Measurement for T2 for Glycerin

with open('/home/minato132/Documents/Data/glyc/glyc_t2') as file:
	data = pd.read_csv(file)
	data.drop(data.loc[:,'Unnamed: 2':],axis = 'columns', inplace = True)
	data = data.rename(columns = {'time (us)':'time'})
	data['time'] = data['time'] / 1000

def t2_glyc(ar1, ar2, ar3):
	a, b = parameter_get(ar1, ar2, T2, ar3)

	plt.errorbar(ar1, ar2, yerr = ar3, fmt = ',', color = 'green', label = 'Error')
	plt.scatter(ar1, ar2, marker = 'x', color = 'purple', label = 'Data')
	plt.plot(ar1, T2(ar1, *a), color = 'red', label = 'Fitted Curve')
	plt.xlabel('Time (ms)')
	plt.ylabel('Voltage (v)')
	plt.title('T2 of Glycerin')
	plt.legend()

	print(*a, f'\n Error of b is {b[1, 1]}')
	plt.show()
	return 0

error = []
for i in data['amp']:
	i *= .1
	error.append(i)



print(t2_glyc(data['time'], data['amp'], error))

