# Lab3-Parte1

Instalar el siguiente archivo: ]
requirements.txt

con el siguiente comando:
```
pip install -r requirements.txt
```
## Flooding:







## Distance Vector:

Cómo ejecutar el programa:
Asegúrate estar en el directorio correcto(DistanceVector) que contiene los siguientes archivos:

main_dv.py
distance_vector.py
topo-default.txt (si es necesario para la configuración)
user_test.txt (si es necesario para la configuración)


Ejecuta el programa principal usando el comando:

```
python main_dv.py
```
Se presentará un menú con las siguientes opciones:

1. Start Chat Session: Si se selecciona esta opción, se le pedirá que ingrese su nombre de usuario (por ejemplo: example@alumchat.xyz) y su contraseña. Una vez proporcionados, se iniciará la sesión de chat.
2. Exit Application: Al seleccionar esta opción, el programa se cerrará.
Siempre sigue las indicaciones en pantalla y asegúrate de ingresar datos válidos cuando se te solicite.


#### Cuando se inicia una sesión de chat

el programa presenta un menú interactivo que permite al usuario realizar diversas acciones relacionadas con la comunicación y la gestión de la red. A continuación, se describen las opciones del menú y cómo funcionan:

* "Actualizar Tabla": -
Al seleccionar esta opción, el programa utiliza el algoritmo de Bellman-Ford para recalcular la tabla de enrutamiento basándose en la topología de la red. La tabla de enrutamiento es esencial para determinar el camino más corto para enviar mensajes a otros nodos en la red. Una vez recalculada, la tabla se comparte con los vecinos, asegurando que todos los nodos de la red tengan información actualizada para el enrutamiento.

* "Mostrar Tabla:" - 
Cuando seleccionas esta opción, el programa te muestra la tabla de enrutamiento actual. Esta tabla proporciona información sobre cómo se enrutarán los mensajes a través de la red, mostrando el próximo salto y el costo asociado para llegar a cada nodo.

* "Enviar Mensaje:" - 
Seleccionar esta opción te permite enviar un mensaje a otro nodo en la red. Debes especificar el nodo destinatario (por ejemplo, A, B, C) y escribir el mensaje que deseas enviar. El programa utiliza la tabla de enrutamiento para determinar el camino más corto y luego envía el mensaje al nodo destinatario a través de ese camino.

* "Salir:" - 
Si eliges esta opción, el programa finalizará la sesión de chat actual y se desconectará de la red. Es importante seleccionar esta opción cuando hayas terminado de interactuar con el programa para cerrar la sesión correctamente y liberar los recursos asociados.

## Link State Routing:

Cómo ejecutar el programa:
Asegúrate estar en el directorio correcto(LinkState) que contiene los siguientes archivos:

main.py
linkstate.py
topo-default.txt (si es necesario para la configuración)
user_test.txt (si es necesario para la configuración)


Ejecuta el programa principal usando el comando:

```
python main.py
```
Se presentará un menú con las siguientes opciones:

1. Start Chat Session: Si se selecciona esta opción, se le pedirá que ingrese su nombre de usuario (por ejemplo: example@alumchat.xyz) y su contraseña. Una vez proporcionados, se iniciará la sesión de chat.
2. Exit Application: Al seleccionar esta opción, el programa se cerrará.
Siempre sigue las indicaciones en pantalla y asegúrate de ingresar datos válidos cuando se te solicite.

#### Cuando se inicia una sesión de chat

el programa presenta un menú interactivo que permite al usuario realizar diversas acciones relacionadas con la comunicación y la gestión de la red. A continuación, se describen las opciones del menú y cómo funcionan:

* "Actualizar Tabla": -
Al seleccionar esta opción, el programa utiliza el algoritmo de Dijkstra para recalcular la tabla de enrutamiento basándose en la topología de la red.
La tabla de enrutamiento es esencial para determinar el camino más corto para enviar mensajes a otros nodos en la red.
Una vez recalculada, la tabla se comparte con los vecinos, asegurando que todos los nodos de la red tengan información actualizada para el enrutamiento.

* "Mostrar Tabla:" - 
Al elegir esta opción, el programa mostrará la tabla de enrutamiento actual al usuario.
Esta tabla proporciona información sobre cómo se enrutarán los mensajes a través de la red, mostrando el próximo salto y el costo asociado para llegar a cada nodo.

* "Enviar Mensaje:" - 
Esta opción permite al usuario enviar un mensaje a otro nodo en la red.
Se le pedirá al usuario que especifique el nodo destinatario (por ejemplo, A, B, C) y que ingrese el mensaje que desea enviar.
El programa utiliza la tabla de enrutamiento para determinar el camino más corto y luego envía el mensaje al nodo destinatario a través de ese camino.

* "Salir:" - 
Al seleccionar esta opción, el programa terminará la sesión de chat actual y se desconectará de la red.
Es importante elegir esta opción cuando el usuario haya terminado de interactuar con el programa para cerrar correctamente la sesión y liberar los recursos asociados.
