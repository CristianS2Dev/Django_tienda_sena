Feature: Pruebas de Productos

  Background:
    * def baseUrl = 'http://127.0.0.1:8000'
    Given url baseUrl + '/login/'
    And request { correo: 'vendedor@predeterminado.com', password: '123456' }
    When method post
    Then status 200
    * def sessionid = responseCookies['sessionid'].value

  Scenario: Obtener lista de productos
    Given url baseUrl + '/lista_productos'
    And header Cookie = 'sessionid=' + sessionid
    When method get
    Then status 200
    And match response[0] contains { nombre: '#string', stock: '#number' }

