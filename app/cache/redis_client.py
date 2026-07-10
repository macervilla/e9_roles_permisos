import os

import redis


class RedisFake:
    def __init__(self):
        self._datos = {}

    def get(self, clave):
        return self._datos.get(clave)

    def set(self, clave, valor, ex=None):
        self._datos[clave] = valor
        return True

    def setex(self, clave, tiempo, valor):
        self._datos[clave] = valor
        return True

    def delete(self, *claves):
        for clave in claves:
            self._datos.pop(clave, None)
        return True


if os.getenv("TESTING") == "1":
    redis_client = RedisFake()
else:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True,
    )
