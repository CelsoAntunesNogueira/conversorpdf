from flask import Flask, request, send_file, render_template
import os
from docx2pdf import convert

app = Flask(__name__)

# Definição das pastas de upload e saída
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado"
    
    file = request.files['file']
    if file.filename == '':
        return "Nenhum arquivo selecionado"
    
    if file and file.filename.endswith('.docx'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        pdf_filename = file.filename.replace('.docx', '.pdf')
        pdf_path = os.path.join(OUTPUT_FOLDER, pdf_filename)

        # Converte o arquivo DOCX para PDF
        convert(file_path, OUTPUT_FOLDER)

        # Espera até o arquivo ser gerado corretamente
        if not os.path.exists(pdf_path):
            return "Erro na conversão do arquivo", 500

        # Certifique-se de que o Flask está servindo os arquivos corretamente
        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)

    return "Arquivo inválido. Envie um documento .docx"


if __name__ == '__main__':
    app.run(debug=True)
