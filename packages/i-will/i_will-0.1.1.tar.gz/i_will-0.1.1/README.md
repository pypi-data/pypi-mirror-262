# I

Execute commands with respect for English grammar

## How to install

```console
pip install i-will
```

## How to use

To use, attach `I`, `I will`, or `please` in front of the command and switch the order of the second and first argument of the command. For example, `pip list` can be used as `I list pip` or `please list pip`.

```console
I list pip                 # executes: `pip list`
I will run cargo           # executes: `cargo run`
please install pip i-will  # executes: `pip install i-will`
XXX please will run cargo  # This will cause error.
```
