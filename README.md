Description of my casino Python program.
<pre>
.
    ├── Turn-base_Casino
    │   ├── .casino_log/                       # project logs
    │   ├── src/                               # Source code
    │       ├── common/                        # main functions of the console
    │            ├── __init__.py               #
    │            ├── config.py                 # logging config
    │       ├── facade/                        # place to gather everything
    │            ├── __init__.py               #
    │            ├── facade.py                 # file for simpler usage of program functional
    │       ├── infrastructure/                # folder with main program files
    │            ├── __init__.py               #
    │            ├── casino.py                 # casino itself
    │            ├── collection.py             # players, geese and casino collections
    │            ├── events.py                 # list of random events
    │            ├── geese.py                  # goose types
    │            ├── players.py                # casino players
    │   ├── tests/                             # Code tests
    │   ├── .gitignore                         # git ignore files
    │   ├── .pre-commit-config.yaml            # Code-style check
    │   ├── pyproject.toml                     # Project configuration
    │   ├── README.md                          # Laboratory report with a project description
</pre>