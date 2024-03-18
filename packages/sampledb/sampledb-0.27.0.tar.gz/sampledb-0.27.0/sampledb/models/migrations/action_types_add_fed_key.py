# coding: utf-8
"""
Add fed_id and component_id columns to action_types table.
"""

import os

import flask_sqlalchemy

from .utils import table_has_column

MIGRATION_INDEX = 81
MIGRATION_NAME, _ = os.path.splitext(os.path.basename(__file__))


def run(db: flask_sqlalchemy.SQLAlchemy) -> bool:
    # Skip migration by condition
    if table_has_column('action_types', 'fed_id'):
        return False

    # Perform migration
    db.session.execute(db.text("""
        ALTER TABLE action_types
            ADD fed_id INTEGER,
            ADD component_id INTEGER,
            ADD FOREIGN KEY(component_id) REFERENCES components(id),
            ADD CONSTRAINT action_types_fed_id_component_id_key UNIQUE(fed_id, component_id)
    """))
    return True
