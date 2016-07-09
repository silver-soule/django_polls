
from __future__ import absolute_import
from mysite.celery import app
import time,requests


@app.task
def sendmail(email_id):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd36b23cdec494baeb2ae92a4d6654902.mailgun.org/messages",
        auth=("api", "key-aeaeaabd8ae4f6456e1719a4aa4d4632"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd36b23cdec494baeb2ae92a4d6654902.mailgun.org>",
              "to": "Neelaksh Chauhan <"+email_id+">",
              "subject": "Hello",
              "text": "Seems like our moderators are sleeping!",
              "html": "<html><b>They will get back yo you soon!!</b></html>"})
