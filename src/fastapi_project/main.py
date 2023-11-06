from dataclasses import asdict
from typing import Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.category.application.usecase.create_category import CreateCategoryRequest, CreateCategory
from core.category.application.usecase.get_category import GetCategoryRequest, GetCategory
from core.category.infrastructure.fastapi_app.category_sqlalchemy_repository import CategorySQLAlchemyRepository
from core.category.infrastructure.fastapi_app.orm import start_mappers, metadata

app = FastAPI()

# Setup database
DATABASE_URL = "sqlite://"  # TODO: use ROOT_DIR (same DB as Django)


def get_db():
    start_mappers()
    engine = create_engine(DATABASE_URL)
    metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: could this be my usecase object?
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    is_active: Optional[bool] = True


class CategoryCreateResponse(BaseModel):
    id: UUID


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: str
    is_active: bool


@app.post("/api/categories/", response_model=CategoryCreateResponse)
def create_category(request: CategoryCreate, db: Session = Depends(get_db)):
    input = CreateCategoryRequest(**request.model_dump())
    output = CreateCategory(category_repository=CategorySQLAlchemyRepository(session=db)).execute(input)
    return CategoryCreateResponse(id=output.id)


@app.get("/api/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    input = GetCategoryRequest(category_id=category_id)
    output = GetCategory(category_repository=CategorySQLAlchemyRepository(session=db)).execute(input)
    if not output.category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryResponse(**asdict(output.category))
