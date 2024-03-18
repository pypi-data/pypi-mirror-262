# coding: utf-8
"""

"""

import logging

import flask_sqlalchemy

from .utils import find_migrations, should_skip_by_index, update_migration_index


def run(db: flask_sqlalchemy.SQLAlchemy) -> None:
    logger = logging.getLogger('sampledb.migrations')
    for index, name, function in find_migrations():
        logger.info('Migration #%d "%s":', index, name)

        # Skip migration by migration index
        if should_skip_by_index(db, index):
            logger.info("Skipped (index).")
            continue

        try:
            # Perform migration
            if function(db):
                logger.info("Done.")
            else:
                logger.info("Skipped (condition).")

            # Update migration index to skip this migration by index in the future
            update_migration_index(db, index)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
