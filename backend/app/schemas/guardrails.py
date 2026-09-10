from pydantic import BaseModel, Field


class GuardrailIssue(BaseModel):
    issue_type: str = Field(min_length=1)
    message: str = Field(min_length=1)
    severity: str = Field(min_length=1)


class GuardrailResult(BaseModel):
    passed: bool
    issues: list[GuardrailIssue] = Field(default_factory=list)
    revision_required: bool = False
    confidence: float = Field(ge=0.0, le=1.0)