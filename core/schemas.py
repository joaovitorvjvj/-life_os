COMMON_COLUMNS = [
    "event_id",
    "event_type",
    "event_date",
    "created_at",
    "is_deleted",
    "notes"
]


SCHEMAS = {
    "fitness_events": COMMON_COLUMNS + [
        "workout_id",
        "exercise",
        "sets",
        "reps",
        "weight",
        "duration_min",
        "body_weight"
    ],

    "study_events": COMMON_COLUMNS + [
        "study_session_id",
        "subject",
        "duration_min",
        "difficulty_self",
        "focus_self"
    ],

    "task_events": COMMON_COLUMNS + [
        "task_id",
        "title",
        "priority"
    ],

    "finance_events": COMMON_COLUMNS + [
        "transaction_id",
        "amount",
        "quantity",
        "price"
    ],

    "okr_events": COMMON_COLUMNS + [
        "okr_id",
        "kr_id",
        "target_value",
        "current_value"
    ]
}
