#INICIO_CODIGO_COMPLETO_DISEÑADOR_CORREGIDO_V4
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, Listbox
import json
import os
import re
from PIL import Image, ImageTk
import itertools

# --- INICIO DE LA CORRECCIÓN DE RUTAS ---
def asset_path(filename):
    """ Obtiene la ruta absoluta a un recurso, manejando ejecución normal y empaquetada (PyInstaller). """
    try:
        # sys._MEIPASS es una carpeta temporal creada por PyInstaller que contiene todos los assets.
        base_path = sys._MEIPASS
    except Exception:
        # Si falla (estamos en modo normal), usamos la ruta del propio script.
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, "assets", filename)
# --- FIN DE LA CORRECCIÓN DE RUTAS ---

# --- Constantes y Helpers ---
PLACEHOLDER_TEXTO_INSTRUCCIONES = "Aquí debe introducir un texto que incluya las instrucciones que crea conveniente que reciba el participante antes del experimento"
CONSENTIMIENTO_TEXTO_DEFECTO = "Se informa al participante de que su participación consistirá en la realización de una prueba de aprendizaje, la cual no tendrá ninguna repercusión negativa sobre su persona. \n El número de ACIERTOS o ERRORES obtenidos no significan ninguna valoración de sus capacidades individuales, dado que ello depende del tipo de prueba y edad del participante, por lo que en base a dichas variables, en algunas pruebas y en algunas etapas se suelen produce muchos errores y en otras pruebas o etapas muy pocos errores.\nLa prueba se realizará de forma individual y los datos recogidos en esta investigación se tratarán de forma colectiva, manteniendo el anonimato en todo momento. \nAdemás, el/la participante estará en su derecho de retirar el consentimiento cuando lo considere conveniente, oponiéndose a la colaboración sin ninguna consecuencia ni justificación necesaria, o dando por finalizada la prueba aunque esta no hubiera concluido."
PLACEHOLDER_TEXTO_CONSENTIMIENTO_VISUAL = "Este es el texto por defecto del consentimiento informado. Puede editarlo si lo desea."

APP_NAME = "DiscondV2"
USER_DOCUMENTS_PATH = os.path.join(os.path.expanduser('~'), 'Documents', APP_NAME)
CARPETA_EXPERIMENTOS = os.path.join(USER_DOCUMENTS_PATH, "experimentos")
CARPETA_BANCO_IMAGENES = os.path.join(USER_DOCUMENTS_PATH, "banco_imagenes")

for path in [USER_DOCUMENTS_PATH, CARPETA_EXPERIMENTOS, CARPETA_BANCO_IMAGENES]:
    os.makedirs(path, exist_ok=True)

