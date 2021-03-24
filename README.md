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

## CLI usage

```
usage: okv [-h] [-path [PATH]] [-s SCHEMA] [-n CPU_NUM] [-p PARSER] [--no-strict] [--no-error] [--ok OK]

Validate yaml files.

optional arguments:
  -h, --help            show this help message and exit
  -path [PATH]          folder to validate. Default is current directory.
  -s SCHEMA, --schema SCHEMA
                        filename of schema. Default is schema.yaml.
  -n CPU_NUM, --cpu-num CPU_NUM
                        number of CPUs to use. Default is 4.
  -p PARSER, --parser PARSER
                        YAML library to load files. Choices are "ruamel" or "pyyaml" (default).
  --no-strict           Disable strict mode, unexpected elements in the data will be accepted.
  --no-error            Ignore error when violation of schema is identified.
  --ok OK               This indicates which Open Know specification to use.
```

## Docker

### Usage

The Docker image accepts all of the [CLI arguments as detailed above](#cli-usage).

```
docker run --rm -v ${PWD}/:/tmp/ ok-validate --ok=okh -path=/tmp/path/to/okh-file.yaml
```

## Automatic releasing

<https://github.com/anothrNick/github-tag-action#bumping>

> Manual Bumping: Any commit message that includes #major, #minor, #patch, or #none will trigger the
> respective version bump. If two or more are present, the highest-ranking one will take precedence.
> If #none is contained in the commit message, it will skip bumping regardless DEFAUT_BUMP.