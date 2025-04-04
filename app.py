from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from flask_cors import CORS # type: ignore

app = Flask(__name__)
# Permite CORS de qualquer origem e para qualquer método
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response
    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'  # Armazena no /tmp/
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secreta_chave_aqui'  # Defina uma chave secreta

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Modelo de Usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    estoque = db.relationship('Estoque', backref='dono', lazy=True)  # Relacionamento correto

# Modelo de Estoque
class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Relacionamento correto

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):  # Comparação segura
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
           flash('Usuário ou senha incorretos', 'error')  # Mensagem de erro
    return render_template('login.html')

# Página de dashboard (após login)
@app.route('/dashboard')
@login_required
def dashboard():
    user_estoque = Estoque.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', estoque=user_estoque)

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Função para criar novo usuário (apenas para testes)
@app.route('/create_user')
def create_user():
    hashed_password = generate_password_hash('senha1', method='pbkdf2:sha256')  # Senha segura
    new_user = User(username='usuario1', password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return 'Usuário criado!'

@app.route('/')
def index():
    return render_template('login.html')

# Carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        if User.query.filter_by(username=username).first():
            return "Usuário já existe!"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/add_estoque', methods=['POST'])
@login_required
def add_estoque():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    tipo = request.form['tipo']
    
    novo_item = Produto(nome=nome, quantidade=quantidade, tipo=tipo)
    
    db.session.add(novo_item)
    db.session.commit()

    return redirect(url_for('dashboard'))

# Modelo do banco de dados
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

# Criar tabelas
with app.app_context():
    db.create_all()

# 🔹 Rota para listar todos os produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{ "id": p.id, "nome": p.nome, "quantidade": p.quantidade, "tipo": p.tipo } for p in produtos])

# 🔹 Rota para adicionar um novo produto
@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    data = request.json
    if not data.get('nome') or not data.get('quantidade') or not data.get('tipo'):
        return jsonify({"erro": "Dados inválidos"}), 400

    produto = Produto.query.filter_by(nome=data['nome']).first()
    if produto:
        produto.quantidade += int(data['quantidade'])  # Atualiza quantidade
    else:
        produto = Produto(nome=data['nome'], quantidade=int(data['quantidade']), tipo=data['tipo'])
        db.session.add(produto)

    db.session.commit()
    return jsonify({"mensagem": "Produto adicionado com sucesso!"})

# 🔹 Rota para editar um produto
@app.route('/editar/<int:id>', methods=['PUT'])
def editar_produto(id):
    data = request.json
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produto.quantidade = int(data.get('quantidade', produto.quantidade))
    db.session.commit()
    return jsonify({"mensagem": "Produto atualizado!"})

@app.route('/retirar/<string:nome>', methods=['PUT'])  
def retirar_produto(nome):  
    data = request.get_json()  # Obtém os dados JSON enviados no corpo da requisição  
    quantidade_retirar = data.get("quantidade")  

    if not quantidade_retirar or quantidade_retirar <= 0:  
        return jsonify({"erro": "Quantidade inválida"}), 400  

    produto = Produto.query.filter_by(nome=nome).first()  
    
    if not produto:  
        return jsonify({"erro": "Produto não encontrado"}), 404  
    
    if produto.quantidade < quantidade_retirar:  
        return jsonify({"erro": "Estoque insuficiente"}), 400  

    produto.quantidade -= quantidade_retirar  
    db.session.commit()  
    return jsonify({"mensagem": f"{quantidade_retirar} unidade(s) de {nome} retiradas com sucesso!"})  

# 🔹 Rota para remover um produto
@app.route('/remover/<int:id>', methods=['DELETE'])
def remover_produto(id):
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    db.session.delete(produto)
    db.session.commit()
    return jsonify({"mensagem": "Produto removido!"})

# 🔹 Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)



# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
