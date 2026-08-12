from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from starlette.middleware.sessions import SessionMiddleware

from app.services.health_analyzer import analyze_health_data
from app.services.ai_service import (
    generate_health_insights,
    parse_ai_insights
)

from app.routers.auth import router as auth_router
from app.database import SessionLocal, engine, Base
from app.models.assessment import AssessmentResult

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="AI Health Guardian",
    version="1.0"
)

Base.metadata.create_all(bind=engine)
# =========================================================
# SESSION MIDDLEWARE
# =========================================================

app.add_middleware(
    SessionMiddleware,
    secret_key="CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_KEY",
    max_age=60 * 60 * 24 * 7,
    same_site="lax",
    https_only=False
)


# =========================================================
# AUTH ROUTER
# =========================================================

app.include_router(auth_router)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =========================================================
# TEMPLATES
# =========================================================

templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# ROOT PAGE
# =========================================================

@app.get("/")
def home(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/signup",
            status_code=303
        )

    db = SessionLocal()

    try:

        latest_assessment = (
            db.query(AssessmentResult)
            .filter(
                AssessmentResult.user_id == user_id
            )
            .order_by(
                AssessmentResult.created_at.desc()
            )
            .first()
        )

    finally:

        db.close()


    health_score = (
        latest_assessment.score
        if latest_assessment
        else None
    )


    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "health_score": health_score
        }
    )

# =========================================================
# HEALTH ASSESSMENT PAGE
# =========================================================

@app.get("/assessment", response_class=HTMLResponse)
def assessment_page(request: Request):

    # Check login
    user_id = request.session.get("user_id")

    # -----------------------------------------------------
    # User is NOT logged in
    # -----------------------------------------------------

    if not user_id:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # -----------------------------------------------------
    # User IS logged in
    # -----------------------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="assessment.html",
        context={
            "request": request
        }
    )


# =========================================================
# HEALTH ASSESSMENT SUBMIT
# =========================================================

@app.post("/assessment", response_class=HTMLResponse)
def assessment_submit(
    request: Request,
    age: int = Form(...),
    gender: str = Form(...),
    symptoms: list[str] = Form(default=[]),
    sleep: str = Form(...),
    activity: str = Form(...),
    additional_info: str = Form("")
):

    # -----------------------------------------------------
    # Check login again
    # -----------------------------------------------------

    user_id = request.session.get("user_id")

    if not user_id:

        return RedirectResponse(
            url="/login",
            status_code=303
        )


    # =====================================================
    # HEALTH ANALYSIS
    # =====================================================

    result = analyze_health_data(
        age=age,
        gender=gender,
        symptoms=symptoms,
        sleep=sleep,
        activity=activity,
        additional_info=additional_info
    )

    # =====================================================
    # SAVE ASSESSMENT RESULT
    # =====================================================

    db = SessionLocal()

    try:

        assessment_result = AssessmentResult(
            user_id=user_id,
            score=result["score"],
            status=result["status"]
        )

        db.add(assessment_result)
        db.commit()

    finally:

        db.close()

    # =====================================================
    # HEALTH DATA
    # =====================================================

    health_data = {

        "age": age,

        "gender": gender,

        "symptoms": symptoms,

        "sleep": sleep,

        "activity": activity,

        "additional_info": additional_info
    }


    # =====================================================
    # AI HEALTH INSIGHTS
    # =====================================================

    try:

        ai_insights = generate_health_insights(
            health_data
        )

        ai_sections = parse_ai_insights(
            ai_insights
        )

        ai_error = None


    except Exception as e:

        print(
            "AI Service Error:",
            e
        )

        ai_insights = None

        ai_sections = None

        ai_error = (
            "AI insights are temporarily unavailable. "
            "Your health assessment was still processed successfully."
        )


    # =====================================================
    # RESULT PAGE
    # =====================================================

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={

            "request": request,

            "result": result,

            "ai_insights": ai_insights,

            "ai_sections": ai_sections,

            "ai_error": ai_error
        }
    )