from enum import Enum


class SourceType(str, Enum):
    TEXT = "text"
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    URL = "url"
    AUDIO = "audio"
    VIDEO = "video"


class OutputType(str, Enum):
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    ADVISORY = "advisory"
    INFOGRAPHIC = "infographic"
    EXECUTIVE_SUMMARY = "executive_summary"
    PRESENTATION = "presentation"
    VIDEO = "video"


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OutputStatus(str, Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"