from api.services.google_firestore_service import db
from api.services.google_firestore_service.models.Error import Error


def create_error(error_data):

    error = Error(**error_data)

    db.collection("errors").add(error.dict())
