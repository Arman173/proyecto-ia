# Poke Vs
Este proyecto para la materia IA, su principal objetivo es el poder predecir quien ganará en una batalla pokemon 1 vs 1, cabe aclarar que es una aproximacion tomando en cuenta las caracteristicas del pokemon, en la realidad, esto puede determinarse por la habilidad del entrenador (jugador).


# Helpers

## `type_factor`

Esta función calcula el **factor de tipo** entre dos Pokémon, considerando sus tipos primario y secundario. El factor de tipo se define como la suma de las efectividades ofensivas y defensivas de los tipos de un Pokémon frente a los tipos del otro, y viceversa.

### **Parámetros**
- `types1` (*list[str]*): Una lista con los tipos del primer Pokémon.  
  Ejemplo: `["Fire", "Flying"]`. Si el Pokémon tiene un solo tipo, el segundo tipo debe ser `"None"`.
  
- `types2` (*list[str]*): Una lista con los tipos del segundo Pokémon.  
  Ejemplo: `["Water", "None"]`.

### **Retorno**
- (*float, float*): Dos valores que representan los factores de tipo:
  - `factor1`: El factor de tipo ofensivo/defensivo de `types1` contra `types2`.
  - `factor2`: El factor de tipo ofensivo/defensivo de `types2` contra `types1`.
  - `(-1, -1)`: En el caso que se introduzca algún tipo invalido en `types1` o `types2`.

### **Detalles de implementación**
1. **Efectividad ofensiva y defensiva**:
   - Se utiliza una tabla de tipos (`type_chart`) para determinar la interacción entre cada tipo primario/secundario de ambos Pokémon.
   - Para cada combinación `(i, j)` de tipos de ambos Pokémon, se suman:
     - `type_chart[types1[i]][types2[j]]`: Efectividad del tipo `types1[i]` contra `types2[j]`.
     - `type_chart[types2[i]][types1[j]]`: Efectividad del tipo `types2[i]` contra `types1[j]`.

2. **Cálculo del factor**:
   - `factor1 = af / df`: Relación entre la suma de efectividades ofensivas de `types1` y las defensivas de `types2`.
   - `factor2 = df / af`: Relación inversa.

3. Los tipos `"None"` no afectan los cálculos, ya que tienen un valor de 0 en la tabla de tipos.

### **Ejemplo de uso**
```python
types1 = ["Fire", "Flying"]  # Charizard
types2 = ["Water", "None"]  # Squirtle

factor1, factor2 = type_factor(types1, types2)

print(f"Factor de {types1} contra {types2}: {factor1}")
print(f"Factor de {types2} contra {types1}: {factor2}")
