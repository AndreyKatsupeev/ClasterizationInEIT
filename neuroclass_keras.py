from keras.models import Sequential
from keras.layers import LSTM
from sklearn.cluster import KMeans
from keras.layers import Dense, Embedding, Dropout
from keras.preprocessing import sequence
import numpy as np
fh = open('new/modelheart2.dat', 'r')
heart = fh.readline().split()
countp = [0,0,0]
countm = [0,0,0]
meas = [0,0,0]
prev='n'
for i, item in enumerate(heart):
    heart[i] = float(item)
    if i>0 and heart[i]>heart[i-1]:
         countp[0]+=heart[i]-heart[i-1]
    else:
        if i>0: countm[0]+=heart[i-1]-heart[i]
heart = np.asarray(heart)
heart = heart[:324]
meas[0] = heart.mean()
fh.close()
fl = open('new/modellung2.dat', 'r')
lung = fl.readline().split()
for i, item in enumerate(lung):
    lung[i] = float(item)
    if i > 0 and lung[i] > lung[i - 1]:
        countp[1] += lung[i] - lung[i - 1]
    else:
        if i > 0: countm[1] += lung[i - 1] - lung[i]
lung = np.asarray(lung)
lung = lung[:324]
meas[1] = lung.mean()
fl.close()
nothing = []
for i in range(0,193): nothing.append(0)
nothing = np.asarray(nothing)
X = np.row_stack((heart, lung, nothing))
y = [1,-1,0]
model = Sequential()
model.add(LSTM(400, input_shape=(193,1)))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
X = np.asarray(X)
X = np.expand_dims(X,2)
y = np.asarray(y)
model.fit(X, y, epochs=5)
fe = open('new/modelelem_data2.dat', 'r')
fw = open('result.dat', 'w')
count= [0,0,0]
elel = []
ss=[]
while True:
    el = fe.readline().split()
    if not el: break
    for i, item in enumerate(el):
        el[i] = float(item)
        if i > 0 and el[i] > el[i - 1]:
            countp[2] += el[i] - el[i - 1]
        else:
            if i > 0: countm[2] += el[i - 1] - el[i]
    el = np.asarray(el)
    el = el[:193]
    #el = el[:3]
    ell = []
    ell.append(el)
    ell = np.asarray(ell)
    ell = np.expand_dims(ell, 2)
    s=model.predict(ell)
    ss.append(s[0])
    print(s[0][0])
model = KMeans(n_clusters=3)
ss = np.asarray(ss)
model.fit(ss)
ss = model.predict(ss)
for s in ss:
    fw.write(str(s)+'\n')
    if s>0.34:
        count[0]+=1
        fw.write('1\n')
    elif s<0.31:
        count[1] += 1
        fw.write('-1\n')
    else:
        count[2]+=1
        fw.write('0\n')
fe.close()
fw.close()
print(count)