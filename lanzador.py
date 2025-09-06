import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image, ImageTk
import subprocess
import os
import webbrowser
import sys

# --- INICIO DE LA CORRECCIÓN ---
# He modificado AMBAS funciones que buscaban rutas para no depender de '__file__'.
# Esto crea un método consistente y debería eliminar el NameError en tu entorno.

# Función robusta para obtener ruta a archivo en la carpeta assets
def asset_path(filename):
    try:
        if hasattr(sys, '_MEIPASS'):
            # Entorno congelado (PyInstaller), esto es correcto
            base_path = sys._MEIPASS
        else:
            # Usamos sys.argv[0] que es más robusto que __file__ en muchos entornos
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        asset_file_path = os.path.join(base_path, "assets", filename)
        print("Intentando cargar asset desde:", asset_file_path) # Para depuración
        return asset_file_path
    except Exception as e:
        print(f"Error crítico al determinar la ruta de los assets: {e}")
        return ""


# Rutas a los scripts (asumiendo que estarán en el mismo directorio que lanzador.py)
def obtener_ruta_base_lanzador():
    try:
        if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
            # Entorno congelado (PyInstaller), la ruta del ejecutable es la correcta aquí
            return os.path.dirname(sys.executable)
        else:
            # Usamos sys.argv[0] consistentemente
            return os.path.dirname(os.path.abspath(sys.argv[0]))
    except Exception as e:
        print(f"Error crítico al determinar la ruta del lanzador: {e}")
        return ""
# --- FIN DE LA CORRECCIÓN ---


# --- CAMBIO 1: Asegurarse de que los nombres apuntan a los scripts .py ---
APP1_NAME = "designer.exe"
APP2_NAME = "presenter.exe"

LANZADOR_BASE_PATH = obtener_ruta_base_lanzador()
# --- CAMBIO 2: Renombrar variables para mayor claridad (de _EXE a _PATH) ---
APP1_PATH = os.path.join(LANZADOR_BASE_PATH, APP1_NAME)
APP2_PATH = os.path.join(LANZADOR_BASE_PATH, APP2_NAME)
#PASO_LANZADOR_1_RUTA_TUTORIAL_INICIO
APP_TUTORIAL_NAME = "tutorial.exe"
APP_TUTORIAL_PATH = os.path.join(LANZADOR_BASE_PATH, APP_TUTORIAL_NAME)
#PASO_LANZADOR_1_RUTA_TUTORIAL_FINAL

LOGO_PATH = asset_path("DISCOND.jpg")
PHOTO_PATH = asset_path("mifoto.png")
LOGO_DERECHO_PATH = asset_path("youtube.jpg")
YOUTUBE_URL = "https://youtu.be/0pCqUXQw-hs" # URL actualizada a un canal real

# Definición de ruta para carpeta de datos
APP_NAME_DATOS = "DiscondV2" # Asegúrate que coincide con el nombre en tus otros scripts
USER_DOCUMENTS_PATH = os.path.join(os.path.expanduser('~'), 'Documents', APP_NAME_DATOS)
CARPETA_RESULTS = os.path.join(USER_DOCUMENTS_PATH, "resultados")

# --- CAMBIO 3: Función de lanzamiento modificada para ejecutar scripts .py ---
def launch_app(app_path):
    """ Lanza un ejecutable asegurando el directorio de trabajo correcto. """
    try:
        # Obtenemos el directorio donde se encuentra el .exe a lanzar
        directorio_de_trabajo = os.path.dirname(app_path)
        # Lanzamos el proceso, especificando su directorio de trabajo (cwd)
        subprocess.Popen([app_path], cwd=directorio_de_trabajo)
    except Exception as e:
        messagebox.showerror("Error al lanzar", f"No se pudo ejecutar el componente:\n{app_path}\n\nAsegúrate de que todos los archivos .exe y carpetas de assets están juntos.\n\nError: {e}")
def open_youtube():
    webbrowser.open(YOUTUBE_URL)

