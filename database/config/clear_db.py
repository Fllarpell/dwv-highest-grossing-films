from ..config import Session
from ..models.models import Film

def clear_database():
    session = Session()
    try:
        session.query(Film).delete()
        session.commit()
        
    except Exception as e:
        session.rollback()
    finally:
        session.close()