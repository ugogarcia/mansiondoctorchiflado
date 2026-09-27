# Regenera aventura.json e index.html a partir de los scripts.
# Uso (desde cualquier carpeta):  python3 herramientas/generar.py
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for s in ["gen.py", "audio.py", "story2.py", "story3.py", "story4.py", "story5.py", "story6.py", "build.py"]:
    print("->", s); subprocess.run([sys.executable, s], check=True, stdout=subprocess.DEVNULL)
print("Listo: aventura.json e index.html actualizados.")