def abrir_carpeta_resultados():
    """Abre la carpeta de resultados en el explorador de archivos."""
    if not os.path.exists(CARPETA_RESULTS):
        try:
            os.makedirs(CARPETA_RESULTS, exist_ok=True)
            messagebox.showinfo("Carpeta Creada", f"Se ha creado la carpeta de resultados en:\n{CARPETA_RESULTS}")
        except OSError as e:
            messagebox.showerror("Error de Directorio", f"No se pudo crear la carpeta de resultados:\n{e}")
            return
            
    try:
        os.startfile(os.path.realpath(CARPETA_RESULTS))
    except AttributeError:
        try:
            if sys.platform == "win32":
                subprocess.Popen(['explorer', os.path.realpath(CARPETA_RESULTS)])
            elif sys.platform == "darwin":
                subprocess.Popen(['open', os.path.realpath(CARPETA_RESULTS)])
            else:
                subprocess.Popen(['xdg-open', os.path.realpath(CARPETA_RESULTS)])
        except Exception as e_sub:
            messagebox.showerror("Error al Abrir Carpeta", f"No se pudo abrir la carpeta de resultados:\n{e_sub}")
    except Exception as e_os:
        messagebox.showerror("Error al Abrir Carpeta", f"No se pudo abrir la carpeta de resultados:\n{e_os}")

def close(event=None):
    root.destroy()

# --- Resto de la UI (sin cambios funcionales, solo se usan las nuevas variables) ---

root = tk.Tk()
root.title("Lanzador Discond")
root.attributes("-fullscreen", True)
root.configure(bg="white")
root.bind("<Escape>", close)

top_frame = tk.Frame(root, bg="white")
middle_frame = tk.Frame(root, bg="white")
bottom_frame = tk.Frame(root, bg="white")

top_frame.pack(side=tk.TOP, fill="x", pady=10)
middle_frame.pack(side=tk.TOP, expand=True, fill="both", padx=20)
bottom_frame.pack(side=tk.BOTTOM, fill="x", pady=20)

top_left = tk.Frame(top_frame, bg="white")
top_center = tk.Frame(top_frame, bg="white")
top_right = tk.Frame(top_frame, bg="white")

top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)
top_frame.columnconfigure(2, weight=1)

top_left.grid(row=0, column=0, sticky="nsew", padx=10)
top_center.grid(row=0, column=1, sticky="nsew", padx=10)
top_right.grid(row=0, column=2, sticky="nsew", padx=10)

if os.path.exists(LOGO_PATH):
    try:
        logo_img_pil = Image.open(LOGO_PATH)
        w, h = logo_img_pil.size
        aspect_ratio = w / h
        new_height = 250
        new_width = int(new_height * aspect_ratio)
        logo_img_resized = logo_img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo_img_resized)
        logo_label = tk.Label(top_left, image=logo, bg="white")
        logo_label.image = logo
        logo_label.pack(expand=True, pady=(10, 0))
        
        # --- MODIFICACIÓN SOLICITADA ---
        # Añadir etiqueta con el email debajo del logo
        email_label = tk.Label(top_left, text="DiscondV2@gmail.com", font=("Helvetica", 18), bg="white")
        email_label.pack(expand=True, pady=(5, 10))
        # --- FIN DE LA MODIFICACIÓN ---

    except Exception as e:
        print(f"Error al cargar LOGO_PATH ({LOGO_PATH}): {e}")

if os.path.exists(LOGO_DERECHO_PATH):
    try:
        logo2_img_pil = Image.open(LOGO_DERECHO_PATH)
        w, h = logo2_img_pil.size
        aspect_ratio = w / h
        new_height = 200
        new_width = int(new_height * aspect_ratio)
        logo2_img_resized = logo2_img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logo2 = ImageTk.PhotoImage(logo2_img_resized)
        logo2_label = tk.Label(top_center, image=logo2, bg="white")
        logo2_label.image = logo2
        logo2_label.pack(pady=(20, 5))
        yt_link = tk.Label(top_center, text="▶ Videotutorial", font=("Helvetica", 20, "underline"), fg="blue", bg="white", cursor="hand2")
        yt_link.pack()
        yt_link.bind("<Button-1>", lambda e: open_youtube())
    except Exception as e:
        print(f"Error al cargar LOGO_DERECHO_PATH ({LOGO_DERECHO_PATH}): {e}")

