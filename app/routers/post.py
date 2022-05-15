from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
import sqlalchemy
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # Using SQL Methods
    # cursor.execute("""SELECT * from posts  """)
    # posts=cursor.fetchall()
    print(current_user)
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() (if we want to make the posts privat)
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )
    results = (
        db.query(models.Post, sqlalchemy.func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    print(results)
    return results


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(""" INSERT  INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    # (post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    # conn.commit()

    print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(""" SELECT *  FROM posts  where id = %s""",  (str(id),))
    # post=cursor.fetchone()
    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post with id {id} does not exist!",
        )
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f'the post with id {id} does not exist!'}
    post = (
        db.query(models.Post, sqlalchemy.func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post with id {id} does not exist!",
        )
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f'the post with id {id} does not exist!'}
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Action Forbidden"
        )
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    print(current_user)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"the post with id {id} does not exist!",
        )
        # response.status_code=status.HTTP_404_NOT_FOUNDif
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Action Forbidden"
        )

    # return {"message":f'the post with id {id} does not exist!'}
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
