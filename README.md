# DISCOND
Software para el diseño y ejecución de experimentos de Igualación a la Muestra en Psicología Experimental.

                                                                       
  ## MANUAL DE USUARIO: SISTEMA DE EXPERIMENTACIÓN DISCOND   
                                                                             


### INTRODUCCIÓN

**DISCOND** es un programa creado por el Dr. Santiago Benjumea Rodríguez (@pikoypala) profesor jubilado del Departamento de Psicología Experimental de la Universidad de Sevilla (España), que permite a investigadores y educadores diseñar y ejecutar experimentos de Psicología del Aprendizaje basados en el procedimiento de **Igualación a la Muestra**.

En cada ensayo de este procedimiento, se presenta en la parte superior de la pantalla un estímulo de **muestra**, seguido por varios estímulos de **comparación** en la parte inferior. El participante debe elegir la comparación que se corresponde con la muestra según una regla predefinida. El sistema puede proporcionar retroalimentación sobre si la elección fue correcta o incorrecta. Esta versión utiliza imágenes como estímulos, que pueden ser creadas con cualquier software de presentaciones que pueda guardar las diaposivas como imágenes (Programa recomendado: Microsoft PowerPoint).

El programa es ideal para investigar temas como:
- Discriminaciones condicionales y clases de equivalencia.
- Marcos relacionales (RFT).
- Creación de materiales de enseñanza programada.
- Evaluaciones con opciones de respuesta múltiple (de 2 a 4 opciones).

Si no tiene experiencia en el uso de este tipo de programas le recomendamos que visite el Manual Interactivo (primer botón de la pantalla principal) y/o vea el Videotutorial (enlace superior de la pantalla principal)

DISCONDV2 se compone de dos aplicaciones principales:

1.  **Diseñador de Experimentos**: Herramienta para crear desde cero o modificar experimentos. Define todos los parámetros, secuencias y ensayos, y los guarda en un único archivo con extensión `.exp`.
2.  **Ejecutor de Experimentos**: Herramienta que carga un archivo `.exp`, registra los datos de un participante y ejecuta el experimento, guardando los resultados detallados en un archivo Excel (`.xlsx`).

    
## PARTE 1: DISEÑAR UN EXPERIMENTO
#### PANTALLA INICIAL

Al pulsar el botón correspondiente, se inicia la interfaz para construir tu experimento. Verás dos opciones:

* "Crear nuevo experimento": Inicia el proceso de diseño desde cero.
* "Editar experimento existente": Abre un explorador de archivos para que cargues un fichero `.exp` guardado previamente y puedas modificarlo.

***

#### PANTALLA 1: CONFIGURACIÓN GENERAL

Define los parámetros globales que se aplicarán a todo el experimento.

* **NOMBRE DEL EXPERIMENTO**: Un nombre descriptivo y **obligatorio**. Se usará para nombrar el archivo `.exp` y el archivo de resultados.
* **INSTRUCCIONES**: El texto que leerá el participante antes de comenzar.
* **CONSENTIMIENTO INFORMADO**: Un texto legal estándar que puedes adaptar a las necesidades éticas de tu investigación.

##### PARÁMETROS DEL EXPERIMENTO

* **NÚMERO DE COMPARACIONES (2-4)**: Cuántos estímulos de comparación (opciones de respuesta) aparecerán en cada ensayo debajo de la muestra.
* **DEMORA MUESTRA-COMPARACIÓN (seg, 0-60)**: El tiempo en segundos que la pantalla permanecerá en negro entre la desaparición de la muestra y la aparición de las comparaciones.
* **INTERVALO ENTRE ENSAYOS (seg, 0-60)**: El tiempo de pausa entre el final de un ensayo y el comienzo del siguiente.
* **PRESENTACIÓN (si demora=0)**: Solo visible si la demora es 0.
    * **Sucesiva**: Al hacer clic en la muestra, esta desaparece y aparecen las comparaciones.
    * **Simultánea**: Al hacer clic en la muestra, las comparaciones aparecen debajo y la muestra permanece visible.
