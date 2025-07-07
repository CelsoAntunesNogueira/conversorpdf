import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import subprocess
import sys

# Tenta importar as bibliotecas de conversão e avisa se faltarem
try:
    from docx2pdf import convert as convert_docx
    from fpdf import FPDF
except ImportError:
    messagebox.showerror(
        "Bibliotecas Faltando",
        "Por favor, instale as bibliotecas necessárias com o comando:\n"
        "pip install docx2pdf fpdf2"
    )
    sys.exit()

# --- Funções Auxiliares ---

def open_folder(path):
    """Abre a pasta no explorador de arquivos do sistema operacional."""
    if sys.platform == 'win32':
        os.startfile(path)
    elif sys.platform == 'darwin': # macOS
        subprocess.run(['open', path])
    else: # linux
        subprocess.run(['xdg-open', path])

# --- Classe Principal da Aplicação ---

class UniversalConverter(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela Principal ---
        self.title("Conversor Universal para PDF")
        self.geometry("500x280")
        self.resizable(False, False)

        # --- CAMINHOS ABSOLUTOS: A CORREÇÃO ESTÁ AQUI ---
        # Obtém o diretório onde o script está sendo executado
        self.script_dir = os.path.dirname(os.path.abspath(__file__)) # <-- ALTERAÇÃO IMPORTANTE

        # Constrói caminhos completos para a fonte e para a pasta de saída
        self.font_path = os.path.join(self.script_dir, "DejaVuSans.ttf") # <-- ALTERAÇÃO IMPORTANTE
        self.output_folder = os.path.join(self.script_dir, "output") # <-- ALTERAÇÃO IMPORTANTE (Boa prática)

        # Adiciona um print para depuração. Você pode ver isso no terminal.
        print(f"Procurando pela fonte em: {self.font_path}")
        print(f"Salvando arquivos em: {self.output_folder}")

        os.makedirs(self.output_folder, exist_ok=True)
        self.file_path = None

        # --- Criação dos Widgets ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        self.label_instrucao = ttk.Label(main_frame, text="Selecione um arquivo .docx ou .txt para converter", font=("Helvetica", 12))
        self.label_instrucao.pack(pady=(0, 10))

        self.btn_select = ttk.Button(main_frame, text="Selecionar Arquivo", command=self.select_file)
        self.btn_select.pack(pady=5, ipadx=10, ipady=5)

        self.label_file = ttk.Label(main_frame, text="Nenhum arquivo selecionado")
        self.label_file.pack(pady=5)

        self.btn_convert = ttk.Button(main_frame, text="Converter para PDF", state="disabled", command=self.start_conversion_thread)
        self.btn_convert.pack(pady=10, ipadx=10, ipady=5)
        
        self.status_label = ttk.Label(self, text=f"PDFs serão salvos em: 'output/'", relief="sunken", anchor="w", padding=5)
        self.status_label.pack(side="bottom", fill="x")

    def select_file(self):
        """Abre a caixa de diálogo para selecionar um arquivo .docx ou .txt."""
        path = filedialog.askopenfilename(
            title="Selecione um Documento",
            filetypes=[
                ("Documentos Suportados", "*.docx *.txt"),
                ("Documentos Word", "*.docx"),
                ("Arquivos de Texto", "*.txt"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if path:
            self.file_path = path
            filename = os.path.basename(self.file_path)
            self.label_file.config(text=filename)
            self.btn_convert.config(state="normal")
            self.status_label.config(text=f"Pronto para converter '{filename}'")

    def _convert_txt_to_pdf(self, input_path, output_path):
        """Converte um arquivo de texto para PDF usando FPDF2 e uma fonte customizada."""
        if not os.path.exists(self.font_path):
            # A mensagem de erro agora mostrará o caminho completo que falhou
            raise FileNotFoundError(
                f"Arquivo de fonte não encontrado no caminho esperado:\n{self.font_path}\n\n"
                "Verifique se o arquivo 'DejaVuSans.ttf' está na mesma pasta do script."
            )
        
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("DejaVu", "", self.font_path)
        pdf.set_font("DejaVu", size=12)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        pdf.multi_cell(0, 10, txt=text)
        pdf.output(output_path)

    def start_conversion_thread(self):
        """Inicia a conversão em uma thread separada para não travar a interface."""
        if not self.file_path:
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo primeiro.")
            return

        self.btn_select.config(state="disabled")
        self.btn_convert.config(state="disabled")
        self.status_label.config(text="Convertendo, por favor aguarde...")

        thread = threading.Thread(target=self.convert_file, daemon=True)
        thread.start()

    def convert_file(self):
        """Função de conversão que decide qual método usar com base na extensão."""
        try:
            filename = os.path.basename(self.file_path)
            
            if self.file_path.lower().endswith('.docx'):
                pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
                convert_docx(self.file_path, self.output_folder)
            
            elif self.file_path.lower().endswith('.txt'):
                pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
                pdf_path = os.path.join(self.output_folder, pdf_filename)
                self._convert_txt_to_pdf(self.file_path, pdf_path)
            
            else:
                messagebox.showerror("Erro", f"Tipo de arquivo não suportado: {filename}")
                self.reset_ui()
                return

            messagebox.showinfo("Sucesso!", f"Arquivo '{pdf_filename}' salvo com sucesso na pasta 'output'.")
            
            if messagebox.askyesno("Abrir Pasta", "Deseja abrir a pasta onde o PDF foi salvo?"):
                open_folder(self.output_folder)

        except Exception as e:
            messagebox.showerror("Erro na Conversão", f"Ocorreu um erro:\n\n{e}")
        finally:
            self.reset_ui()
    
    def reset_ui(self):
        """Reseta a interface para o estado inicial."""
        self.btn_select.config(state="normal")
        self.btn_convert.config(state="disabled")
        self.label_file.config(text="Nenhum arquivo selecionado")
        self.status_label.config(text=f"Aguardando... Salvo em: 'output/'")
        self.file_path = None

if __name__ == "__main__":
    app = UniversalConverter()
    app.mainloop()