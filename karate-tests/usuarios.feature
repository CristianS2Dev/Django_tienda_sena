Feature: Pruebas de Usuarios

  Scenario: Registrar un nuevo usuario
    Given url baseUrl + "registrarse/"
    And request { 
        "nombre": "Usuario Prueba", 
        "correo": "prueba@example.com", 
        "password": "Password123!", 
        "valid_password": "Password123!" 
    }
    When method post
    Then status 201
    And match response.correo == 'prueba@example.com'

  Scenario: Iniciar sesión
    Given url baseUrl + "login/"
    And request { 
        "correo": "prueba@example.com", 
        "password": "Password123!" 
    }
    When method post
    Then status 200
    * def sessionid = responseCookies['sessionid'].value
    And match response contains { "nombre_apellido": "#string", "rol": "#number" }

  Scenario: Actualizar perfil del usuario
    # Primero, inicia sesión y guarda la cookie
    Given url baseUrl + "login/"
    And request { 
        "correo": "prueba@example.com", 
        "password": "Password123!" 
    }
    When method post
    Then status 200
    * def sessionid = responseCookies['sessionid'].value

    # Ahora, usa la cookie para actualizar el perfil
    Given url baseUrl + "actualizar_perfil/"
    And header Cookie = 'sessionid=' + sessionid
    And request { 
        "nombre": "Usuario Actualizado", 
        "contacto": "1234567890" 
    }
    When method post
    Then status 200
    And match response.nombre == 'Usuario Actualizado'