* **CHECKBOX "Mostrar información del ensayo"**: Si se marca esta opción, al ejecutarse el experimento en cada ensayo se mostrará en la parte superior de la pantalla el número de secuencia, el número de repeticiones de ésta y el número de ensayo actual. Útil para depurar.Debería inhabilitarse al correr el experimento con participantes reales.
* **CHECKBOX "Mostrar cuenta regresiva en intervalos"**: Si el intervalo es mayor que 0, muestra un contador numérico descendente. Si no se marca, solo se ve el mensaje "Espere un momento por favor...".

##### BOTONES DE NAVEGÁCION

* "Atrás: Inicio": Vuelve a la pantalla de inicio.
* "Siguiente: Gestor de Secuencias": Guarda esta configuración y avanza a la siguiente pantalla.

***

#### PANTALLA 2: GESTOR DE SECUENCIAS

Esta pantalla es el centro de control de la estructura de tu experimento. Un experimento puede estar formado por múltiples fases o **secuencias** que se ejecutan una tras otra.

* Si no hay secuencias, irás directamente a la página de creación de secuencias.
* Si ya existen, verás una lista con un resumen de cada una.

##### ACCIONES

* **"Añadir Nueva Secuencia"**: Agrega una nueva secuencia vacía y abre directamente su pantalla de configuración.
* **"Editar Seleccionada"**: Abre la pantalla de configuración para la secuencia que hayas seleccionado en la lista.
* **"Eliminar Seleccionada"**: Borra permanentemente la secuencia seleccionada.
* **"Subir"**: Mueve la secuencia seleccionada una posición hacia arriba en el orden de ejecución.
* **"Bajar"**: Mueve la secuencia seleccionada una posición hacia abajo en el orden de ejecución.

##### BOTONES DE NAVEGÁCION

* "Atrás: General": Vuelve a la pantalla de Configuración General.
* "Siguiente: Configurar Ensayos": Te lleva a la pantalla para definir las imágenes de cada ensayo, comenzando por el primer ensayo de la primera secuencia.

***

#### PANTALLA 3: CONFIGURACIÓN DE SECUENCIA

Al añadir o editar una secuencia, accederás a esta pantalla para que definas sus propiedades específicas.

##### PARÁMETROS DE LA SECUENCIA

* **NÚMERO DE ENSAYOS**: El número de ensayos únicos que componen esta secuencia.
* **PRESENTACIONES DE LA SECUENCIA**: Cuántas veces se presentará el bloque completo de ensayos de esta secuencia.
* **CHECKBOX "Aleatorizar orden de ensayos"**: Si se marca, los ensayos de la secuencia se presentarán en orden aleatorio en cada repetición (método de extracción de bolas). Si no, se presentarán en el orden definido.

##### VALORES POR DEFECTO PARA LOS ENSAYOS

* **CHECKBOX "¿Mostrar retroalimentación?"**: Si se marca, todos los ensayos de la secuencia recibirán feedback por defecto.
* **CHECKBOX "¿Repetir ensayo hasta acertar?"**: Si se marca, todos los ensayos de la secuencia se repetirán de inmediato si el participante comete un error.

*Nota: Ambas opciones se pueden modificar posteriormente para cada ensayo de forma individual.*

##### CRITERIO DE FINALIZACIÓN (OPCIONAL)

Permite que una secuencia termine antes de completar todas sus presentaciones si el participante alcanza un criterio de ejecución. Al activar un criterio, el campo "Presentaciones de la secuencia" pasa a llamarse "**Máximo de presentaciones**".

* **Ninguno**: La secuencia se ejecutará el número de veces definido en "Presentaciones de la secuencia".
* **% de Aciertos**: La secuencia se considerará superada si el participante alcanza un porcentaje mínimo de aciertos en una de las repeticiones.
    * **MÍNIMO % DE ACIERTOS**: El porcentaje (ej: 90) que se debe superar para avanzar a la siguiente secuencia.
