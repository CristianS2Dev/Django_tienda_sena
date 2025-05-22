Feature: Pruebas de Productos

  Background:
    # Realiza login y guarda la cookie de sesión
    Given url baseUrl + '/login/'
    And request { correo: '	vendedor@predeterminado.com', password: '123456' }
    When method post
    Then status 200
    * def sessionid = responseCookies['sessionid'].value

  Scenario: Obtener lista de productos
    Given url baseUrl + '/lista_productos'
    And header Cookie = 'sessionid=' + sessionid
    When method get
    Then status 200
    And match response[0] contains { "nombre": "#string", "stock": "#number" }

 Scenario: Crear un nuevo producto
  Given url baseUrl + '/agregar_producto'
  And header Cookie = 'sessionid=' + sessionid
  And request { 
      "nombre": "Producto de prueba", 
      "descripcion": "Descripción de prueba", 
      "precio_original": 100.0, 
      "stock": 10, 
      "categoria": 1, 
      "color": 2 
  }
  When method post
  Then status 201
  And match response.nombre == 'Producto de prueba'

  Scenario: Actualizar un producto existente
    Given url baseUrl + '/editar_producto/31/'
    And header Cookie = 'sessionid=' + sessionid
    And request { 
        "nombre": "Producto actualizado", 
        "descripcion": "Descripción actualizada", 
        "precio_original": 150.0 
    }
    When method put
    Then status 200
    And match response.nombre == 'Producto actualizado'

  Scenario: Eliminar un producto
    Given url baseUrl + '/eliminar_producto/44/'
    And header Cookie = 'sessionid=' + sessionid
    When method delete
    Then status 204