from core.schemas import SCHEMAS
from core.exceptions import SchemaValidationError, EventValidationError, DuplicateEventError


def validate_sheet_schema(df, sheet_name: str):
    expected = SCHEMAS[sheet_name]
    actual = list(df.columns)

    if actual != expected:
        raise SchemaValidationError(
            f"Schema inválido em '{sheet_name}'.\n"
            f"Esperado: {expected}\n"
            f"Encontrado: {actual}"
        )


def validate_event_schema(event: dict, sheet_name: str):
    expected_cols = SCHEMAS[sheet_name]

    for col in expected_cols:
        if col not in event:
            raise EventValidationError(f"Campo obrigatório ausente: {col}")

    extra = set(event.keys()) - set(expected_cols)
    if extra:
        raise EventValidationError(f"Campos não permitidos: {extra}")


def validate_common_fields(event: dict):
    if not isinstance(event["event_id"], str) or not event["event_id"]:
        raise EventValidationError("event_id inválido")

    if not isinstance(event["event_type"], str):
        raise EventValidationError("event_type inválido")

    if not isinstance(event["is_deleted"], bool):
        raise EventValidationError("is_deleted deve ser boolean")


def validate_semantics(event: dict, sheet_name: str):
    et = event["event_type"]

    if sheet_name == "fitness_events":
        if et == "workout_session" and event["duration_min"] is None:
            raise EventValidationError("Workout exige duration_min")

        if et == "exercise_log":
            for f in ["exercise", "sets", "reps"]:
                if event[f] is None:
                    raise EventValidationError(f"{f} obrigatório em exercise_log")

    if sheet_name == "study_events":
        if et == "study_session":
            if event["duration_min"] is None or event["subject"] is None:
                raise EventValidationError("Sessão de estudo incompleta")

    if sheet_name == "task_events":
        if et == "task_created" and not event["title"]:
            raise EventValidationError("Task precisa de título")

    if sheet_name == "finance_events":
        amount = event["amount"]
        if amount == 0:
            raise EventValidationError("amount não pode ser zero")

        if et == "income" and amount < 0:
            raise EventValidationError("income deve ser positivo")

        if et == "expense" and amount > 0:
            raise EventValidationError("expense deve ser negativo")


def ensure_event_id_unique(event_id: str, df):
    if event_id in df["event_id"].values:
        raise DuplicateEventError(f"event_id duplicado: {event_id}")
