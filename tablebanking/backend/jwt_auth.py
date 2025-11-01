import jwt
import frappe
from datetime import datetime, timedelta

class JWTAuth:
    def __init__(self):
        self.secret_key = frappe.conf.get("jwt_secret_key", "tablebanking-secret-key")
    
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm="HS256")
    
    def verify_token(self, token: str):
        return jwt.decode(token, self.secret_key, algorithms=["HS256"])
