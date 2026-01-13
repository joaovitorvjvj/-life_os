import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

from core.writer import append_event
from adapters.gsheets import load_sheet, save_sheet
from core.exceptions import EventValidationError, SchemaValidationError, DuplicateEventError
from streamlit_gsheets import GSheetsConnection


# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Life OS — Fitness (MVP)", layout="centered")

SPREADSHEET_URL = "SUA_PLANILHA_AQUI"
SHEET_NAME = "fitness_events"

conn = st.connection("gsheets", type=GSheetsConnection)


# ===============================
# HELPERS
# ===============================
def new_event_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def empty_event():
    return {
        "event_id": None,
        "event_type": None,
        "event_date": None,
        "created_at": None,
        "is_deleted": False,
        "notes": None,
        "workout_id": None,
        "exercise": None,
        "sets": None,
        "reps": None,
        "weight": None,
        "duration_min": None,
        "body_weight": None,
    }


# ===============================
# UI
# ===============================
st.title("🏋️ Fitness — Registro de Evento")
st.caption("UI mínima • append-only • sem métricas")

event_type = st.selectbox(
    "Tipo de Evento",
    [
        "workout_session",
        "exercise_log",
        "body_measurement"
    ]
)

event_date = st.date_input("Data do evento", value=datetime.today())
notes = st.text_area("Notas (opcional)")

st.divider()

event = empty_event()
event["event_id"] = new_event_id("fit")
event["event_type"] = event_type
event["event_date"] = event_date.isoformat()
event["created_at"] = datetime.utcnow().isoformat()
event["notes"] = notes


# ===============================
# EVENT-SPECIFIC FIELDS
# ===============================
if event_type == "workout_session":
    event["duration_min"] = st.number_input("Duração (min)", min_value=1)

if event_type == "exercise_log":
    event["exercise"] = st.text_input("Exercício")
    event["sets"] = st.number_input("Séries", min_value=1)
    event["reps"] = st.number_input("Repetições", min_value=1)
    event["weight"] = st.number_input("Carga (kg)", min_value=0.0)

if event_type == "body_measurement":
    event["body_weight"] = st.number_input("Peso corporal (kg)", min_value=1.0)


# ===============================
# SUBMIT
# ===============================
if st.button("Registrar evento"):
    try:
        df = load_sheet(conn, SPREADSHEET_URL, SHEET_NAME)
        df_new = append_event(df, event, SHEET_NAME)
        save_sheet(conn, SPREADSHEET_URL, SHEET_NAME, df_new)

        st.success("Evento registrado com sucesso.")
        st.code(event, language="json")

    except (EventValidationError, SchemaValidationError, DuplicateEventError) as e:
        st.error(str(e))

    except Exception as e:
        st.error(f"Erro inesperado: {e}")
