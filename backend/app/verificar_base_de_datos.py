from __future__ import annotations

from sqlalchemy import text

from .database import RUTA_ARCHIVO_BASE_DE_DATOS, FabricaDeSesiones, inicializar_base_de_datos


def ejecutar_verificacion_de_base_de_datos() -> None:
    print("=== Verificación de Base de Datos Joyas Misterio ===")
    print(f"Ruta esperada del archivo SQLite: {RUTA_ARCHIVO_BASE_DE_DATOS}")

    inicializar_base_de_datos()
    print("Tablas verificadas/creadas correctamente.")

    sesion_base_de_datos = FabricaDeSesiones()
    try:
        resultado_sql = sesion_base_de_datos.execute(text("SELECT 1"))
        valor = resultado_sql.scalar_one()
        print(f"Consulta de prueba OK. Resultado: {valor}")
    finally:
        sesion_base_de_datos.close()

    print("Verificación finalizada sin errores.")


if __name__ == "__main__":
    ejecutar_verificacion_de_base_de_datos()
