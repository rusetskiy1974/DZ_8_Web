import os
import sys
import datetime

import pika
from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='sms')


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Send sms message  to {contact.phone} on {datetime.datetime.now()}")
        contact.message_sent = True
        contact.save()


def consume_messages():
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sms', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def main_consumer_sms():
    try:
        consume_messages()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    main_consumer_sms()
