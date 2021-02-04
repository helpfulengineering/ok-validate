Validators
----------
Here are some custom validators to extend `yamale` functionality.

### Key - `key(key_name)`
Validates that a given dictionary (map) has a given key.
- arguments: single name of a key, surrounded by quotes.

Examples:
- `key('documentation-home')`

```yaml
hello: key('world')
```

#### Valid Data:
```yaml
hello:
    foo: bar
    world: true
```

### License - `license()`
Validates that a given license is a valid SPDX identifier as defined at https://spdx.org/licenses/.

Examples:
- `license()`

```yaml
license:
    software: license()
```

#### Valid Data:
```yaml
license:
    software: Apache-2.0
```