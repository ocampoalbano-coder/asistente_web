from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.excel_reports import generar_reporte

IN = Path("data"); IN.mkdir(exist_ok=True, parents=True)

class H(FileSystemEventHandler):
    def on_created(self, e):
        if e.is_directory: return
        p = Path(e.src_path)
        if p.suffix.lower() == ".csv":
            print("ðŸ“¥ Nuevo CSV:", p.name)
            out = generar_reporte(p)
            print("âœ… Reporte:", out)

if __name__ == "__main__":
    obs = Observer(); obs.schedule(H(), str(IN), recursive=False); obs.start()
    print("ðŸ‘€ Observando carpeta 'data'... (Ctrl+C para salir)")
    try:
        while True: time.sleep(1)
    finally:
        obs.stop(); obs.join()
