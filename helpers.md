## Función `type_factor`

### Descripción
Esta función calcula el factor de efectividad entre los tipos de dos Pokémon, basado en un diccionario `type_chart`. El factor de efectividad se utiliza para evaluar cómo un tipo de Pokémon interactúa con otro, por ejemplo, si un Pokémon de tipo Fuego tiene ventaja sobre uno de tipo Planta. El diccionario `type_chart` contiene los valores que determinan qué tan efectivo es un tipo sobre otro.

### Parámetros
- **types1**: Una lista de dos cadenas que representan los tipos del primer Pokémon (ej. `["Fire", "None"]`).
- **types2**: Una lista de dos cadenas que representan los tipos del segundo Pokémon (ej. `["Water", "None"]`).

### Proceso
1. La función verifica que los tipos de ambos Pokémon sean válidos, es decir, que existan en el diccionario `type_chart`. Si alguno de los tipos es inválido, imprime un mensaje de error y retorna `-1, -1`.
   
2. Si los tipos son válidos, la función calcula dos factores de efectividad:
   - **`af`**: Factor de efectividad para el primer Pokémon, que es la suma de la efectividad de los tipos del primer Pokémon sobre los del segundo.
   - **`df`**: Factor de efectividad para el segundo Pokémon, que es la suma de la efectividad de los tipos del segundo Pokémon sobre los del primero.
   
3. Estos factores se utilizan para calcular los dos factores de tipo normalizados:
   - **`factor1`**: El factor de efectividad del primer Pokémon en relación con el segundo.
   - **`factor2`**: El factor de efectividad del segundo Pokémon en relación con el primero.

### Resultado
Devuelve dos valores:
- **`factor1`**: La efectividad del primer Pokémon sobre el segundo.
- **`factor2`**: La efectividad del segundo Pokémon sobre el primero.

### Código

```python
def type_factor(types1, types2):
    if (types1[0] not in type_chart or types1[1] not in type_chart) or (types2[0] not in type_chart or types2[1] not in type_chart):
        print("Error hay un tipo invalido....", types1, types2)
        return -1, -1
    af = 1
    df = 1
    for i in range(2):
        for j in range(2):
            af += type_chart[types1[i]][types2[j]]
            df += type_chart[types2[i]][types1[j]]
    factor1 = af / df
    factor2 = df / af

    return factor1, factor2
```

## Función `normalize_tf`

### Descripción
Esta función calcula la diferencia entre los factores de efectividad de dos Pokémon basándose en sus tipos, utilizando la función `type_factor`. El resultado de la normalización es simplemente la resta de los dos factores calculados.

### Parámetros
- **tp1**: Lista con los tipos del primer Pokémon (ej. `["Fire", "None"]`).
- **tp2**: Lista con los tipos del segundo Pokémon (ej. `["Water", "None"]`).

### Proceso
1. Llama a la función `type_factor` para obtener los dos factores de efectividad (`f1` y `f2`) para los tipos de los dos Pokémon.
2. Retorna la diferencia entre estos dos factores, es decir, `f1 - f2`.

### Resultado
Devuelve la diferencia entre los dos factores de efectividad calculados entre los tipos de los dos Pokémon.

### Código

```python
def normalize_tf(tp1, tp2):
    f1, f2 = type_factor(tp1, tp2)
    return f1 - f2
```

## Función `normalize_columns`

### Descripción
Esta función normaliza las columnas de un DataFrame de `pandas` a un rango definido, como por ejemplo de -10.0 a 10.0. La normalización de datos es importante en el contexto de análisis de datos y machine learning, ya que permite que las variables con diferentes escalas se comporten de manera comparable y puedan ser procesadas de forma eficiente.

### Parámetros
- **df**: `pandas.DataFrame`  
  El DataFrame que contiene los datos que se desean normalizar.

- **columns**: `list`  
  Una lista de los nombres de las columnas que se desean normalizar.

- **min_val** (opcional): `float`, por defecto -10.0  
  El valor mínimo del rango al cual las columnas serán normalizadas.

- **max_val** (opcional): `float`, por defecto 10.0  
  El valor máximo del rango al cual las columnas serán normalizadas.

### Proceso
1. Se crea una copia del DataFrame original para evitar modificar el conjunto de datos original.
2. Para cada columna seleccionada, se calculan el valor mínimo (`col_min`) y el valor máximo (`col_max`) de los datos en esa columna.
3. Cada valor en la columna se transforma para que encaje dentro del rango definido por `min_val` y `max_val` utilizando la siguiente fórmula:
   
   \[
   \text{valor normalizado} = \left(\frac{\text{valor} - \text{mínimo de la columna}}{\text{máximo de la columna} - \text{mínimo de la columna}}\right) \times (\text{max_val} - \text{min_val}) + \text{min_val}
   \]

