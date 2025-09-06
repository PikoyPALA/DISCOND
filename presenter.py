import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import json
import pygame
import random
import pandas as pd
from PIL import Image, ImageTk
import datetime
import time

def asset_path(filename):
    """ Obtiene la ruta absoluta a un recurso de forma robusta,
        funciona para desarrollo y para PyInstaller. """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, "assets", filename)

try:
    pygame.mixer.init()
    SONIDO_CORRECTO = asset_path("correcto.wav")
    SONIDO_INCORRECTO = asset_path("incorrecto.wav")
except Exception as e:
    print(f"Advertencia: No se pudo inicializar pygame.mixer. Error: {e}")
    SONIDO_CORRECTO, SONIDO_INCORRECTO = None, None

APP_NAME = "DiscondV2"
USER_DOCUMENTS_PATH = os.path.join(os.path.expanduser('~'), 'Documents', APP_NAME)
CARPETA_EXPERIMENTOS_PARA_CARGAR = os.path.join(USER_DOCUMENTS_PATH, "experimentos")
CARPETA_BANCO_IMAGENES = os.path.join(USER_DOCUMENTS_PATH, "banco_imagenes")
CARPETA_RESULTS = os.path.join(USER_DOCUMENTS_PATH, "resultados")
os.makedirs(CARPETA_RESULTS, exist_ok=True)

CONSENTIMIENTO_TEXTO_DEFECTO = "Se informa al participante de que su participación consistirá en la realización de una prueba de aprendizaje, la cual no tendrá ninguna repercusión negativa en su desarrollo ni funcionamiento posterior. El número de ACIERTOS o ERRORES obtenidos no significan ninguna valoración de sus capacidades individuales, dado que ello depende del tipo de prueba y edad del participante, por lo que en base a dichas variables, en algunas pruebas y en algunas etapas se suelen producir muchos errores y en otras pruebas o etapas muy pocos errores.\nLa prueba se realizará de forma individual y los datos recogidos en esta investigación se tratarán de forma colectiva, manteniendo el anonimato en todo momento. \nAdemás, el/la participante estará en su derecho de retirar el consentimiento cuando lo considere conveniente, oponiéndose a la colaboración sin ninguna consecuencia ni justificación necesaria, o dando por finalizada la prueba aunque esta no hubiera concluido."

