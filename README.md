[![progress-banner](https://backend.codecrafters.io/progress/kafka/82e3bb60-5bac-4bee-b5ad-986f1a7e549f)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a starting point for Python solutions to the
["Build Your Own Kafka" Challenge](https://codecrafters.io/challenges/kafka).

In this challenge, you'll build a toy Kafka clone that's capable of accepting
and responding to APIVersions & Fetch API requests. You'll also learn about
encoding and decoding messages using the Kafka wire protocol. You'll also learn
about handling the network protocol, event loops, TCP sockets and more.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# Passing the first stage

The entry point for your Kafka implementation is in `app/main.py`. Study and
uncomment the relevant code, and push your changes to pass the first stage:

```sh
git commit -am "pass 1st stage" # any msg
git push origin master
```

That's all!

# Stage 2 & beyond

Note: This section is for stages 2 and beyond.

1. Ensure you have `python (3.x)` installed locally
1. Run `./your_program.sh` to run your Kafka broker, which is implemented in
   `app/main.py`.
1. Commit your changes and run `git push origin master` to submit your solution
   to CodeCrafters. Test output will be streamed to your terminal.

# Troubleshooting

## module `socket` has no attribute `create_server`

When running your server locally, you might see an error like this:

```
Traceback (most recent call last):
  File "/.../python3.7/runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "/.../python3.7/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/app/app/main.py", line 11, in <module>
    main()
  File "/app/app/main.py", line 6, in main
    s = socket.create_server(("localhost", 6379), reuse_port=True)
AttributeError: module 'socket' has no attribute 'create_server'
```

This is because `socket.create_server` was introduced in Python 3.8, and you
might be running an older version.

You can fix this by installing Python 3.8 locally and using that.

If you'd like to use a different version of Python, change the `language_pack`
value in `codecrafters.yml`.

# 📌 Python `struct.pack` Format Cheat Sheet

## **Endianness and Alignment**
| Symbol | Meaning |
|--------|---------|
| `@` | Native endianness and alignment (default) |
| `<` | Little-endian (least significant byte first) |
| `>` | Big-endian (network byte order) |
| `!` | Big-endian (network order, standard alignment) |
| `=` | Native endianness, standard alignment |

## **Integer Types**
| Format | C Type | Python Type | Size (bytes) |
|--------|--------|------------|-------------|
| `b` | `signed char` | `int` | 1 |
| `B` | `unsigned char` | `int` | 1 |
| `h` | `short` | `int` | 2 |
| `H` | `unsigned short` | `int` | 2 |
| `i` | `int` | `int` | 4 |
| `I` | `unsigned int` | `int` | 4 |
| `l` | `long` | `int` | 4 |
| `L` | `unsigned long` | `int` | 4 |
| `q` | `long long` | `int` | 8 |
| `Q` | `unsigned long long` | `int` | 8 |

## **Floating-Point Types**
| Format | C Type | Python Type | Size (bytes) |
|--------|--------|------------|-------------|
| `f` | `float` | `float` | 4 |
| `d` | `double` | `float` | 8 |

## **Other Types**
| Format | Meaning | Size |
|--------|---------|------|
| `c` | Single character (bytes) | 1 |
| `s` | String (bytes) | Variable |
| `p` | Pascal-style string | Variable |
| `x` | Pad byte (no value) | 1 |

## **Examples**
```python
import struct

# Packing values
data = struct.pack(">hI", 42, 123456)  # Big-endian short (2 bytes) + int (4 bytes)
print(data.hex())  # 002a 0001e240

# Unpacking values
unpacked = struct.unpack(">hI", data)
print(unpacked)  # (42, 123456)

# Packing a string
string_data = struct.pack("5s", b"hello")  # 5-byte string
print(string_data)  # b'hello'

