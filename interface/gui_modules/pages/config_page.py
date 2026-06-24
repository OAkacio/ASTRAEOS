#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Importações                                                              │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
import tkinter as tk
import customtkinter as ctk
import json
import sys
import os
import numpy as np
from tkinter import filedialog, messagebox
from PIL import Image
import threading


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
    return os.path.join(base_path, relative_path)


#
# ? ╭────────────────────────────────────────────────────╮
# ? │   Configuração de Caminhos Globais                 │
# ? ╰────────────────────────────────────────────────────╯
#
PRESETS_PATH = get_resource_path("interface/gui_modules/presets")
BASE_DIR = get_resource_path("")
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)
from astraeos_core.utils import *


#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Componentes de Interface Auxiliares                                      │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.mostrar_tooltip)
        self.widget.bind("<Leave>", self.ocultar_tooltip)

    def mostrar_tooltip(self, event):
        if self.tooltip_window or not self.text:
            return
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.attributes("-alpha", 0.0)
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#282C34",
            foreground="#ABB2BF",
            relief="solid",
            borderwidth=1,
            font=("Roboto", 10, "normal"),
            padx=8,
            pady=4,
            justify="left",
        )
        label.pack()
        offset_x = 15
        offset_y = 15
        x_inicial = event.x_root + offset_x
        y_inicial = event.y_root + offset_y
        self.tooltip_window.wm_geometry(f"+{x_inicial}+{y_inicial}")
        self.tooltip_window.update_idletasks()
        tooltip_width = self.tooltip_window.winfo_reqwidth()
        tooltip_height = self.tooltip_window.winfo_reqheight()
        screen_width = self.tooltip_window.winfo_screenwidth()
        screen_height = self.tooltip_window.winfo_screenheight()
        x = event.x_root + offset_x
        y = event.y_root + offset_y
        if x + tooltip_width > screen_width:
            x = event.x_root - tooltip_width - offset_x
        if y + tooltip_height > screen_height:
            y = event.y_root - tooltip_height - offset_y
        x = max(0, x)
        y = max(0, y)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        self.tooltip_window.attributes("-topmost", True)
        self.tooltip_window.attributes("-alpha", 1.0)

    def ocultar_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


