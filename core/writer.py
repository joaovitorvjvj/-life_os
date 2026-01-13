from core.validator import (
    validate_sheet_schema,
    validate_event_schema,
    validate_common_fields,
    validate_semantics,
    ensure_event_id_unique
)


def append_event(df, event: dict, sheet_name: str):
    validate_sheet_schema(df, sheet_name)
    validate_event_schema(event, sheet_name)
    validate_common_fields(event)
    validate_semantics(event, sheet_name)
    ensure_event_id_unique(event["event_id"], df)

    return df._append(event, ignore_index=True)
