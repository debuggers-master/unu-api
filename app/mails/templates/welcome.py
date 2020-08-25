"""
Welcome HTML template.
"""


def welcome_template(name: str) -> str:
    """
    Return a welcome template.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Unu Events</title>
    </head>
    <body>
      <div style="text-align: center;" class="card">
        <h1 style="text-decoration: underline; margin-bottom: 25px;">Unu Events</h1>
        <h2>Bienvenido {name}, a Unu App</h2>
      </div>
      <h4><strong>Unu</strong> te permite crear y gestionar
        la organización de tus eventos en un solo lugar.
        Podras crear y personalizar la página de tu evento. Añadir colaboradores
        para que en equipo puedan lanzar un proyecto del más alto nivel.
      </h4>
      <h3>No esperes más y comienza ya!</h3>
      <button style="color: #ec6d64;">
        <a href="https://unu.vercel.app">Go to Unu</a>
      </button>
    </body>
    </html>
    """
