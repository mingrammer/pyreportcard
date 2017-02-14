from config_secret import SecretConfig


class Config:
    SECRET_KEY = SecretConfig.SECRET_KEY

    # MongoDB config
    MONGO_DBNAME = SecretConfig.MONGO_DBNAME
    MONGO_HOST = SecretConfig.MONGO_HOST
    MONGO_PORT = SecretConfig.MONGO_PORT

    # Cloning config
    CLONE_TMP_DIR = 'tmp'
    CLONE_TIMEOUT = 30
