import customtkinter as ctk
import threading
from tkinter import filedialog
from pathlib import Path
import convert_lytics  # Importa o módulo de exportação
import sys
import os

def resource_path(relative_path):
    """Obtém o caminho absoluto para um recurso, funcionando tanto em desenvolvimento quanto no .exe"""
    if hasattr(sys, '_MEIPASS'):
        # Caminho quando empacotado como .exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ModernMusicExporter:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("Conversor de Músicas")
        self.root.geometry("550x400")
        try:
            # Usa resource_path para encontrar o ícone
            self.root.iconbitmap(resource_path("img/icon.ico"))
        except Exception as e:
            print(f"Erro ao carregar o ícone: {e}")

        self.exportando = False
        self.total = 0
        self.contador = 0

        self.db_path = r"C:\Program Files (x86)\Louvor JA\config\database.db"  # Caminho padrão
        self.build_interface()
        self.root.mainloop()

    def build_interface(self):
        self.frame = ctk.CTkFrame(self.root, corner_radius=12)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Frame interno com margem de 10px
        self.inner_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

        title_font = ctk.CTkFont(size=20, weight="bold")
        subtitle_font = ctk.CTkFont(size=14)

        self.title = ctk.CTkLabel(self.inner_frame, text="Conversor de Músicas", font=title_font)
        self.title.pack(pady=(10, 5))

        self.subtitle = ctk.CTkLabel(self.inner_frame, text="Converta músicas do LouvorJa para Holytics", font=subtitle_font)
        self.subtitle.pack(pady=(0, 20))

        self.db_path_var = ctk.StringVar(value=self.db_path)

        db_label = ctk.CTkLabel(self.inner_frame, text="Caminho do Banco de Dados:", font=("Helvetica", 12, "bold"))
        db_label.pack(anchor="w")

        db_frame = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        db_frame.pack(fill="x", pady=5)

        self.db_entry = ctk.CTkEntry(db_frame, textvariable=self.db_path_var, height=38, corner_radius=12)
        self.db_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(db_frame, text="Selecionar", command=self.selecionar_db, height=38, corner_radius=12)
        browse_btn.pack(side="right")

        self.progress_label = ctk.CTkLabel(self.inner_frame, text="Preparando...")
        self.progress_label.pack(pady=(20, 5))

        self.progress_bar = ctk.CTkProgressBar(self.inner_frame)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar.set(0)

        self.counter_label = ctk.CTkLabel(self.inner_frame, text="0/0", font=subtitle_font)
        self.counter_label.pack(pady=(5, 15))

        button_frame = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.start_button = ctk.CTkButton(button_frame, text="▶ Iniciar Exportação", command=self.iniciar_exportacao, height=38, corner_radius=12)
        self.start_button.pack(side="left", padx=10)

        self.cancel_button = ctk.CTkButton(button_frame, text="✖ Cancelar", command=self.cancelar_exportacao, state="disabled", height=38, corner_radius=12)
        self.cancel_button.pack(side="left", padx=10)

    def selecionar_db(self):
        arquivo = filedialog.askopenfilename(
            title="Selecione o banco de dados",
            filetypes=[("Arquivos .db", "*.db")],
            initialdir=str(Path(self.db_path).parent) if Path(self.db_path).parent.exists() else "C:"
        )
        if arquivo:
            self.db_path_var.set(arquivo)
            self.db_path = arquivo

    def iniciar_exportacao(self):
        self.exportando = True
        self.start_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        threading.Thread(target=self.exportar_musicas, daemon=True).start()

    def exportar_musicas(self):
        self.progress_label.configure(text="Conectando ao banco de dados...")
        self.root.update()

        def callback(idx, total):
            self.contador = idx
            self.total = total
            self.root.after(0, self.atualizar_interface)

        def cancel_check():
            return not self.exportando

        try:
            resultado = convert_lytics.exportar_musicas(self.db_path, callback, cancel_check)
            self.progress_label.configure(text=resultado)
        except Exception as e:
            self.progress_label.configure(text=f"❌ Erro inesperado: {e}")
        finally:
            self.start_button.configure(state="normal")
            self.cancel_button.configure(state="disabled")
            self.exportando = False

    def atualizar_interface(self):
        self.progress_label.configure(text=f"Exportando música {self.contador}...")
        self.counter_label.configure(text=f"{self.contador}/{self.total}")
        self.progress_bar.set(self.contador / self.total)

    def cancelar_exportacao(self):
        self.exportando = False

if __name__ == "__main__":
    app = ModernMusicExporter()