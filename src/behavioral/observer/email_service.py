from observer_interface import Observer
from typing import List


class EmailService:
    """
    Serviço de envio de emails (simulado).

    Esta classe simula o envio de emails para os observadores.
    Em um sistema real, aqui seria integrado um serviço de email
    como SendGrid, AWS SES, etc.
    """

    @staticmethod
    def enviar_email(observer: Observer, mensagem: str) -> dict:
        """
        Simula o envio de um email para um observador.

        Args:
            observer: O observador que receberá o email
            mensagem: Conteúdo do email

        Returns:
            Dict com informações do email enviado
        """
        email_info = {
            "destinatario_nome": observer.get_nome(),
            "destinatario_email": observer.get_email(),
            "mensagem": mensagem,
            "status": "enviado"
        }

        # Simula o log do envio
        print(f"{'-' * 80}")
        print(f"Email enviado para {observer.get_nome()} - {observer.get_email()}")
        print(f"Mensagem: {mensagem}")
        print()

        return email_info

    @staticmethod
    def enviar_emails_em_lote(observers: List[Observer], mensagem: str) -> List[dict]:
        """
        Envia emails para múltiplos observadores.

        Args:
            observers: Lista de observadores
            mensagem: Mensagem a ser enviada

        Returns:
            Lista de dicts com informações dos emails enviados
        """
        resultados = []
        for observer in observers:
            resultado = EmailService.enviar_email(observer, mensagem)
            resultados.append(resultado)

        return resultados
