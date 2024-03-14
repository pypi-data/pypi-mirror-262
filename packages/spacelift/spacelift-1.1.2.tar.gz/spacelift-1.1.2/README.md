# Spacelift Client
Simple client library for working with the [spacelift.io](https://spacelift.io) API.

## Essential features:
- Read operations for Spaces, Contexts, Stacks, and Blueprints
- Create operations for Spaces, Contexts, and Stacks (from Blueprints)
- Trigger a run for a Stack

## Install
```bash
pip install spacelift
```

## Usage
```python
from spacelift import Spacelift


def main():
    sl = Spacelift(
        base_url="https://ORGNAME.app.spacelift.io/graphql",
        key_id="01HCJMP<API_KEY_ID ~26CHAR LONG>",
        key_secret="e355ae6fd5<API_KEY_SECRET ~64 CHAR LONG>"
    )
    result = sl.get_stacks()
    print(result)

    result = sl.get_stacks(query_fields=["id", "name", "branch", "namespace", "repository", "state"])
    print(result)


if __name__ == "__main__":
    main()
```
```shell
$ python main.py
[{'id': 'demo-stack', 'space': 'legacy'}]
[{'id': 'demo-stack', 'name': 'Demo stack', 'branch': 'showcase', 'namespace': 'spacelift-io', 'repository': 'onboarding', 'state': 'FINISHED'}]
$ 
```
#### Relevant Methods
```python
from spacelift import Spacelift
sl = Spacelift()
sl.get_stacks()
sl.get_stack_by_id(stack_id)
sl.get_spaces()
sl.get_space_by_id(space_id)
sl.get_contexts()
sl.get_context_by_id(context_id)
sl.get_blueprints()
sl.get_blueprint_by_id(blueprint_id)

sl.create_stack_from_blueprint(blueprint_id, inputs=[{'id': 'bp_var1', 'value': 'bp_var1_value'}])

sl.trigger_run(stack_id)
```
### Environment Variables
the `Spacelift` object can also infer its parameters from the following environment variables:

```bash
SPACELIFT_BASE_URL="https://ORGNAME.app.spacelift.io/graphql"
SPACELIFT_KEY_ID="01HCJMP<API_KEY_ID ~26CHAR LONG>"
SPACELIFT_KEY_SECRET="e355ae6fd5<API_KEY_SECRET ~64 CHAR LONG>"
```

### API Keys
Currently, this depends on the API Key workflow [here](https://docs.spacelift.io/integrations/api#spacelift-api-key-token).
The Current Spacelift.io documentation doesn't clearly specify this, but the API Key ID is the 26 character code that 
appears after the name in the web UI.  It does not appear at all in the downloaded `.config` file.  

The required Secret value is the first code (64 characters long) that appears in the downloaded `.config` file.

### Raw GraphQL
The `Spacelift` object also has a `_execute` method that accepts a raw GraphQL query object.  This can be created by 
sending a valid GraphQL query string to `gql.gql()` from the [gql package](https://pypi.org/project/gql/).  This is 
necessary for more advanced queries.

### Mocked Version
There's also a mocked version `MockedSpacelift` that can be used for testing.  It offers mocked versions of all the 
CRUD methods without any real API calls.

## Development

### Publishing
```bash
poetry build
poetry publish
```