class PresentacionExperimento:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("DiscondV2 - Presentador de Experimentos - Programa creado por Santiago Benjumea(@PikoyPala)-2025")

        try:
            self.ventana.state('zoomed')
        except tk.TclError:
            self.ventana.attributes("-fullscreen", True)
        
        self.ventana.configure(bg="black")
        self.ventana.bind("<Escape>", self.close_on_escape)

        try:
            self.check_on = ImageTk.PhotoImage(Image.open(asset_path("check_on.png")).resize((48, 48)))
            self.check_off = ImageTk.PhotoImage(Image.open(asset_path("check_off.png")).resize((48, 48)))
        except Exception as e:
            print(f"Advertencia: No se pudieron cargar imágenes de UI: {e}")
            self.check_on, self.check_off = None, None

        self.configuracion = None
        self.resultados = []
        self.trial_execution_queue = []
        self.current_trial_in_block_idx = 0
        self.global_ensayo_idx_ejecucion = 0
        self.active_sequence_idx = 0
        self.reps_done_in_current_sequence = 0
        self.current_block_outcomes = []
        self.reintentar_ensayo_actual = False
        self.nombre_participante = ""
        self.edad_participante = ""
        self.sexo_participante = ""
        self.consentimiento_aceptado_var = tk.BooleanVar(value=False)
        self.start_time_latencia = None
        self.consecutive_outcomes_for_sequence = []
        self.limpiar_referencias_widgets()
        self.ventana.after(100, self.pantalla_cargar_configuracion)

    def close_on_escape(self, event=None):
        self.ventana.destroy()

    # --- NUEVA FUNCIÓN DE CIERRE PARA EL EXPERIMENTADOR ---
    def close_by_admin(self, event=None):
        """Cierra la ventana forzosamente, pensado para el experimentador."""
        if messagebox.askyesno("Confirmar Salida", "¿Está seguro de que desea finalizar el experimento? Los datos no guardados se perderán."):
            self.ventana.destroy()
    # ----------------------------------------------------

    def limpiar_referencias_widgets(self):
        self.button_iniciar_experimento = None
        self.label_ensayo_num = None
        self.frame_comparaciones_contenedor = None
        self.label_feedback = None
        self.label_espera = None
        self.label_cuenta = None
        self.boton_muestra = None
        self.tk_img_muestra = None
        self.tk_imgs_comparaciones_refs = []

    def limpiar_pantalla(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()
        self.limpiar_referencias_widgets()

    def pantalla_cargar_configuracion(self):
        self.limpiar_pantalla()
        if not self.ventana.winfo_exists(): return
        tk.Label(self.ventana, text="CARGAR EXPERIMENTO", font=("Arial", 32, "bold"), bg="black", fg="white").pack(pady=50)
        tk.Button(self.ventana, text="Seleccionar Archivo de Experimento", font=("Arial", 24), command=self.cargar_configuracion_y_mostrar_siguiente).pack(pady=20)
        tk.Button(self.ventana, text="Salir", font=("Arial", 24), command=self.ventana.destroy).pack(pady=10)

    def cargar_configuracion_y_mostrar_siguiente(self):
        nombre_archivo = filedialog.askopenfilename(initialdir=CARPETA_EXPERIMENTOS_PARA_CARGAR, title="Seleccionar Experimento", filetypes=[("Archivos Discond", "*.exp")])
        if not nombre_archivo: return
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as f:
                self.configuracion = json.load(f)
            
            if "secuencias" not in self.configuracion or not isinstance(self.configuracion.get("secuencias"), list) or not self.configuracion.get("secuencias"):
                raise ValueError("El archivo de experimento no tiene el formato correcto o no contiene secuencias.")

            self.pantalla_consentimiento_y_bienvenida()
        except Exception as e:
            self.configuracion = None
            messagebox.showerror("Error al Cargar", f"No se pudo cargar o procesar el archivo de configuración.\nError: {e}")
            self.pantalla_cargar_configuracion()

    def pantalla_consentimiento_y_bienvenida(self):
        self.limpiar_pantalla()
        if not self.ventana.winfo_exists() or not self.configuracion: return

        frame_principal = tk.Frame(self.ventana, bg="black")
        frame_principal.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(frame_principal, text="CONSENTIMIENTO INFORMADO", font=("Arial", 24, "bold"), bg="black", fg="white").pack(pady=5)
        text_consent = scrolledtext.ScrolledText(frame_principal, font=("Arial", 16), bg="gray10", fg="white", wrap=tk.WORD, height=8, relief="sunken", bd=2)
        text_consent.insert(tk.END, self.configuracion.get("texto_consentimiento", CONSENTIMIENTO_TEXTO_DEFECTO))
        text_consent.config(state=tk.DISABLED)
        text_consent.pack(pady=5, padx=50, fill="x")

        tk.Label(frame_principal, text="INSTRUCCIONES", font=("Arial", 24, "bold"), bg="black", fg="white").pack(pady=(20, 5))
        text_instr = scrolledtext.ScrolledText(frame_principal, font=("Arial", 16), bg="gray10", fg="white", wrap=tk.WORD, height=8, relief="sunken", bd=2)
        text_instr.insert(tk.END, self.configuracion.get("texto_instrucciones", "No se proporcionaron instrucciones."))
        text_instr.config(state=tk.DISABLED)
        text_instr.pack(pady=5, padx=50, fill="x")

        frame_datos = tk.Frame(frame_principal, bg="black")
        frame_datos.pack(pady=20)
        self.entry_nombre_participante = self._crear_entry_con_label(frame_datos, "Nombre/Código:", self.nombre_participante)
        self.entry_edad_participante = self._crear_entry_con_label(frame_datos, "Edad:", self.edad_participante, 10)
        self.entry_sexo_participante = self._crear_entry_con_label(frame_datos, "Sexo/genero:", self.sexo_participante, 10)

        frame_check = tk.Frame(frame_principal, bg="black")
        frame_check.pack(pady=10)
        self.consentimiento_aceptado_var = tk.BooleanVar(value=False)
        
        if self.check_on and self.check_off:
            chk = tk.Checkbutton(frame_check, image=self.check_off, selectimage=self.check_on, variable=self.consentimiento_aceptado_var, command=self._actualizar_estado_boton_inicio, compound="left", indicatoron=False, bd=0, bg="black", activebackground="black")
            chk.pack(side=tk.LEFT)
            tk.Label(frame_check, text=" Acepto participar en el estudio", font=("Arial", 18), bg="black", fg="white").pack(side=tk.LEFT)
        else:
            chk = tk.Checkbutton(frame_check, text=" Acepto participar en el estudio", variable=self.consentimiento_aceptado_var, command=self._actualizar_estado_boton_inicio, font=("Arial", 18), bg="black", fg="white", selectcolor="black", activebackground="black", activeforeground="white", highlightthickness=0)
            chk.pack()

        self.button_iniciar_experimento = tk.Button(frame_principal, text="Iniciar Experimento", font=("Arial", 22, "bold"), state=tk.DISABLED, command=self._verificar_datos_y_empezar)
        self.button_iniciar_experimento.pack(pady=20)

    def _crear_entry_con_label(self, frame, texto, valor_inicial, ancho=30):
        container = tk.Frame(frame, bg="black")
        container.pack(pady=5)
        tk.Label(container, text=texto, font=("Arial", 18), bg="black", fg="white").pack(side=tk.LEFT, padx=10)
        entry = tk.Entry(container, font=("Arial", 18), width=ancho, insertbackground="white", bg="gray20", fg="white")
        entry.pack(side=tk.LEFT)
        entry.insert(0, str(valor_inicial))
        return entry

    def _actualizar_estado_boton_inicio(self):
        if self.button_iniciar_experimento and self.button_iniciar_experimento.winfo_exists():
            self.button_iniciar_experimento.config(state=tk.NORMAL if self.consentimiento_aceptado_var.get() else tk.DISABLED)

    def _verificar_datos_y_empezar(self):
        self.nombre_participante = self.entry_nombre_participante.get().strip()
        self.edad_participante = self.entry_edad_participante.get().strip()
        self.sexo_participante = self.entry_sexo_participante.get().strip()

        if not all([self.nombre_participante, self.edad_participante, self.sexo_participante]):
            messagebox.showwarning("Datos Incompletos", "Por favor, rellene todos los campos de datos del participante.")
            return

        try:
            int(self.edad_participante)
        except ValueError:
            messagebox.showerror("Dato Inválido", "El campo 'Edad' debe ser un número entero.")
            return

        # --- CAMBIO DE COMPORTAMIENTO DE LA VENTANA ---
        # Desvinculamos la tecla ESC normal
        self.ventana.unbind("<Escape>")
        # Vinculamos la nueva combinación de teclas para el experimentador
        self.ventana.bind("<Control-q>", self.close_by_admin)
        # Pasamos a pantalla completa real para "bloquear" la sesión
        self.ventana.attributes("-fullscreen", True)
        # -----------------------------------------------

        self.iniciar_experimento()

    def iniciar_experimento(self):
        if not self.configuracion: return
        self.resultados = []
        self.global_ensayo_idx_ejecucion = 0
        self.active_sequence_idx = 0
        self.reps_done_in_current_sequence = 0
        self.consecutive_outcomes_for_sequence = []

        if self._preparar_siguiente_bloque_de_ensayos():
            self.mostrar_intervalo(callback_al_finalizar=self._mostrar_ensayo_de_cola)
        else:
            self.finalizar_experimento("No se encontraron secuencias o ensayos válidos.")

    def _preparar_siguiente_bloque_de_ensayos(self):
        if not self.configuracion or self.active_sequence_idx >= len(self.configuracion["secuencias"]):
            return False
        
        current_sequence_config = self.configuracion['secuencias'][self.active_sequence_idx]
        
        self.trial_execution_queue = []
        self.current_trial_in_block_idx = 0
        self.current_block_outcomes = []
        
        ensayos = current_sequence_config.get("ensayos", [])
        if not ensayos: return False
        
        indices = list(range(len(ensayos)))
        if current_sequence_config.get("orden_aleatorio", False):
            random.shuffle(indices)

        for original_idx in indices:
            self.trial_execution_queue.append({
                "secuencia_original_idx": self.active_sequence_idx,
                "original_index_en_secuencia": original_idx,
                "data": ensayos[original_idx],
                "numero_intento": 1,
                "primera_respuesta_registrada": False
            })
        
        return True

    def _mostrar_ensayo_de_cola(self):
        if not self.configuracion: return
        self.limpiar_pantalla()
        if self.current_trial_in_block_idx >= len(self.trial_execution_queue):
            self.finalizar_experimento("Error: Se intentó mostrar un ensayo fuera de la cola."); return

        ensayo_info_actual = self.trial_execution_queue[self.current_trial_in_block_idx]
        self.ensayo = ensayo_info_actual.get("data", {})
        
        seq_idx = ensayo_info_actual.get("secuencia_original_idx")
        current_sequence_config = self.configuracion['secuencias'][seq_idx]
        ruta_subcarpeta = current_sequence_config.get("ruta_imagenes", "")
        base_path_imagenes = os.path.join(CARPETA_BANCO_IMAGENES, ruta_subcarpeta)
        
        try:
            self.ventana.update_idletasks()
            screen_width, screen_height = self.ventana.winfo_width(), self.ventana.winfo_height()
            
            num_base_para_calculo = 4
            ancho_comp = (screen_width * 0.96 - (screen_width * 0.015 * (num_base_para_calculo - 1))) / num_base_para_calculo
            alto_comp = ancho_comp * 0.75
            alto_zona_comps = alto_comp * 1.2
            max_alto_muestra = (screen_height - alto_zona_comps) * 0.95

            ruta_muestra = os.path.join(base_path_imagenes, self.ensayo["muestra_img_nombre"])
            img_muestra_pil = self._redimensionar_manteniendo_aspecto(Image.open(ruta_muestra), int(screen_width * 0.95), int(max_alto_muestra))
            self.tk_img_muestra = ImageTk.PhotoImage(img_muestra_pil)

            self.tk_imgs_comparaciones_refs = []
            for nombre_img in self.ensayo["comparaciones_img_nombres"]:
                ruta_comp = os.path.join(base_path_imagenes, nombre_img)
                img_comp_pil = self._redimensionar_manteniendo_aspecto(Image.open(ruta_comp), int(ancho_comp), int(alto_comp))
                self.tk_imgs_comparaciones_refs.append(ImageTk.PhotoImage(img_comp_pil))

        except Exception as e:
            messagebox.showerror("Error de Imagen", f"No se pudo cargar una imagen del ensayo.\nVerifique la carpeta: {base_path_imagenes}\nError: {e}")
            self._decidir_siguiente_paso(); return

        if self.configuracion.get("mostrar_num_ensayo", True):
            tk.Label(self.ventana, text=self._generar_texto_info_ensayo(), font=("Arial", 16), bg="black", fg="white").pack(side=tk.TOP, pady=5)
        
        self.frame_muestra_contenedor = tk.Frame(self.ventana, bg="black")
        self.frame_muestra_contenedor.pack(side=tk.TOP, expand=True, fill="both")
        self.boton_muestra = tk.Button(self.frame_muestra_contenedor, image=self.tk_img_muestra, bg="black", bd=0, activebackground="black", command=self.iniciar_demora_o_comparaciones)
        self.boton_muestra.image = self.tk_img_muestra
        self.boton_muestra.pack()

    def iniciar_demora_o_comparaciones(self, event=None):
        if not hasattr(self, 'boton_muestra') or not self.boton_muestra.winfo_exists(): return
        
        if self.configuracion.get("tipo_presentacion_demora_cero") != "simultánea" or self.configuracion.get("demora_muestra_comparacion", 0) > 0:
            self.boton_muestra.config(state=tk.DISABLED)
            self.boton_muestra.pack_forget()
        else:
             self.boton_muestra.config(command=lambda: None, relief="flat")
        
        demora = self.configuracion.get("demora_muestra_comparacion", 0)
        if demora > 0:
            self.ventana.after(int(demora * 1000), self._mostrar_comparaciones)
        else:
            self._mostrar_comparaciones()
            
    def _mostrar_comparaciones(self):
        self.frame_comparaciones_contenedor = tk.Frame(self.ventana, bg="black")
        self.frame_comparaciones_contenedor.pack(side=tk.BOTTOM, expand=True, fill="both")
        sub_frame = tk.Frame(self.frame_comparaciones_contenedor, bg="black")
        sub_frame.pack()
        for i, tk_img in enumerate(self.tk_imgs_comparaciones_refs):
            cmd = lambda idx=i: self.evaluar_respuesta(idx)
            btn = tk.Button(sub_frame, image=tk_img, bg="black", bd=0, activebackground="black", command=cmd)
            btn.image = tk_img
            btn.pack(side=tk.LEFT, padx=10)
        
        self.start_time_latencia = time.perf_counter()

    def evaluar_respuesta(self, indice_elegido):
        latencia_ms = 0
        if self.start_time_latencia:
            latencia_ms = (time.perf_counter() - self.start_time_latencia) * 1000
        
        if not self.ensayo: return
        es_correcto = (indice_elegido == self.ensayo["correcta"])
        ensayo_info = self.trial_execution_queue[self.current_trial_in_block_idx]
        
        if not ensayo_info["primera_respuesta_registrada"]:
            self.current_block_outcomes.append(es_correcto)
            ensayo_info["primera_respuesta_registrada"] = True

            if es_correcto:
                self.consecutive_outcomes_for_sequence.append(True)
            else:
                self.consecutive_outcomes_for_sequence = []
        
        self.resultados.append({
            "Secuencia": ensayo_info["secuencia_original_idx"] + 1,
            "Ensayo": ensayo_info["original_index_en_secuencia"] + 1,
            "Intento_Num": ensayo_info["numero_intento"],
            "Latencia_ms": int(latencia_ms),
            "Muestra": self.ensayo["muestra_img_nombre"],
            "Comparaciones": ", ".join(self.ensayo["comparaciones_img_nombres"]),
            "Elegida": self.ensayo["comparaciones_img_nombres"][indice_elegido],
            "Correcta": self.ensayo["comparaciones_img_nombres"][self.ensayo["correcta"]],
            "Resultado": "Correcto" if es_correcto else "Error"
        })
        
        self.reintentar_ensayo_actual = False
        if not es_correcto and self.ensayo.get("repetir_hasta_acierto", False):
            self.reintentar_ensayo_actual = True
            ensayo_info["numero_intento"] += 1
        
        self.limpiar_pantalla()
        
        def post_feedback_action():
            self._decidir_siguiente_paso()

        if self.ensayo.get("retro", True):
            color = "green" if es_correcto else "red"
            if SONIDO_CORRECTO and es_correcto: pygame.mixer.Sound(SONIDO_CORRECTO).play()
            elif SONIDO_INCORRECTO and not es_correcto: pygame.mixer.Sound(SONIDO_INCORRECTO).play()
            tk.Label(self.ventana, text="Correcto" if es_correcto else "Error", font=("Arial", 300, "bold"), bg=color, fg="white").place(relx=0.5, rely=0.5, anchor="center")
            self.ventana.after(1000, post_feedback_action)
        else:
            post_feedback_action()

    def mostrar_intervalo(self, callback_al_finalizar=None):
        self.limpiar_pantalla()
        if not self.configuracion: return

        if callback_al_finalizar is None:
            callback_al_finalizar = self._decidir_siguiente_paso
        
        self.label_espera = tk.Label(self.ventana, text="Espere un momento por favor...", font=("Arial", 40), bg="black", fg="white")
        self.label_espera.place(relx=0.5, rely=0.4, anchor="center")

        intervalo = self.configuracion.get("intervalo_entre_ensayos", 0)
        if intervalo > 0:
            if self.configuracion.get("mostrar_countdown", True):
                self.label_cuenta = tk.Label(self.ventana, text="", font=("Arial", 80), bg="black", fg="white")
                self.label_cuenta.place(relx=0.5, rely=0.6, anchor="center")
                self._cuenta_atras(intervalo * 10, callback_al_finalizar)
            else:
                self.ventana.after(int(intervalo * 1000), callback_al_finalizar)
        else:
            callback_al_finalizar()

    def _cuenta_atras(self, i, callback_al_finalizar):
        if i < 0:
            if callable(callback_al_finalizar):
                callback_al_finalizar()
        else:
            if hasattr(self, 'label_cuenta') and self.label_cuenta.winfo_exists():
                self.label_cuenta.config(text=f"{i / 10:.1f}s")
                self.ventana.after(100, lambda: self._cuenta_atras(i - 1, callback_al_finalizar))

    def _decidir_siguiente_paso(self):
        if self.reintentar_ensayo_actual:
            self.reintentar_ensayo_actual = False
            self.mostrar_intervalo(callback_al_finalizar=self._mostrar_ensayo_de_cola)
            return

        if not self.configuracion: return
        
        current_sequence_config = self.configuracion['secuencias'][self.active_sequence_idx]
        criterio_tipo = current_sequence_config.get("criterio_tipo", "ninguno")

        if criterio_tipo == "consecutivos":
            if self._verificar_criterio_cumplido():
                self._procesar_fin_de_bloque()
                return 
        
        es_fin_de_bloque = self.current_trial_in_block_idx + 1 >= len(self.trial_execution_queue)
        
        self.current_trial_in_block_idx += 1
        self.global_ensayo_idx_ejecucion += 1
        
        if es_fin_de_bloque:
            self._procesar_fin_de_bloque()
        else:
            self.mostrar_intervalo(callback_al_finalizar=self._mostrar_ensayo_de_cola)

    def _verificar_criterio_cumplido(self):
        current_sequence_config = self.configuracion['secuencias'][self.active_sequence_idx]
        criterio_tipo = current_sequence_config.get("criterio_tipo", "ninguno")

        if criterio_tipo == "ninguno" and current_sequence_config.get("criterio_porcentaje_activo", False):
            criterio_tipo = "porcentaje"

        if criterio_tipo == "porcentaje":
            es_ultimo_ensayo_del_bloque = self.current_trial_in_block_idx + 1 >= len(self.trial_execution_queue)
            if es_ultimo_ensayo_del_bloque:
                if self.current_block_outcomes:
                    porcentaje_actual = (sum(self.current_block_outcomes) / len(self.current_block_outcomes)) * 100
                    criterio_target = current_sequence_config.get("criterio_porcentaje_valor", 80)
                    if porcentaje_actual >= criterio_target:
                        return True
        
        elif criterio_tipo == "consecutivos":
            n_consecutivos_target = current_sequence_config.get("criterio_consecutivos_valor", 5)
            if len(self.consecutive_outcomes_for_sequence) >= n_consecutivos_target:
                return True
        
        return False

    def _procesar_fin_de_bloque(self):
        if not self.configuracion: return
        
        self.reps_done_in_current_sequence += 1
        
        current_sequence_config = self.configuracion['secuencias'][self.active_sequence_idx]
        max_reps = current_sequence_config.get("n_repeticiones", 1)

        criterio_cumplido = self._verificar_criterio_cumplido()
        max_reps_alcanzado = self.reps_done_in_current_sequence >= max_reps

        if criterio_cumplido:
            self._avanzar_a_siguiente_secuencia_o_finalizar()
        elif max_reps_alcanzado:
            terminar_experimento = current_sequence_config.get("terminar_exp_si_max_reps", False)
            if terminar_experimento and not criterio_cumplido:
                self.finalizar_experimento()
            else:
                self._avanzar_a_siguiente_secuencia_o_finalizar()
        else:
            if self._preparar_siguiente_bloque_de_ensayos():
                self.mostrar_intervalo(callback_al_finalizar=self._mostrar_ensayo_de_cola)
            else:
                self.finalizar_experimento("Error al repetir la secuencia.")

    def _avanzar_a_siguiente_secuencia_o_finalizar(self):
        es_ultima_secuencia = self.active_sequence_idx >= len(self.configuracion['secuencias']) - 1
        
        if not es_ultima_secuencia:
            self.active_sequence_idx += 1
            self.reps_done_in_current_sequence = 0
            self.consecutive_outcomes_for_sequence = []

            if self._preparar_siguiente_bloque_de_ensayos():
                self.mostrar_intervalo(callback_al_finalizar=self._mostrar_ensayo_de_cola)
            else:
                self.finalizar_experimento("Error al preparar la siguiente secuencia.")
        else:
            self.finalizar_experimento()

    def finalizar_experimento(self, mensaje_log_interno=None):
        self.limpiar_pantalla()
        tk.Label(self.ventana, text=f"Muchas gracias {self.nombre_participante} por su participación.", font=("Arial", 28), bg="black", fg="white", wraplength=self.ventana.winfo_screenwidth()*0.9).pack(expand=True)
        self.guardar_resultados_excel()
        if mensaje_log_interno:
            print(f"INFO: Experimento finalizado. Causa: {mensaje_log_interno}")
        self.ventana.after(5000, self.ventana.destroy)

    def guardar_resultados_excel(self):
        if not self.resultados or not self.configuracion: return
        
        info_resumen = [
            ("Nombre Experimento", self.configuracion.get("nombre_experimento")),
            ("Participante", self.nombre_participante),
            ("Edad", self.edad_participante),
            ("Sexo/género", self.sexo_participante),
            ("", ""),
            ("--- Resumen de Aciertos por Secuencia ---", "")
        ]
        
        for i, seq_config in enumerate(self.configuracion['secuencias']):
            secuencia_num_actual = i + 1
            resultados_secuencia = [r for r in self.resultados if r.get("Secuencia") == secuencia_num_actual]
            if not resultados_secuencia: continue
            resultados_pi = [r for r in resultados_secuencia if r.get("Intento_Num") == 1]
            aciertos_pi = sum(1 for r in resultados_pi if r["Resultado"] == "Correcto")
            total_pi = len(resultados_pi)
            porcentaje_pi = (aciertos_pi / total_pi * 100) if total_pi > 0 else 0
            aciertos_global = sum(1 for r in resultados_secuencia if r["Resultado"] == "Correcto")
            total_global = len(resultados_secuencia)
            porcentaje_global = (aciertos_global / total_global * 100) if total_global > 0 else 0
            info_resumen.extend([
                (f"Secuencia {secuencia_num_actual} - % Aciertos (Primer Intento)", f"{porcentaje_pi:.2f}% ({aciertos_pi}/{total_pi})"),
                (f"Secuencia {secuencia_num_actual} - % Aciertos (Global)", f"{porcentaje_global:.2f}% ({aciertos_global}/{total_global})"),
            ])

        df_resumen = pd.DataFrame(info_resumen, columns=["Dato", "Valor"])
        df_detalle = pd.DataFrame(self.resultados)
        
        nombre_exp = self.configuracion.get("nombre_experimento", "exp").replace(" ", "_")
        nombre_part = "".join(c for c in self.nombre_participante if c.isalnum()).replace(' ', '_')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = os.path.join(CARPETA_RESULTS, f"{nombre_exp}_{nombre_part}_{timestamp}.xlsx")

        try:
            with pd.ExcelWriter(nombre_archivo) as writer:
                df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                df_detalle.to_excel(writer, sheet_name='Resultados Detallados', index=False)
            print(f"Resultados guardados en {nombre_archivo}")
        except Exception as e:
            print(f"Error al guardar el archivo de Excel: {e}")
            
    def _redimensionar_manteniendo_aspecto(self, img, max_w, max_h):
        img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        return img
        
    def _generar_texto_info_ensayo(self):
        if not self.configuracion: return ""
        ensayo_actual = self.current_trial_in_block_idx + 1
        total_ensayos = len(self.trial_execution_queue)
        reps_hechas = self.reps_done_in_current_sequence + 1
        return f"Secuencia {self.active_sequence_idx + 1} | Rep. {reps_hechas} | Ensayo {ensayo_actual}/{total_ensayos}"

if __name__ == "__main__":
    app = PresentacionExperimento()
    app.ventana.mainloop()