import sys
import os

# Add the project root to sys.path to allow importing from 'app'
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:5521@localhost:5432/lexContractbd"

def normalize_statuses():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("Normalizando estados de contratos a MAYÚSCULAS...")
        
        # SQL to update all statuses to uppercase
        result = db.execute(text("UPDATE contrato SET estado = UPPER(estado) WHERE estado != UPPER(estado)"))
        db.commit()
        
        print(f"Se actualizaron {result.rowcount} contratos.")
        
        # Verify
        remaining = db.execute(text("SELECT id, estado FROM contrato WHERE estado != UPPER(estado)")).fetchall()
        if not remaining:
            print("Verificación exitosa: Todos los estados están en mayúsculas.")
        else:
            print(f"Advertencia: Aún quedan {len(remaining)} contratos sin normalizar.")
            
    except Exception as e:
        print(f"Error durante la normalización: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    normalize_statuses()
