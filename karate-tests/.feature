Feature: Prueba básica

  Scenario: Obtener lista de productos
    Given url 'http://localhost:8000/lista_productos'
    When method get
    Then status 200
    # Puedes agregar más validaciones si sabes la estructura del JSON