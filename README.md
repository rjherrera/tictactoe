# Implementaciones

La primera es [minimax](minimax.py). La idea es jugar gato contra un computador que realiza una busqueda MiniMax en cada turno suyo.

El algoritmo MiniMax tiene los siguientes pasos:
1. Construir un árbol con todas las ramificaciones posibles.
2. Otorgar valores a las hojas, o estados terminales, en este caso 0 a los empates, 1 a los triunfos y -1 a las derrotas.
3. Recorrer el árbol creado para otorgarle valores a todos los nodos, hasta llegar al nodo raíz. MiniMax utiliza estas reglas:
    - Si el nodo corresponde a una jugada propia: elige el hijo con un mayor valor.
    - Si el nodo corresponde a una jugada del oponente: elige el hijo con un menor valor.

La intuición es que el algoritmo decide optimizar sus elecciones (máx) asumiendo el peor escenario posible por parte de su oponente (mín).

## Alfa-Beta
La segunda es [minimax con poda alfa-beta](minimax_alpha_beta.py) que realiza lo mismo pero en el tercer paso evita realizar búsquedas sobre ramas en las que sabe que no modifican el máximo o mínimo, manteniendo referencias a valores alfa y beta para ese objetivo.

Con esta poda se realizan aproximadamente un 3.3% de los cálculos que se realizan sin ella en el peor caso. En términos de rendimiento, la evaluación (paso 3) se reduce drásticamente, realizándose en un 10% del tiempo original. Sin embargo, el tiempo de construcción del árbol (paso 1) se mantiene constante.

### Alfa-Beta Optimizado
La tercera implementación es [minimax con poda alfa-beta en tiempo de construcción](minimax_alpha_beta_on_build.py) la cual realiza la construcción del árbol y el cálculo de los valores en la misma pasada, y realizando la poda, realiza los 3 pasos en 1. Con esto, no construye el árbol entero, sino que construye solo aquello que le es útil.


Esta construcción traspasa la mejora de la evaluación a la construcción, por lo que el tiempo se reduce drásticamente. En la poda anterior la reducción del aproximado 96.7% en tiempo de evaluación repercutía en una nula disminución del tiempo de construcción, y del tiempo de evaluación de 0.5 segundos. Ahora, la misma reducción al ser en tiempo de construcción repercute en una disminución de alrededor de 13.1 segundos.

La cantidad de llamadas recursivas para calcular los valores de cada nodo en el peor caso para el algoritmo sin poda es de 549946, lo que se ve reducido drásticamente con la poda a 18297. La diferencia radica en cuando realizarla.

# Comparación

Se realizan 5 muestreos para obtener un promedio del tiempo de ejecución para cada implementación, tabulando la decisión más difícil, que es la de elegir que casilla seleccionar al partir el juego. Las siguientes decisiones, a partir del segundo turno, siempre toman un tiempo despreciable, por lo que el primero y segundo son los únicos casos interesantes.

|Algoritmo|Tiempo en el peor caso (s)|Tiempo en el segundo peor caso (s)
|:-:|:-:|:-:|
|MiniMax|15.718|1.765|
|MiniMax con poda Alpha-Beta|15.284|1.712|
|MiniMax con poda Alpha-Beta optimizado|0.495|0.096|

Se confirma entonces el poder de reducción de la poda cuando es aplicada de forma correcta, y lo eficiente que es. Queda pendiente en adelante mayores optimizaciones para dejar bajo 0.1 segundos la primera decisión.
