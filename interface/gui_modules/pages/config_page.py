# * ============================================
# * Importações
# * ============================================
import tkinter as tk
import customtkinter as ctk
import json
import os
import numpy as np
from tkinter import filedialog, messagebox
from PIL import Image
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "src")
from astraeos_core.utils import *


# * ============================================
# * Componentes de Interface Auxiliares
# * ============================================
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

        self.tooltip_window.wm_geometry(f"+{event.x_root}+{event.y_root}")
        self.tooltip_window.update_idletasks()

        tooltip_width = self.tooltip_window.winfo_reqwidth()
        tooltip_height = self.tooltip_window.winfo_reqheight()

        screen_width = self.tooltip_window.winfo_screenwidth()
        screen_height = self.tooltip_window.winfo_screenheight()

        offset_x = 15
        offset_y = 15
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


# * ============================================
# * Classe Principal: Página de Configuração
# * ============================================
class ConfigPage(ctk.CTkScrollableFrame):
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

        # ? --- Injeção de Dependências ---
        self.app_state = state
        self.on_run_click = on_run_click
        self.on_update_click = on_update_click
        self.on_abort_click = on_abort_click
        self.on_simulate_exo_click = on_simulate_exo_click
        self.assets_path = assets_path
        self.exo_inputs = []  # Lista para guardar os widgets do exoplaneta

        # ? --- Configuração de Layout Principal ---
        self.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, pady=(10, 2), sticky="ew", padx=20)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame, text="Simulation Settings", font=("Consolas", 18, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, sticky="w")

        # Tentativa de carregamento dos assets de botões
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
        except Exception:
            img_load, img_save, img_export, img_about = None, None, None, None

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
        ToolTip(self.btn_load_prof, "Load Input Profile (*.json)")

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
        ToolTip(self.btn_save_prof, "Save Input Profile (*.json)")

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
        ToolTip(
            self.btn_export,
            "Export Data for Analysis\nGenerates a raw scientific dataset (*.csv) from the current simulation.",
        )

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
        ToolTip(
            self.btn_about,
            "About ASTRAEOS\nObjective, Architecture, and Acknowledgments.",
        )

        self.tabview = ctk.CTkTabview(self, height=250)
        self.tabview.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        aba_astro = self.tabview.add("Star & Corona")
        aba_onda = self.tabview.add("Wind & Wave")
        aba_num = self.tabview.add("Numerical Setup")
        aba_gp = self.tabview.add("Plot Preferences")
        aba_more = self.tabview.add("More Options")

        self._construir_aba_astro(aba_astro)
        self._construir_aba_onda(aba_onda)
        self._construir_aba_numerico(aba_num)
        self._construir_aba_gp(aba_gp)
        self._construir_aba_more(aba_more)

        self.lbl_exo = ctk.CTkLabel(
            self,
            text="Exoplanet Settings",
            font=("Consolas", 18, "bold"),
        )
        self.lbl_exo.grid(row=2, column=0, pady=(15, 2), sticky="w", padx=20)

        self.tabview_exo = ctk.CTkTabview(self, height=180)
        self.tabview_exo.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        aba_orbita = self.tabview_exo.add("Orbit & Habitability")
        aba_magnet = self.tabview_exo.add("Magnetosphere")

        self._construir_aba_orbita(aba_orbita)
        self._construir_aba_magnet(aba_magnet)

        self.btn_sim_exo = ctk.CTkButton(
            self,
            text="Simulate Exoplanet",
            command=self.iniciar_sim_exo,
            fg_color="#627683",
            hover_color="#404C55",
            font=("Consolas", 14, "bold"),
            height=25,
            state="disabled",  # IMPEDE CLIQUE ANTES DA PRIMEIRA SIMULAÇÃO
        )
        self.btn_sim_exo.grid(row=4, column=0, padx=20, pady=(5, 20), sticky="ew")

        # ? --- Rodapé e Botões de Controle da Estrela ---
        self.frame_rodape = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_rodape.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="ew")
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

        # Força os inputs do exoplaneta a começarem bloqueados
        self.set_exoplanet_state("disabled")

    # * ============================================
    # * Ferramentas de Dados (Export & About)
    # * ============================================
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

        conteudo = (
            "ASTRAEOS - Astrophysical Stellar Wind and Exoplanet Environment Simulator\n"
            "Version: v0.1.0\n"
            "Developer: Victor M. Acacio\n\n"
            "■ Objective:\n"
            "A highly customizable suite for Magnetohydrodynamic (MHD) modeling of stellar winds "
            "in late-type stars (e.g., M-dwarfs) and analyzing their direct impact on exoplanet habitability "
            "and magnetospheric boundaries.\n\n"
            "■ Methods & Framework:\n"
            "Powered by a robust Runge-Kutta (RK4) integrator coupled with dynamic critical point topology resolution "
            "(L'Hôpital limits) in Julia. The software incorporates classical and Kopparapu habitable zones, "
            "alongside Chapman-Ferraro standoff calculations.\n\n"
            "■ Open Science & Reproducibility:\n"
            "ASTRAEOS is built with a strong commitment to open reproducible research. All arrays and variables "
            "are fully exportable for independent statistical analysis and plotting via external engines like R or Python.\n\n"
            "■ Acknowledgments:\n"
            "Developed at the Institute of Astronomy, Geophysics and Atmospheric Sciences (IAG/USP). "
            "Special thanks to the academic guidance of Profa. Dra. Vera Jatenco Silva Pereira."
        )
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
                # allow_pickle=True é essencial para carregar strings/listas salvas no npz
                dados = np.load(filepath_npz, allow_pickle=True)

                # Função auxiliar para extrair escalares com segurança
                def val(key):
                    if key in dados:
                        v = dados[key]
                        if isinstance(v, np.ndarray) and v.size == 1:
                            return v.item()
                        return v
                    return "N/A"

                with open(export_path, "w", encoding="utf-8") as f:
                    # =======================================================
                    # Cabeçalho Físico Analítico (Incluindo TODOS os metadados)
                    # =======================================================
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
                        f"# Expansion Factor (S): {val('S_divergencia')} | Initial Wave Amp (dv0^2): {val('deltav0')}\n"
                    )
                    f.write(
                        f"# Initial Flux (phi0): {val('phi0')} | Damping Length (L0): {val('L0')} | Constant Damping: {val('cte')}\n"
                    )

                    f.write("#\n# [ 3. NUMERICAL SETUP & TOPOLOGY ]\n")
                    f.write(
                        f"# Simulation Dist: {val('x_sim')} | Step (h_rk): {val('h_rk')} | ve0: {val('ve0')}\n"
                    )
                    f.write(
                        f"# Search Lower Limit: {val('u0_ini')} | Search Step: {val('u0_step')} | Final Base Vel (u0): {val('u0')}\n"
                    )
                    f.write(
                        f"# Critical Point (x_crit): {val('x_crit')} | Velocity at Crit (y_crit): {val('y_crit')} | Alfvén Point (x_t): {val('x_t')}\n"
                    )
                    f.write(
                        f"# Critical Jump Size: {val('tamanho_pulo')} | Backtrack Steps: {val('recuo_pulo')}\n"
                    )
                    f.write(
                        f"# Crit. Numerator Idx: {val('idx_crit_num')} | Crit. Denominator Idx: {val('idx_crit_den')}\n"
                    )

                    f.write("#\n# [ 4. EXOPLANET & HABITABILITY ]\n")
                    f.write(f"# Exoplanet Simulated: {val('habitabilidade')}\n")
                    f.write(
                        f"# Exoplanet Name: {val('exoplanet_name')} | Orbital Dist [AU]: {val('Dorb')}\n"
                    )
                    f.write(
                        f"# Eccentricity: {val('e')} | Bond Albedo: {val('Ab')} | Planet Radius [Rearth]: {val('Rplan')}\n"
                    )
                    f.write(
                        f"# Dipole Moment [Am2]: {val('Mmag')} | Magnetospheric compression factor (f0): {val('f0')}\n"
                    )
                    f.write(
                        f"# Kopparapu Inner Edge: {val('d_int')} | Kopparapu Outer Edge: {val('d_ext')}\n"
                    )
                    f.write(
                        f"# Classic Inner Edge: {val('dc_int')} | Classic Outer Edge: {val('dc_ext')}\n"
                    )

                    f.write("#\n# [ 5. PLOTTING PREFERENCES ]\n")
                    f.write(
                        f"# X-Scale: {val('x_scale')} | Y-Scale: {val('y_scale')}\n"
                    )
                    f.write(
                        f"# Ref Distances: {val('x_ref')} | Ref Names: {val('nome_ref')} | Ref Colors: {val('color_ref')}\n"
                    )
                    f.write(
                        f"# Sigma From: {val('sigmas_ref')} | Sigma Name: {val('sigmas_nome_ref')}\n"
                    )
                    f.write("# " + "=" * 60 + "\n")

                    # =======================================================
                    # Lógica inteligente para as colunas matriciais
                    # =======================================================
                    colunas_possiveis = [
                        "x_tot",
                        "y_tot",
                        "va_total",
                        "cs",
                        "rho_total",
                        "phi_total",
                        "deltav2_total",
                        "dmdt_total",
                        "P_din",
                        "Rmag",
                        "num_alpha_array",
                        "den_alpha_array",
                    ]

                    colunas_validas = []
                    arrays_para_empilhar = []

                    # O x_tot dita o tamanho que as arrays da malha principal devem ter
                    tamanho_alvo = len(dados["x_tot"]) if "x_tot" in dados else 0

                    for k in colunas_possiveis:
                        if k in dados:
                            v = dados[k]
                            # Se for uma array exatamente com o tamanho da malha de simulação, é coluna!
                            if isinstance(v, np.ndarray) and v.size == tamanho_alvo:
                                colunas_validas.append(k)
                                arrays_para_empilhar.append(v)

                    # Escreve o cabeçalho das colunas separadas por vírgula
                    f.write(",".join(colunas_validas) + "\n")

                    # Despejo Matricial ultrarrápido
                    if arrays_para_empilhar:
                        matriz = np.column_stack(arrays_para_empilhar)
                        np.savetxt(f, matriz, delimiter=",", fmt="%.8e")

                # Devolve o controlo à thread principal da Interface para mostrar o aviso
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

        # Inicia o processo isolado para não congelar o programa
        import threading

        threading.Thread(target=tarefa_exportacao, daemon=True).start()

    # * ============================================
    # * Gestão Dinâmica de Perfis (JSON)
    # * ============================================
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
                },
                "advanced": {
                    "multicurve": self.app_state.multicurve.get(),
                    "searchdv2": self.app_state.searchdv2.get(),
                    "ldv2": self.app_state.ldv2.get(),
                    "hdv2": self.app_state.hdv2.get(),
                    "stepdv2": self.app_state.stepdv2.get(),
                },
                "plot": {
                    "sigma_ini": self.app_state.sigma_ini.get(),
                    "sigma_fim": self.app_state.sigma_fim.get(),
                    "sigma_nome": self.app_state.sigma_nome.get(),
                    "sigma_cor": self.app_state.sigma_cor.get(),
                    "axis_x": self.app_state.axis["X Axis"].get(),
                    "axis_y": self.app_state.axis["Y Axis"].get(),
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
            with open(filepath, "w") as f:
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

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            mapping = {
                "star": ["nome", "Mstar", "Rstar", "Teff", "Lstar","T", "rho0", "B0", "mu"],
                "wave": ["S_divergencia", "deltav0", "phi0", "L0", "cte", "parker"],
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
                ],
                "advanced": ["multicurve", "searchdv2", "ldv2", "hdv2", "stepdv2"],
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
                if "refs" in p:
                    for i, r in enumerate(p["refs"]):
                        if i < len(self.app_state.refs):
                            self.app_state.refs[i]["x"].set(r.get("x", ""))
                            self.app_state.refs[i]["nome"].set(r.get("nome", ""))
                            self.app_state.refs[i]["cor"].set(r.get("cor", ""))
                            self.app_state.refs[i]["estilo"].set(r.get("estilo", "-"))

        except Exception as e:
            print(f"Error loading profile: {e}")

    # * ============================================
    # * Construtores de Abas (Estrela)
    # * ============================================
    def _construir_aba_astro(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)

        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (0, "Target Name:", self.app_state.nome, ""),
            (1, "Stellar Mass ( M ) :", self.app_state.Mstar, "[ Msun ]"),
            (2, "Stellar Radius ( R ) :", self.app_state.Rstar, "[ Rsun ]"),
            (3, "Effective Temperature ( Teff ) :", self.app_state.Teff, "[ K ]"),
            (4, "Stellar Luminosity ( L ) :", self.app_state.Lstar, "[ Lsun ]"),
            (5, "Coronal Temperature ( T ) :", self.app_state.T, "[ K ]"),
            (6, "Coronal Base Density ( rho0 ) :", self.app_state.rho0, "[ g/cm³ ]"),
            (7, "Surface Magnetic Field ( B0 ) :", self.app_state.B0, "[ G ]"),
            (8, "Mean Molecular Weight ( mu ) :", self.app_state.mu, "[ adm ]"),
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
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

    def _construir_aba_onda(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)

        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (0, "Expansion Factor ( S ) :", self.app_state.S_divergencia, "[ adm ]"),
            (
                1,
                "Initial Wave Amplitude ( DeltaV0² ) :",
                self.app_state.deltav0,
                "[ ve0² ]",
            ),
            (2, "Initial Alfvén Flux ( phi0 ) :", self.app_state.phi0, "[ erg/cm²/s ]"),
            (3, "Damping Length ( L0 ) :", self.app_state.L0, "[ r0 ]"),
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
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

        # ? --- NOVA LÓGICA: ComboBox de Damping ---
        ctk.CTkLabel(aba, text="Damping Model:", font=fonte, text_color="#E5C07B").grid(
            row=6, column=0, padx=20, pady=15, sticky="w"
        )

        # Função para distribuir os valores booleanos com base na escolha
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

        # Sincroniza a interface caso você use o botão "Load Profile" (.json)
        def sync_combo_damping(*args):
            try:
                is_cte = self.app_state.cte.get()
                is_parker = self.app_state.parker.get()

                if is_parker:
                    combo_damping.set("Undamped (Parker)")
                elif is_cte:
                    combo_damping.set("Constant")
                else:
                    combo_damping.set("Ressonant")
            except Exception:
                pass

        # Adiciona rastreio a ambas as variáveis para reverter a UI num load
        self.app_state.cte.trace_add("write", sync_combo_damping)
        self.app_state.parker.trace_add("write", sync_combo_damping)
        sync_combo_damping()  # Chama a primeira vez para iniciar com o valor correto

    def _construir_aba_numerico(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_columnconfigure(1, weight=1)
        aba.grid_columnconfigure(2, weight=1)

        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")
        fonte_uni = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        campos = [
            (0, "Simulation Distance :", self.app_state.x_sim, "[ Rstar ]"),
            (1, "Integration Step :", self.app_state.h_rk, "[ Rstar ]"),
            (
                2,
                "Base Velocity Search - Lower Limit :",
                self.app_state.u0_ini,
                "[ ve0 ]",
            ),
            (3, "Base Velocity Search - Step :", self.app_state.u0_step, "[ ve0 ]"),
            (4, "Critical Point Jump Size :", self.app_state.tamanho_pulo, "[ Rstar ]"),
            (
                5,
                "Topology Backtrack Steps :",
                self.app_state.recuo_pulo,
                "[ 1e-5 Rstar ]",
            ),
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
            aba.grid_rowconfigure(len(campos), weight=1, minsize=10)

    def _construir_aba_gp(self, aba):
        fonte = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        headers = ["Distance [r0]", "Label", "Color [Hex]", "Line Style"]
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

        row_offset = len(self.app_state.refs) + 1

        ctk.CTkLabel(aba, text="Sigma Zone", font=fonte, text_color="#E5C07B").grid(
            row=row_offset, column=0, columnspan=4, pady=(10, 5)
        )
        frame_sigma = ctk.CTkFrame(aba, fg_color="transparent")
        frame_sigma.grid(row=row_offset + 1, column=0, columnspan=4, pady=5)

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
            row=row_offset, column=0, columnspan=4, pady=(10, 5)
        )

        frame_axis = ctk.CTkFrame(aba, fg_color="transparent")
        frame_axis.grid(row=row_offset + 1, column=0, columnspan=4, pady=5)

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
        self.btn_update_plot = ctk.CTkButton(
            aba,
            text="Update Plot",
            command=self.iniciar_replot,
            fg_color="#5C7174",
            state="disabled",
        )
        self.btn_update_plot.grid(row=row_offset, column=0, columnspan=4, pady=(20, 10))

    def _construir_aba_more(self, aba):
        aba.grid_columnconfigure(0, weight=1)

        fonte_titulo = ctk.CTkFont(family="Consolas", size=14, weight="bold")
        fonte_check = ctk.CTkFont(family="Roboto", size=13, weight="normal")
        fonte_var = ctk.CTkFont(family="Roboto", size=12, weight="normal")

        ctk.CTkLabel(
            aba,
            text="Advanced Execution Scripts",
            font=fonte_titulo,
            text_color="#E5C07B",
        ).grid(row=0, column=0, pady=(20, 15), sticky="w", padx=30)

        cb_multicurve = ctk.CTkCheckBox(
            aba,
            text="Run Multicurve Analysis (Resonant vs Constant Damping)",
            variable=self.app_state.multicurve,
            font=fonte_check,
            fg_color="#61AFEF",
            hover_color="#56B6C2",
            command=self._on_multicurve_toggle,
        )
        cb_multicurve.grid(row=1, column=0, padx=30, pady=10, sticky="w")
        ToolTip(
            cb_multicurve,
            "Runs the simulation twice to overlay resonant\n and constant damping velocity profiles.",
        )

        cb_searchdv2 = ctk.CTkCheckBox(
            aba,
            text="Run DeltaV0² Search Script",
            variable=self.app_state.searchdv2,
            font=fonte_check,
            fg_color="#61AFEF",
            hover_color="#56B6C2",
            command=self._alternar_parametros_dv2,
        )
        cb_searchdv2.grid(row=2, column=0, padx=30, pady=(10, 0), sticky="w")
        ToolTip(
            cb_searchdv2,
            "Enables optimization algorithm to find the optimal\n initial amplitude for Alfvén waves. \nComputationally expensive.",
        )

        self.frame_dv2 = ctk.CTkFrame(aba, fg_color="transparent")
        self.frame_dv2.grid(row=3, column=0, padx=(60, 30), pady=(5, 15), sticky="w")

        self.lbl_ldv2 = ctk.CTkLabel(
            self.frame_dv2, text="Lower limit:", font=fonte_check
        )
        self.lbl_ldv2.grid(row=0, column=0, padx=(0, 5))
        self.entry_ldv2 = ctk.CTkEntry(
            self.frame_dv2, textvariable=self.app_state.ldv2, font=fonte_var, width=60
        )
        self.entry_ldv2.grid(row=0, column=1, padx=(0, 20))

        self.lbl_hdv2 = ctk.CTkLabel(
            self.frame_dv2, text="Upper limit:", font=fonte_check
        )
        self.lbl_hdv2.grid(row=0, column=2, padx=(0, 5))
        self.entry_hdv2 = ctk.CTkEntry(
            self.frame_dv2, textvariable=self.app_state.hdv2, font=fonte_var, width=60
        )
        self.entry_hdv2.grid(row=0, column=3, padx=(0, 20))

        self.lbl_stepdv2 = ctk.CTkLabel(self.frame_dv2, text="Step:", font=fonte_check)
        self.lbl_stepdv2.grid(row=0, column=4, padx=(0, 5))
        self.entry_stepdv2 = ctk.CTkEntry(
            self.frame_dv2,
            textvariable=self.app_state.stepdv2,
            font=fonte_var,
            width=60,
        )
        self.entry_stepdv2.grid(row=0, column=5, padx=(0, 0))

        self.lbl_contagem_dv2 = ctk.CTkLabel(
            self.frame_dv2,
            text="Estimated iterations: 0",
            font=("Roboto", 11, "normal"),
            text_color="#5c6269",
        )
        self.lbl_contagem_dv2.grid(
            row=1, column=0, columnspan=6, pady=(8, 0), sticky="e"
        )

        self.app_state.ldv2.trace_add("write", self._atualizar_contagem_dv2)
        self.app_state.hdv2.trace_add("write", self._atualizar_contagem_dv2)
        self.app_state.stepdv2.trace_add("write", self._atualizar_contagem_dv2)

        aba.grid_rowconfigure(4, weight=1)
        self._alternar_parametros_dv2()

    # * ============================================
    # * Construtores de Abas (Exoplanetas)
    # * ============================================
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
            aba, text="Planetary Radius ( Rplan ) :", font=fonte, text_color="#E5C07B"
        ).grid(row=0, column=0, padx=20, pady=5, sticky="w")
        entry_rplan = ctk.CTkEntry(
            aba, textvariable=self.app_state.Rplan, font=fonte_var
        )
        entry_rplan.grid(
            row=0, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we"
        )
        self.exo_inputs.append(entry_rplan)
        ctk.CTkLabel(
            aba, text="  [ Rearth ]", font=fonte_uni, text_color="#8b949e"
        ).grid(row=0, column=3, padx=(0, 20), pady=5, sticky="w")

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
            text="Magnetospheric Compression Factor ( f0 ) :",
            font=fonte,
            text_color="#E5C07B",
        ).grid(row=2, column=0, padx=20, pady=5, sticky="w")
        entry_f0 = ctk.CTkEntry(aba, textvariable=self.app_state.f0, font=fonte_var)
        entry_f0.grid(row=2, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="we")
        self.exo_inputs.append(entry_f0)
        ctk.CTkLabel(aba, text="  [ adm ]", font=fonte_uni, text_color="#8b949e").grid(
            row=2, column=3, padx=(0, 20), pady=5, sticky="w"
        )

    # * ============================================
    # * Lógica Dinâmica da Interface
    # * ============================================
    def set_exoplanet_state(self, state_str):
        for widget in self.exo_inputs:
            widget.configure(state=state_str)

            # ? --- Feedback Visual de Bloqueio/Desbloqueio ---
            if isinstance(widget, ctk.CTkEntry):
                if state_str == "disabled":
                    widget.configure(
                        text_color="#3c4044",  # Texto fantasma (cinza escuro)
                        border_color="#282C34",  # Borda ofuscada
                        fg_color="#1E1E1E",  # Fundo fundido com o painel
                    )
                else:
                    widget.configure(
                        text_color="white",  # Texto ativo (padrão)
                        border_color="#565b5e",  # Borda ativa
                        fg_color="#343638",  # Fundo ativo
                    )

            elif isinstance(widget, ctk.CTkSlider):
                if state_str == "disabled":
                    widget.configure(
                        button_color="#282C34",  # Botão cinza escuro
                        progress_color="#282C34",  # Trilha cinza escuro
                        button_hover_color="#282C34",
                    )
                else:
                    widget.configure(
                        button_color="#61AFEF",  # Azul ASTRAEOS (ativo)
                        progress_color="#1F618D",  # Trilha preenchida
                        button_hover_color="#56B6C2",
                    )

    def _alternar_parametros_dv2(self):
        estado_ativo = self.app_state.searchdv2.get()
        if estado_ativo:
            self.app_state.multicurve.set(False)

        cor_texto = "#8b949e" if estado_ativo else "#5c6269"
        estado_widget = "normal" if estado_ativo else "disabled"

        self.lbl_ldv2.configure(text_color=cor_texto)
        self.lbl_hdv2.configure(text_color=cor_texto)
        self.lbl_stepdv2.configure(text_color=cor_texto)

        self.entry_ldv2.configure(state=estado_widget)
        self.entry_hdv2.configure(state=estado_widget)
        self.entry_stepdv2.configure(state=estado_widget)

        if estado_ativo:
            self.lbl_contagem_dv2.grid()
            self._atualizar_contagem_dv2()
        else:
            self.lbl_contagem_dv2.grid_remove()

    def _on_multicurve_toggle(self):
        if self.app_state.multicurve.get():
            self.app_state.searchdv2.set(False)
            self._alternar_parametros_dv2()

    def _atualizar_contagem_dv2(self, *args):
        try:
            min_val = float(self.app_state.ldv2.get())
            max_val = float(self.app_state.hdv2.get())
            step_val = float(self.app_state.stepdv2.get())

            if step_val > 0 and max_val > min_val:
                runs = int(round((max_val - min_val) / step_val, 5))
                self.lbl_contagem_dv2.configure(text=f"Estimated iterations: {runs}")
            else:
                self.lbl_contagem_dv2.configure(text="Estimated iterations: 0")
        except ValueError:
            self.lbl_contagem_dv2.configure(text="Estimated iterations: --")

    # * ============================================
    # * Ações de Controle
    # * ============================================
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
