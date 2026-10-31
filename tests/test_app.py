import pytest
from app import create_app

@pytest.fixture
def client(tmp_path):
    app = create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'teste.db'), 'SECRET_KEY': 'chave-de-teste'})
    return app.test_client()

def login(client):
    return client.post('/login', data={'usuario': 'admin', 'senha': 'TroqueEstaSenha123!'}, follow_redirects=True)

def test_inicio(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'SoproGest' in response.get_data(as_text=True)

def test_acesso_requer_login(client):
    response = client.get('/animais')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login_invalido(client):
    response = client.post('/login', data={'usuario': 'admin', 'senha': 'errada'}, follow_redirects=True)
    assert 'inválidos' in response.get_data(as_text=True)

def test_cadastro_e_listagem(client):
    login(client)
    response = client.post('/animais/novo', data={'nome': 'Mingau', 'especie': 'Gato', 'idade': '2', 'saude': 'Saudável', 'status': 'Disponível'}, follow_redirects=True)
    texto = response.get_data(as_text=True)
    assert 'cadastrado com sucesso' in texto
    assert 'Mingau' in texto

def test_cadastro_rejeita_idade_negativa(client):
    login(client)
    response = client.post('/animais/novo', data={'nome': 'Mingau', 'especie': 'Gato', 'idade': '-2', 'saude': 'Saudável', 'status': 'Disponível'}, follow_redirects=True)
    assert 'Confira os dados' in response.get_data(as_text=True)
