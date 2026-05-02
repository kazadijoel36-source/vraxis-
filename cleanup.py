from app import app, db, Drop
from datetime import datetime

def purge_expired():
    with app.app_context():
        # Delete drops that are either retrieved or past their expiry
        deleted = Drop.query.filter(
            (Drop.is_retrieved == True) | (Drop.expires_at < datetime.utcnow())
        ).delete()
        db.session.commit()
        print(f"Purge complete: {deleted} drops removed from Potchefstroom node.")

if __name__ == "__main__":
    purge_expired()