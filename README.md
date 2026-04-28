[README.md](https://github.com/user-attachments/files/27152474/README.md)
# ADT Polinomio

## Implementación mediante Lista Enlazada con aplicaciones en Física Relativista

**Autor:** Witczak Sanabria, M. N.  
**Materia:** INF-220 Estructuras de Datos I  
**Docente:** Peña, J. C.  
**Institucion:** Universidad Autonoma Gabriel Rene Moreno  
**Año:** 2026  

---

## Resumen

El presente proyecto implementa el Tipo de Dato Abstracto (ADT) Polinomio utilizando una lista enlazada como estructura de datos principal. Cada nodo de la lista representa un término del polinomio, almacenando su coeficiente y exponente. La implementación se extiende hacia la aproximación de funciones físicas mediante Series de Taylor, con énfasis en el Factor de Lorentz de la relatividad especial de Einstein. El proyecto incluye además un simulador de asignación de memoria que modela la gestión de bloques libres mediante una segunda lista enlazada. La interfaz gráfica fue desarrollada con PyQt6 y matplotlib.

**Palabras clave:** lista enlazada, ADT, polinomio, Series de Taylor, Factor de Lorentz, relatividad especial, simulador de memoria, PyQt6.

---

## 1. Descripción del Proyecto

Este proyecto desarrolla una solución completa para la representación y manipulación de polinomios matemáticos mediante listas enlazadas en Python. La implementación abarca tres módulos principales:

El primer módulo gestiona las operaciones algebraicas fundamentales sobre polinomios, incluyendo inserción de términos, evaluación para un valor dado de x, suma de dos polinomios y cálculo de la derivada. El segundo módulo extiende la representación polinomial para aproximar funciones trascendentes mediante Series de Taylor, con aplicaciones directas en la física relativista. El tercer módulo simula la asignación y liberación de bloques de memoria del sistema operativo mediante una lista enlazada de bloques libres.

---

## 2. Arquitectura del Sistema

El proyecto sigue el patrón de diseño Modelo-Vista-Controlador (MVC), separando la lógica de negocio de la interfaz de usuario.

### 2.1 Modelo

Los archivos de modelo contienen toda la lógica matemática y de datos:

- `nodo.py` — define la clase NodoTermino, unidad atómica de la lista enlazada
- `polinomio.py` — define la clase Polinomio con sus operaciones fundamentales
- `taylor.py` — define la clase TaylorPolinomio, que hereda de Polinomio
- `memoria.py` — define las clases NodoMemoria y SimuladorMemoria

### 2.2 Vista

Los archivos de vista construyen la interfaz gráfica:

- `tab_operaciones.py` — pestaña de operaciones con polinomios
- `tab_taylor.py` — pestaña de Series de Taylor y física relativista
- `tab_memoria.py` — pestaña del simulador de memoria
- `graficas.py` — canvas de matplotlib embebido en PyQt6
- `estilos.py` — definición del tema visual

### 2.3 Controlador

Los métodos de control se encuentran dentro de cada pestaña: `_cargar()`, `_sumar()`, `_derivar()`, `_evaluar()` y `_graficar()`, que coordinan la interacción entre la vista y el modelo.

### 2.4 Punto de entrada

- `main.py` — ensambla las pestañas y lanza la ventana principal

---

## 3. Estructura de Datos

### 3.1 Nodo de la Lista Enlazada

Cada término del polinomio se representa como un nodo con tres atributos: el coeficiente, el exponente y el puntero al siguiente nodo.

```python
class NodoTermino:
    def __init__(self, coef, exp):
        self.coeficiente = coef
        self.exponente   = exp
        self.siguiente   = None
```

### 3.2 Lista Enlazada del Polinomio

La clase Polinomio mantiene un puntero a la cabeza de la lista, que sirve como único punto de entrada a la cadena de nodos. La lista se mantiene ordenada de mayor a menor exponente.

```
cabeza -> [3, x^4] -> [2, x^1] -> [1, x^0] -> None
```

### 3.3 Operaciones del ADT Polinomio

| Operacion | Descripcion | Complejidad |
|-----------|-------------|-------------|
| insertar(coef, exp) | Inserta un termino en orden descendente | O(n) |
| evaluar(x) | Calcula P(x) para un valor dado | O(n) |
| sumar(otro) | Suma dos polinomios | O(n + m) |
| derivar() | Calcula la derivada del polinomio | O(n) |
| mostrar() | Convierte la lista a cadena legible | O(n) |
| puntos(x_min, x_max) | Genera coordenadas para la grafica | O(n * k) |

---

## 4. Series de Taylor y Fisica Relativista

### 4.1 Herencia y Polimorfismo

La clase TaylorPolinomio hereda de Polinomio, reutilizando todas sus operaciones y agregando metodos de clase para la generacion de aproximaciones polinomiales.

### 4.2 Funciones Implementadas

Las siguientes funciones matematicas se aproximan mediante Series de Taylor:

**Funcion seno:**

```
sin(x) = x - x^3/3! + x^5/5! - x^7/7! + ...
```

Aplicaciones: Movimiento Armonico Simple, ondas electromagneticas, interferencia y difraccion.

**Funcion coseno:**

```
cos(x) = 1 - x^2/2! + x^4/4! - x^6/6! + ...
```

Aplicaciones: oscilaciones acopladas, optica ondulatoria, Transformada de Fourier.

**Funcion exponencial:**

```
e^x = 1 + x + x^2/2! + x^3/3! + ...
```

Aplicaciones: decaimiento radiactivo, enfriamiento de Newton, mecanica cuantica.

**Factor de Lorentz:**

```
gamma(beta) = 1 / sqrt(1 - beta^2)
```

Expansion de Taylor:

```
gamma(beta) = 1 + (1/2)beta^2 + (3/8)beta^4 + (5/16)beta^6 + ...
```

donde beta = v/c representa la velocidad como fraccion de la velocidad de la luz.

**Energia cinetica relativista:**

```
K / mc^2 = gamma - 1 = (1/2)beta^2 + (3/8)beta^4 + ...
```

### 4.3 Conexion entre Mecanica Clasica y Relatividad Especial

El primer termino no trivial de la expansion del Factor de Lorentz es exactamente la energia cinetica clasica normalizada:

```
(1/2)beta^2 = (1/2)mv^2 / mc^2 = K_clasica / mc^2
```

Esto demuestra que la mecanica newtoniana es la aproximacion de primer orden de la relatividad especial de Einstein. La diferencia entre ambas teorias se hace significativa para velocidades superiores al 10% de la velocidad de la luz (beta > 0.1).

---

## 5. Simulador de Asignacion de Memoria

### 5.1 Estructura

El simulador modela la gestion de memoria libre del sistema operativo mediante una lista enlazada de bloques, ordenada por direccion de memoria:

```
cabeza -> [dir=0, tam=1024] -> None
```

### 5.2 Estrategias de Asignacion

**Primer ajuste:** selecciona el primer bloque libre cuyo tamano sea suficiente para la solicitud. Tiene complejidad O(n) en el peor caso y favorece la velocidad de asignacion.

**Mejor ajuste:** recorre toda la lista y selecciona el bloque libre que deje el menor desperdicio posible. Tiene complejidad O(n) pero reduce la fragmentacion interna.

### 5.3 Fusion de Bloques

Al liberar un bloque, el simulador lo reinserta en la lista libre y ejecuta el algoritmo de fusion, que combina bloques contiguos para evitar la fragmentacion externa:

```
Condicion de contigüedad:
bloque_1.direccion + bloque_1.tamanio == bloque_2.direccion
```

---

## 6. Requisitos del Sistema

### 6.1 Dependencias

- Python 3.10 o superior
- PyQt6
- matplotlib
- numpy

### 6.2 Dependencias adicionales en Linux

```bash
sudo apt install libxcb-cursor0
```

---

## 7. Instalacion y Ejecucion

```bash
# Clonar el repositorio
git clone https://github.com/Wolnas/ADT-POLINOMIOS.git
cd ADT-POLINOMIOS

# Crear entorno virtual
python3 -m venv entorno
source entorno/bin/activate

# Instalar dependencias
pip install PyQt6 matplotlib numpy

# Ejecutar
python main.py
```

---

## 8. Uso del Sistema

### 8.1 Pestaña Operaciones

Los terminos del polinomio se ingresan como pares coeficiente,exponente separados por espacios:

```
3,4 2,1 1,0   representa   3x^4 + 2x + 1
```

### 8.2 Pestaña Taylor y Relatividad

El usuario selecciona la funcion matematica del menu desplegable y ajusta el numero de terminos mediante el control deslizante. La grafica muestra simultaneamente la aproximacion polinomial (linea solida) y la funcion exacta (linea punteada) para comparacion visual del error de aproximacion.

El boton Evaluar calcula y muestra en la consola el valor aproximado por Taylor, el valor exacto y el error absoluto entre ambos.

### 8.3 Pestaña Memoria

El usuario puede solicitar bloques de memoria especificando el nombre del programa y el tamano en bytes, seleccionando la estrategia de asignacion. El mapa visual muestra en tiempo real los bloques libres y ocupados. El boton Ver nodos de P1 muestra como los nodos del polinomio cargado en la pestaña Operaciones se distribuyen en memoria.

---

## 9. Estandares de Codificacion

El codigo sigue la guia de estilo PEP 8 (Van Rossum, Warsaw y Coghlan, 2001):

- Nombres de clases en CamelCase
- Nombres de funciones y variables en snake_case
- Docstrings en todas las clases y metodos publicos
- Maximo 79 caracteres por linea
- Dos lineas en blanco entre definiciones de clases

---

## 10. Referencias

Goodrich, M. T., Tamassia, R. y Goldwasser, M. H. (2013). *Data structures and algorithms in Python*. John Wiley and Sons.

Riverbank Computing Limited. (2023). *PyQt6 reference guide*. https://www.riverbankcomputing.com/static/Docs/PyQt6/

Serway, R. A. y Moses, R. J. (2004). *Modern physics* (3ra ed.). Thomson Brooks/Cole.

Van Rossum, G., Warsaw, B. y Coghlan, N. (2001). *PEP 8: Style guide for Python code*. Python Software Foundation. https://peps.python.org/pep-0008/

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science and Engineering*, 9(3), 90-95. https://doi.org/10.1109/MCSE.2007.55

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van Kerkwijk, M. H., Brett, M., Haldane, A., del Rio, J. F., Wiebe, M., Peterson, P., ... Oliphant, T. E. (2020). Array programming with NumPy. *Nature*, 585, 357-362. https://doi.org/10.1038/s41586-020-2649-2
