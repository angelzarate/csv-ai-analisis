from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from sqlalchemy import JSON



class Base(DeclarativeBase):
    pass


class RequestModel(Base):
    __tablename__ = "requests"

    id_solicitud: Mapped[str] = mapped_column(primary_key=True)
    cliente: Mapped[str]
    canal: Mapped[str]
    fecha: Mapped[date]
    descripcion: Mapped[str]
    producto: Mapped[str]
    ciudad: Mapped[str]
    prioridad_manual: Mapped[str]
    comentarios_adicionales: Mapped[str]



class RequestResponse(Base):
    __tablename__ = "request_responses"

    id_solicitud: Mapped[str] = mapped_column(primary_key=True)
    categoria_sugerida: Mapped[str]
    prioridad_sugerida: Mapped[str]
    sentimiento: Mapped[str]
    resumen: Mapped[str]
    datos_faltantes: Mapped[list[str]] = mapped_column(JSON)
    requiere_revision_humana: Mapped[bool]
    justificacion: Mapped[str]
    tokens_usados: Mapped[int]
    modelo_usado: Mapped[str]
