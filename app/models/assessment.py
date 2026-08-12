from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class AssessmentResult(Base):

    __tablename__ = "assessment_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    score = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )