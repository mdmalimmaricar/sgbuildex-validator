from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import jsonschema

app = FastAPI()

# schema...
manpower_utilization_schema = {...}

@app.post("/validate/{schema_name}")
async def validate_payload(schema_name: str, request: Request):
    try:
        payload = await request.json()
        if schema_name == "manpower_utilization":
            jsonschema.validate(instance=payload, schema=manpower_utilization_schema)
            return {"valid": True, "message": "Payload is valid."}
        else:
            return JSONResponse(status_code=400, content={"error": f"Unknown schema: {schema_name}"})
    except jsonschema.exceptions.ValidationError as ve:
        return JSONResponse(status_code=422, content={"valid": False, "error": str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Internal server error: {str(e)}"})
