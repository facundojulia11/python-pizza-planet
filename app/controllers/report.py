from typing import Tuple
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Optional, Tuple

from app.repositories.managers import ReportManager
from ..repositories.managers import IndexManager


class ReportController:
    manager = ReportManager

    @classmethod
    def get_all(cls) -> Tuple[Any, Optional[str]]:
        try:
            return cls.manager.get_report(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)