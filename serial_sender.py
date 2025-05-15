pip install pyserial
from serial_sender import enviar_comando

# Cambiar color LED RGB
r, g, b = 255, 100, 180
enviar_comando(f"COLOR {r:03} {g:03} {b:03}")

# Encender buzzer
enviar_comando("BUZZER_ON")

# Mostrar texto en pantalla OLED
enviar_comando("TEXT Inception Vol:80")
