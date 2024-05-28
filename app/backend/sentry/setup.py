import sentry_sdk


def setup_sentry(dsn: str):
    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )