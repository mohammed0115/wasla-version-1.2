from __future__ import annotations

import logging
import os

from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError

logger = logging.getLogger("system.go_live")


class SystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "system"

    def ready(self) -> None:
        if not getattr(settings, "GO_LIVE_STARTUP_CHECK_ENABLED", True):
            return

        # Avoid running twice in dev server reloaders when possible.
        if os.environ.get("RUN_MAIN") == "false":
            return

        # Defer the check until after apps are fully loaded to avoid
        # "Accessing the database during app initialization" warning.
        from django.db.models.signals import post_migrate

        def _run_go_live_check(sender, **kwargs):
            try:
                from system.application.use_cases.check_go_live import CheckGoLiveUseCase

                report = CheckGoLiveUseCase.execute()
                logger.info(
                    "go_live_startup_check",
                    extra={
                        "ok": report.ok,
                        "score": report.score,
                        "hard_blockers": len(report.hard_blockers),
                        "warnings": len(report.warnings),
                    },
                )
            except (OperationalError, ProgrammingError):
                logger.warning("go_live_startup_check_skipped", extra={"reason": "db_not_ready"})
            except Exception as exc:  # pragma: no cover - fail open
                logger.exception("go_live_startup_check_failed", extra={"error_code": exc.__class__.__name__})

        # Only connect once
        post_migrate.connect(_run_go_live_check, sender=self, dispatch_uid="system_go_live_check")