#
# * ╭────────────────────────────────────────────────────────────────────────────╮
# * │   Classe Principal: Página de Configuração                                 │
# * ╰────────────────────────────────────────────────────────────────────────────╯
#
class ConfigPage(ctk.CTkFrame):
    def __init__(
        self,
        master,
        state,
        on_run_click,
        on_update_click,
        on_abort_click,
        on_simulate_exo_click,
        assets_path,
    ):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        #
        # ? ╭────────────────────────────────────────────────────╮
        # ? │   Injeção de Dependências e Layout Principal       │
        # ? ╰────────────────────────────────────────────────────╯
        #
        self.app_state = state
        self.on_run_click = on_run_click
        self.on_update_click = on_update_click
        self.on_abort_click = on_abort_click
        self.on_simulate_exo_click = on_simulate_exo_click
        self.assets_path = assets_path
        self.exo_inputs = []
        self.parker_disabled_inputs = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_area.grid(row=0, column=0, sticky="nsew")
        self.scroll_area.grid_columnconfigure(0, weight=1)
        self.header_frame = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, pady=(10, 2), sticky="ew", padx=20)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame, text="Simulation Settings", font=("Consolas", 18, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, sticky="w")
        try:
            img_load = ctk.CTkImage(
                Image.open(os.path.join(self.assets_path, "load.png")), size=(18, 18)
            )
            img_save = ctk.CTkImage(
                Image.open(os.path.join(self.assets_path, "save.png")), size=(18, 18)
            )
            img_export = ctk.CTkImage(
                Image.open(os.path.join(self.assets_path, "database.png")),
                size=(18, 18),
            )
            img_about = ctk.CTkImage(
                Image.open(os.path.join(self.assets_path, "about.png")), size=(18, 18)
            )
            img_cancel = ctk.CTkImage(
                Image.open(os.path.join(self.assets_path, "cancel.png")), size=(14, 14)
            )
        except Exception:
            img_load, img_save, img_export, img_about, img_cancel = (
                None,
                None,
                None,
                None,
                None,
            )
        self.img_cancel = img_cancel
        self.btn_load_prof = ctk.CTkButton(
            self.header_frame,
            text="" if img_load else "L",
            image=img_load,
            width=28,
            height=28,
            fg_color="#282C34",
            hover_color="#404C55",
            command=self.load_profile,
        )
        self.btn_load_prof.grid(row=0, column=1, padx=(0, 5), sticky="e")
        ToolTip(self.btn_load_prof, "Load Profile")
        self.btn_save_prof = ctk.CTkButton(
            self.header_frame,
            text="" if img_save else "S",
            image=img_save,
            width=28,
            height=28,
            fg_color="#282C34",
            hover_color="#404C55",
            command=self.save_profile,
        )
        self.btn_save_prof.grid(row=0, column=2, padx=(0, 5), sticky="e")
        ToolTip(self.btn_save_prof, "Save Profile")
        self.btn_export = ctk.CTkButton(
            self.header_frame,
            text="" if img_export else "E",
            image=img_export,
            width=28,
            height=28,
            fg_color="#282C34",
            hover_color="#404C55",
            command=self.export_data,
        )
        self.btn_export.grid(row=0, column=3, padx=(0, 5), sticky="e")
        ToolTip(self.btn_export, "Export Data")
        self.btn_about = ctk.CTkButton(
            self.header_frame,
            text="" if img_about else "A",
            image=img_about,
            width=28,
            height=28,
            fg_color="#282C34",
            hover_color="#404C55",
            command=self.show_about,
        )
        self.btn_about.grid(row=0, column=4, sticky="e")
        ToolTip(self.btn_about, "About")
        self.tabview = ctk.CTkTabview(self.scroll_area, height=440)
        self.tabview.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        aba_astro = self.tabview.add("Star & Corona")
        aba_onda = self.tabview.add("Wind & Wave")
        aba_num = self.tabview.add("Numerical Setup")
        aba_gp = self.tabview.add("Plot Preferences")
        self._construir_aba_astro(aba_astro)
        self._construir_aba_onda(aba_onda)
        self._construir_aba_numerico(aba_num)
        self._construir_aba_gp(aba_gp)
        self.lbl_exo = ctk.CTkLabel(
            self.scroll_area, text="Exoplanet Settings", font=("Consolas", 18, "bold")
        )
        self.lbl_exo.grid(row=2, column=0, pady=(15, 2), sticky="w", padx=20)
        self.tabview_exo = ctk.CTkTabview(self.scroll_area, height=180)
        self.tabview_exo.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")
        aba_orbita = self.tabview_exo.add("Orbit & Habitability")
        aba_magnet = self.tabview_exo.add("Magnetosphere")
        self._construir_aba_orbita(aba_orbita)
        self._construir_aba_magnet(aba_magnet)
        self.btn_sim_exo = ctk.CTkButton(
            self.scroll_area,
            text="Simulate Exoplanet",
            command=self.iniciar_sim_exo,
            fg_color="#627683",
            hover_color="#404C55",
            font=("Consolas", 14, "bold"),
            height=25,
            state="disabled",
        )
        self.btn_sim_exo.grid(row=4, column=0, padx=20, pady=(5, 20), sticky="ew")
        self.frame_rodape = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_rodape.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.frame_rodape.grid_columnconfigure(0, weight=1)
        self.frame_rodape.grid_columnconfigure(1, weight=1)
        self.btn_run = ctk.CTkButton(
            self.frame_rodape,
            text="Run Star Simulation",
            command=self.iniciar_processo,
            fg_color="#325E3E",
            hover_color="#213D28",
            font=("Consolas", 14, "bold"),
            height=30,
        )
        self.btn_run.grid(row=0, column=0, sticky="ew")
        self.btn_abort = ctk.CTkButton(
            self.frame_rodape,
            text="Abort",
            command=self.abortar_processo,
            fg_color="#75353A",
            hover_color="#77312A",
            font=("Consolas", 14, "bold"),
            height=30,
            state="disabled",
        )
        self.btn_abort.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        self.set_exoplanet_state("disabled")

    #
    # * ╭────────────────────────────────────────────────────────────────────────────╮
    # * │   Ferramentas de Dados (Export & About)                                    │
    # * ╰────────────────────────────────────────────────────────────────────────────╯
    #
    def show_about(self):
        about_win = ctk.CTkToplevel(self)
        about_win.title("About ASTRAEOS")
        about_win.geometry("500x420")
        about_win.resizable(False, False)
        about_win.attributes("-topmost", True)
        txt = ctk.CTkTextbox(
            about_win,
            wrap="word",
            font=("Roboto", 13),
            fg_color="#1E1E1E",
            text_color="#ABB2BF",
        )
        txt.pack(fill="both", expand=True, padx=20, pady=20)
        VERSAO_ASTRAEOS = "v1.0.0"
        MODELO_MHD_ATUAL = (
            "Modelo JPO (Jatenco-Pereira & Opher) com amortecimento de Ondas de Alfvén"
        )
        MODELO_TERMICO = "Modelo de Parker (Termicamente Impulsionado)"

        texto_about = f"""ASTRAEOS Version: {VERSAO_ASTRAEOS} 
        Developer: Victor M. Acacio

        ■ Scientific Objective
        A computational suite optimized for magnetohydrodynamic (MHD) modeling of stellar winds. ASTRAEOS aims to investigate wind topology and quantify the impact of dynamic pressure on magnetospheric compression and the habitability of exoplanetary systems.

        ■ Physical and Numerical Models
        The key advantage of the simulator's architecture is its ability to contrast purely thermal winds ({MODELO_TERMICO}) with models driven by plasma wave pressure ({MODELO_MHD_ATUAL}). The software numerically resolves the momentum balance by incorporating Alfvén wave flux and different damping regimes (constant or resonant), which are crucial for explaining the high mass-loss rates in red dwarfs. The numerical core is powered by high-precision Runge-Kutta (RK4) integrators coupled with optimized search algorithms to solve the critical point topology.

        ■ Key Features
        • Generation of dynamic radial profiles (velocity, density, wave flux, and dynamic pressure).
        • Delimitation of classic Habitable Zones (Kopparapu limits).
        • Calculation of the magnetopause radius and analysis of CME impacts on the magnetosphere.
        • Native and structured export of numerical data matrices, ensuring full compliance with Open Science best practices and reproducibility.

        ■ Academic Information
        Developed with the support of the Institute of Astronomy, Geophysics and Atmospheric Sciences of the University of São Paulo (IAG-USP). Undergraduate Thesis (TG) under the advisement of Prof. Dr. Vera Jatenco Silva Pereira."""

        conteudo = texto_about
        txt.insert("0.0", conteudo)
        txt.configure(state="disabled")

    def export_data(self):
        cte = self.app_state.cte.get()
        filepath_npz = os.path.join(os.getcwd(), "data", f"curve_{cte}.npz")

        if not os.path.exists(filepath_npz):
            messagebox.showerror(
                "Export Error",
                "No simulation data found in memory. Please 'Run Star Simulation' first.",
            )
            return

        export_path = filedialog.asksaveasfilename(
            initialdir=os.path.join(os.getcwd(), "data"),
            title="Export Scientific Data",
            defaultextension=".csv",
            filetypes=[
                ("CSV Data File", "*.csv"),
                ("Text File", "*.txt"),
                ("All Files", "*.*"),
            ],
        )
        if not export_path:
            return
        self.btn_export.configure(state="disabled")

        def tarefa_exportacao():
            try:
                dados = np.load(filepath_npz, allow_pickle=True)

                def val(key):
                    if key in dados:
                        v = dados[key]
                        if isinstance(v, np.ndarray) and v.size == 1:
                            return v.item()
                        return v
                    return "N/A"

                with open(export_path, "w", encoding="utf-8") as f:
                    f.write("# " + "=" * 60 + "\n")
                    f.write("# ASTRAEOS - SCIENTIFIC DATA EXPORT\n")
                    f.write("# " + "=" * 60 + "\n")
                    f.write("# [ 1. STAR & CORONA ]\n")
                    f.write(f"# Target Name: {val('nome')}\n")
                    f.write(
                        f"# Stellar Mass [Msun]: {val('Mstar')} | Stellar Radius [Rsun]: {val('Rstar')} | Stellar Luminosity [Lsun]: {val('Lstar')}\n"
                    )
                    f.write(
                        f"# Effective Temp [K]: {val('Teff')} | Coronal Temp [K]: {val('T')}\n"
                    )
                    f.write(
                        f"# Base Density [g/cm3]: {val('rho0')} | Surface B-Field [G]: {val('B0')} | Mean Mol. Weight: {val('mu')}\n"
                    )
                    f.write("#\n# [ 2. WIND & WAVES ]\n")
                    f.write(
                        f"# Expansion Factor (S): {val('S_divergencia')} | Transition Factor (F): {val('F')} | Initial Wave Amp (dv0^2): {val('deltav0')}\n"
                    )
                    f.write(
                        f"# Initial Flux (phi0): {val('phi0')} | Damping Length (L0): {val('L0')} | Constant Damping: {val('cte')} | Parker Wind: {val('parker')}\n"
                    )
                    f.write(f"# Mass Loss Rate (dM/dt): {val('dmdt0')} Msun/yr\n")
                    f.write("#\n# [ 3. NUMERICAL SETUP & TOPOLOGY ]\n")
                    f.write(
                        f"# Simulation Dist: {val('x_sim')} | Step (h_rk): {val('h_rk')} | ve0: {val('ve0')} | Sound Speed (cs): {val('cs')}\n"
                    )
                    f.write(
                        f"# Search Lower Limit: {val('u0_ini')} | Search Step: {val('u0_step')} | Final Base Vel (u0): {val('u0')}\n"
                    )
                    f.write(
                        f"# Critical Point (x_crit): {val('x_crit')} | Velocity at Crit (y_crit): {val('y_crit')} | Transition Radius (x_t): {val('x_t')}\n"
                    )
                    f.write(
                        f"# Critical Jump Size: {val('tamanho_pulo')} | Backtrack Steps: {val('recuo_pulo')}\n"
                    )
                    f.write(
                        f"# Crit. Numerator Idx: {val('idx_crit_num')} | Crit. Denominator Idx: {val('idx_crit_den')}\n"
                    )
                    f.write("#\n# [ 4. EXOPLANET & HABITABILITY ]\n")
                    f.write(
                        f"# Exoplanet Simulated: {val('habitabilidade')} | Exoplanet Name: {val('exoplanet_name')}\n"
                    )
                    f.write(
                        f"# Orbital Dist [AU]: {val('Dorb')} | Eccentricity: {val('e')} | Bond Albedo: {val('Ab')} | Planet Radius [Rearth]: {val('Rplan')}\n"
                    )
                    f.write(
                        f"# Dipole Moment [Am2]: {val('Mmag')} | Chapman-Ferraro factor (f0): {val('f0')} | CME Factor (k): {val('k_cme')} | Ionosphere (hion): {val('hion')} km\n"
                    )
                    f.write(
                        f"# Dynamic Pressure at Orbit (P_din): {val('P_din')} dyn/cm2 | Standoff Radius (Rmag): {val('Rmag')} R_earth | Atmos. Lost Area: {val('Aperdida')}%\n"
                    )
                    f.write(
                        f"# Kopparapu Inner Edges: Recent Venus = {val('d_int_rv')} | Runaway = {val('d_int_rg')} | Moist = {val('d_int_mg')}\n"
                    )
                    f.write(
                        f"# Kopparapu Outer Edges: Max Greenhouse = {val('d_ext_mg')} | Early Mars = {val('d_ext_em')}\n"
                    )
                    f.write(
                        f"# Classic Edges: Inner = {val('dc_int')} | Outer = {val('dc_ext')}\n"
                    )
                    f.write("#\n# [ 5. PLOTTING PREFERENCES ]\n")
                    f.write(
                        f"# X-Scale: {val('x_scale')} | Y-Scale: {val('y_scale')} | X-units: {val('x_un')} | Y-units: {val('y_un')}\n"
                    )
                    f.write(
                        f"# Ref Distances: {val('x_ref')} | Ref Names: {val('nome_ref')} | Ref Colors: {val('color_ref')}\n"
                    )
                    f.write(
                        f"# Sigma From: {val('sigmas_ref')} | Sigma Name: {val('sigmas_nome_ref')}\n"
                    )
                    f.write("# " + "=" * 60 + "\n")
                    colunas_possiveis = [
                        "x_tot",
                        "y_tot",
                        "va_total",
                        "rho_total",
                        "phi_total",
                        "deltav2_total",
                        "L_total",
                        "Pdin_total",
                        "num_alpha_array",
                        "den_alpha_array",
                    ]
                    colunas_validas = []
                    arrays_para_empilhar = []
                    tamanho_alvo = len(dados["x_tot"]) if "x_tot" in dados else 0
                    for k in colunas_possiveis:
                        if k in dados:
                            v = dados[k]
                            if isinstance(v, np.ndarray) and v.size == tamanho_alvo:
                                colunas_validas.append(k)
                                arrays_para_empilhar.append(v)
                    f.write(",".join(colunas_validas) + "\n")
                    if arrays_para_empilhar:
                        matriz = np.column_stack(arrays_para_empilhar)
                        np.savetxt(f, matriz, delimiter=",", fmt="%.8e")
                self.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Export Success",
                        f"Dataset successfully exported to:\n{export_path}",
                    ),
                )
            except Exception as e:
                self.after(
                    0,
                    lambda: messagebox.showerror(
                        "Export Failed", f"An error occurred during extraction:\n{e}"
                    ),
                )
            finally:
                self.after(0, lambda: self.btn_export.configure(state="normal"))

        import threading

        threading.Thread(target=tarefa_exportacao, daemon=True).start()

    #
    # * ╭────────────────────────────────────────────────────────────────────────────╮
    # * │   Gestão Dinâmica de Perfis (JSON)                                         │
    # * ╰────────────────────────────────────────────────────────────────────────────╯
    #
    def save_profile(self):
        filepath = filedialog.asksaveasfilename(
            initialdir=os.path.join(os.getcwd(), "data"),
            title="Save Input Profile",
            defaultextension=".json",
            filetypes=[("ASTRAEOS Profile", "*.json"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        try:
            data = {
                "star": {
                    "nome": self.app_state.nome.get(),
                    "Mstar": self.app_state.Mstar.get(),
                    "Rstar": self.app_state.Rstar.get(),
                    "Teff": self.app_state.Teff.get(),
                    "Lstar": self.app_state.Lstar.get(),
                    "T": self.app_state.T.get(),
                    "rho0": self.app_state.rho0.get(),
                    "B0": self.app_state.B0.get(),
                    "mu": self.app_state.mu.get(),
                },
                "wave": {
                    "S_divergencia": self.app_state.S_divergencia.get(),
                    "F": self.app_state.F.get(),
                    "deltav0": self.app_state.deltav0.get(),
                    "phi0": self.app_state.phi0.get(),
                    "L0": self.app_state.L0.get(),
                    "cte": self.app_state.cte.get(),
                    "parker": self.app_state.parker.get(),
                },
                "numeric": {
                    "x_sim": self.app_state.x_sim.get(),
                    "h_rk": self.app_state.h_rk.get(),
                    "u0_ini": self.app_state.u0_ini.get(),
                    "u0_step": self.app_state.u0_step.get(),
                    "tamanho_pulo": self.app_state.tamanho_pulo.get(),
                    "recuo_pulo": self.app_state.recuo_pulo.get(),
                },
                "exoplanet": {
                    "exoplanet_name": self.app_state.exoplanet_name.get(),
                    "Dorb": self.app_state.Dorb.get(),
                    "e": self.app_state.e.get(),
                    "Ab": self.app_state.Ab.get(),
                    "Rplan": self.app_state.Rplan.get(),
                    "Mmag": self.app_state.Mmag.get(),
                    "f0": self.app_state.f0.get(),
                    "k_cme": self.app_state.k_cme.get(),
                    "hion": self.app_state.hion.get(),
                },
                "plot": {
                    "sigma_ini": self.app_state.sigma_ini.get(),
                    "sigma_fim": self.app_state.sigma_fim.get(),
                    "sigma_nome": self.app_state.sigma_nome.get(),
                    "sigma_cor": self.app_state.sigma_cor.get(),
                    "axis_x": self.app_state.axis["X Axis"].get(),
                    "axis_y": self.app_state.axis["Y Axis"].get(),
                    "x_un": self.app_state.units["x_un"].get(),
                    "y_un": self.app_state.units["y_un"].get(),
                    "refs": [
                        {
                            "x": r["x"].get(),
                            "nome": r["nome"].get(),
                            "cor": r["cor"].get(),
                            "estilo": r["estilo"].get(),
                        }
                        for r in self.app_state.refs
                    ],
                },
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving profile: {e}")

    def load_profile(self):
        filepath = filedialog.askopenfilename(
            initialdir=os.path.join(os.getcwd(), "data"),
            title="Load Input Profile",
            filetypes=[("ASTRAEOS Profile", "*.json"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        self._load_from_filepath(filepath)

    def _load_from_filepath(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            mapping = {
                "star": [
                    "nome",
                    "Mstar",
                    "Rstar",
                    "Teff",
                    "Lstar",
                    "T",
                    "rho0",
                    "B0",
                    "mu",
                ],
                "wave": [
                    "S_divergencia",
                    "F",
                    "deltav0",
                    "phi0",
                    "L0",
                    "cte",
                    "parker",
                ],
                "numeric": [
                    "x_sim",
                    "h_rk",
                    "u0_ini",
                    "u0_step",
                    "tamanho_pulo",
                    "recuo_pulo",
                ],
                "exoplanet": [
                    "exoplanet_name",
                    "Dorb",
                    "e",
                    "Ab",
                    "Rplan",
                    "Mmag",
                    "f0",
                    "k_cme",
                    "hion",
                ],
            }
            for group, keys in mapping.items():
                if group in data:
                    for key in keys:
                        if key in data[group]:
                            getattr(self.app_state, key).set(data[group][key])
            if "plot" in data:
                p = data["plot"]
                if "sigma_ini" in p:
                    self.app_state.sigma_ini.set(p["sigma_ini"])
                if "sigma_fim" in p:
                    self.app_state.sigma_fim.set(p["sigma_fim"])
                if "sigma_nome" in p:
                    self.app_state.sigma_nome.set(p["sigma_nome"])
                if "sigma_cor" in p:
                    self.app_state.sigma_cor.set(p["sigma_cor"])
                if "axis_x" in p:
                    self.app_state.axis["X Axis"].set(p["axis_x"])
                if "axis_y" in p:
                    self.app_state.axis["Y Axis"].set(p["axis_y"])
                if "x_un" in p:
                    self.app_state.units["x_un"].set(p["x_un"])
                if "y_un" in p:
                    self.app_state.units["y_un"].set(p["y_un"])
                if "refs" in p:
                    for i, r in enumerate(p["refs"]):
                        if i < len(self.app_state.refs):
                            self.app_state.refs[i]["x"].set(r.get("x", ""))
                            self.app_state.refs[i]["nome"].set(r.get("nome", ""))
                            self.app_state.refs[i]["cor"].set(r.get("cor", ""))
                            self.app_state.refs[i]["estilo"].set(r.get("estilo", "-"))
        except Exception as e:
            print(f"Error loading profile: {e}")

    #
    # * ╭────────────────────────────────────────────────────────────────────────────╮
    # * │   Construtores de Abas (Estrela)                                           │
    # * ╰────────────────────────────────────────────────────────────────────────────╯
    #
    def _construir_aba_astro(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        campos = [
            (0, "Target Name:", self.app_state.nome, ""),
            (1, "Stellar Mass ( M★ ) :", self.app_state.Mstar, "[ M⊙ ]"),
            (2, "Stellar Radius ( R★ ) :", self.app_state.Rstar, "[ R⊙ ]"),
            (3, "Effective Temperature ( Teff ) :", self.app_state.Teff, "[ K ]"),
            (4, "Stellar Luminosity ( L★ ) :", self.app_state.Lstar, "[ L⊙ ]"),
            (5, "Coronal Temperature ( T ) :", self.app_state.T, "[ K ]"),
            (6, "Coronal Base Density ( ρ₀ ) :", self.app_state.rho0, "[ g/cm³ ]"),
            (7, "Surface Magnetic Field ( B₀ ) :", self.app_state.B0, "[ G ]"),
            (8, "Mean Molecular Weight ( μ ) :", self.app_state.mu, "[ adm ]"),
        ]
        for linha, texto, var, uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            entry = ctk.CTkEntry(aba, textvariable=var, font=fonte_var)
            entry.grid(row=linha, column=1, padx=(10, 0), pady=5, sticky="sw")
            if var == self.app_state.B0:
                self.parker_disabled_inputs.append(entry)
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0, 50), pady=5, sticky="w"
            )
        linha_atual = len(campos)
        linha_atual += 1
        ctk.CTkLabel(
            aba,
            text="Stellar Catalog (Presets)",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#E5C07B",
        ).grid(
            row=linha_atual, column=0, columnspan=3, pady=(25, 5), sticky="w", padx=20
        )
        presets_dir = PRESETS_PATH
        try:
            os.makedirs(presets_dir, exist_ok=True)
        except OSError:
            pass

        if os.path.exists(presets_dir):
            arquivos_json = [f for f in os.listdir(presets_dir) if f.endswith(".json")]
        else:
            arquivos_json = []

        if not arquivos_json:
            linha_atual += 1
            ctk.CTkLabel(
                aba,
                text="No .json presets found in 'presets/' folder.",
                font=fonte_var,
                text_color="#5c6269",
            ).grid(row=linha_atual, column=0, columnspan=3, padx=30, pady=5, sticky="w")
        else:
            for arquivo in arquivos_json:
                linha_atual += 1
                nome_preset = arquivo.replace(".json", "")
                frame_preset = ctk.CTkFrame(aba, fg_color="transparent")
                frame_preset.grid(
                    row=linha_atual,
                    column=0,
                    columnspan=3,
                    sticky="ew",
                    padx=30,
                    pady=2,
                )
                frame_preset.grid_columnconfigure(1, weight=1)
                lbl_seta = ctk.CTkLabel(
                    frame_preset, text="➤", font=fonte_var, text_color="#61AFEF"
                )
                lbl_seta.grid(row=0, column=0, sticky="w", padx=(0, 10))
                lbl_nome = ctk.CTkLabel(
                    frame_preset, text=nome_preset, font=fonte_var, text_color="#ABB2BF"
                )
                lbl_nome.grid(row=0, column=1, sticky="w")
                caminho_completo = os.path.join(presets_dir, arquivo)

                def carregar(caminho=caminho_completo):
                    self._load_from_filepath(caminho)

                btn_load = ctk.CTkButton(
                    frame_preset,
                    text="Load",
                    width=50,
                    height=24,
                    fg_color="#282C34",
                    hover_color="#1F618D",
                    border_width=1,
                    border_color="#61AFEF",
                    text_color="#61AFEF",
                    font=fonte_var,
                    command=carregar,
                )
                btn_load.grid(row=0, column=2, sticky="e")
        aba.grid_rowconfigure(linha_atual + 1, weight=1, minsize=10)

    def _construir_aba_onda(self, aba):
        aba.grid_columnconfigure(0, weight=0, minsize=200)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)

        # ====================================================================
        # WIDGET DO GRÁFICO DINÂMICO (NO TOPO)
        # ====================================================================
        self.frame_geom = ctk.CTkFrame(
            aba, fg_color="#1E1E1E", corner_radius=8, height=160
        )
        self.frame_geom.grid(
            row=0, column=0, columnspan=3, padx=20, pady=(10, 15), sticky="ew"
        )
        self.frame_geom.pack_propagate(False)

        self.lbl_geom_wait = ctk.CTkLabel(
            self.frame_geom,
            text="Loading Geometry...",
            text_color="#5c5c5c",
            font=("Consolas", 14, "italic"),
        )
        self.lbl_geom_wait.place(relx=0.5, rely=0.5, anchor="center")
        self.update_timer = None

        def update_live_geometry(*args):
            if self.update_timer:
                self.after_cancel(self.update_timer)
            self.update_timer = self.after(500, perform_update)

        def perform_update():
            try:
                s_val = float(self.app_state.S_divergencia.get())
                f_val = float(self.app_state.F.get())
            except ValueError:
                return

            try:
                from astraeos_core.plot_curve import plot_preview_wind

                fig_geom = plot_preview_wind(F_val=f_val, S_val=s_val, theme="dark")

                for widget in self.frame_geom.winfo_children():
                    widget.destroy()

                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

                canvas = FigureCanvasTkAgg(fig_geom, master=self.frame_geom)
                tk_widget = canvas.get_tk_widget()
                tk_widget.configure(bg="#1E1E1E", highlightthickness=0)
                tk_widget.pack(side="top", fill="both", expand=True)

                import matplotlib.pyplot as plt

                plt.close(fig_geom)
            except Exception:
                pass
            caixa_S.focus_set()

        self.app_state.S_divergencia.trace_add("write", update_live_geometry)
        self.app_state.F.trace_add("write", update_live_geometry)

        self.app_state.S_divergencia.trace_add("write", update_live_geometry)
        self.app_state.F.trace_add("write", update_live_geometry)
        self.after(300, update_live_geometry)

        # ====================================================================
        # INPUTS DA ABA (ABAIXO DO GRÁFICO)
        # ====================================================================
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (1, "Expansion Factor ( S ) :", self.app_state.S_divergencia, "[ adm ]"),
            (2, "Transition Factor ( F ) :", self.app_state.F, "[ adm ]"),
            (
                3,
                "Initial Wave Amplitude ( Δv₀² ) :",
                self.app_state.deltav0,
                "[ ve0² ]",
            ),
            (4, "Initial Alfvén Flux ( φ₀ ) :", self.app_state.phi0, "[ erg/cm²/s ]"),
            (5, "Damping Length ( L₀ ) :", self.app_state.L0, "[ R★ ]"),
        ]

        for linha, texto, var, uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            entry = ctk.CTkEntry(aba, textvariable=var, font=fonte_var)
            entry.grid(row=linha, column=1, padx=(10, 0), pady=5, sticky="sw")
            self.parker_disabled_inputs.append(entry)
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0, 10), pady=5, sticky="w"
            )
            aba.grid_rowconfigure(linha, weight=1, minsize=10)
            caixa_S = self.parker_disabled_inputs[0]

        ctk.CTkLabel(aba, text="Damping Model:", font=fonte, text_color="#E5C07B").grid(
            row=6, column=0, padx=20, pady=15, sticky="w"
        )

        def on_combo_change(choice):
            if choice == "Ressonant":
                self.app_state.cte.set(False)
                self.app_state.parker.set(False)
            elif choice == "Constant":
                self.app_state.cte.set(True)
                self.app_state.parker.set(False)
            elif choice == "Undamped (Parker)":
                self.app_state.cte.set(False)
                self.app_state.parker.set(True)

        combo_damping = ctk.CTkComboBox(
            aba,
            values=["Ressonant", "Constant", "Undamped (Parker)"],
            font=fonte_var,
            state="readonly",
            command=on_combo_change,
        )
        combo_damping.grid(row=6, column=1, padx=(10, 0), pady=15, sticky="sw")

        def sync_combo_damping(*args):
            try:
                is_cte = self.app_state.cte.get()
                is_parker = self.app_state.parker.get()
                if is_parker:
                    combo_damping.set("Undamped (Parker)")
                    self.set_parker_inputs_state("disabled")
                elif is_cte:
                    combo_damping.set("Constant")
                    self.set_parker_inputs_state("normal")
                else:
                    combo_damping.set("Ressonant")
                    self.set_parker_inputs_state("normal")
            except Exception:
                pass

        self.app_state.cte.trace_add("write", sync_combo_damping)
        self.app_state.parker.trace_add("write", sync_combo_damping)
        sync_combo_damping()

    def _construir_aba_numerico(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)

        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (0, "Simulation Distance :", self.app_state.x_sim, "[ R★ ]"),
            (1, "Integration Step :", self.app_state.h_rk, "[ R★ ]"),
            (
                2,
                "Base Velocity Search - Lower Limit :",
                self.app_state.u0_ini,
                "[ ve0 ]",
            ),
            (3, "Base Velocity Search - Step :", self.app_state.u0_step, "[ ve0 ]"),
            (4, "Critical Point Jump Size :", self.app_state.tamanho_pulo, "[ R★ ]"),
            (5, "Topology Backtrack Steps :", self.app_state.recuo_pulo, "[ 1e-5 R★ ]"),
        ]

        for linha, texto, var, uni in campos:
            ctk.CTkLabel(aba, text=texto, font=fonte, text_color="#E5C07B").grid(
                row=linha, column=0, padx=20, pady=5, sticky="w"
            )
            ctk.CTkEntry(aba, textvariable=var, font=fonte_var).grid(
                row=linha, column=1, padx=(10, 0), pady=5, sticky="sw"
            )
            ctk.CTkLabel(aba, text=uni, font=fonte_uni, text_color="#8b949e").grid(
                row=linha, column=2, padx=(0, 50), pady=5, sticky="w"
            )
            # Removemos o weight=1 daqui para não esticar as linhas
            aba.grid_rowconfigure(linha, weight=0)

        linha_atual = len(campos)

        def toggle_tol():
            if self.app_state.checkautotol.get():
                entry_tol.configure(
                    state="normal",
                    text_color="white",
                    fg_color="#343638",
                    border_color="#565b5e",
                )
            else:
                entry_tol.configure(
                    state="disabled",
                    text_color="#3c4044",
                    fg_color="#1E1E1E",
                    border_color="#282C34",
                )

        cb_optimize = ctk.CTkCheckBox(
            aba,
            text="Optimize Guess",
            variable=self.app_state.checkautotol,
            font=fonte,
            text_color="#E5C07B",
            checkbox_width=18,
            checkbox_height=18,
            border_width=1.5,
            corner_radius=3,
            border_color="#5C6370",
            hover_color="#2C313A",
            fg_color="#282C34",
            checkmark_color="#E5C07B",
            command=toggle_tol,
        )
        cb_optimize.grid(row=linha_atual, column=0, padx=20, pady=(15, 5), sticky="w")
        ToolTip(
            cb_optimize,
            "Optimize the initial guess for the velocity profile.\n\n"
            "The algorithm repeatedly updates the profile to converge toward the ideal \n"
            "initial value, stopping once the user-defined tolerance is reached.\n\n"
            "Lower tolerance values will require more iterations and increase computation time.",
        )

        frame_tol = ctk.CTkFrame(aba, fg_color="transparent")
        frame_tol.grid(
            row=linha_atual,
            column=1,
            columnspan=2,
            padx=(10, 0),
            pady=(15, 5),
            sticky="sw",
        )

        ctk.CTkLabel(
            frame_tol, text="Tolerance:", font=fonte, text_color="#E5C07B"
        ).pack(side="left", padx=(0, 10))
        entry_tol = ctk.CTkEntry(
            frame_tol, textvariable=self.app_state.autotol, font=fonte_var, width=80
        )
        entry_tol.pack(side="left")
        ctk.CTkLabel(
            frame_tol, text="[ ve0 ]", font=fonte_uni, text_color="#8b949e"
        ).pack(side="left", padx=(10, 0))

        self.after(100, toggle_tol)
        aba.grid_rowconfigure(linha_atual, weight=0)
        aba.grid_rowconfigure(linha_atual + 1, weight=1)

    def _construir_aba_gp(self, aba):
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        headers = ["Distance [R★]", "Label", "Color [Hex]", "Line Style"]
        for col, text in enumerate(headers):
            aba.grid_columnconfigure(col, weight=1)
            ctk.CTkLabel(aba, text=text, font=fonte, text_color="#E5C07B").grid(
                row=0, column=col, pady=(5, 5)
            )
        for i, ref in enumerate(self.app_state.refs):
            row = i + 1
            ctk.CTkEntry(
                aba, textvariable=ref["x"], font=fonte_var, width=65, justify="center"
            ).grid(row=row, column=0, padx=5, pady=5)
            ctk.CTkEntry(
                aba,
                textvariable=ref["nome"],
                font=fonte_var,
                width=65,
                justify="center",
            ).grid(row=row, column=1, padx=5, pady=5)
            ctk.CTkEntry(aba, textvariable=ref["cor"], width=80, justify="center").grid(
                row=row, column=2, padx=5, pady=5
            )
            estilos = ["-", "--", "-.", ":"]
            ctk.CTkComboBox(
                aba,
                variable=ref["estilo"],
                font=fonte_var,
                values=estilos,
                width=70,
                state="readonly",
            ).grid(row=row, column=3, padx=5, pady=5)

            def make_clear_cmd(r=ref):
                def clear():
                    r["x"].set("")
                    r["nome"].set("")
                    r["cor"].set("")
                    r["estilo"].set("-")

                return clear

            btn_clear = ctk.CTkButton(
                aba,
                text="" if self.img_cancel else "X",
                image=self.img_cancel,
                width=28,
                height=28,
                fg_color="#282C34",
                hover_color="#75353A",
                command=make_clear_cmd(),
            )
            btn_clear.grid(row=row, column=4, padx=5, pady=5)
        row_offset = len(self.app_state.refs) + 1
        frame_sigma_header = ctk.CTkFrame(aba, fg_color="transparent")
        frame_sigma_header.grid(row=row_offset, column=0, columnspan=5, pady=(10, 5))
        ctk.CTkLabel(
            frame_sigma_header, text="Sigma Zone", font=fonte, text_color="#E5C07B"
        ).pack(side="left", padx=(0, 10))

        def clear_sigma():
            self.app_state.sigma_ini.set("")
            self.app_state.sigma_fim.set("")
            self.app_state.sigma_nome.set("")
            self.app_state.sigma_cor.set("")

        btn_clear_sigma = ctk.CTkButton(
            frame_sigma_header,
            text="" if self.img_cancel else "X",
            image=self.img_cancel,
            width=24,
            height=24,
            fg_color="#282C34",
            hover_color="#75353A",
            command=clear_sigma,
        )
        btn_clear_sigma.pack(side="left")
        frame_sigma = ctk.CTkFrame(aba, fg_color="transparent")
        frame_sigma.grid(row=row_offset + 1, column=0, columnspan=5, pady=5)
        ctk.CTkLabel(frame_sigma, text="From:").grid(row=0, column=0, padx=5)
        ctk.CTkEntry(
            frame_sigma, textvariable=self.app_state.sigma_ini, font=fonte_var, width=55
        ).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_sigma, text="To:").grid(row=0, column=2, padx=(15, 5))
        ctk.CTkEntry(
            frame_sigma, textvariable=self.app_state.sigma_fim, font=fonte_var, width=55
        ).grid(row=0, column=3, padx=5)
        ctk.CTkLabel(frame_sigma, text="Label:").grid(row=0, column=4, padx=(15, 5))
        ctk.CTkEntry(
            frame_sigma,
            textvariable=self.app_state.sigma_nome,
            font=fonte_var,
            width=50,
        ).grid(row=0, column=5, padx=5)
        ctk.CTkLabel(frame_sigma, text="Color:").grid(row=0, column=6, padx=(15, 5))
        ctk.CTkEntry(
            frame_sigma, textvariable=self.app_state.sigma_cor, font=fonte_var, width=75
        ).grid(row=0, column=7, padx=5)
        row_offset += 2
        ctk.CTkLabel(aba, text="Axis Scales", font=fonte, text_color="#E5C07B").grid(
            row=row_offset, column=0, columnspan=5, pady=(10, 5)
        )
        frame_axis = ctk.CTkFrame(aba, fg_color="transparent")
        frame_axis.grid(row=row_offset + 1, column=0, columnspan=5, pady=5)
        estilos_escala = ["log", "linear"]
        ctk.CTkLabel(frame_axis, text="X Axis Scale:").grid(row=0, column=0, padx=5)
        ctk.CTkComboBox(
            frame_axis,
            variable=self.app_state.axis["X Axis"],
            font=fonte_var,
            values=estilos_escala,
            width=100,
            state="readonly",
        ).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_axis, text="Y Axis Scale:").grid(
            row=0, column=2, padx=(30, 5)
        )
        ctk.CTkComboBox(
            frame_axis,
            variable=self.app_state.axis["Y Axis"],
            font=fonte_var,
            values=estilos_escala,
            width=100,
            state="readonly",
        ).grid(row=0, column=3, padx=5)
        row_offset += 2
        ctk.CTkLabel(aba, text="Axis Units", font=fonte, text_color="#E5C07B").grid(
            row=row_offset, column=0, columnspan=5, pady=(10, 5)
        )
        frame_units = ctk.CTkFrame(aba, fg_color="transparent")
        frame_units.grid(row=row_offset + 1, column=0, columnspan=5, pady=5)
        ctk.CTkLabel(frame_units, text="X Axis Unit:").grid(row=0, column=0, padx=5)

        def on_x_unit_change(choice):
            self.app_state.units["x_un"].set("r" if choice == "AU" else "r/r0")

        combo_x_unit = ctk.CTkComboBox(
            frame_units,
            values=["Normalized", "AU"],
            font=fonte_var,
            width=130,
            state="readonly",
            command=on_x_unit_change,
        )
        combo_x_unit.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(frame_units, text="Y Axis Unit:").grid(
            row=0, column=2, padx=(30, 5)
        )

        def on_y_unit_change(choice):
            self.app_state.units["y_un"].set("u" if choice == "km/s" else "u/ve0")

        combo_y_unit = ctk.CTkComboBox(
            frame_units,
            values=["Normalized", "km/s"],
            font=fonte_var,
            width=130,
            state="readonly",
            command=on_y_unit_change,
        )
        combo_y_unit.grid(row=0, column=3, padx=5)

        def sync_combo_units(*args):
            try:
                x_val = self.app_state.units["x_un"].get()
                y_val = self.app_state.units["y_un"].get()
                combo_x_unit.set("AU" if x_val == "r" else "Normalized")
                combo_y_unit.set("km/s" if y_val == "u" else "Normalized")
            except Exception:
                pass

        self.app_state.units["x_un"].trace_add("write", sync_combo_units)
        self.app_state.units["y_un"].trace_add("write", sync_combo_units)
        sync_combo_units()
        row_offset += 2
        self.btn_update_plot = ctk.CTkButton(
            aba,
            text="Update Plot",
            command=self.iniciar_replot,
            fg_color="#5C7174",
            state="disabled",
            height=25,
        )
        self.btn_update_plot.grid(
            row=row_offset, column=0, columnspan=5, pady=(20, 10), sticky="ew"
        )

    #
    # * ╭────────────────────────────────────────────────────────────────────────────╮
    # * │   Construtores de Abas (Exoplanetas)                                       │
    # * ╰────────────────────────────────────────────────────────────────────────────╯
    #
    def _construir_aba_orbita(self, aba):
        aba.grid_columnconfigure(0, weight=0, minsize=180)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=3)
        aba.grid_columnconfigure(3, weight=0, minsize=50)
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        ctk.CTkLabel(
            aba, text="Exoplanet Designation:", font=fonte, text_color="#E5C07B"
        ).grid(row=0, column=0, padx=20, pady=5, sticky="w")
        entry_nome_exo = ctk.CTkEntry(
            aba, textvariable=self.app_state.exoplanet_name, font=fonte_var
        )
        entry_nome_exo.grid(
            row=0, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we"
        )
        self.exo_inputs.append(entry_nome_exo)
        ctk.CTkLabel(
            aba, text="Orbital Distance ( Dorb ) :", font=fonte, text_color="#E5C07B"
        ).grid(row=1, column=0, padx=20, pady=5, sticky="w")
        entry_dorb = ctk.CTkEntry(
            aba, textvariable=self.app_state.Dorb, font=fonte_var, width=80
        )
        entry_dorb.grid(row=1, column=1, padx=(10, 5), pady=5, sticky="w")
        self.exo_inputs.append(entry_dorb)
        try:
            valor_minimo = float(self.app_state.Rstar.get()) * rsunAU
            valor_maximo = (
                float(self.app_state.x_sim.get())
                * float(self.app_state.Rstar.get())
                * rsunAU
            )
        except ValueError:
            valor_minimo = 0.001
            valor_maximo = 0.100
        self.slider_dorb = ctk.CTkSlider(
            aba,
            from_=valor_minimo,
            to=valor_maximo,
            height=8,
            button_length=12,
            button_color="#61AFEF",
            button_hover_color="#56B6C2",
            progress_color="#1F618D",
            command=lambda v: self.app_state.Dorb.set(f"{v:.5f}"),
        )
        self.slider_dorb.grid(row=1, column=2, padx=(5, 10), pady=5, sticky="we")
        self.exo_inputs.append(self.slider_dorb)
        ctk.CTkLabel(aba, text=" [ AU ]", font=fonte_uni, text_color="#8b949e").grid(
            row=1, column=3, padx=(0, 20), pady=5, sticky="w"
        )

        def update_dorb_slider(*args):
            try:
                self.slider_dorb.set(float(self.app_state.Dorb.get()))
            except ValueError:
                pass

        self.app_state.Dorb.trace_add("write", update_dorb_slider)
        update_dorb_slider()
        ctk.CTkLabel(
            aba, text="Orbital Eccentricity ( e ) :", font=fonte, text_color="#E5C07B"
        ).grid(row=2, column=0, padx=20, pady=5, sticky="w")
        entry_e = ctk.CTkEntry(aba, textvariable=self.app_state.e, font=fonte_var)
        entry_e.grid(row=2, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we")
        self.exo_inputs.append(entry_e)
        ctk.CTkLabel(aba, text="  [ adm ]", font=fonte_uni, text_color="#8b949e").grid(
            row=2, column=3, padx=(0, 20), pady=5, sticky="w"
        )
        ctk.CTkLabel(
            aba, text="Bond Albedo ( Ab ) :", font=fonte, text_color="#E5C07B"
        ).grid(row=3, column=0, padx=20, pady=5, sticky="w")
        entry_ab = ctk.CTkEntry(aba, textvariable=self.app_state.Ab, font=fonte_var)
        entry_ab.grid(row=3, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we")
        self.exo_inputs.append(entry_ab)
        ctk.CTkLabel(aba, text="  [ adm ]", font=fonte_uni, text_color="#8b949e").grid(
            row=3, column=3, padx=(0, 20), pady=5, sticky="w"
        )

    def _construir_aba_magnet(self, aba):
        aba.grid_columnconfigure(0, weight=0, minsize=200)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=3)
        aba.grid_columnconfigure(3, weight=0, minsize=50)
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        ctk.CTkLabel(
            aba, text="Planetary Radius ( Rₚ ) :", font=fonte, text_color="#E5C07B"
        ).grid(row=0, column=0, padx=20, pady=5, sticky="w")
        entry_rplan = ctk.CTkEntry(
            aba, textvariable=self.app_state.Rplan, font=fonte_var
        )
        entry_rplan.grid(
            row=0, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we"
        )
        self.exo_inputs.append(entry_rplan)
        ctk.CTkLabel(aba, text="  [ R⊕ ]", font=fonte_uni, text_color="#8b949e").grid(
            row=0, column=3, padx=(0, 20), pady=5, sticky="w"
        )
        ctk.CTkLabel(
            aba,
            text="Magnetic Dipole Moment ( Mmag ) :",
            font=fonte,
            text_color="#E5C07B",
        ).grid(row=1, column=0, padx=20, pady=5, sticky="w")
        entry_mmag = ctk.CTkEntry(
            aba, textvariable=self.app_state.Mmag, font=fonte_var, width=80
        )
        entry_mmag.grid(row=1, column=1, padx=(10, 5), pady=5, sticky="w")
        self.exo_inputs.append(entry_mmag)
        slider_mmag = ctk.CTkSlider(
            aba,
            from_=1e21,
            to=1e23,
            height=8,
            button_length=12,
            button_color="#61AFEF",
            button_hover_color="#56B6C2",
            progress_color="#1F618D",
            command=lambda v: self.app_state.Mmag.set(f"{v:.2e}"),
        )
        slider_mmag.grid(row=1, column=2, padx=(5, 10), pady=5, sticky="we")
        self.exo_inputs.append(slider_mmag)
        ctk.CTkLabel(aba, text="  [ Am² ]", font=fonte_uni, text_color="#8b949e").grid(
            row=1, column=3, padx=(0, 20), pady=5, sticky="w"
        )

        def update_mmag_slider(*args):
            try:
                slider_mmag.set(float(self.app_state.Mmag.get()))
            except ValueError:
                pass

        self.app_state.Mmag.trace_add("write", update_mmag_slider)
        update_mmag_slider()
        ctk.CTkLabel(
            aba,
            text="Chapman-Ferraro Factor ( f₀ ) :",
            font=fonte,
            text_color="#E5C07B",
        ).grid(row=2, column=0, padx=20, pady=5, sticky="w")
        entry_f0 = ctk.CTkEntry(aba, textvariable=self.app_state.f0, font=fonte_var)
        entry_f0.grid(row=2, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we")
        self.exo_inputs.append(entry_f0)
        ctk.CTkLabel(aba, text="  [ adm ]", font=fonte_uni, text_color="#8b949e").grid(
            row=2, column=3, padx=(0, 20), pady=5, sticky="w"
        )
        ctk.CTkLabel(
            aba, text="Compression Factor ( k ):", font=fonte, text_color="#E5C07B"
        ).grid(row=3, column=0, padx=20, pady=5, sticky="w")
        entry_k_cme = ctk.CTkEntry(
            aba, textvariable=self.app_state.k_cme, font=fonte_var
        )
        entry_k_cme.grid(
            row=3, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we"
        )
        self.exo_inputs.append(entry_k_cme)
        ctk.CTkLabel(aba, text="  [ adm ]", font=fonte_uni, text_color="#8b949e").grid(
            row=3, column=3, padx=(0, 20), pady=5, sticky="w"
        )
        ctk.CTkLabel(
            aba, text="Ionosphere Height ( hion ):", font=fonte, text_color="#E5C07B"
        ).grid(row=4, column=0, padx=20, pady=5, sticky="w")
        entry_hion = ctk.CTkEntry(aba, textvariable=self.app_state.hion, font=fonte_var)
        entry_hion.grid(
            row=4, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we"
        )
        self.exo_inputs.append(entry_hion)
        ctk.CTkLabel(aba, text="  [ km ]", font=fonte_uni, text_color="#8b949e").grid(
            row=4, column=3, padx=(0, 20), pady=5, sticky="w"
        )

    #
    # * ╭────────────────────────────────────────────────────────────────────────────╮
    # * │   Lógica Dinâmica da Interface e Ações de Controle                         │
    # * ╰────────────────────────────────────────────────────────────────────────────╯
    #
    def _alterar_visual_widget(self, widget, state_str):
        widget.configure(state=state_str)
        if isinstance(widget, ctk.CTkEntry):
            if state_str == "disabled":
                widget.configure(
                    text_color="#3c4044", border_color="#282C34", fg_color="#1E1E1E"
                )
            else:
                widget.configure(
                    text_color="white", border_color="#565b5e", fg_color="#343638"
                )
        elif isinstance(widget, ctk.CTkSlider):
            if state_str == "disabled":
                widget.configure(
                    button_color="#282C34",
                    progress_color="#282C34",
                    button_hover_color="#282C34",
                )
            else:
                widget.configure(
                    button_color="#61AFEF",
                    progress_color="#1F618D",
                    button_hover_color="#56B6C2",
                )

    def set_exoplanet_state(self, state_str):
        for widget in self.exo_inputs:
            self._alterar_visual_widget(widget, state_str)

    def set_parker_inputs_state(self, state_str):
        for widget in self.parker_disabled_inputs:
            self._alterar_visual_widget(widget, state_str)

    def iniciar_processo(self):
        self.btn_run.configure(state="disabled", text="Calculating...")
        self.on_run_click()

    def iniciar_replot(self):
        self.btn_update_plot.configure(state="disabled", text="Plotting...")
        self.on_update_click()

    def iniciar_sim_exo(self):
        self.btn_sim_exo.configure(state="disabled", text="Plotting...")
        self.on_simulate_exo_click()

    def abortar_processo(self):
        self.btn_abort.configure(state="disabled", text="Aborting...")
        self.on_abort_click()