* **N Ensayos Consecutivos**: La secuencia se considerará superada si el participante acierta un número determinado de ensayos seguidos.
    * **Nº DE ENSAYOS CONSECUTIVOS**: El número de aciertos consecutivos necesarios para superar la secuencia.
* **CHECKBOX "Finalizar el experimento si se alcanza el máximo de repeticiones sin cumplir el criterio"**: Si esta opción está marcada y el participante agota el "Máximo de repeticiones" sin haber superado el criterio, el experimento terminará por completo en ese punto.

##### CARGA AUTOMÁTICA DE IMÁGENES

Estas herramientas automatizan la creación de ensayos, ahorrando una gran cantidad de tiempo.

* **"Cargar Imágenes Linealmente..."**:
    * **Función**: Rellena los ensayos de la secuencia de forma ordenada a partir de una carpeta de imágenes.
    * **Uso**: Seleccionas una carpeta donde las imágenes están organizadas por bloques de `1 Muestra + N Comparaciones`. El programa las asignará en orden estricto.
    * **Requisito**: La carpeta debe contener exactamente `Nº Ensayos * (1 + Nº Comparaciones)` imágenes.
* **"Cargar y Generar Permutaciones..."**:
    * **Función**: Crea automáticamente todos los ensayos posibles a partir de "bloques" de estímulos, permutando la posición de las comparaciones.
    * **Uso**: Creas las diapositivas para un ensayo base por cada muestra. El programa generará todas las variaciones de orden de las comparaciones, ajustando cuál es la respuesta correcta en cada caso.
    * **Requisito**: En tu archivo base, la imagen de la comparación 1 debe ser siempre la correcta.
    * **Requisito**: El número total de imágenes en la carpeta debe ser un múltiplo exacto de `(1 + Nº Comparaciones)`.

##### BOTONES DE NAVEGACIÓN

* "Atrás (Sin Guardar)": Vuelve al Gestor de Secuencias sin guardar los cambios de esta pantalla.
* "Guardar y Volver al Gestor": Valida y guarda los parámetros de la secuencia y regresa al gestor.

***

#### PANTALLA 4: CONFIGURACIÓN DE ENSAYOS

Aquí se define el contenido de cada ensayo de forma individual. Es el paso final y más detallado. Si has usado la carga automática, aquí puedes revisar o modificar ensayos específicos.

* **INDICADOR DE ENSAYO**: En la parte superior verás qué ensayo (`Ensayo X de Y`) de qué secuencia estás editando.

##### DEFINICIÓN DEL ENSAYO

Aqui podrás cambiar para cada ensayo individual las imágenes que cargaste automáticamente (si lo hiciste) así como los valores por defecto que estableciste para todos los ensayos en el editor de secuencias

* **ESTÍMULO MUESTRA**: Haz clic en "Seleccionar..." para elegir la imagen de muestra para este ensayo. Si las imágenes ya fueron cargadas, aparecerá su nombre, pero puedes modificarla.
* **COMPARACIÓN 1, 2, ...**: Selecciona las imágenes para cada una de las opciones de comparación.
* **Nº COMPARACIÓN CORRECTA**: Introduce el número (1, 2, 3 o 4) que corresponde a la comparación correcta. (Este campo vendrá ya relleno si utilizaste el método de carga automática con generación de ensayos por permutación)
* **CHECKBOX "¿Mostrar retroalimentación?"**: Define si para este ensayo específico se dará feedback tras la respuesta.
* **CHECKBOX "¿Repetir ensayo hasta acertar?"**: Si se marca, un error en este ensayo provocará que se vuelva a presentar inmediatamente hasta que el participante acierte.

##### BOTONES DE NAVEGACIÓN Y ACCIÓN