if os.path.exists(PHOTO_PATH):
    try:
        photo_img_pil = Image.open(PHOTO_PATH)
        w, h = photo_img_pil.size
        aspect_ratio = w / h
        new_height = 250
        new_width = int(new_height * aspect_ratio)
        photo_img_resized = photo_img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(photo_img_resized)
        photo_label = tk.Label(top_right, image=photo, bg="white")
        photo_label.image = photo
        # Se ajusta el pady para reducir el espacio inferior y acercar el texto
        photo_label.pack(expand=True, pady=(10, 0))

        # --- MODIFICACIÓN SOLICITADA ---
        # Añadir etiqueta con el nombre debajo de la foto
        author_label = tk.Label(top_right, text="Dr. Santiago Benjumea (@pikoypala)", font=("Helvetica", 18), bg="white")
        # Se ajusta el pady para reducir el espacio superior y acercarlo a la foto
        author_label.pack(expand=True, pady=(5, 10))
        # --- FIN DE LA MODIFICACIÓN ---

    except Exception as e:
        print(f"Error al cargar PHOTO_PATH ({PHOTO_PATH}): {e}")

instructions_title = tk.Label(middle_frame, text="Para salir pulse la tecla ESC", font=("Helvetica", 20 ), bg="white")
instructions_title.pack(pady=(5, 0))

instructions = scrolledtext.ScrolledText(middle_frame, wrap=tk.WORD, font=("Helvetica", 20), height=10, width=120, bd=5, relief="groove")
instructions_text = """
██████████████████████████████████████████████████████████████████████████████████████████████████████
                                                                       
                                                                                      MANUAL DE USUARIO: SISTEMA DE EXPERIMENTACIÓN DISCONDV2   
                                                                             
██████████████████████████████████████████████████████████████████████████████████████████████████████

## INTRODUCCIÓN

**DISCONDV2** es un programa creado por el Dr. Santiago Benjumea Rodríguez (@pikoypala) profesor jubilado del Departamento de Psicología Experimental de la Universidad de Sevilla (España), que permite a investigadores y educadores diseñar y ejecutar experimentos de Psicología del Aprendizaje basados en el procedimiento de **Igualación a la Muestra**.

En cada ensayo de este procedimiento, se presenta en la parte superior de la pantalla un estímulo de **muestra**, seguido por varios estímulos de **comparación** en la parte inferior. El participante debe elegir la comparación que se corresponde con la muestra según una regla predefinida. El sistema puede proporcionar retroalimentación sobre si la elección fue correcta o incorrecta. Esta versión utiliza imágenes como estímulos, que pueden ser creadas con cualquier software de presentaciones que pueda guardar las diaposivas como imágenes (Programa recomendado: Microsoft PowerPoint).

El programa es ideal para investigar temas como:
- Discriminaciones condicionales y clases de equivalencia.
- Marcos relacionales (RFT).
- Creación de materiales de enseñanza programada.
- Evaluaciones con opciones de respuesta múltiple (de 2 a 4 opciones).

Si no tiene experiencia en el uso de este tipo de programas le recomendamos que visite el Manual Interactivo (primer botón de abajo) y/o vea el Videotutorial (enlace en la parte superior)

DISCONDV2 se compone de dos aplicaciones principales:

1.  **Diseñador de Experimentos**: Herramienta para crear desde cero o modificar experimentos. Define todos los parámetros, secuencias y ensayos, y los guarda en un único archivo con extensión `.exp`.
2.  **Ejecutor de Experimentos**: Herramienta que carga un archivo `.exp`, registra los datos de un participante y ejecuta el experimento, guardando los resultados detallados en un archivo Excel (`.xlsx`).

=========================================================================================================================
                                                                                PARTE 1: DISEÑAR UN EXPERIMENTO 
=========================================================================================================================

#### PANTALLA DE INICIO

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

* Si no hay secuencias, verás un mensaje de ayuda.
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

=========================================================================================================================
                                                                                PARTE 2: EJECUTAR UN EXPERIMENTO 
=========================================================================================================================
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

### FLUJO DE EJECUCIÓN DEL EXPERIMENTO
****ATENCIÓN: Una vez comenzado el experimento sólo se puede salir de él oprimiendo simultáneamente las teclas CTRL + Q

1.  **Presentación de la Muestra**: Aparece la imagen de muestra. El participante hace clic sobre ella.
2.  **Demora (si > 0)**: La pantalla se queda en negro durante el tiempo de demora configurado.
3.  **Presentación de las Comparaciones**: Aparecen las imágenes de comparación.
4.  **Respuesta**: El participante hace clic en una de las comparaciones. El tiempo de reacción (latencia) se mide desde que aparecen hasta que se hace clic.
5.  **Retroalimentación (si está activa)**: Si se configuró, la pantalla se vuelve verde (acierto) o roja (error), acompañada de un sonido.
6.  **Intervalo entre ensayos (si > 0)**: Aparece el mensaje "Espere un momento por favor..." durante el tiempo de intervalo configurado (con o sin cuenta regresiva).
7.  El ciclo se repite para todos los ensayos de todas las secuencias, respetando los criterios de orden (lineal/aleatorio) y finalización.

────────────────────────────
FINALIZACIÓN DEL EXPERIMENTO
────────────────────────────

* Cuando el experimento concluye, aparecerá un mensaje: "Muchas gracias [Nombre del participante] por su participación". Debajo, un botón "Salir".

* **IMPORTANTE: GUARDADO AUTOMÁTICO DE RESULTADOS**: En este punto, la aplicación automáticamente guardará los resultados en la carpeta de documentos/DiscondV2/resultados.
* **Automáticamente**, el programa genera un archivo Excel en la carpeta `Documentos/DiscondV2/resultados`.
* El nombre del archivo de resultados se compone del nombre del experimento, el nombre del participante y la fecha/hora, garantizando que no se sobrescriba ningún dato.
* El archivo Excel contiene dos hojas:
    * **Resumen**: Con los datos del participante y los porcentajes de acierto por secuencia.
    * **Resultados Detallados**: Un registro completo, ensayo por ensayo, de cada respuesta, su latencia en milisegundos, si fue correcta, etc.
"""


