from pytest_bdd import scenario, given, when, then
from fastapi.testclient import TestClient
from app.main import app

# Instancia del cliente de pruebas
client = TestClient(app)

@scenario('../features/app.feature', 'Acceso a la página principal')
def test_acceso_home():
    pass

@scenario('../features/app.feature', 'Acceso al dashboard')
def test_acceso_dashboard():
    pass

@given("la aplicación está ejecutándose", target_fixture="app_client")
def app_client():
    return client

@when('el usuario solicita la ruta "/"', target_fixture="response")
def request_home(app_client):
    return app_client.get("/")

@when('el usuario solicita la ruta "/dashboard"', target_fixture="response")
def request_dashboard(app_client):
    return app_client.get("/dashboard")

@then('la respuesta debe ser exitosa con código 200')
def verify_success(response):
    assert response.status_code == 200
