"""
    Neural Network Pokemon Combats
"""
# Bibliotecas a usar
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

# Cargamos nuestros datos
data = pd.read_csv('datasets/combat_train.csv')
# imprimimos nuestros datos
print(data.head())

# Separamos nuestros datos para usarlos en matplotlilb y tensorflow
X = data[["type_factor","HP_diff","Attack_diff","Defense_diff","Sp_Atk_diff","Sp_Def_diff","Speed_diff","Legendary_diff"]].to_numpy()
Y = data["Winner"].to_numpy()

print(X.shape, Y.shape)

# Definimos nuestras capas
capa1 = tf.keras.layers.Dense(units=16, input_shape=[8], kernel_regularizer=tf.keras.regularizers.L2(0.0015))
capa2 = tf.keras.layers.Dense(units=16, activation='tanh', kernel_regularizer=tf.keras.regularizers.L2(0.0015))
capa3 = tf.keras.layers.Dense(units=1, activation='sigmoid')

# Definimos nuestro modelo
modelo = tf.keras.Sequential([
    capa1,
    capa2,
    # tf.keras.layers.Dropout(0.4),
    capa3
])

modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.001735),
    loss='binary_crossentropy'
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,  # Reduce el learning rate a 10%
    patience=100,  # Si no mejora en 100 épocas
    min_lr=1e-8  # Learning rate mínimo
)

# entrenamos nuestro modelo
print('Entrenando el Modelo...')
historial = modelo.fit(X, Y,
                       batch_size=512,
                       epochs=2000,
                       verbose=1,
                       validation_split=0.2,
                       callbacks=[reduce_lr]
                    )
print('Entrenamiento completado.')

print(historial.history.keys())
# Graficar pérdida (loss)
plt.plot(historial.history['loss'], label='Pérdida de entrenamiento')
plt.plot(historial.history['val_loss'], label='Pérdida de validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()
plt.show()