instructions.insert(tk.END, instructions_text)
instructions.configure(state='disabled', bg="lightgray", fg="black")
instructions.pack(pady=5, padx=20, fill="both", expand=True)

action_buttons_frame = tk.Frame(bottom_frame, bg="white")
action_buttons_frame.pack(expand=True)

#PASO_LANZADOR_3_CREAR_BOTONES_INICIO
# Estilo común para los botones
button_font = ("Arial", 14, "bold")
button_width = 28  # Ancho ajustado para que quepan 4 botones
button_height = 3
button_pady = 15

# --- BOTÓN 1 (NUEVO): TUTORIAL ---
btn_tutorial = tk.Button(
    action_buttons_frame,
    text="Ver Manual Interactivo",
    font=button_font,
    width=button_width,
    height=button_height,
    command=lambda: launch_app(APP_TUTORIAL_PATH)
)
btn_tutorial.pack(side=tk.LEFT, padx=10, pady=button_pady) # Espaciado ajustado

# --- BOTÓN 2: DISEÑADOR ---
btn1 = tk.Button(
    action_buttons_frame,
    text="Diseñar un Experimento",
    font=button_font,
    width=button_width,
    height=button_height,
    command=lambda: launch_app(APP1_PATH)
)
btn1.pack(side=tk.LEFT, padx=10, pady=button_pady)

# --- BOTÓN 3: EJECUTOR ---
btn2 = tk.Button(
    action_buttons_frame,
    text="Ejecutar un Experimento",
    font=button_font,
    width=button_width,
    height=button_height,
    command=lambda: launch_app(APP2_PATH)
)
btn2.pack(side=tk.LEFT, padx=10, pady=button_pady)

# --- BOTÓN 4: RESULTADOS ---
btn3 = tk.Button(
    action_buttons_frame,
    text="Ver Carpeta de Resultados",
    font=button_font,
    width=button_width,
    height=button_height,
    command=abrir_carpeta_resultados 
)
btn3.pack(side=tk.LEFT, padx=10, pady=button_pady)
#PASO_LANZADOR_3_CREAR_BOTONES_FINAL

root.mainloop()