import ssl
from django.core.mail.backends.smtp import EmailBackend


class SSLEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        self.connection = self.connection_class(
            self.host, self.port, timeout=self.timeout
        )
        self.connection.ehlo()
        if self.use_tls:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            self.connection.starttls(context=ctx)
            self.connection.ehlo()
        if self.username and self.password:
            self.connection.login(self.username, self.password)
        return True