"""Connector for mail."""
import logging
import re

import redmail

import multi_notifier.connectors.exceptions
import multi_notifier.connectors.interface

MODULE_LOGGER = logging.getLogger(__name__)


class Mail(multi_notifier.connectors.interface.Interface):
	"""Class to send e-mails."""

	__html_pattern = re.compile(r"<[^<]+?>")

	def __init__(self, user: str, password: str, smtp_host: str, smtp_port: int):
		"""Init Mail class.

		:param user: username to log in to mail account
		:param password: password to log in to mail account
		:param smtp_host: smtp host name (e.g. smtp.ionos.de)
		:param smtp_port: smtp port
		:raises multi_notifier.connectors.exceptions.ConnectorConfigurationException: If mail configuration is faulty
		"""
		self.mail_sender = redmail.EmailSender(smtp_host, smtp_port, user, password)

	def send_message(self, recipient: str | list[str], message: str, subject: str | None = None, images: dict[str, str] | None = None) -> None:
		"""Send a message to one or multiple recipients

		:param recipient: one or multiple recipients. (Must be mail addresses!)
		:param message: Message which should be sent
		:param subject: Subject of the mail
		:param images: Images which will be added to the mail
		:raises multi_notifier.connectors.exceptions.ConnectorException: if mail could not be sent
		"""
		if images is None:
			images = {}

		# check if content of message is HTML and set text / HTML
		is_html = bool(self.__html_pattern.search(message))
		text = message if not is_html else None
		html = message if is_html else None

		try:
			self.mail_sender.send(
				subject=subject,
				receivers=recipient,
				text=text,
				html=html,
				body_images=images
			)
		except Exception as exc:
			MODULE_LOGGER.exception(msg := f"Could not send mail | Reason: {exc}")
			raise multi_notifier.connectors.exceptions.ConnectorException(msg)
