import numpy as np
import json
import tensorflow as tf
  
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=128, input_shape=(10,),activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))
model.compile(optimizer='adam',loss='categorical_crossentropy' , metrics=['accuracy'])

y_train = []
x_train = []

x_predict = []
y_predict = []


for i in range(11000):
    f = open('podaci_treniranje/' + str(i) + '.json')
    data = json.load(f)
    match = []
    match_blue_win = []
    
    for i in range(10):
        match.append(data["info"]["participants"][i]["championId"])

    if data["info"]["participants"][0]["win"] == True:
        y_train.append([1,0])
    else:
        y_train.append([0,1])
    x_train.append(match)

    f.close()

x_train = np.array(x_train)
y_train = np.array(y_train)


x_predict.append([41,203,4,67,117,516,57,86,498,16])
x_predict = np.array(x_predict)
y_predict.append([0,1])
y_predict = np.array(y_predict)

print(model.summary())

model.fit(x_train, y_train, batch_size=32, epochs=15, validation_split=0.05)
predictions = model.predict(x_predict)

print(predictions)
print(y_predict)

