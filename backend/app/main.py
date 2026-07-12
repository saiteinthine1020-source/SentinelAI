from fastapi import FastAPI  # type: ignore[import]

app = FastAPI(
    title="SentinelAI API",
    description="Backend API for the SentinelAI security and observability platform.",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return the basic backend process health status."""
    return {
        "status": "",
        "service": "sentinelai-backend",
    }