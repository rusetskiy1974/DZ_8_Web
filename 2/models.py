from mongoengine import connect, Document, StringField, BooleanField

connect(
    db="HW_8_WEB_2",
    host="mongodb+srv://user19:12345@cluster0.1kaswoc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)


class Contact(Document):
    full_name = StringField(max_length=150, required=True)
    email = StringField(max_length=100, required=True)
    phone = StringField(max_length=50, required=True)
    contact_method = StringField(max_length=10, required=True)
    message_sent = BooleanField(default=False)
    meta = {"collection": "contacts"}
