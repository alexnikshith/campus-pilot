from typing import Generic, TypeVar, Type, Optional, List, Any, Tuple, Union, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, asc
from pydantic import BaseModel

from app.models.base import Base
from app.core.exceptions import EntityNotFoundException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic Base Repository providing standardized CRUD operations and pagination queries
    using SQLAlchemy 2.0 ORM patterns.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Fetch a single record by primary key, or None if not found."""
        return db.get(self.model, id)

    def get_or_404(self, db: Session, id: Any) -> ModelType:
        """Fetch a single record by primary key, raising EntityNotFoundException if missing."""
        record = self.get(db, id)
        if not record:
            raise EntityNotFoundException(entity_name=self.model.__name__, identifier=id)
        return record

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "id",
        order: str = "asc",
        filter_by: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[ModelType], int]:
        """
        Fetch paginated collection of records with total count, sorting, and optional equality filters.
        """
        # Base query
        stmt = select(self.model)
        count_stmt = select(func.count()).select_from(self.model)

        # Apply equality filters
        if filter_by:
            for field, value in filter_by.items():
                if hasattr(self.model, field) and value is not None:
                    attr = getattr(self.model, field)
                    stmt = stmt.where(attr == value)
                    count_stmt = count_stmt.where(attr == value)

        # Count total matching records
        total = db.scalar(count_stmt) or 0

        # Apply sorting
        if hasattr(self.model, sort_by):
            sort_attr = getattr(self.model, sort_by)
            stmt = stmt.order_by(desc(sort_attr) if order.lower() == "desc" else asc(sort_attr))
        elif hasattr(self.model, "id"):
            stmt = stmt.order_by(asc(getattr(self.model, "id")))

        # Apply pagination limits
        stmt = stmt.offset(skip).limit(limit)
        items = list(db.scalars(stmt).all())

        return items, total

    def create(self, db: Session, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        """Create a new database record from a Pydantic schema or dictionary."""
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing database record with non-null incoming fields."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """Delete a record by primary key."""
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def count(self, db: Session, filter_by: Optional[Dict[str, Any]] = None) -> int:
        """Count records matching optional equality filters."""
        stmt = select(func.count()).select_from(self.model)
        if filter_by:
            for field, value in filter_by.items():
                if hasattr(self.model, field) and value is not None:
                    stmt = stmt.where(getattr(self.model, field) == value)
        return db.scalar(stmt) or 0

