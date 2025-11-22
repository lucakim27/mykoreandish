from typing import Dict, Any
from flask import flash
from project.config.db import get_db

class NoteManager:
    def __init__(self, firestore_module: Any):
        self.db = get_db()
        self.notes_ref = self.db.collection('Notes')
        self.firestore = firestore_module
    
    def add_note(self, name, user_id, note_content) -> Dict[str, Any]:
        existing_note = self.get_note_by_dish_and_user(name, user_id)
        if existing_note:
            query = self.notes_ref.where('name', '==', name).where('user_id', '==', user_id).limit(1)
            results = query.stream()
            for doc in results:
                if note_content == '':
                    doc.reference.delete()
                    flash('Note deleted successfully!', 'success')
                    return None
                else:
                    doc.reference.update({'content': note_content})
                    flash('Note updated successfully!', 'success')
                    return {'name': name, 'user_id': user_id, 'content': note_content}
        else:
            if note_content == '':
                return None
            note_data = {
                'name': name,
                'user_id': user_id,
                'content': note_content
            }
            self.notes_ref.add(note_data)
            flash('Note added successfully!', 'success')
            return note_data

    def get_note_by_dish_and_user(self, name, user_id) -> Dict[str, Any]:
        query = self.notes_ref.where('name', '==', name).where('user_id', '==', user_id).limit(1)
        results = query.stream()
        for doc in results:
            return doc.to_dict()
        return None