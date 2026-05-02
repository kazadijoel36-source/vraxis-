from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import string

db = SQLAlchemy()

class Drop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    code = db.Column(db.String(4), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_retrieved = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_code():
        """Generates a unique 4-digit numeric code."""
        while True:
            code = ''.join(random.choices(string.digits, k=4))
            if not Drop.query.filter_by(code=code).first():
                return code