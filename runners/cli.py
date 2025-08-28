import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from core.router import route
from core.utils import ensure_dirs

if __name__ == "__main__":
    ensure_dirs()
    if len(sys.argv) < 2:
        print('Uso: python runners/cli.py "genera reporte data/ventas.csv"')
        sys.exit(0)
    command = " ".join(sys.argv[1:])
    print(route(command))