* "Anterior Ensayo": Guarda el ensayo actual y navega al anterior.
* "Guardar Ensayo Actual": Guarda los datos del ensayo en pantalla sin navegar a otro.
* **Botón Dinámico (derecha)**: Su texto y función cambian según el contexto:
    * "Siguiente Ensayo": Guarda el ensayo actual y carga el siguiente de la misma secuencia.
    * "Ir a Secuencia [N]": Si estás en el último ensayo de una secuencia, te lleva al primer ensayo de la siguiente.
    * "Finalizar y Guardar": Si estás en el último ensayo de la última secuencia, finaliza el diseño.
* "Volver al Gestor de Secuencias": Te permite regresar a la vista general de secuencias.
* "Finalizar y Guardar TODO" (Botón Verde): La acción final. Valida que todos los ensayos de todas las secuencias estén completos y te pide guardar el experimento en un archivo `.exp`.


## PARTE 2: EJECUTAR UN EXPERIMENTO 

Esta aplicación carga un archivo `.exp` y lo presenta a un participante.

___________________
PANTALLA DE CARGA

La aplicación se abre en pantalla completa.

* **"Seleccionar Archivo de Experimento"**: Abre el explorador para que elijas el archivo `.exp` que quieres ejecutar.
* **"Salir"**: Cierra el programa.

____________________________________
PANTALLA DE BIENVENIDA Y DATOS

Una vez cargado el archivo, se muestra esta pantalla.

* **CONSENTIMIENTO INFORMADO**: Muestra el texto que definiste en el diseñador.
* **INSTRUCCIONES**: Muestra las instrucciones del experimento que definiste en el diseñador
* **DATOS DEL PARTICIPANTE**: Campos **obligatorios** para Nombre/Código, Edad y Sexo.
* **CHECKBOX DE ACEPTACIÓN**: El participante debe marcar la casilla "Acepto participar en el estudio" para poder continuar.
* **"Iniciar Experimento"**: Este botón solo se activa cuando todos los datos están rellenos y el consentimiento ha sido aceptado.


______________________________________________________________________________________________________
#### ¡ATENCIÓN: Una vez comenzado el experimento sólo se puede salir de él oprimiendo simultáneamente las teclas CTRL + Q!
______________________________________________________________________________________________________

### FLUJO DE EJECUCIÓN DEL EXPERIMENTO
1.  **Presentación de la Muestra**: Aparece la imagen de muestra. El participante hace clic sobre ella.
2.  **Demora (si > 0)**: La pantalla se queda en negro durante el tiempo de demora configurado.
3.  **Presentación de las Comparaciones**: Aparecen las imágenes de comparación.
4.  **Respuesta**: El participante hace clic en una de las comparaciones. El tiempo de reacción (latencia) se mide desde que aparecen hasta que se hace clic.
5.  **Retroalimentación (si está activa)**: Si se configuró, la pantalla se vuelve verde (acierto) o roja (error), acompañada de un sonido.
6.  **Intervalo entre ensayos (si > 0)**: Aparece el mensaje "Espere un momento por favor..." durante el tiempo de intervalo configurado (con o sin cuenta regresiva).
7.  El ciclo se repite para todos los ensayos de todas las secuencias, respetando los criterios de orden (lineal/aleatorio) y finalización.

### FINALIZACIÓN DEL EXPERIMENTO
* Cuando el experimento concluye, aparecerá un mensaje: "Muchas gracias [Nombre del participante] por su participación". Debajo, un botón "Salir".

* ****IMPORTANTE: GUARDADO AUTOMÁTICO DE RESULTADOS**: En este punto, la aplicación automáticamente guardará los resultados en la carpeta de documentos/DiscondV2/resultados.
* **Automáticamente**, el programa genera un archivo Excel en la carpeta `Documentos/DiscondV2/resultados`.
* El nombre del archivo de resultados se compone del nombre del experimento, el nombre del participante y la fecha/hora, garantizando que no se sobrescriba ningún dato.
* El archivo Excel contiene dos hojas:
    * **Resumen**: Con los datos del participante y los porcentajes de acierto por secuencia.
    * **Resultados Detallados**: Un registro completo, ensayo por ensayo, de cada respuesta, su latencia en milisegundos, si fue correcta, etc.
