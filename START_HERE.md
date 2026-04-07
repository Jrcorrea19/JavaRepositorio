# 🚀 Empezá por acá (si no sabés dónde poner el código)

Perfecto: esta guía es para vos si pensaste **"no sé dónde poner cada archivo"**.

## 0) ¿En consola o en Visual Studio Code?
Las dos cosas:
- **Visual Studio Code**: para crear/editar archivos y pegar el código.
- **Consola/terminal**: para ejecutar comandos (`pip install`, `uvicorn`, `python -m http.server`).

En VS Code abrí la carpeta del proyecto y luego abrí la terminal integrada con **Terminal > New Terminal**.
Así hacés todo en la misma app, sin complicarte.


## 1) Creá una carpeta de proyecto
```bash
mkdir JoyasMisterio
cd JoyasMisterio
```

## 2) Copiá esta estructura exacta
```text
JoyasMisterio/
  backend/
    requirements.txt
    app/
      __init__.py
      main.py
      database.py
      models.py
      schemas.py
      classifier.py
      realtime.py
  frontend/
    index.html
    styles.css
    app.js
  README.md
  START_HERE.md
```

## 3) ¿Dónde va cada código?
- Código Python del backend: en `backend/app/`
- Dependencias Python: en `backend/requirements.txt`
- Pantalla web: en `frontend/index.html`
- Estilos: en `frontend/styles.css`
- Lógica del navegador: en `frontend/app.js`

## 4) Levantar backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 5) Levantar frontend
Abrí otra terminal:
```bash
cd frontend
python -m http.server 5500
```

Entrá a `http://localhost:5500`.

## 6) Probar rápido sin Facebook
- Botón **"+ Simular comentario"** en la UI, o
- Llamá por terminal:
```bash
curl -X POST http://localhost:8000/simulate
```

## 7) Si no funciona
Chequeá:
1. ¿Está el backend en `http://localhost:8000`?
2. ¿Abriste frontend con `http.server` y no doble click directo al HTML?
3. ¿Instalaste dependencias dentro del venv?

Si querés, en el próximo paso te armo una versión con **instalación 1 comando** (`make dev`) para que sea todavía más simple.
