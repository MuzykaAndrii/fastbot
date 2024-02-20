import shelve

from sqlalchemy import select

from app.backend.users.models import User
from app.backend.db.session import async_session_maker
from app.backend.vocabulary.models import LanguagePair, VocabularySet

async def save_user_data_to_shelve():
    async with async_session_maker() as session:
        stmt = select(User)
        instances = await session.execute(stmt)
        users = instances.scalars().all()

        # Write user data to shelve file
        with shelve.open('backups/user_data') as db:
            for user in users:
                db[str(user.id)] = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'password_hash': user.password_hash,
                    'is_superuser': user.is_superuser
                }

async def save_vocabulary_set_data_to_shelve():
    async with async_session_maker() as session:
        stmt = select(VocabularySet)
        instances = await session.scalars(stmt)
        vocabulary_sets = instances.unique().all()

        # Write vocabulary set data to shelve file
        with shelve.open('backups/vocabulary_set_data') as db:
            for vocabulary_set in vocabulary_sets:
                db[str(vocabulary_set.id)] = {
                    'id': vocabulary_set.id,
                    'owner_id': vocabulary_set.owner_id,
                    'name': vocabulary_set.name,
                    'created_at': vocabulary_set.created_at,
                    'is_active': vocabulary_set.is_active
                }

async def save_language_pair_data_to_shelve():
    async with async_session_maker() as session:
        stmt = select(LanguagePair)
        instances = await session.scalars(stmt)
        language_pairs = instances.unique().all()

        # Write language pair data to shelve file
        with shelve.open('backups/language_pair_data') as db:
            for language_pair in language_pairs:
                db[str(language_pair.id)] = {
                    'id': language_pair.id,
                    'vocabulary_id': language_pair.vocabulary_id,
                    'word': language_pair.word,
                    'translation': language_pair.translation
                }


async def save_db_data_to_shelve():
    await save_user_data_to_shelve()
    await save_vocabulary_set_data_to_shelve()
    await save_language_pair_data_to_shelve()


async def save_data_from_shelve_to_db():
    async with async_session_maker() as session:
        # Save users data from shelve
        with shelve.open('backups/user_data') as db:
            for key in db:
                user_data = db[key]
                user = User(**user_data)
                session.add(user)

        # Save vocabulary sets data from shelve
        with shelve.open('backups/vocabulary_set_data') as db:
            for key in db:
                vocabulary_set_data = db[key]
                vocabulary_set = VocabularySet(**vocabulary_set_data)
                session.add(vocabulary_set)

        # Save language pairs data from shelve
        with shelve.open('backups/language_pair_data') as db:
            for key in db:
                language_pair_data = db[key]
                language_pair = LanguagePair(**language_pair_data)
                session.add(language_pair)

        # Commit the changes to the database
        await session.commit()
