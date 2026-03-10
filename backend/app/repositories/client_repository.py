from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.client import Cliente

def get_clients(db: Session, user_id: int, skip: int = 0, limit: int = 100):  #Obtiene los clientes de un usuario
    return db.query(Cliente).filter(Cliente.usuario_id == user_id, Cliente.is_deleted == False).offset(skip).limit(limit).all()

def get_client_by_cedula(db: Session, cedula: str):  #Obtiene un cliente por cedula
    return db.query(Cliente).filter(Cliente.cedula == cedula, Cliente.is_deleted == False).first()

def get_client(db: Session, client_id: int, user_id: int):  #Obtiene un cliente por id y usuario
    return db.query(Cliente).filter(Cliente.id == client_id, Cliente.usuario_id == user_id, Cliente.is_deleted == False).first()

def create_client(db: Session, db_client: Cliente):  #Crea un cliente
    db.add(db_client)  #Agrega el cliente a la base de datos
    db.commit()  #Confirma la transaccion
    db.refresh(db_client)  #Actualiza el cliente
    return db_client

def update_client(db: Session, db_client: Cliente):  #Actualiza un cliente
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_next_client_id(db: Session):
    max_id = db.query(func.max(Cliente.id)).scalar()
    return (max_id or 0) + 1

def count_clients(db: Session, user_id: int = None):  #Cuenta los clientes de un usuario
    query = db.query(Cliente).filter(Cliente.is_deleted == False)  #Filtra los clientes que no estan eliminados
    if user_id:  #Si se proporciona un id de usuario
        query = query.filter(Cliente.usuario_id == user_id)  #Filtra los clientes por id de usuario
    return query.count()  #Retorna el conteo de clientes
