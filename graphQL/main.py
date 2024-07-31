from flask import Flask
from flask import request, jsonify
import graphene

app = Flask(__name__)

# Types


class Item(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()


# Data store and resolvers
items = []


class Query(graphene.ObjectType):
    all_items = graphene.List(Item)

    def resolve_all_items(self, info):
        return items

# Mutation: CRUD


class CreateItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    item = graphene.Field(lambda: Item)

    def mutate(self, info, name, description):
        item = Item(id=len(items) + 1, name=name, description=description)
        items.append(item)
        return CreateItem(item=item)


class UpdateItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        description = graphene.String()

    item = graphene.Field(lambda: Item)

    def mutate(self, info, id, name=None, description=None):
        item = next((item for item in items if item.id == id), None)
        if item is None:
            raise Exception('Item not found')

        if name:
            item.name = name
        if description:
            item.description = description

        return UpdateItem(item=item)


class DeleteItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        global items
        items = [item for item in items if item.id != id]
        return DeleteItem(ok=True)


class Mutation(graphene.ObjectType):
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()


# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    result = schema.execute(data.get('query'))
    return jsonify(result.data)


if __name__ == '__main__':
    app.run(debug=True)
