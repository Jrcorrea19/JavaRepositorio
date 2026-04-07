from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

# Ruta absoluta para evitar errores cuando Uvicorn se ejecuta desde otra carpeta.
RUTA_CARPETA_BACKEND = Path(__file__).resolve().parents[1]
RUTA_ARCHIVO_BASE_DE_DATOS = RUTA_CARPETA_BACKEND / "joyas_misterio.db"
URL_BASE_DE_DATOS = f"sqlite:///{RUTA_ARCHIVO_BASE_DE_DATOS}"

motor_sqlalchemy = create_engine(
    URL_BASE_DE_DATOS,
    connect_args={"check_same_thread": False},
)

FabricaDeSesiones = sessionmaker(
    bind=motor_sqlalchemy,
    autoflush=False,
    autocommit=False,
    class_=Session,
)


def obtener_sesion_de_base_de_datos() -> Session:
    sesion_base_de_datos = FabricaDeSesiones()
    try:
        yield sesion_base_de_datos
    finally:
        sesion_base_de_datos.close()


def inicializar_base_de_datos() -> None:
    Base.metadata.create_all(bind=motor_sqlalchemy)
