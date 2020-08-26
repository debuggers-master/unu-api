"""
Event close HTML template.
"""


def event_close_template(event_name: str, event_url: str) -> str:
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
      El evento {event_name} se acerca.
      Recuerda, mañana inicia.
      Programa: {event_url}
    </body>
    </html>
    """
