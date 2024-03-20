from __future__ import annotations

import asyncio

from suppawt.backup_ps.pruner import Pruner
from .sqlmodel_backup import SQLModelBackup


async def schedule_backup_prune(backupbot: SQLModelBackup, pruner_bot: Pruner, sleep: int):
    """
    Runs backup, copy, and prune operations in a loop with a specified sleep interval.

    :param backupbot: An instance of SQLModelBot for handling database backup operations.
    :param pruner_bot: An instance of Pruner for handling file pruning operations.
    :param sleep: Time in seconds to wait between each backup operation.
    """
    while True:
        backupbot.backup()
        pruner_bot.copy_and_prune()
        await asyncio.sleep(sleep)
