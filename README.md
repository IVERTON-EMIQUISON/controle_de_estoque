# Controlo-de-estoque
# 📦 Sistema de Gerenciamento de Estoque

## 📝 Sobre o Projeto
O **Sistema de Gerenciamento de Estoque** é uma aplicação web desenvolvida para facilitar o controle de produtos, permitindo a adição, remoção e monitoramento de itens em estoque. A plataforma oferece uma interface intuitiva, segurança no login e uma gestão eficiente dos produtos cadastrados por cada usuário.

## 🚀 Tecnologias Utilizadas
O projeto foi desenvolvido utilizando as seguintes tecnologias:
- **Python** (Flask) - Backend
- **SQLite** - Banco de Dados
- **HTML, CSS e JavaScript** - Frontend
- **Bootstrap** - Estilização responsiva

## 🔧 Funcionalidades
✅ Cadastro e login de usuário com autenticação segura.  
✅ Adicionar novos produtos ao estoque.  
✅ Remover produtos do estoque.  
✅ Exibir o estoque atualizado em tempo real.  
✅ Interface moderna e responsiva.  

## 📂 Estrutura do Projeto
```
📦 sistema-estoque
├── 📁 templates          # Arquivos HTML
│   ├── login.html
│   ├── cadastro.html
│   ├── dashboard.html
├── app.py               # Arquivo principal Flask
├── models.py            # Modelos do banco de dados
├── database.db          # Banco de dados SQLite
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto
```

## 🛠️ Como Executar o Projeto

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/seu-usuario/sistema-estoque.git
cd sistema-estoque
```

### 2️⃣ Crie um ambiente virtual e ative
```bash
python -m venv venv
# Ativar no Windows
venv\Scripts\activate
# Ativar no Linux/Mac
source venv/bin/activate
```

### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Execute a aplicação
```bash
python app.py
```

Acesse no navegador: `http://127.0.0.1:5000`

## 🔒 Segurança
- Senhas armazenadas com **hashing seguro** (bcrypt).
- Proteção contra **CSRF e SQL Injection**.
- Controle de acesso com **Flask-Login**.

## 📌 Melhorias Futuras
- 📊 Geração de relatórios e gráficos.
- 📧 Notificações por e-mail.
- 📈 Integração com APIs de terceiros.

---
**Desenvolvido por:** [Iverton Emiquison](https://github.com/IVERTON-EMIQUISON) 🚀

