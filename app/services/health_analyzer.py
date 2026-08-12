def analyze_health_data(
    age,
    gender,
    symptoms,
    sleep,
    activity,
    additional_info
):
    """
    Analyze the submitted health information.

    This is currently a basic rule-based engine.
    Later, an AI model will be connected here.
    """

    observations = []
    recommendations = []

    # -------------------------
    # Sleep analysis
    # -------------------------

    if sleep == "less_than_5":

        observations.append(
            "Your reported sleep duration is relatively low."
        )

        recommendations.append(
            "Try to maintain a consistent and adequate sleep schedule."
        )

    elif sleep == "5_to_7":

        observations.append(
            "Your reported sleep duration is moderate."
        )

        recommendations.append(
            "Maintaining a consistent sleep routine may support better wellbeing."
        )

    elif sleep == "7_to_9":

        observations.append(
            "Your reported sleep duration is within a commonly recommended range."
        )

    elif sleep == "more_than_9":

        observations.append(
            "You reported a relatively long sleep duration."
        )


    # -------------------------
    # Activity analysis
    # -------------------------

    if activity == "low":

        observations.append(
            "Your reported physical activity level is low."
        )

        recommendations.append(
            "Consider incorporating suitable regular physical activity into your routine."
        )

    elif activity == "moderate":

        observations.append(
            "You reported a moderate level of physical activity."
        )

    elif activity == "high":

        observations.append(
            "You reported a high level of physical activity."
        )


    # -------------------------
    # Symptom analysis
    # -------------------------

    if symptoms:

        observations.append(
            f"You reported {len(symptoms)} symptom(s)."
        )

    else:

        observations.append(
            "No symptoms were selected in the assessment."
        )

# -------------------------
    # Health Score
    # -------------------------

    score = 100

    # Sleep
    if sleep == "less_than_5":
        score -= 10

    elif sleep == "5_to_7":
        score -= 5

    elif sleep == "more_than_9":
        score -= 5


    # Physical activity
    if activity == "low":
        score -= 10

    elif activity == "moderate":
        score -= 3


    # Symptoms
    score -= len(symptoms) * 8


    # Keep score between 0 and 100
    score = max(0, min(100, score))
    # -------------------------
    # Overall status
    # -------------------------

    if len(symptoms) >= 3:

        status = "Needs Attention"

    elif len(symptoms) > 0:

        status = "Monitor"

    else:

        status = "General Wellness"


    # -------------------------
    # Final result
    # -------------------------

    return {
    "status": status,
    "score": score,
    "observations": observations,
    "recommendations": recommendations,
    "symptoms": symptoms
}
    