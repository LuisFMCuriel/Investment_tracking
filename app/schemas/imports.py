from pydantic import BaseModel

class ImportError(BaseModel):
    row: int
    error: str

class ImportTransactionsResponse(BaseModel):
    created: int
    errors: list[ImportError]