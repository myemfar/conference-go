import json
import pika
import django
import os
import sys
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
    print(" Received %r" % body)
    content = json.loads(body)
    email = content["presenter_email"]
    name = content["presenter_name"]
    title = content["title"]
    send_mail(
        'Your presentation has been accepted',
        f"{name}, we're happy to tell you that your presentation {title} has been accepted",
        'admin@conference.go',
        [email],
        fail_silently=False,
        )

parameters = pika.ConnectionParameters(host='rabbitmq')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='presentation_approvals')
channel.basic_consume(
    queue='presentation_approvals',
    on_message_callback=process_approval,
    auto_ack=True,
)
channel.start_consuming()


# def process_rejections(ch, method, properties, body):
#     print(" Received %r" % body)
#     send_mail(
#         'Your presentation has been rejected',
#         f"{body['presenter_name']}, Unfortunately your presentation {body['title']} has been rejected.",
#         'admin@conference.go',
#         [body['presenter_email']],
#         fail_silently=False,
#     )
