[README (1).md](https://github.com/user-attachments/files/27228135/README.1.md)
# ADT Polinomio — INF-220 Estructuras de Datos I

Implementacion de un polinomio como tipo de dato abstracto (ADT) utilizando una lista enlazada en Python. El proyecto incluye una interfaz grafica desarrollada con Kivy que permite cargar, sumar y evaluar polinomios, ademas de visualizar graficamente un polinomio y su derivada.

---

## Estructura del proyecto

```
polinomios ED1/
    main.py
    modelo/
        nodo.py
        polinomio.py
    controlador/
        controladores.py
    vista/
        vista_polinomio.py
```

- **modelo/** contiene la logica del ADT: la clase `NodoTermino` y la clase `Polinomio` con sus operaciones.
- **controlador/** actua como intermediario entre la vista y el modelo.
- **vista/** contiene la interfaz grafica construida con Kivy.
- **main.py** es el punto de entrada de la aplicacion.

---

## Requisitos

- Python 3.10 o superior
- Kivy 2.x
- NumPy

Instalacion de dependencias:

```bash
pip install kivy numpy
```

---

## Como ejecutar

```bash
cd "polinomios ED1"
python main.py
```

---

## Como usar la aplicacion

La interfaz tiene dos pestanas: **Polinomios** y **Derivada (Extra)**.

### Pestana Polinomios

Permite cargar dos polinomios, sumarlos y evaluarlos en un valor de x.

**Formato de entrada:**

Los polinomios se ingresan como pares `coeficiente,exponente` separados por espacios.

```
3,4 2,1 1,0
```

Esto representa el polinomio: 3x^4 + 2x + 1

**Pasos:**

1. Escribe el polinomio P1 en el campo correspondiente y presiona **Cargar P1**.
2. Escribe el polinomio P2 y presiona **Cargar P2**.
3. Presiona **Sumar P1 + P2** para obtener la suma.
4. Escribe un valor de x y presiona **Calcular** para evaluar los polinomios.

Los resultados aparecen en la consola verde en la parte inferior.

### Pestana Derivada (Extra)

Muestra la grafica de P1 y su derivada en el mismo plano cartesiano.

1. Carga P1 desde la pestana Polinomios.
2. Ve a la pestana Derivada (Extra).
3. Presiona **Graficar P1 y su Derivada**.

La linea azul representa P1 y la linea naranja representa su derivada P1'.

---

## Operaciones disponibles

| Operacion | Descripcion |
|-----------|-------------|
| Insertar  | Agrega un termino al polinomio ordenado por exponente descendente |
| Evaluar   | Calcula el valor del polinomio para un x dado |
| Sumar     | Suma dos polinomios combinando terminos con el mismo exponente |
| Derivar   | Calcula la derivada del polinomio aplicando la regla de la potencia |
| Mostrar   | Devuelve una representacion legible del polinomio |

---

## Ejemplo de uso

Entrada:
```
P1: 3,4 2,1 1,0   ->  3x^4 + 2x + 1
P2: 1,4 5,2       ->  x^4 + 5x^2
```

Suma:
```
P1 + P2 = 4x^4 + 5x^2 + 2x + 1
```

Evaluacion en x = 2:
```
P1(2) = 53.000000
P2(2) = 36.000000
Suma(2) = 89.000000
```

---

## Curso

INF-220 Estructuras de Datos I  
Docente: Ing. Juan Carlos Pena
