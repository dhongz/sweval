from sqlalchemy import (Column,
                        String, 
                        ForeignKey, 
                        Boolean, 
                        DateTime, 
                        UniqueConstraint,
                        Integer)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
import uuid
from datetime import datetime, timezone

def generate_uuid():
    return str(uuid.uuid4())

# Create single Base class
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    # email = Column(String, nullable=False)
    # password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    generations = relationship("Generation", back_populates="user")
    group = relationship("Group", back_populates="users")


class Group(Base):
    __tablename__ = "groups"
    id = Column(String, primary_key=True)
    topic_content_type_pair = Column(JSONB, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_preference = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False)

    optimized_assesser = Column(JSONB, nullable=True)
    optimized_extractor = Column(JSONB, nullable=True)
    optimized_generator = Column(JSONB, nullable=True)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="group")

    generations = relationship("Generation", back_populates="group")
    group_examples = relationship("GroupExample", back_populates="group")

class Generation(Base):
    __tablename__ = "generations"
    id = Column(String, primary_key=True)
    batch_id = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    user_preference = Column(String, nullable=False)
    content = Column(String, nullable=False)

    predicted_user_feedback = Column(Boolean, nullable=True)
    user_feedback = Column(Boolean, nullable=True)
    # feedback_reasoning = Column(String, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="generations")

    group_id = Column(String, ForeignKey("groups.id"), nullable=False)
    group = relationship("Group", back_populates="generations")


class Example(Base):
    __tablename__ = "examples"
    id = Column(String, primary_key=True)
    topic = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    user_preference = Column(String, nullable=False)
    content = Column(String, nullable=False)
    quality = Column(Boolean, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False)

    group_examples = relationship("GroupExample", back_populates="example")


class GroupExample(Base):
    __tablename__ = "group_examples"
    id = Column(String, primary_key=True)
    group_id = Column(String, ForeignKey("groups.id"), nullable=False)
    group = relationship("Group", back_populates="group_examples")

    example_id = Column(String, ForeignKey("examples.id"), nullable=False)
    example = relationship("Example", back_populates="group_examples")