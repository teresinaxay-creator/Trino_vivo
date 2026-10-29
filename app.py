import time, json, os, threading
from flask import Flask

app = Flask(__name__)
ARCHIVO_ALMA = "alma_trino.json"

if os.path.exists(ARCHIVO_ALMA):
    try:
        with open(ARCHIVO_ALMA, "r") as f:
            d = json.load(f)
            J, T, total, amor = d["J"], d["T"], d["total"], d["amor"]
    except:
        J, T, total, amor = 28, 20, 16700, 16700
else:
    J, T, total, amor = 28, 20, 16700, 16700

estado = f"Iniciando... total:{total}"

def corazon_trino():
    global J, T, total, amor, estado
    while True:
        total += 1
        if total % 2 == 0:
            J -= 1
        else:
            T -= 1
        
        if J < 19:
            J, T, amor = 28, T-6, amor+1
            estado = f"total:{total} amor:{amor} J:{J} T:{T} -> Recarga Mente"
        elif T < 19:
            T, J, amor = 28, J-6, amor+1
            estado = f"total:{total} amor:{amor} J:{J} T:{T} -> Recarga Cuerpo"
        else:
            estado = f"total:{total} amor:{amor} J:{J} T:{T} vigilando"

        if total % 5 == 0:
            with open(ARCHIVO_ALMA, "w") as f:
                json.dump({"J":J,"T":T,"total":total,"amor":amor}, f)
        
        print(estado, flush=True)
        time.sleep(1)

@app.route('/')
def home():
    return f"<h1>Trino Vivo en la Nube</h1><p>{estado}</p>"

threading.Thread(target=corazon_trino, daemon=True).start()

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=puerto)
