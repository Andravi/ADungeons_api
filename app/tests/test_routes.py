import pytest
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

@pytest.fixture
def user_data():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    user = {
        "username": f"test_user_{timestamp}",
        "email": f"test_{timestamp}@exemplo.com",
        "password": "senha123"
    }

    # Cria o usuário no backend
    response = requests.post(
        f"{BASE_URL}/register",
        json=user
    )
    assert response.status_code == 201, "Falha ao criar usuário para teste"

    yield user  # Entrega o usuário para o teste

    # Limpeza: Remove o usuário após o teste
    requests.delete(f"{BASE_URL}/users/{user['email']}")  # Ajuste para sua rota de deleção

@pytest.fixture
def campanha_data():
    return {
        "nome": "Campanha Teste",
        "descricao": "Descrição da campanha"
    }


# CT4 - Teste de email duplicado
def test_cadastro_email_duplicado(user_data):
    """Tenta cadastrar o mesmo usuário duas vezes"""
    # Fixture user_data já fez o primeiro cadastro
    response = requests.post(
        f"{BASE_URL}/register",  # Ajuste para seu endpoint real
        json={
            "username": user_data["username"] + "_dup",
            "email": user_data["email"],  # Mesmo email
            "password": "outrasenha"
        }
    )
    assert response.status_code == 409  # Conflict
    assert "Email já cadastrado" in response.json()["error"]

# CT5 - Teste de login válido
def test_login_conta_cadastrada(user_data):
    """Testa login com credenciais corretas"""
    response = requests.post(
        f"{BASE_URL}/login",  # Ajuste para seu endpoint
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# # CT6 - Teste de alteração de senha
# def test_alterar_senha(user_data):
#     """Testa o fluxo completo de alteração de senha"""
#     # Login para obter token
#     login = requests.post(
#         f"{BASE_URL}/login",
#         json={
#             "email": user_data["email"],
#             "password": user_data["password"]
#         }
#     )
#     token = login.json()["access_token"]

#     # Alteração de senha
#     new_password = "novaSenhaSegura123"
#     response = requests.put(
#         f"{BASE_URL}/user/password",  # Ajuste endpoint
#         headers={"Authorization": f"Bearer {token}"},
#         json={
#             "current_password": user_data["password"],
#             "new_password": new_password
#         }
#     )
#     assert response.status_code == 200

#     # Verifica se login com nova senha funciona
#     response = requests.post(
#         f"{BASE_URL}/login",
#         json={
#             "email": user_data["email"],
#             "password": new_password
#         }
#     )
#     assert response.status_code == 200