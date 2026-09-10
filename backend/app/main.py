from fastapi import FastAPI

app = FastAPI(
    title="PRISM API",
    description="Provenance-Reasoned Intelligent Synthesis for Multi-channel Content",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "prism-api",
    }