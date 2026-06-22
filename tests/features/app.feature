Feature: Verificación de las vistas de la aplicación
  Como usuario de la aplicación
  Quiero poder acceder a la página de inicio, al dashboard y a la vista de administración
  Para poder interactuar con la plataforma

  Scenario: Acceso a la página principal
    Given la aplicación está ejecutándose
    When el usuario solicita la ruta "/"
    Then la respuesta debe ser exitosa con código 200

  Scenario: Acceso al dashboard
    Given la aplicación está ejecutándose
    When el usuario solicita la ruta "/dashboard"
    Then la respuesta debe ser exitosa con código 200
