import tensorflow as tf
from tensorflow import keras
import numpy as np

def get_dataset(training=True):
    mnist = keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    if training:
        return (np.array(train_images), np.array(train_labels))
    return (np.array(test_images), np.array(test_labels))

def print_stats(train_images, train_labels):
    first_dimension = len(train_images)
    second_dimension = len(train_images[0])
    third_dimension = len(train_images[0][0])
    print(first_dimension)
    print(str(second_dimension) + "x" + str(third_dimension))
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    i = 0
    for name in class_names:
        num_occurences = 0
        for label in train_labels:
            if label == i:
                num_occurences += 1
        print(str(i) + ". " + name + " - " + str(num_occurences))
        i += 1

def build_model():
    model = keras.Sequential()
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(keras.layers.Dense(64, activation=tf.nn.relu))
    model.add(keras.layers.Dense(10))
    opt = keras.optimizers.Adam(learning_rate=0.001)
    scce = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer=opt, loss=scce, metrics=['accuracy'])
    return model

def train_model(model, train_images, train_labels, T):
    model.fit(train_images, train_labels, epochs=T)

def evaluate_model(model, test_images, test_labels, show_loss=True):
    test_loss, test_accuracy = model.evaluate(test_images, test_labels)
    if show_loss:
        print("Loss: " + str(round(test_loss*10000)/10000))
    print("Accuracy: " + str(round(test_accuracy*100)/100) + "%")

def predict_label(model, test_images, index):
    predictions = model.predict([test_images])
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    for i in range(3):
        maximum = np.argmax(predictions[index])
        print(str(class_names[maximum]) + ": " + str(round(predictions[index][maximum]*10000)/100) + "%")
        predictions[index][maximum] = 0
