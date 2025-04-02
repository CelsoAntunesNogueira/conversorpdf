# Conversor de DOCX para PDF

📌 Sobre o projeto:

Este é um Conversor de DOCX para PDF desenvolvido com Flask (Python) no backend e uma interface simples em HTML, CSS e JavaScript no frontend. O usuário pode fazer upload de um arquivo DOCX, que será convertido para PDF e disponibilizado para download automaticamente.

🚀 Tecnologias Utilizadas:<br>

-Python (Flask) - Para o backend e manipulação de arquivos <br>
-docx2pdf - Biblioteca usada para conversão de DOCX para PDF <br>
-HTML, CSS - Para a interface do usuário <br>
-JavaScript (Fetch API) - Para envio do arquivo e download do PDF <br>

🎯 Funcionalidades <br>
✅ Upload de arquivos DOCX<br>
✅ Conversão automática para PDF<br>
✅ Download do arquivo convertido<br>

📂 conversor-docx-pdf/
│── 📂 static/           # Pasta para arquivos CSS e JS
│── 📂 templates/        # HTML do projeto
│── 📂 uploads/          # Onde os arquivos enviados são armazenados
│── 📂 output/           # Onde os PDFs convertidos são armazenados
│── app.py              # Código principal do backend Flask
│── requirements.txt    # Lista de dependências do projeto
│── README.md           # Documentação do projeto

🛠 Como Rodar o Projeto

1️⃣ Clone este repositório <br>
git clone https://github.com/seuusuario/conversor-docx-pdf.git <br>
cd conversor-docx-pdf

2️⃣ Crie um ambiente virtual (opcional, mas recomendado) <br>
python -m venv venv <br>
source venv/bin/activate  # Linux/Mac <br>
venv\Scripts\activate     # Windows <br>

3️⃣ Instale as dependências<br>
pip install -r requirements.txt

4️⃣ Execute o servidor<br>
python app.py <br>
O servidor Flask será iniciado e poderá ser acessado via http://127.0.0.1:5000.<br>

🖼️ Interface <br>
Aqui está uma prévia da interface do projeto: <br>
![image](interface.png)


📜 Licença <br>
Este projeto está sob a licença MIT. Sinta-se à vontade para modificar e usar como quiser!
