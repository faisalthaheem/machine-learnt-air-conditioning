
# coding: utf-8

# In[1]:


import sys
import numpy
import pprint
import time
import os
import h5py
import argparse as argparse
import json


# In[2]:


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.utils import np_utils
from keras import optimizers
from keras.callbacks import History
from sklearn.preprocessing import LabelEncoder
import pandas


# In[3]:


#my code
import shared


# In[4]:


numDays = 90


# In[ ]:


#warning do not execute in jupyter
ap=argparse.ArgumentParser()
ap.add_argument("-d", "--days", default=2,
    help="How many days of data to include in learning")
args = vars(ap.parse_args())
numDays= float(args["days"])


# In[5]:


print("Will be loading data for past {} days.".format(numDays))

df = shared.getData(numDays)
df = df.drop(['temperature'],axis=1)


# In[6]:


pprint.pprint(df.dtypes)
print("There are %d rows in the dataframe" % len(df))
pprint.pprint(df)

pprint.pprint(df.axes)
indexOfState = df.axes[1].tolist().index("state")


# In[7]:


if indexOfState == (len(df.axes[1])-1):
    # the temperature/label column is at the end.. easy
    dataset = df.values[:,0:(indexOfState)].astype(float)
    labels = df.values[:,indexOfState].astype(int)


# In[8]:


#debug print
pprint.pprint(dataset)
pprint.pprint(labels)


# In[9]:


# encode class values as integers
encoder = LabelEncoder()
encoder.fit(labels)
encoded_labels = encoder.transform(labels)
# convert integers to dummy variables (i.e. one hot encoded)
one_hot_labels = np_utils.to_categorical(encoded_labels)


# In[10]:


pprint.pprint(encoded_labels)
pprint.pprint(one_hot_labels)


# In[11]:


if one_hot_labels.shape[1] == 1:
    sys.exit("Cannot run classification on 1 class. Was the A/c state changed? Try including more data..")


# In[12]:


input_dimension = dataset.shape[1]
output_dimension = one_hot_labels.shape[1]
print("input_dimension", input_dimension)
print("output_dimension ", output_dimension)
print("input size", dataset.shape[0])
# define baseline model
def baseline_model():

    model=Sequential()
    model.add(Dense(11,input_dim=input_dimension, activation='relu'))
    model.add(Dense(8,activation='relu'))
    model.add(Dense(1,activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


# In[13]:


model = baseline_model()
history = History()


# In[14]:


model.fit(dataset,encoded_labels, epochs=50, batch_size=3, callbacks=[history])


# In[25]:


final_loss = history.history['loss'][len(history.history['loss'])-1]
if final_loss >  1.0:
    sys.exit("Unsatisfactory loss ( >1.0) found. will not save model.")


# In[26]:


#create new model directory
base_path = "assets/trained-models"
this_model_name = "state-model-%d" % time.time()
#ensure directory exists
this_model_base_path = "%s/%s" % (base_path, this_model_name)
os.makedirs(this_model_base_path)
print("Created path " + this_model_base_path)

this_model_json_path = ("{}/model.json".format(this_model_base_path))
this_model_weights_path = ("{}/model.h5".format(this_model_base_path))
print("Saving model to " + this_model_json_path)
print("Saving weights to " + this_model_weights_path)


# In[27]:


model_json = model.to_json()
with open(this_model_json_path, "w") as json_file:
    json_file.write(model_json)
    json_file.close()
model.save_weights(this_model_weights_path)


# In[28]:


#update the root index with the path to the latest model
model_latest_index = "%s/state.model.index" % base_path
with open(model_latest_index,"w") as model_latest_index_file:
    model_latest_index_file.write(this_model_name)
    model_latest_index_file.close()
    
print("Model successfully saved.")

