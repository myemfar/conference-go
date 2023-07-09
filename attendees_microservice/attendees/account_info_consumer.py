from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()
from attendees.models import AccountVO


def update_account(ch, method, properties, body):
    content = json.loads(body)
    first_name = content["first_name"]
    last_name = content["last_name"]
    email = content["email"]
    is_active = content["is_active"]
    updated_string = content["updated"]
    updated = datetime.fromisoformat(updated_string)
#   updated = convert updated_string from ISO string to datetime
    if is_active:
        AccountVO.objects.update_or_create(
            first_name,
            last_name,
            email,
            updated_string,
            updated,
        )
    else:
        AccountVO.objects.delete()
#       Use the update_or_create method of the AccountVO.objects QuerySet
#           to update or create the AccountVO object
#   otherwise:
#       Delete the AccountVO object with the specified email, if it exists


# Based on the reference code at
#   https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py
while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.exchange_declare(exchange='account_info', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='account_info', queue=queue_name)
        def callback(ch, method, properties, body):
            print(" [x] %r" % body.decode())

        print(' [*] Waiting for logs. To exit press CTRL+C')
        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
#       do a basic_consume for the queue name that calls
#           function above
#       tell the channel to start consuming
    except AMQPConnectionError:
        print('cannot connect to RabbitMQ')
        time.sleep(2)
#       print that it could not connect to RabbitMQ
#       have it sleep for a couple of seconds
