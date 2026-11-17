from fastapi import FastAPI, HTTPException, Response

from app.repository import PostNotFoundError, PostRepository
from app.schemas import PostCreate, PostOut, PostPatch, PostReplace

app = FastAPI(title="Bulletin Board")
repo = PostRepository()


@app.post("/posts", response_model=PostOut, status_code=201)
def create_post(body: PostCreate) -> PostOut:
    return PostOut.model_validate(repo.create(body.model_dump()))


@app.get("/posts/{post_id}", response_model=PostOut)
def read_post(post_id: int) -> PostOut:
    try:
        return PostOut.model_validate(repo.get(post_id))
    except PostNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.put("/posts/{post_id}", response_model=PostOut)
def replace_post(post_id: int, body: PostReplace) -> PostOut:
    try:
        return PostOut.model_validate(repo.replace(post_id, body.model_dump()))
    except PostNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.patch("/posts/{post_id}", response_model=PostOut)
def patch_post(post_id: int, body: PostPatch) -> PostOut:
    try:
        return PostOut.model_validate(
            repo.patch(post_id, body.model_dump(exclude_unset=True))
        )
    except PostNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.delete("/posts/{post_id}", status_code=204, response_class=Response)
def delete_post(post_id: int) -> Response:
    try:
        repo.delete(post_id)
    except PostNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)
