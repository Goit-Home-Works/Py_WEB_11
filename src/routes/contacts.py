from typing import List

from fastapi import Path, Depends, HTTPException, Query, status, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.database import get_db
from schemas import ContactFavoriteModel, ContactModel, ContactResponse
from repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    skip: int = 0,
    limit: int = Query(default=10, le=100, ge=10),
    db: Session = Depends(get_db),
):
    contacts = None
    if first_name or last_name or email:
        param = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "skip": skip,
            "limit": limit,
        }
        contacts = await repository_contacts.search_contacts(param, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("/search/birtdays", response_model=List[ContactResponse])
async def search_contacts(
    days: int = Query(default=7, le=30, ge=1),
    skip: int = 0,
    limit: int = Query(default=10, le=100, ge=10),
    db: Session = Depends(get_db),
):
    contacts = None
    if days:
        param = {
            "days": days,
            "skip": skip,
            "limit": limit,
        }
        contacts = await repository_contacts.search_birthday(param, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("", response_model=List[ContactResponse])
async def get_contacts(
    skip: int = 0,
    limit: int = Query(default=10, le=100, ge=10),
    favorite: bool = None,
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.get_contacts(
        db=db, skip=skip, limit=limit, favorite=favorite
    )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Email is exist!"
        )
    try:
        contact = await repository_contacts.create(body, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {err}"
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/{contact_id}/favorite", response_model=ContactResponse)
async def favorite_update(
    body: ContactFavoriteModel,
    contact_id: int = Path(ge=1),
    db: Session = Depends(get_db),
):
    contact = await repository_contacts.favorite_update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.delete(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return None
