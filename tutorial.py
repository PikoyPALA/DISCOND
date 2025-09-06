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

# --- FUNCIONES DE RUTA DEFINITIVAS ---
def asset_path(filename):
    """ Obtiene la ruta a un recurso en la carpeta 'assets' de forma robusta. """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, "assets", filename)

def tutorial_asset_path(filename):
    """ Obtiene la ruta a un recurso en la carpeta 'tutorial_assets' de forma robusta. """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, "tutorial_assets", filename)

try:
    pygame.mixer.init()
    SONIDO_CORRECTO = asset_path("correcto.wav")
    SONIDO_INCORRECTO = asset_path("incorrecto.wav")
except Exception as e:
    print(f"Advertencia: No se pudo inicializar pygame.mixer. Error: {e}")
    SONIDO_CORRECTO, SONIDO_INCORRECTO = None, None

CARPETA_EXPERIMENTO_TUTORIAL = tutorial_asset_path("tutorial.exp")
CARPETA_BANCO_IMAGENES = tutorial_asset_path("banco_imagenes_tutorial")

CARPETA_RESULTS = os.path.join(os.path.expanduser('~'), 'Documents', "DiscondV2", "resultados_tutorial")
os.makedirs(CARPETA_RESULTS, exist_ok=True)

class PresentacionExperimento:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("DiscondV2 - Tutorial Interactivo. Programa creado por Santiago Benjumea (@PikoyPala) 2025")

        # Inicia maximizado CON título
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
            messagebox.showerror("Error de Archivo", f"No se pudieron cargar las imágenes de UI para el tutorial.\nError: {e}")
            self.ventana.destroy()
            return
            
        self.configuracion = None
        self.aciertos = 0
        self.errores = 0
        self.resultados = []
        self.trial_execution_queue = [] 
        self.current_trial_in_block_idx = 0 
        self.global_ensayo_idx_ejecucion = 0
        self.active_sequence_type = 0
        self.reps_done_s1 = 0
        self.reps_done_s2 = 0
        self.current_block_outcomes = []
        self.reintentar_ensayo_actual = False
        self.tk_img_muestra = None
        self.tk_imgs_comparaciones_refs = []
        self.demora = 0
        self.intervalo_entre_ensayos = 0
        self.tipo_presentacion_demora_cero = "sucesiva"
        self.mostrar_num_ensayo = True
        self.n_comparaciones = 2
        self.secuencia1_config = {}
        self.secuencia2_config = {}
        self.secuencia2_activa = False
        self.limpiar_referencias_widgets()
        self.ventana.after(100, self._cargar_tutorial_automaticamente)
    
    def close_on_escape(self, event=None):
        self.ventana.destroy()

    # --- PEGA AQUÍ EL RESTO COMPLETO DE TU CÓDIGO DE tutorial.py ---
    # (Desde la función 'limpiar_referencias_widgets' hasta el final)
    # ...
    def limpiar_referencias_widgets(self):
        self.label_ensayo_num = None
        self.frame_comparaciones_contenedor = None
        self.boton_muestra = None

    def _cargar_tutorial_automaticamente(self):
        self.limpiar_pantalla()
        if not os.path.exists(CARPETA_EXPERIMENTO_TUTORIAL):
            messagebox.showerror("Error del Tutorial", f"No se encontró el archivo del tutorial en:\n{CARPETA_EXPERIMENTO_TUTORIAL}")
            self.ventana.destroy()
            return

        try:
            with open(CARPETA_EXPERIMENTO_TUTORIAL, 'r', encoding='utf-8') as f:
                self.configuracion = json.load(f)

            self.demora = self.configuracion.get("demora_muestra_comparacion", 0)
            self.intervalo_entre_ensayos = self.configuracion.get("intervalo_entre_ensayos", 0)
            self.tipo_presentacion_demora_cero = self.configuracion.get("tipo_presentacion_demora_cero", "sucesiva")
            self.mostrar_num_ensayo = self.configuracion.get("mostrar_num_ensayo", True)
            self.n_comparaciones = self.configuracion.get("n_comparaciones", 2)
            
            if "secuencias" in self.configuracion:
                self.secuencia1_config = self.configuracion["secuencias"][0] if len(self.configuracion["secuencias"]) > 0 else {}
                self.secuencia2_activa = len(self.configuracion["secuencias"]) > 1
                self.secuencia2_config = self.configuracion["secuencias"][1] if self.secuencia2_activa else {}
            else:
                self.secuencia1_config = {"n_ensayos": self.configuracion.get("n_ensayos_secuencia1", 0), "n_repeticiones": self.configuracion.get("n_repeticiones_secuencia1", 1), "orden_aleatorio": self.configuracion.get("orden_aleatorio_secuencia1", False), "ensayos": self.configuracion.get("secuencia1_ensayos", [])}
                self.secuencia2_activa = self.configuracion.get("secuencia2_activa", False)
                self.secuencia2_config = {"n_ensayos": self.configuracion.get("n_ensayos_secuencia2", 0), "n_repeticiones": self.configuracion.get("n_repeticiones_secuencia2", 1), "orden_aleatorio": self.configuracion.get("orden_aleatorio_secuencia2", False), "ensayos": self.configuracion.get("secuencia2_ensayos", []) if self.secuencia2_activa else []}
            
            self.iniciar_experimento()

        except Exception as e:
            messagebox.showerror("Error al Cargar Tutorial", f"Ocurrió un error al leer el archivo del tutorial:\n{e}")
            self.ventana.destroy()

    def iniciar_experimento(self):
        self.aciertos = 0
        self.errores = 0
        self.resultados = []
        self.global_ensayo_idx_ejecucion = 0
        self.reps_done_s1 = 0
        self.reps_done_s2 = 0
        self.trial_execution_queue = []
        self.current_trial_in_block_idx = 0
        self.current_block_outcomes = []
        self.active_sequence_type = 1 
        if self._preparar_siguiente_bloque_de_ensayos():
            self._mostrar_ensayo_de_cola()
        else:
            messagebox.showinfo("Fin del Experimento", "No se encontraron ensayos válidos para presentar en la configuración.")
            self.finalizar_experimento()

    def _preparar_siguiente_bloque_de_ensayos(self):
        self.trial_execution_queue = []
        self.current_trial_in_block_idx = 0
        self.current_block_outcomes = []
        sequence_config_to_run = None
        sequence_type_to_run = 0
        if self.active_sequence_type == 1:
            if self.reps_done_s1 < self.secuencia1_config.get("n_repeticiones", 1):
                sequence_config_to_run = self.secuencia1_config
                sequence_type_to_run = 1
            else:
                self.active_sequence_type = 2
                return self._preparar_siguiente_bloque_de_ensayos()
        elif self.active_sequence_type == 2:
            if self.secuencia2_activa and self.reps_done_s2 < self.secuencia2_config.get("n_repeticiones", 1):
                sequence_config_to_run = self.secuencia2_config
                sequence_type_to_run = 2
            else:
                return False
        if not sequence_config_to_run:
            return False
        ensayos_originales = sequence_config_to_run.get("ensayos", [])
        if not ensayos_originales:
            return False
        ensayos_para_bloque = list(enumerate(ensayos_originales))
        if sequence_config_to_run.get("orden_aleatorio", False):
            random.shuffle(ensayos_para_bloque)
        for original_idx, ensayo_data in ensayos_para_bloque:
            if (ensayo_data and "muestra_img_nombre" in ensayo_data and "comparaciones_img_nombres" in ensayo_data and "correcta" in ensayo_data):
                self.trial_execution_queue.append({"secuencia_original_tipo": sequence_type_to_run, "original_index_en_secuencia": original_idx + 1, "data": ensayo_data, "numero_intento": 1, "primera_respuesta_registrada": False})
        if not self.trial_execution_queue:
            if sequence_type_to_run == 1:
                self.active_sequence_type = 2
                return self._preparar_siguiente_bloque_de_ensayos()
            return False
        return True

    def _redimensionar_manteniendo_aspecto(self, pil_image, ancho_max, alto_max):
        img_copia = pil_image.copy()
        img_copia.thumbnail((ancho_max, alto_max), Image.Resampling.LANCZOS)
        return img_copia

    def _generar_texto_info_ensayo(self):
        ensayo_num_en_bloque = self.current_trial_in_block_idx + 1
        total_ensayos_en_bloque = len(self.trial_execution_queue)
        texto_secuencia = f"Secuencia {self.active_sequence_type}"
        rep_actual = (self.reps_done_s1 if self.active_sequence_type == 1 else self.reps_done_s2) + 1
        texto_repeticion = f"Rep. {rep_actual}"
        return f"Ensayo Global {self.global_ensayo_idx_ejecucion + 1}  |  {texto_secuencia}, {texto_repeticion}  |  Prueba {ensayo_num_en_bloque}/{total_ensayos_en_bloque}"

    def _mostrar_ensayo_de_cola(self):
        self.limpiar_pantalla()
        if self.current_trial_in_block_idx >= len(self.trial_execution_queue):
            self.finalizar_experimento(); return
        ensayo_info_actual = self.trial_execution_queue[self.current_trial_in_block_idx]
        self.ensayo = ensayo_info_actual.get("data", {})
        if not self.ensayo:
             messagebox.showerror("Error de Datos de Ensayo", "Faltan datos en el ensayo.")
             self._decidir_siguiente_paso(); return
        try:
            self.ventana.update_idletasks()
            screen_width = self.ventana.winfo_width()
            screen_height = self.ventana.winfo_height()
            
            num_base_para_calculo = 4
            ancho_comp = (screen_width * 0.96 - (screen_width * 0.015 * (num_base_para_calculo - 1))) / num_base_para_calculo
            alto_comp = ancho_comp * 0.75
            alto_zona_comps = alto_comp * 1.2
            max_alto_muestra = (screen_height - alto_zona_comps) * 0.95

            nombre_img_muestra = self.ensayo["muestra_img_nombre"]
            ruta_img_muestra = os.path.join(CARPETA_BANCO_IMAGENES, nombre_img_muestra)
            pil_img_muestra_orig = Image.open(ruta_img_muestra)
            pil_img_muestra_resized = self._redimensionar_manteniendo_aspecto(pil_img_muestra_orig, int(screen_width * 0.95), int(max_alto_muestra))
            self.tk_img_muestra = ImageTk.PhotoImage(pil_img_muestra_resized)

            self.tk_imgs_comparaciones_refs = []
            for nombre_img_comp in self.ensayo["comparaciones_img_nombres"]:
                ruta_img_comp = os.path.join(CARPETA_BANCO_IMAGENES, nombre_img_comp)
                pil_img_comp_orig = Image.open(ruta_img_comp)
                pil_img_comp_resized = self._redimensionar_manteniendo_aspecto(pil_img_comp_orig, int(ancho_comp), int(alto_comp))
                tk_img_comp = ImageTk.PhotoImage(pil_img_comp_resized)
                self.tk_imgs_comparaciones_refs.append(tk_img_comp)

        except Exception as e:
            messagebox.showerror("Error al Cargar Imagen", f"No se pudo cargar o procesar una imagen para el tutorial.\nVerifique la carpeta 'tutorial_assets'.\nError: {e}")
            self.ventana.destroy(); return

        if self.mostrar_num_ensayo:
            display_text = self._generar_texto_info_ensayo()
            tk.Label(self.ventana, text=display_text, font=("Arial", 20), bg="black", fg="white").pack(side=tk.TOP, pady=5)
        
        frame_muestra_contenedor = tk.Frame(self.ventana, bg="black")
        frame_muestra_contenedor.pack(side=tk.TOP, expand=True, fill="both")
        self.boton_muestra = tk.Button(frame_muestra_contenedor, image=self.tk_img_muestra, bg="black", bd=0, activebackground="black", command=self.iniciar_demora_o_comparaciones)
        self.boton_muestra.image = self.tk_img_muestra
        self.boton_muestra.pack()

    def iniciar_demora_o_comparaciones(self):
        if not (self.demora == 0 and self.tipo_presentacion_demora_cero == "simultanea"):
            self.boton_muestra.pack_forget()
        else:
            self.boton_muestra.config(command=lambda: None, relief="flat")
        
        if self.demora > 0:
            self.ventana.after(int(self.demora * 1000), self._mostrar_comparaciones)
        else:
            self._mostrar_comparaciones()

    def _mostrar_comparaciones(self):
        frame_comparaciones_contenedor = tk.Frame(self.ventana, bg="black")
        frame_comparaciones_contenedor.pack(side=tk.BOTTOM, expand=True, fill="both")
        sub_frame_comparaciones = tk.Frame(frame_comparaciones_contenedor, bg="black")
        sub_frame_comparaciones.pack()
        for i, tk_img_comp in enumerate(self.tk_imgs_comparaciones_refs):
            cmd = lambda idx=i: self.evaluar_respuesta(idx)
            boton_comp = tk.Button(sub_frame_comparaciones, image=tk_img_comp, bg="black", bd=0, activebackground="black", command=cmd)
            boton_comp.image = tk_img_comp
            boton_comp.pack(side=tk.LEFT, padx=10)

    def evaluar_respuesta(self, indice_elegido):
        es_correcto = (indice_elegido == self.ensayo["correcta"])
        resultado_texto = "Correcto" if es_correcto else "ERROR"
        
        if es_correcto:
            self.aciertos += 1
        else:
            self.errores += 1
        
        if not es_correcto and self.ensayo.get("repetir_hasta_acierto", False):
            self.reintentar_ensayo_actual = True
        
        self.limpiar_pantalla()
        
        if self.ensayo.get("retro", True):
            sonido = SONIDO_CORRECTO if es_correcto else SONIDO_INCORRECTO
            if pygame.mixer.get_init() and sonido and os.path.exists(sonido):
                pygame.mixer.Sound(sonido).play()
            color = "green" if es_correcto else "red"
            tk.Label(self.ventana, text=resultado_texto.upper(), font=("Arial", 200, "bold"), bg=color, fg="white").place(relx=0.5, rely=0.5, anchor="center")
            self.ventana.after(1000, self.mostrar_intervalo)
        else:
            self.mostrar_intervalo()

    def mostrar_intervalo(self):
        self.limpiar_pantalla()
        if self.intervalo_entre_ensayos > 0:
            tk.Label(self.ventana, text="Espere un momento...", font=("Arial", 36), bg="black", fg="white").pack(pady=50)
            self.ventana.after(int(self.intervalo_entre_ensayos * 1000), self._decidir_siguiente_paso)
        else:
            self._decidir_siguiente_paso()

    def _decidir_siguiente_paso(self):
        if self.reintentar_ensayo_actual:
            self.reintentar_ensayo_actual = False
            self._mostrar_ensayo_de_cola()
            return
        
        self.current_trial_in_block_idx += 1
        
        if self.current_trial_in_block_idx >= len(self.trial_execution_queue):
            self._procesar_fin_de_bloque()
        else:
            self._mostrar_ensayo_de_cola()

    def _procesar_fin_de_bloque(self):
        if self.active_sequence_type == 1:
            self.reps_done_s1 += 1
            if self.reps_done_s1 >= self.secuencia1_config.get("n_repeticiones", 1):
                self.active_sequence_type = 2
        elif self.active_sequence_type == 2:
            self.reps_done_s2 += 1
            if self.reps_done_s2 >= self.secuencia2_config.get("n_repeticiones", 1):
                self.finalizar_experimento()
                return

        if self._preparar_siguiente_bloque_de_ensayos():
            self._mostrar_ensayo_de_cola()
        else:
            self.finalizar_experimento()

    def finalizar_experimento(self):
        self.limpiar_pantalla()
        tk.Label(self.ventana, text="Has completado el tutorial.", font=("Arial", 32), bg="black", fg="white").pack(pady=50)
        tk.Button(self.ventana, text="Salir del Tutorial", font=("Arial", 28), command=self.ventana.destroy, bg="gray", fg="white").pack(pady=20)

    def limpiar_pantalla(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app_presentacion = PresentacionExperimento()
    app_presentacion.ventana.mainloop()