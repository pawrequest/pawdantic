"""
Import and export SQLModel database session to json once or on a schedule
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from pydantic.alias_generators import to_snake
from sqlmodel import SQLModel, Session, select
from loguru import logger


class SQLModelBackup:
    """
    Back-up a SQLModel database Session() to JSON file - once, or on a schedule.

    :param session: SQLModel session for database operations.
    :param models: List of SQLModel classes to backup.
    """

    def __init__(
            self,
            session: Session,
            models: list[type(SQLModel)],
            output_dir: Path,
    ):
        self.session = session
        self.output_dir = output_dir
        self.json_key_to_model_map = model_map_from_list(models)
        self.backup_target = self.output_dir / 'backup.json'
        self.restore_target = self.output_dir / 'restore.json'

        if self.output_dir.is_file():
            raise FileExistsError('Output directory is a file')
        if not self.output_dir.exists():
            logger.warning(f'Output directory does not exist, creating: {self.output_dir}')
            self.output_dir.mkdir(parents=True, exist_ok=True)

        if self.backup_target.is_dir():
            raise NotImplementedError('Backup Target is a directory')

    async def backup_loop(self, sleep_time: int):
        """
        Backup every ``sleep_time`` seconds.

        :param sleep_time: Interval in seconds between backup operations.
        """
        logger.info(f'Initialised, backing up now and every {sleep_time} seconds')
        while True:
            logger.debug('Waking')
            self.backup()
            logger.debug(f'Sleeping for {sleep_time} seconds')
            await asyncio.sleep(sleep_time)

    def backup(self):
        """
        Backup ``self.session`` to ``self.backup_target``.
        """
        backup_d = self.make_backup_dict()

        if not backup_d:
            logger.info('No models to backup')
            return

        with open(self.backup_target, 'w') as f:
            json.dump(backup_d, f, indent=4)
        logger.info(
            f'Saved {sum(len(v) for v in backup_d.values())} models to {self.backup_target}',
            category='BACKUP'
        )

    def make_backup_dict(self) -> dict:
        """
        :returns: Dictionary: {model.__name__ : [model instances]} in JSON format.
        """
        json_map = self.json_key_to_model_map
        session = self.session
        backup_dict = {
            model_name_in_json: [_.model_dump_json() for _ in
                                 session.exec(select(model_class)).all()]
            for model_name_in_json, model_class in json_map.items()
        }
        backup_up_model_strs = [f'{len(backup_dict[model])} {model}s' for model in backup_dict if
                                backup_dict[model]]
        logger.info(f"Dumped {', '.join(backup_up_model_strs)} to json", category='BACKUP')
        return backup_dict

    def restore(self):
        """
        Restore database from self.restore_target.
        """
        try:
            with open(self.restore_target) as f:
                backup_j = json.load(f)
        except Exception as e:
            logger.error(f'Error loading json: {e}')
            return

        for json_key, model_class in self.json_key_to_model_map.items():
            added = 0
            for json_string in backup_j.get(json_key):
                json_record = json.loads(json_string)
                model_instance = model_class.model_validate(json_record)

                try:
                    if self.session.get(model_class, model_instance.id):
                        continue

                except AttributeError:
                    if self.session.query(model_class).filter_by(**model_instance.dict()).first():
                        continue

                self.session.add(model_instance)
                added += 1
            if added:
                logger.info(
                    f'Loaded {added} {json_key} from {self.restore_target}',
                    category='BACKUP'
                )

        if self.session.new:
            self.session.commit()


def model_map_from_list[T:type[SQLModel]](models: list[T]) -> dict[str, T]:
    """
    :param models: A list of SQLModel classes.
    :returns: A dictionary mapping model.__name__ to type(model).
    """
    return {f'{to_snake(model.__name__)}s': model for model in models}
