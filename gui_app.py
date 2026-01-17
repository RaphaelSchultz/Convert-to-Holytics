"""
Convert-to-Holytics - Native Windows GUI Application
Standalone desktop application for exporting Louvor JA music to text files.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import sqlite3
from pathlib import Path
import sys
import os

# Import existing logic
from app.repositories.music_repository import MusicRepository
from app.utils import formatters


class HolyticsApp:
    """Main GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Convert-to-Holytics - Exportador de Músicas")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Colors (Supabase inspired)
        self.bg = "#1C1C1C"
        self.fg = "#EDEDED"
        self.brand = "#3ECF8E"
        self.border = "#2E2E2E"
        
        # Configure root style
        self.root.configure(bg=self.bg)
        self.setup_styles()
        
        # Variables
        self.db_path = tk.StringVar()
        self.is_exporting = False
        self.exported_files = []
        
        # Build UI
        self.create_widgets()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button style
        style.configure('Brand.TButton',
                       background=self.brand,
                       foreground='#000000',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Inter', 10, 'bold'))
        style.map('Brand.TButton',
                 background=[('active', '#2FB574')])
        
        # Secondary button
        style.configure('Secondary.TButton',
                       background=self.border,
                       foreground=self.fg,
                       borderwidth=1,
                       focuscolor='none',
                       font=('Inter', 10))
        
        # Progress bar
        style.configure('Brand.Horizontal.TProgressbar',
                       background=self.brand,
                       troughcolor=self.border,
                       bordercolor=self.border,
                       lightcolor=self.brand,
                       darkcolor=self.brand)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Header
        header = tk.Frame(self.root, bg='#000000', height=80)
        header.pack(fill='x', padx=0, pady=0)
        
        title = tk.Label(header, 
                        text="🎵 Convert-to-Holytics",
                        bg='#000000',
                        fg=self.fg,
                        font=('Inter', 18, 'bold'))
        title.pack(pady=20)
        
        subtitle = tk.Label(header,
                           text="Exportador de Músicas do Louvor JA",
                           bg='#000000',
                           fg='#A0A0A0',
                           font=('Inter', 10))
        subtitle.pack()
        
        # Main container
        main = tk.Frame(self.root, bg=self.bg)
        main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Database selection card
        db_card = self.create_card(main)
        db_card.pack(fill='x', pady=(0, 15))
        
        tk.Label(db_card,
                text="Banco de Dados",
                bg=self.bg,
                fg=self.fg,
                font=('Inter', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # File picker row
        picker_frame = tk.Frame(db_card, bg=self.bg)
        picker_frame.pack(fill='x')
        
        db_entry = tk.Entry(picker_frame,
                           textvariable=self.db_path,
                           bg=self.border,
                           fg=self.fg,
                           font=('Inter', 10),
                           relief='flat',
                           insertbackground=self.fg)
        db_entry.pack(side='left', fill='x', expand=True, ipady=8, ipadx=10)
        
        browse_btn = ttk.Button(picker_frame,
                               text="📁 Procurar",
                               command=self.browse_file,
                               style='Secondary.TButton')
        browse_btn.pack(side='right', padx=(10, 0), ipady=4, ipadx=15)
        
        # Actions
        actions_frame = tk.Frame(db_card, bg=self.bg)
        actions_frame.pack(fill='x', pady=(15, 0))
        
        self.start_btn = ttk.Button(actions_frame,
                                    text="▶ Iniciar Exportação",
                                    command=self.start_export,
                                    style='Brand.TButton')
        self.start_btn.pack(side='left', ipady=8, ipadx=20)
        
        # Progress card
        self.progress_card = self.create_card(main)
        self.progress_card.pack(fill='x', pady=(0, 15))
        self.progress_card.pack_forget()  # Hidden initially
        
        tk.Label(self.progress_card,
                text="Exportando...",
                bg=self.bg,
                fg=self.fg,
                font=('Inter', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        self.progress_label = tk.Label(self.progress_card,
                                      text="Preparando exportação...",
                                      bg=self.bg,
                                      fg='#A0A0A0',
                                      font=('Inter', 9))
        self.progress_label.pack(anchor='w', pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(self.progress_card,
                                           length=400,
                                           mode='determinate',
                                           style='Brand.Horizontal.TProgressbar')
        self.progress_bar.pack(fill='x', pady=(5, 5))
        
        self.progress_count = tk.Label(self.progress_card,
                                      text="0 / 0 músicas",
                                      bg=self.bg,
                                      fg='#A0A0A0',
                                      font=('Inter', 9))
        self.progress_count.pack(anchor='w')
        
        # Results card
        self.results_card = self.create_card(main)
        self.results_card.pack(fill='both', expand=True)
        self.results_card.pack_forget()  # Hidden initially
        
        results_header = tk.Frame(self.results_card, bg=self.bg)
        results_header.pack(fill='x', pady=(0, 10))
        
        tk.Label(results_header,
                text="✅ Músicas Exportadas",
                bg=self.bg,
                fg=self.fg,
                font=('Inter', 12, 'bold')).pack(side='left')
        
        open_folder_btn = ttk.Button(results_header,
                                     text="📂 Abrir Pasta",
                                     command=self.open_output_folder,
                                     style='Brand.TButton')
        open_folder_btn.pack(side='right', ipady=4, ipadx=15)
        
        # Results table
        table_frame = tk.Frame(self.results_card, bg=self.border)
        table_frame.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox for files
        self.files_list = tk.Listbox(table_frame,
                                    bg=self.border,
                                    fg=self.fg,
                                    font=('Inter', 9),
                                    relief='flat',
                                    selectbackground=self.brand,
                                    selectforeground='#000000',
                                    yscrollcommand=scrollbar.set)
        self.files_list.pack(fill='both', expand=True, padx=1, pady=1)
        scrollbar.config(command=self.files_list.yview)
        
    def create_card(self, parent):
        """Create a card-like frame"""
        card = tk.Frame(parent,
                       bg=self.bg,
                       highlightbackground=self.border,
                       highlightthickness=1)
        
        inner = tk.Frame(card, bg=self.bg)
        inner.pack(fill='both', expand=True, padx=15, pady=15)
        
        return inner
    
    def browse_file(self):
        """Open file picker for database"""
        filename = filedialog.askopenfilename(
            title="Selecione o banco de dados do Louvor JA",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        if filename:
            self.db_path.set(filename)
    
    def start_export(self):
        """Start export process in background thread"""
        if not self.db_path.get():
            messagebox.showerror("Erro", "Selecione um banco de dados!")
            return
        
        if not Path(self.db_path.get()).exists():
            messagebox.showerror("Erro", "Arquivo não encontrado!")
            return
        
        # Disable button
        self.start_btn.config(state='disabled')
        self.is_exporting = True
        
        # Show progress
        self.progress_card.pack(fill='x', pady=(0, 15))
        
        # Start export thread
        thread = threading.Thread(target=self.export_worker, daemon=True)
        thread.start()
    
    def export_worker(self):
        """Worker thread for export"""
        try:
            # Create output directory
            output_dir = Path("musicas_txt_formatadas")
            output_dir.mkdir(exist_ok=True)
            
            # Clean existing files
            for file in output_dir.glob('*.txt'):
                file.unlink()
            
            # Initialize repository
            repository = MusicRepository(self.db_path.get())
            
            # Get all musics
            musics = repository.get_all_musics()
            total = len(musics)
            
            self.update_progress(0, total, "Iniciando exportação...")
            
            used_filenames = set()
            files_written = 0
            
            for i, music in enumerate(musics):
                nome_com, nome_album, nome, faixa, id_music = music
                
                # Get lyrics
                lyrics = repository.get_lyrics_by_music_id(id_music)
                
                # Generate filename
                song_name = nome_com or nome or 'Sem_título'
                
                if nome_album and "Hinário Adventista" in nome_album:
                    filename_base = song_name
                else:
                    filename_base = f"{song_name} - {id_music}"
                
                filename = formatters.sanitize_filename(filename_base)
                
                # Ensure unique
                original_filename = filename
                counter = 1
                while filename in used_filenames:
                    filename = f"{original_filename}_{counter}"
                    counter += 1
                
                used_filenames.add(filename)
                file_path = output_dir / f"{filename}.txt"
                
                # Format and write
                formatted_lyrics = formatters.formatar_letra(lyrics)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Título: {nome or ''}\n")
                    f.write(f"Artista: {nome_album or ''}\n\n")
                    f.write(formatted_lyrics)
                
                files_written += 1
                self.exported_files.append(f"{filename}.txt")
                
                # Update progress
                self.update_progress(files_written, total, f"Exportando: {filename}")
            
            # Done
            self.export_complete(files_written)
            
        except Exception as e:
            self.export_error(str(e))
    
    def update_progress(self, current, total, message):
        """Update progress bar and label"""
        def update():
            self.progress_bar['maximum'] = total
            self.progress_bar['value'] = current
            self.progress_label.config(text=message)
            self.progress_count.config(text=f"{current} / {total} músicas")
        
        self.root.after(0, update)
    
    def export_complete(self, count):
        """Handle export completion"""
        def complete():
            self.is_exporting = False
            self.start_btn.config(state='normal')
            self.progress_card.pack_forget()
            
            # Show results
            self.results_card.pack(fill='both', expand=True)
            
            # Populate list
            self.files_list.delete(0, 'end')
            for filename in sorted(self.exported_files):
                self.files_list.insert('end', filename)
            
            messagebox.showinfo("Sucesso", f"✅ {count} músicas exportadas com sucesso!")
        
        self.root.after(0, complete)
    
    def export_error(self, error):
        """Handle export error"""
        def show_error():
            self.is_exporting = False
            self.start_btn.config(state='normal')
            self.progress_card.pack_forget()
            messagebox.showerror("Erro", f"Erro durante exportação:\n{error}")
        
        self.root.after(0, show_error)
    
    def open_output_folder(self):
        """Open output folder in file explorer"""
        output_dir = Path("musicas_txt_formatadas").resolve()
        if sys.platform == 'win32':
            os.startfile(output_dir)
        elif sys.platform == 'darwin':
            os.system(f'open "{output_dir}"')
        else:
            os.system(f'xdg-open "{output_dir}"')


def main():
    """Main entry point"""
    root = tk.Tk()
    app = HolyticsApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
