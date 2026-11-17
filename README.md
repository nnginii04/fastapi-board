# FastAPI Bulletin Board

A minimal bulletin-board (게시판) API with five endpoints on an in-memory store.
Endpoints: `POST /posts`, `GET/PUT/PATCH/DELETE /posts/{post_id}`.

Run the server:

    pip install -r requirements.txt
    uvicorn app.main:app --reload

Run the tests:

    pytest
