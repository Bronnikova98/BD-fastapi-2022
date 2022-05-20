import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

# класс авторизатор
class AuthHandler():
    # чтобы фастапи мог считывать пароли
    secutiy = HTTPBearer()
    pwd_context=CryptContext(
        # алгоритм
        schemes=['bcrypt'],
        # настройка 
        deprecated = 'auto'
    )
    # ключ для проверки (подпись токена)
    secret='Злата не спит на паре'
    
    def get_passwird_hash(self, password):
        return self.pwd_context.hash(password)
    
    # проверка пароля хешированного
    # input_pass введенный пароль
    # hash_pass хэшированный пароль
    def verify_password(self, input_pass, hash_pass):
        return self.pwd_context.verify(input_pass, hash_pass)
    # создание jwt токена
    def encode_token(self, username):
        payload={
            # время жизни токена (станет просроченным через)
            'exp': datetime.utcnow()+timedelta(minutes=10),
            # начальное время создания
            'iat': datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
   
    def decode_token(self, token):
        try:
            payload= jwt.decode(
                token,
                self.secret,
                algorithms=['HS256']
            )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, 'Просрочено')
        except jwt.InvalidTokenError as e:
            raise HTTPException(401, 'Плохой токен')
        
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials=Security(secutiy)):
        return self.decode_token(auth.credentials)