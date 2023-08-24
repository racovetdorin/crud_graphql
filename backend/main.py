import re
import graphene
from bson import ObjectId
from starlette_graphene3 import GraphQLApp
from datetime import datetime
from fastapi import FastAPI
from .database import db
from .models import PersonModel, IdValidator, UpdatePersonModel


app = FastAPI()

collection = db.get_collection('personCollection')


class Dates(graphene.ObjectType):
    lastlogin = graphene.String(description='Last login date')
    register = graphene.String(description='Registration date')


class Person(graphene.ObjectType):
    id = graphene.String(description='Person ID')
    name = graphene.String(description='Person name')
    surname = graphene.String(description='Person surname')
    dates = graphene.Field(Dates, description='Person dates')

    async def resolve_dates(root, info):

        person_id = root.id
        person = await collection.find_one({'_id': ObjectId(person_id)})
        if person and 'dates' in person:
            return Dates(
                lastlogin=person['dates']['lastlogin'].strftime('%Y-%m-%d'),
                register=person['dates']['register'].strftime('%Y-%m-%d')
            )
        else:
            return None


class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        surname = graphene.String()
    person = graphene.Field(Person)

    async def mutate(self, info, name, surname):
        try:
            # perform validation first
            validated_data = PersonModel(name=name, surname=surname)
            # Create a new person with validated data
            new_person = {
                'name': validated_data.name,
                'surname': validated_data.surname,
                'dates': {
                    'lastlogin': datetime.now(),
                    'register': datetime.now()
                }
            }

            result = await collection.insert_one(new_person)
            created_person = await collection.find_one({'_id': result.inserted_id})
            person = Person(
                id = str(created_person['_id']),
                name = created_person['name'],
                surname = created_person['surname'],
                dates = Dates(
                    lastlogin=created_person['dates']['lastlogin'],
                    register=created_person['dates']['register']
                )
            )
            return CreatePerson(person=person)
        except Exception as e:
            raise ValueError(f'Error occurred while creating a person: {e}')


class UpdatePerson(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        surname = graphene.String()

    person = graphene.Field(Person)

    async def mutate(self, info, id, name=None, surname=None):

        validated_data = UpdatePersonModel(name=name, surname=surname, id=id)

        update_fields = {'name': validated_data.name} if name else {}
        update_fields.update({'surname': validated_data.surname} if surname else {})
        update_fields['dates.lastlogin'] = datetime.now()

        result = await collection.update_one({'_id': ObjectId(id)}, {'$set': update_fields})
        if result.modified_count > 0:
            updated_person = await collection.find_one({'_id': ObjectId(id)})
            person = Person(
                id = str(updated_person['_id']),
                name = updated_person['name'],
                surname = updated_person['surname'],
            )
            return UpdatePerson(person=person)
        return None


class DeletePerson(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    success = graphene.Boolean()

    async def mutate(self, info, id):

        validated_data = IdValidator(id=id)

        result = await collection.delete_one({'_id': ObjectId(validated_data.id)})

        if result.deleted_count > 0:
            return DeletePerson(success=True)

        return DeletePerson(success=False)


class PersonMutation(graphene.ObjectType):
    create_person = CreatePerson.Field()


class Query(graphene.ObjectType):
    get_person = graphene.Field(Person, id=graphene.String(description='Person ID'))
    get_all_persons = graphene.List(
        Person, 
        name=graphene.String(),
        surname=graphene.String(), 
        page=graphene.Int(), 
        limit=graphene.Int()
    )

    async def resolve_get_person(self, info, id):

        person = await collection.find_one({'_id': ObjectId(id)})
        if person:
            return Person(
                id = str(person['_id']),
                name = person['name'],
                surname = person['surname'],
                dates = Dates(
                    person['dates']['lastlogin'],
                    person['dates']['register']
                )

            )
        else:
            return None

    async def resolve_get_all_persons(self, info, name=None, surname=None, page=None, limit=None):

        query = {
            field: re.compile(f'^{re.escape(value)}', re.IGNORECASE)
            for field, value in [('name', name), ('surname', surname)]
            if value
        }

        skip = (page - 1) * limit if page and limit else 0
        
        persons = collection.find(query).skip(skip).limit(limit)

        result = [Person(
            id=str(person['_id']),
            name=person['name'],
            surname=person['surname']
        ) async for person in persons]

        return result


class PersonMutation(graphene.ObjectType):
    create_person = CreatePerson.Field()
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()


schema = graphene.Schema(query=Query, mutation=PersonMutation)
app.add_route('/graphql', GraphQLApp(schema=schema))
