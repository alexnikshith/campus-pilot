from typing import Generic, TypeVar, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository, ModelType, CreateSchemaType, UpdateSchemaType
from app.schemas.common import PaginationParams, PaginatedResponse

RepoType = TypeVar("RepoType", bound=BaseRepository)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, RepoType]):
    """
    Base Service layer abstraction encapsulating business rules, domain orchestration,
    and delegating database queries to the repository.
    """
    def __init__(self, repository: RepoType):
        self.repository = repository

    def get_by_id(self, db: Session, id: Any) -> ModelType:
        """Fetch entity by id or raise EntityNotFoundException."""
        return self.repository.get_or_404(db, id=id)

    def get_paginated(
        self,
        db: Session,
        pagination: PaginationParams,
        filter_by: Optional[dict] = None
    ) -> PaginatedResponse[ModelType]:
        """Fetch paginated entities with metadata."""
        items, total = self.repository.get_multi(
            db,
            skip=pagination.offset,
            limit=pagination.page_size,
            sort_by=pagination.sort_by,
            order=pagination.order,
            filter_by=filter_by
        )
        return PaginatedResponse.create(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size
        )

    def create(self, db: Session, obj_in: CreateSchemaType | dict) -> ModelType:
        """Create new entity."""
        return self.repository.create(db, obj_in=obj_in)

    def update(self, db: Session, id: Any, obj_in: UpdateSchemaType | dict) -> ModelType:
        """Update existing entity."""
        db_obj = self.get_by_id(db, id)
        return self.repository.update(db, db_obj=db_obj, obj_in=obj_in)

    def delete(self, db: Session, id: Any) -> ModelType:
        """Delete entity by id."""
        db_obj = self.get_by_id(db, id)
        self.repository.delete(db, id=id)
        return db_obj

