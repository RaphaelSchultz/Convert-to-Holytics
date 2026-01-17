"""Convert PNG to ICO for Windows executable icon."""
from PIL import Image

# Load the generated icon
img = Image.open(r'C:\Users\Rapahel Morais\.gemini\antigravity\brain\eaf63a40-0870-4480-bf2f-8adb89acff27\app_icon_1768678953014.png')

# Resize to multiple sizes for Windows
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save('icon.ico', format='ICO', sizes=icon_sizes)

print("✅ icon.ico criado com sucesso!")
