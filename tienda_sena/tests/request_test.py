import requests

def test_usuarios_json():
    url = "http://localhost:8000/usuarios/json/"
    response = requests.get(url)
    print("Status code:", response.status_code)
    print("Response text:", response.text)  # <-- Agregado para depuración
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0]
        assert 'nombre_apellido' in data[0]
        assert 'rol' in data[0]

if __name__ == "__main__":
    test_usuarios_json()
    print("Prueba exitosa")