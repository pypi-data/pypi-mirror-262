from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from .exception.internal_exception import DatabaseInitializeFailureException, DatabaseConnectFailureException


class MongoDB:
    def __init__(self, connection_url: str, db_name: str, ssl: bool = False, ssl_ca_certs: str = None):
        self.client = None
        self.connection_url = connection_url
        self.db_name = db_name
        self.ssl = ssl
        self.ssl_ca_certs = ssl_ca_certs

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(self.connection_url, ssl=self.ssl, tlsCAFile=self.ssl_ca_certs)
        except ServerSelectionTimeoutError:
            raise DatabaseInitializeFailureException()

    async def close(self):
        if self.client:
            self.client.close()

    def get_database(self):
        if not self.client:
            raise DatabaseConnectFailureException()
        return self.client[self.db_name]
