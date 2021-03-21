# ok-validate

Validation of Open Know How specification and related schemas (https://openknowhow.org)
## GitHub Action

This action uses an Open Knowledge Framework schema to validate your manifest such as for [`OKH`](https://openknowhow.org/)

### Inputs

#### `cpu-num`

*Optional* How many cores to use. Default `"4"`.

#### `ok`

*Optional* Which Open Knowledge Framework schema to use for validation. Default [`"okh"`](./okv/schemas/okh.yaml).

#### `parser`

*Optional*  YAML library to load file. Default `"pyyaml"` (can be one of `"pyyaml"` or `"ruamel"`).

#### `path`

*Required* The path to your manifest or manifests relative to your workspace. Default `"./"`.

#### `schema`

*Optional* The full path to an Open Knowledge Framework schema or custom schema to use for validation. Default `""`.

#### `strict`

*Optional* Whether to run in strict mode. Default `"false"` (can be one of `"true"` or `"false"`).
### Example usage

```yaml
uses: helpfulengineering/ok-validate@v0.0.1
```

```yaml
uses: helpfulengineering/ok-validate@v0.0.1
with:
  path: './some/path/to/file.yaml'
```