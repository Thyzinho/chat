from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
socketio = SocketIO(app)

# Lista de mensagens (apenas para fins de exemplo, em uma aplicação real você usaria um banco de dados)
mensagens = []

# Dicionário para armazenar as cores dos usuários
cores_usuarios = {}

@app.route('/')
def index():
    return redirect(url_for('chat_page'))

@app.route('/chat_page')
def chat_page():
    return render_template('chat.html', mensagens=mensagens)

@socketio.on('enviar_mensagem')
def handle_message(data):
    usuario = data['usuario']
    mensagem = data['mensagem']
    cor = cores_usuarios.get(usuario)  # Verifica se já existe uma cor para o usuário
    if not cor:
        cor = gerar_cor_aleatoria()  # Gera uma cor aleatória se ainda não existir
        cores_usuarios[usuario] = cor  # Armazena a cor para o usuário
    if mensagem.strip():  # Verifica se a mensagem não está vazia após remover espaços em branco
        mensagens.append((usuario, mensagem, cor))
        emit('mensagem_recebida', {'usuario': usuario, 'mensagem': mensagem, 'cor': cor}, broadcast=True)

def gerar_cor_aleatoria():
    import random
    letras = '0123456789ABCDEF'
    cor = '#'
    for _ in range(6):
        cor += random.choice(letras)
    return cor

if __name__ == '__main__':
    socketio.run(app)