### Resultado
Devuelve una copia del DataFrame con las columnas especificadas normalizadas dentro del rango proporcionado por `min_val` y `max_val`.

### Código

```python
def normalize_columns(df: pd.DataFrame, columns, min_val=-10.0, max_val=10.0):
    df_normalized = df.copy()  # Crear una copia del DataFrame para no modificar el original

    for col in columns:
        col_min = df[col].min()  # Valor mínimo de la columna
        col_max = df[col].max()  # Valor máximo de la columna
        
        # Normalizar la columna a [min_val, max_val]
        df_normalized[col] = ((df[col] - col_min) / (col_max - col_min)) * (max_val - min_val) + min_val

    return df_normalized
```

## Función `preprocess_pokemon_data`

### Descripción
Esta función realiza una serie de pasos de preprocesamiento sobre un DataFrame que contiene datos de Pokémon. Su objetivo es limpiar y transformar los datos para que sean más adecuados para su análisis o para modelos de machine learning.

### Pasos de Preprocesamiento:
1. **Rellenar valores nulos en la columna 'Type 2'**: Se reemplazan los valores `NaN` con la cadena `'None'`, lo que indica que el Pokémon no tiene un segundo tipo.
2. **Codificar la columna 'Legendary'**: La columna 'Legendary' se convierte a valores binarios (0 o 1), donde `True` se transforma en 1 y `False` en 0.
3. **Eliminar la columna 'Generation'**: Se elimina la columna 'Generation', ya que no se considera relevante para el análisis o el modelo.

### Parámetros
- **pokemon_df**: `pandas.DataFrame`  
  El DataFrame que contiene los datos de los Pokémon, donde cada fila representa un Pokémon y cada columna representa una característica o atributo del mismo.

### Resultado
Devuelve el DataFrame `pokemon_df` después de haber aplicado los cambios mencionados.

### Código

```python
def preprocess_pokemon_data(pokemon_df):
    """
    Preprocesar los datos de Pokémon:
    - Rellenar valores NaN en 'Type 2' con 'None'.
    - Codificar 'Legendary' como binario.
    - Eliminar la columna 'Generation'.
    """
    pokemon_df["Type 2"].fillna("None", inplace=True)
    pokemon_df["Legendary"] = pokemon_df["Legendary"].astype(int)
    pokemon_df.drop(["Generation"], axis=1, inplace=True)
    return pokemon_df
```

## Función `get_pokemon_types`

### Descripción
Esta función permite obtener los tipos de un Pokémon dado su ID único (representado en la columna "#"). La función busca el Pokémon en el DataFrame proporcionado y devuelve sus dos tipos (si tiene ambos). Si el Pokémon no es encontrado, muestra un mensaje de error.

### Parámetros
- **pokemon_df**: `pandas.DataFrame`  
  El DataFrame que contiene los datos de los Pokémon. Se espera que el DataFrame tenga una columna llamada `"#"` que contenga los IDs únicos de los Pokémon, y las columnas `Type 1` y `Type 2` que representan los tipos del Pokémon.
  
- **pokemon_id**: `int`  
  El ID único del Pokémon cuya información de tipo se desea obtener.

### Resultado
Devuelve una tupla con los dos tipos del Pokémon:
- El primer valor de la tupla corresponde al tipo primario (`Type 1`).
- El segundo valor corresponde al tipo secundario (`Type 2`), o `None` si el Pokémon no tiene un segundo tipo.

Si el Pokémon no es encontrado en el DataFrame, imprime un mensaje de error y retorna


## Función `update_winner_column`

### Descripción
Esta función modifica la columna `Winner` de un DataFrame de batallas para asignar un valor de 1 o 0, dependiendo de si el Pokémon ganador corresponde al primer Pokémon en la batalla. Si el primer Pokémon ganó, la columna `Winner` recibe el valor 1, de lo contrario, recibe 0.

### Parámetros
- **battles_df**: `pandas.DataFrame`  
  Un DataFrame que contiene los registros de las batallas entre Pokémon. Se espera que tenga al menos las siguientes columnas:
  - `First_pokemon`: El nombre o ID del primer Pokémon en la batalla.
  - `Winner`: El nombre o ID del Pokémon que ganó la batalla.

### Resultado
La función modifica el DataFrame `battles_df` in-place, actualizando la columna `Winner` para asignar:
- **1** si el Pokémon de la columna `First_pokemon` ganó la batalla.
- **0** si el Pokémon de la columna `First_pokemon` no ganó la batalla.

### Código

```python
def update_winner_column(battles_df):
    """
    Modificar la columna 'Winner' para asignar 1 o 0 según el ganador.
    """
    battles_df["Winner"] = battles_df.apply(lambda row: 1 if row["First_pokemon"] == row["Winner"] else 0, axis=1)
```
