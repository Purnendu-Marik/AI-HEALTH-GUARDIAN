from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import (
    hash_password,
    verify_password
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# SIGNUP PAGE
# =========================================================

@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={
            "request": request
        }
    )


# =========================================================
# SIGNUP SUBMIT
# =========================================================

@router.post("/signup", response_class=HTMLResponse)
def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):

    db: Session = SessionLocal()

    try:

        # -------------------------------------------------
        # Password confirmation
        # -------------------------------------------------

        if password != confirm_password:

            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={
                    "request": request,
                    "error": "Passwords do not match."
                }
            )

        # -------------------------------------------------
        # Check username
        # -------------------------------------------------

        existing_username = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

        if existing_username:

            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={
                    "request": request,
                    "error": "This username is already taken."
                }
            )

        # -------------------------------------------------
        # Check email
        # -------------------------------------------------

        existing_email = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_email:

            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={
                    "request": request,
                    "error": "An account with this email already exists."
                }
            )

        # -------------------------------------------------
        # Hash password
        # -------------------------------------------------

        hashed_password = hash_password(password)

        # -------------------------------------------------
        # Create new user
        # -------------------------------------------------

        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        # -------------------------------------------------
        # Redirect to login
        # -------------------------------------------------

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    finally:

        db.close()


# =========================================================
# LOGIN PAGE
# =========================================================

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )


# =========================================================
# LOGIN SUBMIT
# =========================================================

@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    db: Session = SessionLocal()

    try:

        # -------------------------------------------------
        # Find user by email
        # -------------------------------------------------

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        # -------------------------------------------------
        # User not found
        # -------------------------------------------------

        if not user:

            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "request": request,
                    "error": "Invalid email or password."
                }
            )

        # -------------------------------------------------
        # Check password account
        # -------------------------------------------------

        if not user.password_hash:

            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "request": request,
                    "error": "This account does not use password login."
                }
            )

        # -------------------------------------------------
        # Verify password
        # -------------------------------------------------

        password_valid = verify_password(
            password,
            user.password_hash
        )

        # -------------------------------------------------
        # Wrong password
        # -------------------------------------------------

        if not password_valid:

            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "request": request,
                    "error": "Invalid email or password."
                }
            )

        # -------------------------------------------------
        # LOGIN SUCCESS
        # -------------------------------------------------

        request.session["user_id"] = user.id
        request.session["user_email"] = user.email
        request.session["username"] = user.username

        print(
            f"User logged in successfully: {user.email}"
        )

        # -------------------------------------------------
        # Redirect to home
        # -------------------------------------------------

        return RedirectResponse(
            url="/",
            status_code=303
        )

    finally:

        db.close()


# =========================================================
# LOGOUT
# =========================================================

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )

# =========================================================
# AUTHENTICATION HELPER
# =========================================================

def get_current_user(request, db):
    """
    Return the currently logged-in user.
    Return None if the user is not logged in.
    """

    user_id = request.session.get("user_id")

    if not user_id:
        return None

    user = db.query(User).filter(User.id == user_id).first()

    return user