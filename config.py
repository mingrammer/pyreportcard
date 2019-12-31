class Config:
    try:
        from config_secret import SecretConfig
        SECRET_KEY = SecretConfig.SECRET_KEY
        # MongoDB config
        MONGO_DBNAME = SecretConfig.MONGO_DBNAME
        MONGO_HOST = SecretConfig.MONGO_HOST
        MONGO_PORT = SecretConfig.MONGO_PORT
        MONGO_URI = 'mongodb://{}:{}'.format(MONGO_HOST, MONGO_PORT)
    except ImportError:
        SECRET_KEY = 'local-secret'
        # MongoDB config
        MONGO_DBNAME = 'reportcard'
        MONGO_HOST = 'localhost'
        MONGO_PORT = 27017
        MONGO_URI = 'mongodb://{}:{}'.format(MONGO_HOST, MONGO_PORT)

    # Cloning config
    CLONE_TMP_DIR = 'tmp'
    CLONE_TIMEOUT = 30
