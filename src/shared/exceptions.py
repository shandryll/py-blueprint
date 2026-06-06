class ApplicationServiceError(Exception):
    def __init__(
        self,
        service_name: str,
        message: str,
        error_code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        self.service_name = service_name
        self.message = message
        self.error_code = error_code or "APPLICATION_ERROR"
        self.status_code = status_code or 500
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"[{self.service_name} Service] - {self.message}"

    def to_dict(self) -> dict[str, str | int]:
        return {
            "service": self.service_name,
            "message": self.message,
            "error_code": self.error_code,
            "status_code": self.status_code,
            "error": "Application Service Error",
        }
