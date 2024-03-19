from django.conf import settings

DEV_ENVIRONMENT = "dev"
TEST_ENVIRONMENT = "test"
STAGE_ENVIRONMENT = "stage"
PROD_ENVIRONMENT = "prod"


def is_dev(env: str = settings.APP_ENVIRONMENT) -> bool:
    return env == DEV_ENVIRONMENT


def is_test(env: str = settings.APP_ENVIRONMENT) -> bool:
    return env == TEST_ENVIRONMENT


def is_stage(env: str = settings.APP_ENVIRONMENT) -> bool:
    return env == STAGE_ENVIRONMENT


def is_prod(env: str = settings.APP_ENVIRONMENT) -> bool:
    return env == PROD_ENVIRONMENT
