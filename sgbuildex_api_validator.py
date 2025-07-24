
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import jsonschema

# Sample schema for manpower_utilization
manpower_utilization_schema = {
    "type": "object",
    "properties": {
        "submission_entity": {"type": "integer"},
        "submission_month": {"type": "string"},
        "person_id_no": {"type": "string"},
        "person_id_and_work_pass_type": {"type": "string"},
        "person_trade": {"type": "string"},
        "person_attendance_date": {"type": "string"},
        "person_attendance_details": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "time_in": {"type": "string"},
                    "time_out": {"type": "string"}
                },
                "required": ["time_in", "time_out"]
            }
        }
    },
    "required": ["submission_entity", "submission_month", "person_id_no", 
                 "person_id_and_work_pass_type", "person_trade", 
                 "person_attendance_date", "person_attendance_details"]
}

app = FastAPI()

@app.post("/validate/{schema_name}")
async def validate_payload(schema_name: str, request: Request):
    try:
        payload = await request.json()
        if schema_name == "manpower_utilization":
            jsonschema.validate(instance=payload, schema=manpower_utilization_schema)
            return {"valid": True, "message": "Payload is valid."}
        else:
            return JSONResponse(status_code=400, content={"error": f"Unknown schema: {schema_name}"})
    except jsonschema.exceptions.ValidationError as e:
        return JSONResponse(status_code=422, content={"valid": False, "error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Internal server error: {str(e)}"})
