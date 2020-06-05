"""
Machine Learning Model
"""

import sys
import io
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer

# function to remove newline from user_input
def rem_newline(content):
    return str(content).replace("\n", " ").replace("\r", "")

# Load data input & transform into array
tFile = {"file":r'dataset.xlsx', "sheet":'DATA', "column":['USER_INPUT', 'YES_NO']}
data = pd.read_excel(tFile['file'], nrows=77000, sheet_name=tFile['sheet'], usecols=tFile['column'])
df = pd.DataFrame(data)
dataset = [rem_newline(_) for _ in df[tFile['column'][0]]]
labelset = [_ for _ in df[tFile['column'][1]]]

# Tokenize USER_INPUT
tokenizer = Tokenizer(num_words=10000, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, oov_token='<OOV>')
tokenizer.fit_on_texts(dataset)

# word_index
#word_index = tokenizer.word_index

# Save to file
"""
with io.open('data_tokenizer.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer.to_json(), ensure_ascii=False))
"""

# Tokenize and add paddings
train_data = tokenizer.texts_to_sequences(dataset)
train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=0, padding="post", maxlen=250)

# Select training set/validation set/test set
x_val = np.asarray(train_data[:35000])
y_val = np.asarray(labelset[:35000])
x_train = np.asarray(train_data[35000:70000])
y_train = np.asarray(labelset[35000:70000])
test_data = np.asarray(train_data[70000:])
test_label = np.asarray(labelset[70000:])

# create model
model = keras.Sequential()
model.add(keras.layers.Embedding(88000, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation="relu"))
model.add(keras.layers.Dense(1, activation="sigmoid"))
model.summary()
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
fitModel = model.fit(x_train, y_train, epochs=40, batch_size=512, validation_data=(x_val, y_val), verbose=1)

# evalute and print results
results = model.evaluate(test_data, test_label)
print(results)

# save model
#model.save("tfmodel.h5")
