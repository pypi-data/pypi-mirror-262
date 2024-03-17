import os
import logging
from .._shell import Shell
from .._errors import display_warning
from .._tempfiles import TempFile

_logger = logging.getLogger(__name__)

def reflect_command(args) -> None:
    """
    """
    _logger.debug(args.reflect)
    user_query = ' '.join(args.reflect)
    TempFile.create('user_query.txt', user_query)

    shell = Shell.get()
    shell.check_complience()
    display_warning("This command will run previous command in the background. You have 4 sec to stop it")

    if os.getenv("GAIDME_DEV") == "True":
        shell.execute("""history | tail -n 2 | head -n 1 | awk '{$1=""; print substr($0, 2)}' > $(echo $GAIDME_BASE_DIR)/command.txt;echo "\nWill run: $(cat $(echo $GAIDME_BASE_DIR)/command.txt)\n";sleep 4;source $(echo $GAIDME_BASE_DIR)/command.txt > $(echo $GAIDME_BASE_DIR)/command_result.txt; python -m gaidme.cli hidden""")
    shell.execute("""history | tail -n 2 | head -n 1 | awk '{$1=""; print substr($0, 2)}' > /tmp/command.txt;echo "\nWill run: $(cat /tmp/command.txt)\n";sleep 4;source /tmp/command.txt > /tmp/command_result.txt; gaidme hidden""")


