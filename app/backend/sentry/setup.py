import logging

import sentry_sdk


log = logging.getLogger("sentry")


def setup_sentry(dsn: str):
    try:
        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        log.info("Sentry initialized successfully")
    except Exception:
        log.exception("Failed to setup sentry")