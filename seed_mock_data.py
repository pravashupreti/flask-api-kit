import click
from alembic import command
from sqlalchemy.orm import Session
from logzero import logger

from mock_seed.confmock import script_path, seed_file_order, session, alembic_cfg
from api.utilities.seed_data import SeedData
from api.utilities.seed_minio_file import SeedMinioFiles
from api.utilities.mode import set_mode, remove_mode, MODE_MAINTENANCE
from config import Config


class MockDataSeed(SeedData):
    seed_path = script_path + '/data/'
    seed_file_order = seed_file_order

    @classmethod
    def run(cls, session_: Session, migration=True, downgrade=True, upgrade=True, load_files=True):

        # Fixes issue with logger being replaced with the alembic logger
        # https://stackoverflow.com/questions/42427487/using-alembic-config-main-redirects-log-output
        alembic_cfg.attributes["configure_logger"] = False

        if downgrade:
            logger.info("starting seed downgrade")
            cls.downgrade(session_)
        if migration:
            logger.info("starting migration downgrade")
            command.downgrade(alembic_cfg, 'base', sql=False, tag=None)
            logger.info("starting migration upgrade")
            command.upgrade(alembic_cfg, 'head', sql=False, tag=None)
        if upgrade:
            logger.info("starting seed upgrade")
            cls.upgrade(session_)
        if load_files:
            logger.info("loading minio files")
            SeedMinioFiles.load_files()

        logger.info("loading default tests")        


@click.command()
@click.option("--update", default=None)
@click.option("--migration/--no-migration", default=True)
@click.option("--downgrade/--no-downgrade", default=True)
@click.option("--upgrade/--no-upgrade", default=True)
@click.option("--load-files/--no-load-files", default=True)
def main(migration: bool, downgrade: bool, upgrade: bool, load_files: bool, update: str):
    if not Config.SEED_DATABASE:
        logger.info("skipping seed `SEED_DATABASE` is False")
        return

    if update:
        MockDataSeed.update(session, update)
        return

    logger.info("starting seed")
    try:
        # puts the server in maintenance mode (prevents request from disrupting seeds/migrations)
        logger.debug("setting maintenance mode")
        set_mode(MODE_MAINTENANCE)
        MockDataSeed.run(session, migration, downgrade, upgrade, load_files)
    except Exception as e:
        logger.error("seeding failed")        
        raise e
    finally:
        # takes the server out of maintenance mode
        logger.debug("removing maintenance mode")
        remove_mode(MODE_MAINTENANCE)
    logger.info("seeding complete")


if __name__ == "__main__" and Config.SEED_DATABASE:
    main()
