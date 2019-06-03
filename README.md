# sawmill
A custom Python logger which can be configured to output logs to the user's preference.

### .env
Sawmill only has 1 environmental variable:

| Name                | Required By         | Purpose             |
|---------------------|---------------------|---------------------|
| SAWMILL_DEVELOPER_LOGS | `sawmill.logger` | True/False - switches between outputting logs to terminal/local file store and outputting to sys.stdout |

### usage
Instead of doing the usual logger setup:
```python
import logging
import sys

logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s %(filename)s'))
stdout_handler.setLevel(logging.INFO)
logger.addHandler(stdout_handler)

logger.info('Logger has been created')
```

Do this instead:
```python
from sawmill.logger import Sawmill

logger = Sawmill.new_logger(__name__)

logger.info('Sawmill logger has been created')
```

All the logging handlers & formatters are handled in the background removing the need to have the setup code
at the top of your *.py files.

### How To
##### - Change log format
Log format can be different per output type AND log level.
Go into the sawmill/config.py file and select a 'MsgFormat' Enum option.
##### - Define a new log format
Go into sawmill/utils.py and add to the existing 'MsgFormat' Enum.
##### - Change log colours
Go into the sawmill/config.py file and select an Enum option for primary, secondary & tertiary colours.
##### - Define a new log colour
Colour Enum values are [256 colour codes].
Go into sawmill/utils.py and add to the existing 'Colour' Enum.

### Terminal commands
`$ make env`
Builds the environment using poetry
`$ make run`
Doesn't do anything! Just here for consistency with our other projects
`$ make test`
Runs the test suite
`$ make lint`
Runs linting on the code
`$ make docs`
Uses Sphinx to auto-create documentation from doc-strings
`$ make requirements`
Creates/updates the requirements.txt

[256 colour codes]: https://jonasjacek.github.io/colors/

License
----
MIT