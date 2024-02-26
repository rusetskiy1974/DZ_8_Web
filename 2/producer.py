import random
import time

from faker import Faker
from models import Contact

import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='HW8 exchange', exchange_type='direct')
channel.queue_declare(queue='sms', durable=False)
channel.queue_declare(queue='email', durable=False)


def create_fake_contacts(num_contacts):
    fake = Faker()
    contacts_ = []
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        contact_method = random.choice(['sms', 'email'])
        contact = Contact(full_name=full_name, email=email, phone=phone, contact_method=contact_method)
        contact.save()
        contacts_.append(contact)
    return contacts_


def send_message_to_queue(queue_name, contact_id):
    # channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange='HW8 exchange', queue=queue_name)
    channel.basic_publish(exchange='HW8 exchange', routing_key=queue_name, body=str(contact_id))
    time.sleep(0.1)


def main_producer():
    num_contacts = 400
    contacts = create_fake_contacts(num_contacts)
    for cont in contacts:
        queue = cont.contact_method
        send_message_to_queue(queue, cont.id)
    connection.close()


if __name__ == '__main__':
    main_producer()
