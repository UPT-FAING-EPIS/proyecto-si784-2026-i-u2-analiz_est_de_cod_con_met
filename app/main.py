from fastapi import FastAPI

app = FastAPI(title="Analizador Estático de Código")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Analizador Estático de Código"}
