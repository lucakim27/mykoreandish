from typing import Dict, Any
from backend.config.db import get_db

class NoteManager:
    def __init__(self, firestore_module: Any):
        self.db = get_db()
        self.notes_ref = self.db.collection('Notes')
        self.firestore = firestore_module
    
    def add_note(self, name, user_id, note_content):
        self.notes_ref.add({
            'name': name,
            'user_id': user_id,
            'content': note_content
        })
    
    def update_note(self, name, user_id, note_content):
        existing_note = self.get_note(name, user_id)

        if existing_note:
            query = (
                self.notes_ref
                .where('name', '==', name)
                .where('user_id', '==', user_id)
                .limit(1)
            )

            for doc in query.stream():
                doc.reference.update({'content': note_content})
                return

    def get_note(self, name, user_id) -> Dict[str, Any]:
        query = self.notes_ref.where('name', '==', name).where('user_id', '==', user_id).limit(1)
        results = query.stream()
        for doc in results:
            return doc.to_dict()
        return {}
    
    def delete_note(self, name, user_id):
        query = (
            self.notes_ref
            .where('name', '==', name)
            .where('user_id', '==', user_id)
            .limit(1)
        )

        for doc in query.stream():
            doc.reference.delete()