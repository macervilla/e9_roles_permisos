import os

import redis
from redis.exceptions import RedisError


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


class RedisSeguro:
    """
    Usa Redis cuando está disponible.
    Si Redis falla, utiliza una caché local en memoria.
    """

    def __init__(self):
        self._fallback = RedisFake()

        self._redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
        )

    def get(self, clave):
        try:
            return self._redis.get(clave)
        except RedisError:
            return self._fallback.get(clave)

    def set(self, clave, valor, ex=None):
        try:
            return self._redis.set(clave, valor, ex=ex)
        except RedisError:
            return self._fallback.set(clave, valor, ex=ex)

    def setex(self, clave, tiempo, valor):
        try:
            return self._redis.setex(clave, tiempo, valor)
        except RedisError:
            return self._fallback.setex(clave, tiempo, valor)

    def delete(self, *claves):
        try:
            return self._redis.delete(*claves)
        except RedisError:
            return self._fallback.delete(*claves)


if os.getenv("TESTING") == "1":
    redis_client = RedisFake()
else:
    redis_client = RedisSeguro()
