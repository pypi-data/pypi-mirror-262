# I

Execute commands with respect for English grammar

## How to install

```console
pip install i-will
```

## How to use

To use, attach `I`, `I will`, or `please` in front of the command and switch the order of the second and first argument of the command. For example, `pip list` can be used as `I list pip` or `please list pip`.

For example:

```console
I run cargo                # executes: `cargo run`
I will list pip            # executes: `pip list`
please install pip i-will  # executes: `pip install i-will`
please will run cargo      # XXX It'll cause error.
```
