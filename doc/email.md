# Email

To send an email using Appier just do the following:

```python
self.email(
    "template.html.tpl",
    subject = "Test email",   
    sender = "sender@email.com",
    receivers = ["receiver@email.com"]
)
```

The previous example uses the [Configuration](doc/configuration.md) to figure
out which SMTP server should be used and how. The following configuration
variables must be set:

* `SMTP_HOST` (`str`) - The host where the SMTP server is running.
* `SMTP_PORT` (`int`) - The port where the SMTP server is listening (default: 25).
* `SMTP_USER` (`str`) - The username used to authenticate with the SMTP server.
* `SMTP_PASSWORD` (`str`) - The password used to authenticate with the SMTP server.
* `SMTP_STARTTLS` (`bool`) - Flag used to tell the server that the client supports Transport Layer Security (default: True).

These configurations can also be provided directly to the ``email`` method
(they will override any configuration set at the app level):

```python
self.email(
    "template.html.tpl",
    subject = "Test email",   
    sender = "sender@email.com",
    receivers = ["receiver@email.com"],
    host = "hostname.com",
    port = 25,
    username = "username",
    password = "password"
    stls = True
)
```

## Templates

Emails are sent out as a MIME multipart message, with a rich version and plain text version.
The mandatory template argument is used to create the rich version, and by default, the
result of that template being processed will be stripped out of its HTML tags automatically
to create the plain text version. In order to specify a specific template for the plain text
version, just send ``plain_template`` keyword argument with the template file name.

The email is encoded in UTF-8 by default. If you want to use another encoding, just send
the ``encoding`` keyword argument with the encoding you desire.