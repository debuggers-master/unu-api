"""
Welcome HTML template.
"""


def special_message_template(event_name: str, message: str) -> str:
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
      Event: {event_name}
      Special message: {message}
    </body>
    </html>
    """
