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

# Dividimos los datos en entrenamiento y prueba
X_train, X_test = X[:-5000], X[-5000:]  # Últimos 2500 datos como prueba
Y_train, Y_test = Y[:-5000], Y[-5000:]  # Últimos 2500 etiquetas como prueba

print(X.shape, Y.shape)

# Definimos nuestras capas
capa1 = tf.keras.layers.Dense(units=9, input_shape=[8], activation='tanh', kernel_regularizer=tf.keras.regularizers.L2(0.00002307))
capa2 = tf.keras.layers.Dense(units=8, activation='sigmoid')
capa3 = tf.keras.layers.Dense(units=1, activation='sigmoid')

# Definimos nuestro modelo
modelo = tf.keras.Sequential([
    capa1,
    capa2,
    # tf.keras.layers.Dropout(0.4),
    capa3
])

modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.000437),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,  # Reduce el learning rate a 20%
    patience=30,  # Si no mejora en 50 épocas
    min_lr=1e-12  # Learning rate mínimo
)

# Configuración del EarlyStopping desde tf.keras
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',  # Métrica a monitorear (puedes cambiarla por 'val_accuracy')
    patience=300,  # Número de épocas sin mejora antes de detener
    restore_best_weights=True,  # Restaura los pesos de la mejor época
    verbose=1  # Muestra mensajes en la consola
)

# entrenamos nuestro modelo
print('Entrenando el Modelo...')
historial = modelo.fit(X_train, Y_train,
                       batch_size=512,
                       epochs=3000,
                       verbose=1,
                       validation_split=0.2,
                       callbacks=[reduce_lr, early_stopping]
                    )
print('Entrenamiento completado.')

# guardamos el modelo
modelo.save('./models/model.keras')

# Evaluar precisión en datos de prueba
loss, accuracy = modelo.evaluate(X_test, Y_test)
print(f"Precisión del modelo en los datos de prueba: {accuracy:.2f}")
print(X_train.shape, X_test.shape)


print(historial.history.keys())
# Gráfica de pérdida (loss)
plt.figure()
plt.plot(historial.history['loss'], label='Pérdida de entrenamiento')
plt.plot(historial.history['val_loss'], label='Pérdida de validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.title('Pérdida durante el entrenamiento')
plt.legend()
plt.savefig("data/Pérdida durante el entrenamiento.png")
plt.show()

# Gráfica de precisión (accuracy)
plt.figure()
plt.plot(historial.history['accuracy'], label='Precisión de entrenamiento')
plt.plot(historial.history['val_accuracy'], label='Precisión de validación')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.title('Precisión durante el entrenamiento')
plt.legend()
plt.savefig("data/Precisión durante el entrenamiento.png")
plt.show()