class ConfiguracionExperimento:

    def _crear_nueva_secuencia(self):
        """Crea un diccionario con la configuración por defecto para una nueva secuencia."""
        return {
            "n_ensayos": 4,
            "n_repeticiones": 1,
            "orden_aleatorio": False,
            "ruta_imagenes": "",
            "ensayos": [],
            "retro_por_defecto": True,
            "repetir_hasta_acierto_por_defecto": True,
            "criterio_porcentaje_activo": False,
            "criterio_porcentaje_valor": 80,
            "criterio_tipo": "ninguno",
            "criterio_consecutivos_valor": 5,
            "terminar_exp_si_max_reps": False,
        }

    def __init__(self):
        self.nombre_experimento = ""
        self.texto_instrucciones = PLACEHOLDER_TEXTO_INSTRUCCIONES
        self.texto_consentimiento = CONSENTIMIENTO_TEXTO_DEFECTO
        self.n_comparaciones = 2
        self.demora = 0
        self.intervalo_entre_ensayos = 0
        self.tipo_presentacion_demora_cero = "sucesiva"
        self.mostrar_num_ensayo = True
        self.mostrar_countdown = True
        self.secuencias = []
        self.ruta_archivo_actual = None
        self.ventana = tk.Tk()
        self.ventana.title("DiscondV2 - Diseñador de Experimentos - Programa creado por Santiago Benjumea(@PikoyPala)-2025")
        try:
            self.ventana.state('zoomed')
        except tk.TclError:
            self.ventana.attributes("-fullscreen", True)
        self.ventana.configure(bg="black")

        try:
            self.check_on = ImageTk.PhotoImage(Image.open(asset_path("check_on.png")).resize((48, 48)))
            self.check_off = ImageTk.PhotoImage(Image.open(asset_path("check_off.png")).resize((48, 48)))
        except Exception as e:
            messagebox.showerror("Error de Archivo", f"No se pudieron cargar las imágenes de UI.\nError: {e}")
            self.ventana.destroy()
            return

        self.limpiar_referencias_widgets()
        self.current_sequence_idx = 0
        self.ensayo_input_idx = 0
        self.mostrar_opciones_inicio()
        
    # --- El resto de tu código de designer.py no necesita cambios ---
    # (Pega aquí el resto del código desde la función 'limpiar_referencias_widgets' hasta el final)
    def limpiar_referencias_widgets(self):
        self.text_instrucciones_widget = None
        self.text_consentimiento_widget = None
        self.entry_nombre_experimento = None
        self.entry_comparaciones = None
        self.entry_demora = None
        self.entry_intervalo = None
        self.frame_presentacion_demora_cero = None
        self.chk_sucesiva = None
        self.chk_simultanea = None
        self.mostrar_num_ensayo_var = None
        self.mostrar_countdown_var = None
        self.entry_n_ensayos_secuencia = None
        self.entry_n_repeticiones_secuencia = None
        self.orden_aleatorio_secuencia_var = None
        self.retro_por_defecto_var = None
        self.repetir_por_defecto_var = None
        self.label_repeticiones = None
        self.criterio_tipo_var = None
        self.entry_criterio_porcentaje_valor = None
        self.entry_criterio_consecutivos_valor = None
        self.frame_criterio_porcentaje_params = None
        self.frame_criterio_consecutivos_params = None
        self.terminar_exp_var = None
        self.frame_terminar_exp = None
        self.listbox_secuencias = None
        self.label_muestra_img_nombre_widget = None
        self.labels_comparaciones_img_nombres_widgets = []
        self.entry_correcta = None
        self.retro_var = None
        self.repetir_hasta_acierto_var = None
        self.label_status = None

    def limpiar_pantalla(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()
        self.limpiar_referencias_widgets()

    def mostrar_opciones_inicio(self):
        self.secuencias = []
        self.limpiar_pantalla()
        tk.Label(self.ventana, text="¿Qué desea hacer?", font=("Arial", 32), bg="black", fg="white").pack(pady=50)
        tk.Button(self.ventana, text="Crear nuevo experimento", font=("Arial", 24), command=self.pantalla_configuracion_general).pack(pady=10)
        tk.Button(self.ventana, text="Editar experimento existente", font=("Arial", 24), command=self.cargar_experimento_existente).pack(pady=10)

    def cargar_experimento_existente(self):
        nombre_archivo = filedialog.askopenfilename(title="Seleccionar archivo de experimento (.exp)", initialdir=CARPETA_EXPERIMENTOS, filetypes=[("Archivos de experimento", "*.exp")])
        if nombre_archivo:
            try:
                with open(nombre_archivo, 'r', encoding='utf-8') as f:
                    configuracion = json.load(f)
                self.ruta_archivo_actual = nombre_archivo
                self.cargar_configuracion_desde_dict(configuracion)
            except Exception as e:
                messagebox.showerror("Error al Cargar", f"Ocurrió un error al cargar el archivo:\n{e}")
                self.mostrar_opciones_inicio()

    def cargar_configuracion_desde_dict(self, config):
        self.nombre_experimento = config.get("nombre_experimento", "")
        self.texto_instrucciones = config.get("texto_instrucciones", PLACEHOLDER_TEXTO_INSTRUCCIONES)
        self.texto_consentimiento = config.get("texto_consentimiento", CONSENTIMIENTO_TEXTO_DEFECTO)
        self.n_comparaciones = config.get("n_comparaciones", 2)
        self.demora = config.get("demora_muestra_comparacion", 0)
        self.intervalo_entre_ensayos = config.get("intervalo_entre_ensayos", 0)
        self.tipo_presentacion_demora_cero = config.get("tipo_presentacion_demora_cero", "sucesiva")
        self.mostrar_num_ensayo = config.get("mostrar_num_ensayo", True)
        self.mostrar_countdown = config.get("mostrar_countdown", True)
        if "secuencias" in config:
            self.secuencias = config.get("secuencias", [])
            for i in range(len(self.secuencias)):
                plantilla = self._crear_nueva_secuencia()
                for clave, valor_defecto in plantilla.items():
                    if clave not in self.secuencias[i]:
                        self.secuencias[i][clave] = valor_defecto
        else:
            self.secuencias = []
            s1 = self._crear_nueva_secuencia()
            s1.update({k.replace('secuencia1_', '').replace('s1_', ''): v for k, v in config.items() if k.startswith(('secuencia1', 's1'))})
            self.secuencias.append(s1)
            if config.get("secuencia2_activa", False):
                s2 = self._crear_nueva_secuencia()
                s2.update({k.replace('secuencia2_', '').replace('s2_', ''): v for k, v in config.items() if k.startswith(('secuencia2', 's2'))})
                self.secuencias.append(s2)
        self.pantalla_configuracion_general()

    def pantalla_configuracion_general(self):
        self.limpiar_pantalla()
        tk.Label(self.ventana, text="CONFIGURACIÓN GENERAL", font=("Arial", 32, "bold"), bg="black", fg="white").pack(pady=20)
        frame_principal = tk.Frame(self.ventana, bg="black")
        frame_principal.pack(pady=10, padx=20, fill="x")
        self.entry_nombre_experimento = self._crear_entry_con_label(frame_principal, "Nombre del experimento:", self.nombre_experimento)
        frame_texto = tk.Frame(frame_principal, bg="black")
        frame_texto.pack(pady=10, fill=tk.BOTH, expand=True)
        self.text_instrucciones_widget = self._crear_area_texto(frame_texto, "INSTRUCCIONES:", self.texto_instrucciones, PLACEHOLDER_TEXTO_INSTRUCCIONES)
        frame_consentimiento = tk.Frame(frame_texto, bg="black")
        frame_consentimiento.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(frame_consentimiento, text="CONSENTIMIENTO INFORMADO (Editable):", font=("Arial", 22, "bold"), bg="black", fg="white").pack(pady=5)
        self.text_consentimiento_widget = tk.Text(frame_consentimiento, font=("Arial", 18), width=40, height=10, wrap="word", relief="sunken", bd=2, insertbackground="white", bg="gray10", fg="white")
        self.text_consentimiento_widget.insert("1.0", self.texto_consentimiento)
        self.text_consentimiento_widget.pack(pady=5, fill=tk.BOTH, expand=True)
        tk.Label(frame_principal, text="Parámetros del Experimento", font=("Arial", 24, "bold"), bg="black", fg="white").pack(pady=(20, 10))
        self.entry_comparaciones = self._crear_entry_con_label(frame_principal, "Número de comparaciones (2-4):", self.n_comparaciones, 5)
        self.entry_demora = self._crear_entry_con_label(frame_principal, "Demora muestra-comparación (seg, 0-60):", self.demora, 5)
        self.entry_intervalo = self._crear_entry_con_label(frame_principal, "Intervalo entre ensayos (seg, 0-60):", self.intervalo_entre_ensayos, 5)
        self.frame_presentacion_demora_cero = tk.Frame(frame_principal, bg="black")
        self.frame_presentacion_demora_cero.pack(pady=5)
        tk.Label(self.frame_presentacion_demora_cero, text="Presentación (si demora=0):", font=("Arial", 18), bg="black", fg="white").pack(side=tk.LEFT, padx=10)
        self.chk_sucesiva, self.chk_simultanea = self._crear_check_exclusivo(self.frame_presentacion_demora_cero, ["Sucesiva", "Simultánea"], self.tipo_presentacion_demora_cero, lambda val: setattr(self, 'tipo_presentacion_demora_cero', val))
        self.entry_demora.bind("<KeyRelease>", self._actualizar_visibilidad_presentacion)
        self._actualizar_visibilidad_presentacion()
        self.mostrar_num_ensayo_var = self._crear_checkbox(frame_principal, "Mostrar información del ensayo en pantalla", self.mostrar_num_ensayo)
        self.mostrar_countdown_var = self._crear_checkbox(frame_principal, "Mostrar cuenta regresiva en intervalos", self.mostrar_countdown)
        self._crear_botones_navegacion("Atrás: Inicio", self.mostrar_opciones_inicio, "Siguiente: Gestor de Secuencias", self.guardar_general_y_mostrar_gestion_secuencias)

    def pantalla_gestion_secuencias(self):
        self.limpiar_pantalla()
        tk.Label(self.ventana, text="GESTOR DE SECUENCIAS", font=("Arial", 32, "bold"), bg="black", fg="white").pack(pady=20)
        frame_lista = tk.Frame(self.ventana, bg="black")
        frame_lista.pack(pady=10, padx=20)
        tk.Label(frame_lista, text="Secuencias del Experimento:", font=("Arial", 22, "bold"), bg="black", fg="white").pack()
        
        if not self.secuencias:
            tk.Label(frame_lista, text="\nAún no hay secuencias en este experimento.\n\nUtilice el botón 'Añadir Nueva Secuencia' para empezar.",
                     font=("Arial", 18, "italic"), bg="black", fg="gray60").pack(pady=20)
            frame_acciones = tk.Frame(self.ventana, bg="black")
            frame_acciones.pack(pady=10)
            tk.Button(frame_acciones, text="Añadir Nueva Secuencia", font=("Arial", 16), command=self.anadir_secuencia).pack()
        else:
            self.listbox_secuencias = Listbox(frame_lista, font=("Arial", 18), width=95, height=8, bg="gray10", fg="white", selectbackground="#0078D7", exportselection=False)
            for i, seq in enumerate(self.secuencias):
                texto_orden = "Aleatorio" if seq.get("orden_aleatorio", False) else "Lineal"
                
                texto_criterio = ""
                criterio_tipo = seq.get("criterio_tipo", "ninguno")
                if criterio_tipo == "ninguno" and seq.get("criterio_porcentaje_activo", False):
                    criterio_tipo = "porcentaje"

                if criterio_tipo == "porcentaje":
                    texto_criterio = f" (Criterio: {seq.get('criterio_porcentaje_valor', 80)}%)"
                elif criterio_tipo == "consecutivos":
                    texto_criterio = f" (Criterio: {seq.get('criterio_consecutivos_valor', 5)} Consecutivos)"

                retro_defecto = seq.get("retro_por_defecto", True)
                repetir_defecto = seq.get("repetir_hasta_acierto_por_defecto", True)
                texto_retro = "Sí" if retro_defecto else "No"
                texto_repetir = "Sí" if repetir_defecto else "No"
                texto_defectos = f" | Por defecto: Retro. {texto_retro}, Repetir {texto_repetir}"

                texto_final = f"Secuencia {i+1}: {seq['n_ensayos']} ensayos, {seq['n_repeticiones']} reps, Orden: {texto_orden}{texto_criterio}{texto_defectos}"
                
                self.listbox_secuencias.insert(tk.END, texto_final)
            self.listbox_secuencias.pack(pady=10)
            frame_acciones = tk.Frame(self.ventana, bg="black")
            frame_acciones.pack(pady=10)
            tk.Button(frame_acciones, text="Añadir Nueva Secuencia", font=("Arial", 16), command=self.anadir_secuencia).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_acciones, text="Editar Seleccionada", font=("Arial", 16), command=self.editar_secuencia_seleccionada).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_acciones, text="Eliminar Seleccionada", font=("Arial", 16), command=self.eliminar_secuencia_seleccionada).pack(side=tk.LEFT, padx=5)
            
            tk.Button(frame_acciones, text="Subir", font=("Arial", 16), command=self.subir_secuencia_seleccionada).pack(side=tk.LEFT, padx=5)
            tk.Button(frame_acciones, text="Bajar", font=("Arial", 16), command=self.bajar_secuencia_seleccionada).pack(side=tk.LEFT, padx=5)
        
        def ir_a_ensayos():
            if not self.secuencias:
                messagebox.showinfo("Información", "Primero debe añadir y configurar al menos una secuencia.")
                return
            for i in range(len(self.secuencias)): self._ajustar_lista_ensayos(i)
            self.current_sequence_idx = 0; self.ensayo_input_idx = 0
            self.pantalla_configuracion_ensayos()
            
        self._crear_botones_navegacion("Atrás: General", self.pantalla_configuracion_general, "Siguiente: Configurar Ensayos", ir_a_ensayos)

    def anadir_secuencia(self):
        """Añade una secuencia y va directamente al editor."""
        self.secuencias.append(self._crear_nueva_secuencia())
        indice_nueva_secuencia = len(self.secuencias) - 1
        self.pantalla_configuracion_secuencia(indice_nueva_secuencia)

    def editar_secuencia_seleccionada(self):
        if not self.listbox_secuencias: return
        seleccion = self.listbox_secuencias.curselection()
        if not seleccion: messagebox.showwarning("Sin Selección", "Por favor, seleccione una secuencia de la lista para editar."); return
        self.pantalla_configuracion_secuencia(seleccion[0])

    def eliminar_secuencia_seleccionada(self):
        if not self.listbox_secuencias: return
        seleccion = self.listbox_secuencias.curselection()
        if not seleccion: messagebox.showwarning("Sin Selección", "Por favor, seleccione una secuencia de la lista para eliminar."); return
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar la Secuencia {seleccion[0] + 1}?"):
            del self.secuencias[seleccion[0]]
            self.pantalla_gestion_secuencias()

    def subir_secuencia_seleccionada(self):
        """Mueve la secuencia seleccionada una posición hacia arriba."""
        if not self.listbox_secuencias: return
        seleccion = self.listbox_secuencias.curselection()
        if not seleccion:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione una secuencia para mover.")
            return
        
        idx = seleccion[0]
        if idx > 0:
            self.secuencias[idx], self.secuencias[idx-1] = self.secuencias[idx-1], self.secuencias[idx]
            self.pantalla_gestion_secuencias()
            if self.listbox_secuencias:
                self.listbox_secuencias.selection_set(idx - 1)

    def bajar_secuencia_seleccionada(self):
        """Mueve la secuencia seleccionada una posición hacia abajo."""
        if not self.listbox_secuencias: return
        seleccion = self.listbox_secuencias.curselection()
        if not seleccion:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione una secuencia para mover.")
            return

        idx = seleccion[0]
        if idx < len(self.secuencias) - 1:
            self.secuencias[idx], self.secuencias[idx+1] = self.secuencias[idx+1], self.secuencias[idx]
            self.pantalla_gestion_secuencias()
            if self.listbox_secuencias:
                self.listbox_secuencias.selection_set(idx + 1)

    def pantalla_configuracion_secuencia(self, seq_idx):
        self.limpiar_pantalla(); self.current_sequence_idx = seq_idx
        secuencia_actual = self.secuencias[seq_idx]
        tk.Label(self.ventana, text=f"CONFIGURACIÓN DE SECUENCIA {seq_idx + 1}", font=("Arial", 32, "bold"), bg="black", fg="white").pack(pady=20)
        frame = tk.Frame(self.ventana, bg="black"); frame.pack(pady=10, padx=20)
        self.entry_n_ensayos_secuencia = self._crear_entry_con_label(frame, "Número de ensayos (mín. 1):", secuencia_actual["n_ensayos"], 5)
        self.label_repeticiones, self.entry_n_repeticiones_secuencia = self._crear_label_y_entry(frame, "Repeticiones (mín. 1):", secuencia_actual["n_repeticiones"], 5)
        self.orden_aleatorio_secuencia_var = self._crear_checkbox(frame, "Aleatorizar orden de ensayos", secuencia_actual["orden_aleatorio"])
        
        tk.Label(frame, text="Valores por defecto para los ensayos:", font=("Arial", 20, "bold"), bg="black", fg="cyan").pack(pady=(15,5))
        self.retro_por_defecto_var = self._crear_checkbox(frame, "¿Mostrar retroalimentación?", secuencia_actual.get("retro_por_defecto", True))
        self.repetir_por_defecto_var = self._crear_checkbox(frame, "¿Repetir ensayo hasta acertar?", secuencia_actual.get("repetir_hasta_acierto_por_defecto", True))

        tk.Label(frame, text="Criterio de Finalización (Opcional)", font=("Arial", 20, "bold"), bg="black", fg="yellow").pack(pady=(15,5))

        initial_criterio_tipo = secuencia_actual.get("criterio_tipo", "ninguno")
        if initial_criterio_tipo == "ninguno" and secuencia_actual.get("criterio_porcentaje_activo", False):
            initial_criterio_tipo = "porcentaje"

        self.criterio_tipo_var = tk.StringVar(value=initial_criterio_tipo)

        def actualizar_visibilidad_criterios(*args):
            tipo = self.criterio_tipo_var.get()
            if tipo == "porcentaje":
                self.frame_criterio_porcentaje_params.pack(pady=2)
                self.frame_criterio_consecutivos_params.pack_forget()
                self.frame_terminar_exp.pack(pady=5)
            elif tipo == "consecutivos":
                self.frame_criterio_porcentaje_params.pack_forget()
                self.frame_criterio_consecutivos_params.pack(pady=2)
                self.frame_terminar_exp.pack(pady=5)
            else:
                self.frame_criterio_porcentaje_params.pack_forget()
                self.frame_criterio_consecutivos_params.pack_forget()
                self.frame_terminar_exp.pack_forget()
            
            texto = "Máximo de presentaciones (mín. 1):" if tipo != "ninguno" else "Presentaciones de la secuencia (mín. 1):"
            if self.label_repeticiones: self.label_repeticiones.config(text=texto)

        frame_criterio_opciones = tk.Frame(frame, bg="black")
        frame_criterio_opciones.pack(pady=5)

        opciones = [("Ninguno", "ninguno"), ("% de Aciertos", "porcentaje"), ("N Ensayos Consecutivos", "consecutivos")]
        
        for texto, valor in opciones:
            tk.Radiobutton(frame_criterio_opciones, text=texto, variable=self.criterio_tipo_var, value=valor,
                           image=self.check_off, selectimage=self.check_on, compound="left",
                           indicatoron=False, bd=0, activebackground="black", bg="black",
                           font=("Arial", 18), fg="white", selectcolor="black",
                           command=actualizar_visibilidad_criterios).pack(side=tk.LEFT, padx=10)

        self.frame_criterio_porcentaje_params = tk.Frame(frame, bg="black")
        self.entry_criterio_porcentaje_valor = self._crear_entry_con_label(
            self.frame_criterio_porcentaje_params, "Mínimo % de aciertos (0-100):", secuencia_actual.get("criterio_porcentaje_valor", 80), 5)

        self.frame_criterio_consecutivos_params = tk.Frame(frame, bg="black")
        self.entry_criterio_consecutivos_valor = self._crear_entry_con_label(
            self.frame_criterio_consecutivos_params, "Nº de ensayos consecutivos (mín. 1):", secuencia_actual.get("criterio_consecutivos_valor", 5), 5)
        
        self.frame_terminar_exp = tk.Frame(frame, bg="black")
        self.terminar_exp_var = self._crear_checkbox(self.frame_terminar_exp, "Finalizar el experimento si se alcanza el máximo de repeticiones de la secuencia sin cumplir el criterio",
                                                    secuencia_actual.get("terminar_exp_si_max_reps", False))

        actualizar_visibilidad_criterios()

        frame_botones_imagenes = tk.Frame(frame, bg="black")
        frame_botones_imagenes.pack(pady=20)
        tk.Button(frame_botones_imagenes, text="Cargar Imágenes Linealmente...", font=("Arial", 14), command=lambda: self._poblar_imagenes_desde_carpeta(seq_idx)).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones_imagenes, text="Cargar y Generar Permutaciones...", font=("Arial", 14), command=lambda: self._poblar_imagenes_con_permutaciones(seq_idx)).pack(side=tk.LEFT, padx=10)
        def guardar_y_volver():
            if self._guardar_config_secuencia(seq_idx): self.pantalla_gestion_secuencias()
        self._crear_botones_navegacion("Atrás (Sin Guardar)", self.pantalla_gestion_secuencias, "Guardar y Volver al Gestor", guardar_y_volver)

    def guardar_general_y_mostrar_gestion_secuencias(self):
        try:
            nombre = self.entry_nombre_experimento.get().strip()
            if not nombre:
                raise ValueError("El nombre del experimento es obligatorio.")
            self.nombre_experimento = nombre
            self.n_comparaciones = int(self.entry_comparaciones.get())
            self.demora = int(self.entry_demora.get())
            self.intervalo_entre_ensayos = int(self.entry_intervalo.get())
            if not (2 <= self.n_comparaciones <= 4 and 0 <= self.demora <= 60 and 0 <= self.intervalo_entre_ensayos <= 60):
                raise ValueError("Por favor, revise los parámetros.\n\n- Nº de comparaciones debe estar entre 2 y 4.\n- Los tiempos de demora e intervalo deben estar entre 0 y 60 segundos.")
            self.texto_instrucciones = self._get_text_from_widget(self.text_instrucciones_widget, PLACEHOLDER_TEXTO_INSTRUCCIONES, "")
            self.texto_consentimiento = self.text_consentimiento_widget.get("1.0", "end-1c").strip()
            if not self.texto_consentimiento: self.texto_consentimiento = CONSENTIMIENTO_TEXTO_DEFECTO
            self.mostrar_num_ensayo = self.mostrar_num_ensayo_var.get()
            self.mostrar_countdown = self.mostrar_countdown_var.get()
            self.pantalla_gestion_secuencias()
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error de Validación", f"Revisa los datos ingresados:\n\n{e}")
            
    def _guardar_config_secuencia(self, seq_idx):
        try:
            secuencia_actual = self.secuencias[seq_idx]
            n_ensayos = int(self.entry_n_ensayos_secuencia.get())
            n_repeticiones = int(self.entry_n_repeticiones_secuencia.get())
            if not (n_ensayos >= 1 and n_repeticiones >= 1):
                raise ValueError("El número de ensayos y de repeticiones debe ser 1 como mínimo.")
            
            criterio_tipo = self.criterio_tipo_var.get()
            criterio_valor_porcentaje = 80
            criterio_valor_consecutivos = 5

            if criterio_tipo == "porcentaje":
                criterio_valor_porcentaje = float(self.entry_criterio_porcentaje_valor.get())
                if not (0 <= criterio_valor_porcentaje <= 100):
                    raise ValueError("El porcentaje para el criterio de aciertos debe estar entre 0 y 100.")
            elif criterio_tipo == "consecutivos":
                criterio_valor_consecutivos = int(self.entry_criterio_consecutivos_valor.get())
                if not (criterio_valor_consecutivos >= 1):
                     raise ValueError("El número de ensayos consecutivos correctos debe ser 1 como mínimo.")

            secuencia_actual.update({
                "n_ensayos": n_ensayos,
                "n_repeticiones": n_repeticiones,
                "orden_aleatorio": self.orden_aleatorio_secuencia_var.get(),
                "retro_por_defecto": self.retro_por_defecto_var.get(),
                "repetir_hasta_acierto_por_defecto": self.repetir_por_defecto_var.get(),
                "criterio_tipo": criterio_tipo,
                "criterio_porcentaje_valor": criterio_valor_porcentaje,
                "criterio_consecutivos_valor": criterio_valor_consecutivos,
                "criterio_porcentaje_activo": (criterio_tipo == "porcentaje"),
                "terminar_exp_si_max_reps": self.terminar_exp_var.get() if criterio_tipo != "ninguno" else False
            })

            retro_nuevo_defecto = self.retro_por_defecto_var.get()
            repetir_nuevo_defecto = self.repetir_por_defecto_var.get()
            
            if secuencia_actual.get("ensayos"):
                msg = ("¿Desea aplicar estos nuevos valores por defecto ('Retroalimentación' y 'Repetir hasta acierto') "
                       "a todos los ensayos ya existentes en esta secuencia?\n\n"
                       "Atención: Esto sobrescribirá cualquier configuración individual que haya hecho en los ensayos.")
                
                if messagebox.askyesno("Aplicar a Ensayos Existentes", msg):
                    for ensayo in secuencia_actual["ensayos"]:
                        if isinstance(ensayo, dict):
                            ensayo["retro"] = retro_nuevo_defecto
                            ensayo["repetir_hasta_acierto"] = repetir_nuevo_defecto
                    
                    messagebox.showinfo("Actualización Completada",
                                        "Los valores por defecto se han aplicado a todos los ensayos de la secuencia.")

            return True
        except (ValueError, TypeError) as e:
            messagebox.showerror("Error de Validación", f"Revisa los datos de la Secuencia {seq_idx + 1}:\n\n{e}")
            return False
        except AttributeError:
             messagebox.showerror("Error Interno", "No se encontraron referencias a los widgets."); return False
    
    def pantalla_configuracion_ensayos(self):
        self.limpiar_pantalla()
        secuencia_actual = self.secuencias[self.current_sequence_idx]
        total_ensayos_secuencia = secuencia_actual["n_ensayos"]
        tk.Label(self.ventana, text=f"CONFIGURAR ENSAYOS: Secuencia {self.current_sequence_idx + 1}", font=("Arial", 30, "bold"), bg="black", fg="white").pack(pady=(10,5))
        tk.Label(self.ventana, text=f"Ensayo {self.ensayo_input_idx + 1} de {total_ensayos_secuencia}", font=("Arial", 22), bg="black", fg="lightgray").pack(pady=(0,15))
        frame_ensayo = tk.Frame(self.ventana, bg="black", bd=2, relief="ridge", padx=10, pady=10)
        frame_ensayo.pack(pady=10, padx=20, fill="x")
        self.label_muestra_img_nombre_widget, _ = self._crear_selector_imagen(frame_ensayo, "Estímulo Muestra:", "muestra")
        frame_comparaciones = tk.Frame(frame_ensayo, bg="black"); frame_comparaciones.pack(pady=5, fill="x")
        self.labels_comparaciones_img_nombres_widgets = []
        for i in range(self.n_comparaciones):
            lbl, _ = self._crear_selector_imagen(frame_comparaciones, f"Comparación {i + 1}:", "comparacion", i)
            self.labels_comparaciones_img_nombres_widgets.append(lbl)
        frame_final = tk.Frame(frame_ensayo, bg="black"); frame_final.pack(pady=(15, 5), fill="x")
        self.entry_correcta = self._crear_entry_con_label(frame_final, f"Nº Comparación Correcta (1 a {self.n_comparaciones}):", "", 3, side=tk.LEFT)
        
        self.retro_var = self._crear_checkbox(frame_final, "¿Mostrar retroalimentación?", True, side=tk.LEFT, padx=20)
        self.repetir_hasta_acierto_var = self._crear_checkbox(frame_final, "¿Repetir ensayo hasta acertar?", True, side=tk.LEFT, padx=20)
        
        self.label_status = tk.Label(self.ventana, text="", font=("Arial", 16, "bold"), bg="black"); self.label_status.pack(pady=(10, 0))
        
        siguiente_texto, siguiente_cmd = self._determinar_siguiente_accion_ensayos()
        frame_nav_main = tk.Frame(self.ventana, bg="black"); frame_nav_main.pack(pady=20, fill="x")
        frame_nav = tk.Frame(frame_nav_main, bg="black"); frame_nav.pack()
        
        tk.Button(frame_nav, text="Anterior Ensayo", font=("Arial", 18, "bold"), command=self.anterior_ensayo).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_nav, text="Guardar Ensayo Actual", font=("Arial", 18, "bold"), command=self.guardar_ensayo).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_nav, text=siguiente_texto, font=("Arial", 18, "bold"), command=siguiente_cmd).pack(side=tk.LEFT, padx=10)
        
        frame_nav_extra = tk.Frame(self.ventana, bg="black"); frame_nav_extra.pack(pady=10, fill="x")
        frame_sub_extra = tk.Frame(frame_nav_extra, bg="black"); frame_sub_extra.pack()

        tk.Button(frame_sub_extra, text="Volver al Gestor de Secuencias", font=("Arial", 16), command=self.pantalla_gestion_secuencias).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_sub_extra, text="Finalizar y Guardar TODO", font=("Arial", 18, "bold"), bg="forest green", fg="white", command=self.finalizar_configuracion_y_guardar).pack(side=tk.LEFT, padx=10)

        self.cargar_datos_ensayo_actual()

    def _ajustar_lista_ensayos(self, seq_idx):
        lista = self.secuencias[seq_idx]['ensayos']
        num_objetivo = self.secuencias[seq_idx]['n_ensayos']
        diferencia = num_objetivo - len(lista)
        if diferencia > 0: lista.extend([None] * diferencia)
        elif diferencia < 0: self.secuencias[seq_idx]['ensayos'] = lista[:num_objetivo]
    
    def guardar_ensayo(self):
        try:
            is_pristine = (self.current_muestra_img_nombre is None and
                           all(img is None for img in self.current_comparaciones_img_nombres) and
                           self.entry_correcta.get().strip() == "")
            if is_pristine:
                return True

            if not self.current_muestra_img_nombre or None in self.current_comparaciones_img_nombres:
                raise ValueError("Faltan imágenes por seleccionar. Debe especificar una imagen de muestra y una para cada comparación.")

            correcta_str = self.entry_correcta.get().strip()
            if not correcta_str:
                raise ValueError("Debe especificar el número de la comparación correcta.")
            
            correcta_idx = int(correcta_str) - 1
            if not (0 <= correcta_idx < self.n_comparaciones):
                raise ValueError(f"El número de la comparación correcta está fuera del rango permitido (debe ser de 1 a {self.n_comparaciones}).")

            ensayo_data = {
                "muestra_img_nombre": self.current_muestra_img_nombre,
                "comparaciones_img_nombres": self.current_comparaciones_img_nombres,
                "correcta": correcta_idx,
                "retro": self.retro_var.get(),
                "repetir_hasta_acierto": self.repetir_hasta_acierto_var.get()
            }
            
            self.secuencias[self.current_sequence_idx]['ensayos'][self.ensayo_input_idx] = ensayo_data
            if self.label_status:
                self.label_status.config(text=f"Ensayo {self.ensayo_input_idx + 1} guardado con éxito.", fg="green")
                self.ventana.after(2500, lambda: self.label_status.config(text=""))
            return True
        except (ValueError, TypeError, IndexError) as e:
            messagebox.showerror("Error al Guardar Ensayo", str(e)); return False

    def anterior_ensayo(self):
        if self.guardar_ensayo():
            if self.ensayo_input_idx > 0:
                self.ensayo_input_idx -= 1
            elif self.current_sequence_idx > 0:
                self.current_sequence_idx -= 1
                self.ensayo_input_idx = self.secuencias[self.current_sequence_idx]["n_ensayos"] - 1
            else:
                return
            self.pantalla_configuracion_ensayos()

    def siguiente_ensayo(self):
        if self.guardar_ensayo():
            self.ensayo_input_idx += 1
            self.pantalla_configuracion_ensayos()

    def pasar_a_siguiente_secuencia(self):
        if self.guardar_ensayo():
            if self.current_sequence_idx < len(self.secuencias) - 1:
                self.current_sequence_idx += 1
                self.ensayo_input_idx = 0
                self.pantalla_configuracion_ensayos()
            else:
                self.finalizar_configuracion_y_guardar()

    def cargar_datos_ensayo_actual(self):
        secuencia_actual = self.secuencias[self.current_sequence_idx]
        lista_ensayos = secuencia_actual['ensayos']
        ensayo_guardado = lista_ensayos[self.ensayo_input_idx] if 0 <= self.ensayo_input_idx < len(lista_ensayos) else None
        
        self.current_muestra_img_nombre = None
        self.current_comparaciones_img_nombres = [None] * self.n_comparaciones
        self.entry_correcta.delete(0, tk.END)
        
        retro_final = secuencia_actual.get("retro_por_defecto", True)
        repetir_final = secuencia_actual.get("repetir_hasta_acierto_por_defecto", True)

        if isinstance(ensayo_guardado, dict):
            self.current_muestra_img_nombre = ensayo_guardado.get("muestra_img_nombre")
            self.current_comparaciones_img_nombres = ensayo_guardado.get("comparaciones_img_nombres", [None]*self.n_comparaciones)
            correcta_idx = ensayo_guardado.get("correcta")
            if correcta_idx is not None:
                self.entry_correcta.insert(0, str(correcta_idx + 1))
            
            retro_final = ensayo_guardado.get("retro", retro_final)
            repetir_final = ensayo_guardado.get("repetir_hasta_acierto", repetir_final)

        self.retro_var.set(retro_final)
        self.repetir_hasta_acierto_var.set(repetir_final)
        
        self._actualizar_label_imagen(self.label_muestra_img_nombre_widget, self.current_muestra_img_nombre)
        for i, label in enumerate(self.labels_comparaciones_img_nombres_widgets):
            nombre_img = self.current_comparaciones_img_nombres[i] if i < len(self.current_comparaciones_img_nombres) else None
            self._actualizar_label_imagen(label, nombre_img)
            
    def _poblar_imagenes_desde_carpeta(self, seq_idx):
        if not hasattr(self, 'entry_n_ensayos_secuencia') or not self._guardar_config_secuencia(seq_idx): 
            if hasattr(self, 'entry_n_ensayos_secuencia'): return

        carpeta_seleccionada = filedialog.askdirectory(title=f"Seleccione carpeta para Secuencia {seq_idx + 1}", initialdir=CARPETA_BANCO_IMAGENES)
        if not carpeta_seleccionada: return
        try:
            extensiones_validas = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
            archivos = [f for f in os.listdir(carpeta_seleccionada) if f.lower().endswith(extensiones_validas)]
            archivos.sort(key=lambda f: int(re.search(r'\d+', f).group()) if re.search(r'\d+', f) else -1)
            
            secuencia = self.secuencias[seq_idx]
            
            # --- INICIO DE LA CORRECCIÓN ---
            # Se calcula el número de ensayos en función de las imágenes encontradas.
            n_estimulos_por_ensayo = 1 + self.n_comparaciones
            n_ensayos_calculado = len(archivos) // n_estimulos_por_ensayo
            
            if n_ensayos_calculado == 0:
                raise ValueError(f"Imágenes insuficientes. Se encontraron {len(archivos)} imágenes, "
                                 f"pero se necesitan {n_estimulos_por_ensayo} para cada ensayo (1 muestra + {self.n_comparaciones} comparaciones).")

            # Actualizar la configuración de la secuencia con el número de ensayos calculado.
            secuencia['n_ensayos'] = n_ensayos_calculado
            secuencia['ruta_imagenes'] = os.path.basename(carpeta_seleccionada)
            secuencia['ensayos'] = [] # Limpiar la lista de ensayos para reconstruirla.

            img_idx_actual = 0
            for i in range(n_ensayos_calculado):
                ensayo_nuevo = {
                    "muestra_img_nombre": archivos[img_idx_actual],
                    "comparaciones_img_nombres": archivos[img_idx_actual + 1 : img_idx_actual + 1 + self.n_comparaciones],
                    "correcta": None, # El usuario debe definir la correcta después
                    "retro": secuencia.get("retro_por_defecto", True),
                    "repetir_hasta_acierto": secuencia.get("repetir_hasta_acierto_por_defecto", True)
                }
                secuencia['ensayos'].append(ensayo_nuevo)
                img_idx_actual += n_estimulos_por_ensayo

            messagebox.showinfo("Éxito", f"Se han calculado y cargado {n_ensayos_calculado} ensayos para la Secuencia {seq_idx + 1}.")
            # --- FIN DE LA CORRECCIÓN ---

            self.pantalla_gestion_secuencias()
        except Exception as e:
            messagebox.showerror("Error en Carga Automática", f"No se pudo completar la operación.\nError: {e}")

    def _poblar_imagenes_con_permutaciones(self, seq_idx):
        if not hasattr(self, 'entry_n_ensayos_secuencia') or not self._guardar_config_secuencia(seq_idx):
            if hasattr(self, 'entry_n_ensayos_secuencia'): return
            
        carpeta_seleccionada = filedialog.askdirectory(title=f"Seleccione carpeta para generar permutaciones (Secuencia {seq_idx + 1})", initialdir=CARPETA_BANCO_IMAGENES)
        if not carpeta_seleccionada: return
        try:
            extensiones_validas = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
            archivos = [f for f in os.listdir(carpeta_seleccionada) if f.lower().endswith(extensiones_validas)]
            archivos.sort(key=lambda f: int(re.search(r'\d+', f).group()) if re.search(r'\d+', f) else -1)
            
            secuencia = self.secuencias[seq_idx]
            n_comp = self.n_comparaciones
            tamano_bloque = 1 + n_comp
            
            if len(archivos) == 0 or len(archivos) % tamano_bloque != 0:
                raise ValueError(f"El número de imágenes ({len(archivos)}) no es un múltiplo de {tamano_bloque} (1 Muestra + {n_comp} Comparaciones).")
            
            ensayos_generados = []
            num_bloques = len(archivos) // tamano_bloque
            
            for i in range(num_bloques):
                inicio_bloque = i * tamano_bloque
                fin_bloque = inicio_bloque + tamano_bloque
                bloque_actual = archivos[inicio_bloque:fin_bloque]
                muestra_img = bloque_actual[0]
                comparaciones_base = bloque_actual[1:]
                imagen_correcta_original = comparaciones_base[0] # Se asume que la primera comparación del bloque es la correcta
                
                for p in itertools.permutations(comparaciones_base):
                    lista_comparaciones_permutada = list(p)
                    nueva_posicion_correcta = lista_comparaciones_permutada.index(imagen_correcta_original)
                    ensayo = {
                        "muestra_img_nombre": muestra_img,
                        "comparaciones_img_nombres": lista_comparaciones_permutada,
                        "correcta": nueva_posicion_correcta,
                        "retro": secuencia.get("retro_por_defecto", True),
                        "repetir_hasta_acierto": secuencia.get("repetir_hasta_acierto_por_defecto", True)
                    }
                    ensayos_generados.append(ensayo)

            # Actualiza la secuencia con los ensayos generados y el nuevo recuento
            secuencia['ruta_imagenes'] = os.path.basename(carpeta_seleccionada)
            secuencia['ensayos'] = ensayos_generados
            secuencia['n_ensayos'] = len(ensayos_generados)
            
            messagebox.showinfo("Éxito", f"Se han generado {len(ensayos_generados)} ensayos a partir de {num_bloques} bloques de imágenes.")
            self.pantalla_gestion_secuencias()
        except Exception as e:
            messagebox.showerror("Error en Generación Automática", f"No se pudo completar la operación.\nError: {e}")

    def finalizar_configuracion_y_guardar(self):
        if hasattr(self, 'entry_correcta') and self.entry_correcta:
            if not self.guardar_ensayo(): return

        for i, secuencia in enumerate(self.secuencias):
            if not secuencia.get("ensayos") or None in secuencia['ensayos']:
                 messagebox.showerror("Error Final", f"No se puede guardar. La Secuencia {i+1} tiene ensayos incompletos.\n\nPor favor, vaya a 'Configurar Ensayos' y complete la información para cada uno de los {secuencia['n_ensayos']} ensayos programados."); return
            for j, ensayo in enumerate(secuencia["ensayos"]):
                if not isinstance(ensayo, dict) or ensayo.get("correcta") is None:
                    messagebox.showerror("Error Final", f"No se puede guardar. El ensayo {j+1} de la Secuencia {i+1} está incompleto (falta definir la respuesta correcta)."); return
        
        configuracion = {
            "nombre_experimento": self.nombre_experimento, "texto_instrucciones": self.texto_instrucciones,
            "texto_consentimiento": self.texto_consentimiento, "n_comparaciones": self.n_comparaciones,
            "demora_muestra_comparacion": self.demora, "intervalo_entre_ensayos": self.intervalo_entre_ensayos,
            "tipo_presentacion_demora_cero": self.tipo_presentacion_demora_cero, "mostrar_num_ensayo": self.mostrar_num_ensayo,
            "mostrar_countdown": self.mostrar_countdown, "secuencias": self.secuencias
        }
        
        nombre_sugerido_base = "".join(c for c in self.nombre_experimento if c.isalnum() or c in (' ', '_', '-')).replace(' ', '_')
        if not nombre_sugerido_base: nombre_sugerido_base = "experimento_sin_nombre"
        
        nombre_sugerido_final = f"{nombre_sugerido_base}.exp"
        
        nombre_archivo_elegido = filedialog.asksaveasfilename(
            initialdir=CARPETA_EXPERIMENTOS,
            title="Guardar experimento como...",
            initialfile=nombre_sugerido_final,
            defaultextension=".exp",
            filetypes=[("Archivos de experimento", "*.exp"), ("Todos los archivos", "*.*")]
        )

        if not nombre_archivo_elegido:
            return
        try:
            with open(nombre_archivo_elegido, 'w', encoding='utf-8') as f:
                json.dump(configuracion, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Configuración Guardada", f"El experimento se ha guardado con éxito en:\n{nombre_archivo_elegido}")
            self.ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Ocurrió un error al guardar la configuración: {e}")

    def _crear_area_texto(self, frame, titulo, texto_inicial, placeholder):
        sub_frame = tk.Frame(frame, bg="black"); sub_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        tk.Label(sub_frame, text=titulo, font=("Arial", 22, "bold"), bg="black", fg="white").pack(pady=5)
        text_widget = tk.Text(sub_frame, font=("Arial", 18), width=40, height=10, wrap="word", relief="sunken", bd=2, insertbackground="white", bg="gray10", fg="white")
        if texto_inicial == placeholder or not texto_inicial:
            text_widget.insert("1.0", placeholder); text_widget.config(fg="gray60")
        else:
            text_widget.insert("1.0", texto_inicial); text_widget.config(fg="white")
        def on_focus_in(event, widget=text_widget, p_text=placeholder):
            if widget.get("1.0", "end-1c").strip() == p_text: widget.delete("1.0", tk.END); widget.config(fg="white")
        def on_focus_out(event, widget=text_widget, p_text=placeholder):
            if not widget.get("1.0", "end-1c").strip(): widget.insert("1.0", p_text); widget.config(fg="gray60")
        text_widget.bind("<FocusIn>", on_focus_in); text_widget.bind("<FocusOut>", on_focus_out)
        text_widget.pack(pady=5, fill=tk.BOTH, expand=True); return text_widget
    
    def _crear_entry_con_label(self, frame, texto, valor_inicial, ancho=30, side=tk.TOP):
        container = tk.Frame(frame, bg="black"); container.pack(pady=2, fill="x")
        tk.Label(container, text=texto, font=("Arial", 18), bg="black", fg="white").pack(side=tk.LEFT, padx=10)
        entry = tk.Entry(container, font=("Arial", 18), width=ancho, insertbackground="white", bg="gray20", fg="white", justify="center")
        entry.pack(side=tk.LEFT, padx=10); entry.insert(0, str(valor_inicial)); return entry
    
    def _crear_label_y_entry(self, frame, texto, valor_inicial, ancho=30):
        container = tk.Frame(frame, bg="black"); container.pack(pady=2, fill="x")
        label = tk.Label(container, text=texto, font=("Arial", 18), bg="black", fg="white"); label.pack(side=tk.LEFT, padx=10)
        entry = tk.Entry(container, font=("Arial", 18), width=ancho, insertbackground="white", bg="gray20", fg="white", justify="center")
        entry.pack(side=tk.LEFT, padx=10); entry.insert(0, str(valor_inicial)); return label, entry

    def _crear_checkbox(self, frame, texto, valor_inicial, command=None, side=tk.TOP, padx=0):
        var = tk.BooleanVar(value=valor_inicial)
        container = tk.Frame(frame, bg="black"); container.pack(pady=2, side=side, padx=padx)
        chk = tk.Checkbutton(container, variable=var, image=self.check_off, selectimage=self.check_on, compound="left", indicatoron=False, bd=0, activebackground="black", bg="black", command=command)
        chk.pack(side=tk.LEFT); tk.Label(container, text=texto, font=("Arial", 18), bg="black", fg="white").pack(side=tk.LEFT, padx=5); return var

    def _crear_check_exclusivo(self, frame, opciones, valor_inicial, command):
        var = tk.StringVar(value=valor_inicial); checks = []
        for opcion in opciones:
            chk = tk.Radiobutton(frame, text=opcion, variable=var, value=opcion.lower(), image=self.check_off, selectimage=self.check_on, compound="left", indicatoron=False, bd=0, activebackground="black", bg="black", font=("Arial", 18), fg="white", selectcolor="black", command=lambda v=var: command(v.get()))
            chk.pack(side=tk.LEFT, padx=5); checks.append(chk)
        return checks

    def _crear_botones_navegacion(self, texto_atras, cmd_atras, texto_siguiente, cmd_siguiente, return_frame=False):
        frame = tk.Frame(self.ventana, bg="black"); frame.pack(pady=20, fill="x")
        sub_frame = tk.Frame(frame, bg="black"); sub_frame.pack()
        tk.Button(sub_frame, text=texto_atras, font=("Arial", 18, "bold"), command=cmd_atras).pack(side=tk.LEFT, padx=10)
        tk.Button(sub_frame, text=texto_siguiente, font=("Arial", 18, "bold"), command=cmd_siguiente).pack(side=tk.LEFT, padx=10)
        if return_frame: return sub_frame

    def _crear_selector_imagen(self, frame_padre, etiqueta_texto, tipo_estimulo, index_comparacion=None):
        frame_selector = tk.Frame(frame_padre, bg="black"); frame_selector.pack(pady=3, fill=tk.X)
        frame_selector.columnconfigure(1, weight=1)
        tk.Label(frame_selector, text=etiqueta_texto, font=("Arial", 18), bg="black", fg="white").grid(row=0, column=0, padx=10, sticky="w")
        nombre_archivo_label = tk.Label(frame_selector, text="Ninguna imagen seleccionada", font=("Arial", 14, "italic"), bg="gray10", fg="gray60", relief="sunken", bd=1, padx=3)
        nombre_archivo_label.grid(row=0, column=1, padx=5, sticky="ew")
        comando_boton = lambda t=tipo_estimulo, i=index_comparacion, lbl=nombre_archivo_label: self._seleccionar_archivo_imagen_para_ensayo(t, i, lbl)
        btn_seleccionar = tk.Button(frame_selector, text="Seleccionar...", font=("Arial", 14), command=comando_boton)
        btn_seleccionar.grid(row=0, column=2, padx=5, sticky="e"); return nombre_archivo_label, btn_seleccionar

    def _seleccionar_archivo_imagen_para_ensayo(self, tipo_estimulo, index_comparacion, label_widget):
        initial_dir = CARPETA_BANCO_IMAGENES
        try:
            secuencia_actual = self.secuencias[self.current_sequence_idx]
            ruta_guardada = secuencia_actual.get("ruta_imagenes", "")
            if ruta_guardada:
                path_sugerido = os.path.join(CARPETA_BANCO_IMAGENES, ruta_guardada)
                if os.path.isdir(path_sugerido):
                    initial_dir = path_sugerido
        except IndexError:
            pass 

        filepath = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            initialdir=initial_dir,
            filetypes=(("Archivos de Imagen", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos los archivos", "*.*"))
        )
        if filepath:
            nombre_archivo = os.path.basename(filepath)
            
            try:
                directorio_completo = os.path.dirname(filepath)
                
                if CARPETA_BANCO_IMAGENES in directorio_completo:
                    ruta_relativa = os.path.relpath(directorio_completo, CARPETA_BANCO_IMAGENES)
                    
                    if ruta_relativa == ".":
                        ruta_relativa = ""
                        
                    secuencia_actual = self.secuencias[self.current_sequence_idx]
                    secuencia_actual["ruta_imagenes"] = ruta_relativa
            except Exception as e:
                print(f"No se pudo determinar la ruta relativa de la imagen: {e}")

            if tipo_estimulo == "muestra":
                self.current_muestra_img_nombre = nombre_archivo
            elif index_comparacion is not None:
                if len(self.current_comparaciones_img_nombres) != self.n_comparaciones:
                    self.current_comparaciones_img_nombres = [None] * self.n_comparaciones
                self.current_comparaciones_img_nombres[index_comparacion] = nombre_archivo
            
            self._actualizar_label_imagen(label_widget, nombre_archivo)

    def _actualizar_label_imagen(self, label_widget, nombre_archivo):
        if label_widget and label_widget.winfo_exists():
            if nombre_archivo: label_widget.config(text=nombre_archivo, fg="lightgreen", font=("Arial", 14, "bold"))
            else: label_widget.config(text="Ninguna imagen seleccionada", fg="gray60", font=("Arial", 14, "italic"))
    
    def _get_text_from_widget(self, widget, placeholder, default_text=None):
        text = widget.get("1.0", "end-1c").strip()
        return default_text if text == placeholder else text if default_text is not None else text

    def _actualizar_visibilidad_presentacion(self, event=None):
        try:
            if int(self.entry_demora.get()) == 0: self.frame_presentacion_demora_cero.pack(pady=5)
            else: self.frame_presentacion_demora_cero.pack_forget()
        except (ValueError, AttributeError):
            if hasattr(self, 'frame_presentacion_demora_cero'): self.frame_presentacion_demora_cero.pack_forget()
    
    def _determinar_siguiente_accion_ensayos(self):
        secuencia_actual = self.secuencias[self.current_sequence_idx]
        total_ensayos_secuencia_actual = secuencia_actual["n_ensayos"]
        es_ultimo_ensayo = self.ensayo_input_idx >= total_ensayos_secuencia_actual - 1
        es_ultima_secuencia = self.current_sequence_idx >= len(self.secuencias) - 1
        if not es_ultimo_ensayo: return "Siguiente Ensayo", self.siguiente_ensayo
        elif not es_ultima_secuencia: return f"Ir a Secuencia {self.current_sequence_idx + 2}", self.pasar_a_siguiente_secuencia
        else: return "Finalizar y Guardar", self.finalizar_configuracion_y_guardar

if __name__ == "__main__":
    app_configuracion = ConfiguracionExperimento()
    app_configuracion.ventana.mainloop()