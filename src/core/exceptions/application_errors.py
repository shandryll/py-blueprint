HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_502_BAD_GATEWAY = 502
HTTP_503_SERVICE_UNAVAILABLE = 503


class ApplicationServiceError(Exception):
    """Exceção base para erros de serviços da aplicação.

    Esta exceção é usada para padronizar o tratamento de erros em toda a aplicação,
    permitindo que serviços lancem erros com informações estruturadas que podem
    ser facilmente convertidas para respostas HTTP ou logs.
    """

    def __init__(
        self,
        service_name: str,
        message: str,
        error_code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        """Inicializa a exceção.

        Args:
            service_name: Nome do serviço que falhou.
            message: Mensagem de erro da exceção.
            error_code: Código de erro para tratamento programático.
                        Se não fornecido, usa "APPLICATION_ERROR" como padrão.
            status_code: Código HTTP (opcional, para uso em APIs).
                         Se não fornecido, usa 500 como padrão.
        """
        self.service_name = service_name
        self.message = message
        self.error_code = error_code or "APPLICATION_ERROR"
        self.status_code = status_code or 500
        super().__init__(self.message)

    def __str__(self) -> str:
        """Retorna representação em string da exceção.

        Returns:
            str: String formatada com nome do serviço e mensagem de erro.
        """
        return f"[{self.service_name} Service] - {self.message}"

    def to_dict(self) -> dict[str, str | int]:
        """Retorna a exceção como dicionário.

        Útil para APIs HTTP que precisam retornar erros em formato JSON.

        Returns:
            dict: Dicionário com os campos da exceção formatados para resposta HTTP.
        """
        return {
            "service": self.service_name,
            "message": self.message,
            "error_code": self.error_code,
            "status_code": self.status_code,
            "error": "Application Service Error",
        }
