class ApplicationServiceError(Exception):
    """Exceção base para erros de serviços da aplicação."""

    def __init__(self, service_name: str, message: str) -> None:
        """Inicializa a exceção de serviço da aplicação.

        Args:
            service_name: Nome do serviço que falhou.
            message: Mensagem de erro da exceção.
        """
        self.service_name = service_name
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Retorna a representação da exceção incluindo o nome do serviço."""
        return f"[{self.service_name} Service] - {self.message}"
