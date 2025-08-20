class AppEnvironment:
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"

    @staticmethod
    def is_local_env(env: str) -> bool:
        return env == AppEnvironment.LOCAL

    @staticmethod
    def is_dev_env(env: str) -> bool:
        return env == AppEnvironment.DEV

    @staticmethod
    def is_prod_env(env: str) -> bool:
        return env == AppEnvironment.PROD
