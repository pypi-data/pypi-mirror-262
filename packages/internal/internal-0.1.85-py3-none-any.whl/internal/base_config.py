from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    DEBUG: bool = False
    RUN_PORT: int = 5000
    TIME_ZONE: str = "Asia/Taipei"

    # Request
    REQUEST_VERIFY_SSL: bool = True
    REQUEST_PROXY: str = ''
    REQUEST_RETRY: int = 5
    REQUEST_CONN_TIMEOUT: float = 5
    REQUEST_READ_TIMEOUT: float = 5
    REQUEST_WRITE_TIMEOUT: float = 5
    REQUEST_POOL_TIMEOUT: float = 5

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_REGION: str = ""
    AWS_PARAMETER_PATH_PREFIX: str = ""
    AWS_LOGGROUP_NAME: str = ""

    # MongoDB
    DATABASE_HOST: str = ''
    DATABASE_USERNAME: str = ''
    DATABASE_PASSWORD: str = ''
    DATABASE_PORT: int = 27017
    DATABASE_NAME: str = ""
    DATABASE_SSL: bool = True
    DATABASE_SSL_CA_CERTS: str = "/rds-combined-ca-bundle.pem"
    DATABASE_SERVER_SELECTION_TIMEOUT_MS: int = 5000
    DATABASE_CONNECT_TIMEOUT_MS: int = 10000

    # Micro Service
    AUTH_BASE_URL: str = "http://auth-service-api"
    ORGANIZATION_BASE_URL: str = "http://organization-service-api"
    CUSTOMER_BASE_URL: str = "http://customer-service-api"
    CAR_BASE_URL: str = "http://car-service-api"
    RELATIONSHIP_MANAGEMENT_BASE_URL: str = "http://relationship-management-service-api"
    TICKET_BASE_URL: str = "http://ticket-service-api"
    NOTIFY_BASE_URL: str = "http://notify-service-api"
    THIRD_PARTY_BASE_URL: str = "http://third-party-service-api"
    SCHEDULER_BASE_URL: str = "http://scheduler-service-api"

    class Config:
        case_sensitive = False
