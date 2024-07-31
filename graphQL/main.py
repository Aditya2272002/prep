from flask import Flask, request, jsonify
import graphene
from graphene import ObjectType, Schema, Field, Int, String, List, Mutation, Boolean

app = Flask(__name__)

# Define the Item type


class Item(ObjectType):
    id = Int()
    name = String()
    description = String()


# In-memory data store
items = []

# Define the Query type


class Query(ObjectType):
    all_items = List(Item)
    item_by_id = Field(Item, id=Int(required=True))

    def resolve_all_items(self, info):
        return items

    def resolve_item_by_id(self, info, id):
        return next((item for item in items if item.id == id), None)

# Define the Mutation type


class CreateItem(Mutation):
    class Arguments:
        name = String(required=True)
        description = String(required=True)

    item = Field(lambda: Item)

    def mutate(self, info, name, description):
        item = Item(id=len(items) + 1, name=name, description=description)
        items.append(item)
        return CreateItem(item=item)


class UpdateItem(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        description = String()

    item = Field(lambda: Item)

    def mutate(self, info, id, name=None, description=None):
        item = next((item for item in items if item.id == id), None)
        if item is None:
            raise Exception('Item not found')

        if name:
            item.name = name
        if description:
            item.description = description

        return UpdateItem(item=item)


class DeleteItem(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = Boolean()

    def mutate(self, info, id):
        global items
        items = [item for item in items if item.id != id]
        return DeleteItem(ok=True)


class Mutation(ObjectType):
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()


# Define the schema
schema = Schema(query=Query, mutation=Mutation)


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    query = data.get('query')
    result = schema.execute(query)
    return jsonify(result.data)


if __name__ == '__main__':
    app.run(debug=True)
