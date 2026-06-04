def detect_patterns(history):

    if len(history) < 2:

        return {
            "trend": "Insufficient history"
        }

    return {
        "trend": "Recurring symptoms detected"
    }