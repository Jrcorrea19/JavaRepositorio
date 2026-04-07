# Guía rápida: errores de base de datos (explicado fácil)

Si te aparece un error de base de datos, seguí este orden exacto.

## 1) Abrí la terminal en VS Code
- Menú: **Terminal > New Terminal**
- Verificá que estás parado en la carpeta `backend`.

```bash
cd backend
```

## 2) Activá entorno virtual
### Linux/Mac
```bash
source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
```

## 3) Instalá dependencias
```bash
pip install -r requirements.txt
```

## 4) Probá la base de datos antes de levantar el servidor
```bash
python -m app.verificar_base_de_datos
```

Si este comando termina con "Verificación finalizada sin errores", la base está bien.

## 5) Recién ahí levantá el backend
```bash
uvicorn app.main:app --reload
```

---

## Errores comunes y solución

### Error: `ModuleNotFoundError: No module named 'app'`
Significa que no estás dentro de `backend`.

**Solución:**
```bash
cd backend
python -m app.verificar_base_de_datos
```

### Error: `no such table`
Significa que faltan tablas.

**Solución:** ejecutar primero:
```bash
python -m app.verificar_base_de_datos
```
Esto crea tablas automáticamente.

### Error: `unable to open database file`
Suele pasar por permisos o ruta.

**Solución recomendada:**
1. Ejecutar desde `backend`.
2. Ver ruta impresa por `verificar_base_de_datos`.
3. Confirmar que tenés permisos de escritura en esa carpeta.

---

## Qué hace cada archivo relacionado a BD
- `backend/app/database.py`: configura conexión SQLite, ruta del archivo y sesiones.
- `backend/app/models.py`: define tablas (`comments`, `products`).
- `backend/app/main.py`: inicializa tablas al arrancar y usa sesiones en endpoints.
- `backend/app/verificar_base_de_datos.py`: prueba guiada para validar la base antes de correr todo.

---

## Consejo para aprender (sin frustrarte)
Primero hacé funcionar el comando de verificación.
Después levantá API.
Después probá frontend.

Nunca intentes todo junto cuando hay errores: avanzá en capas.
