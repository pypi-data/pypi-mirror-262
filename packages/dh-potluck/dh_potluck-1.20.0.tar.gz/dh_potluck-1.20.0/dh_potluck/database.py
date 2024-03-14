from contextlib import contextmanager

import sqlalchemy
from packaging import version
from sqlalchemy import text


@contextmanager
def atomic(session, isolation_level='READ COMMITTED'):
    """
    A context manager that temporarily disables autocommit behaviour. It automatically restores the
    original isolation level when the block ends, and rollbacks any changes if they fail or are
    otherwise uncommitted.

    Parameters:
    - session (sqlalchemy.orm.session.Session): The database session to be used for the transaction.
    - isolation_level (str, optional): The transaction isolation level to be used for this context.
    Defaults to 'READ COMMITTED'.

    Example:
    ```python
    with atomic(db.session):
        db.session.add(new_record)
        # More database operations...
        db.session.commit()
    ```
    """
    if version.parse(sqlalchemy.__version__) < version.parse('2.0.20'):
        raise Exception('This context manager requires SQLAlchemy >= 2.0.20')

    connection = session.connection()
    is_autocommit = connection._is_autocommit_isolation()
    original_isolation_level = connection.default_isolation_level

    if not is_autocommit:
        raise Exception('Isolation level must be AUTOCOMMIT in order to use `atomic()`.')

    # Ensure the current transaction is closed
    session.rollback()

    # Disable autocommit and set isolation level to the provided value
    session.connection(execution_options={'isolation_level': isolation_level})

    try:
        yield
    finally:
        # Re-enable autocommit and discard anything not explicitly committed in the context manager
        session.rollback()

        # Restore the original isolation level if necessary. This is necessary because while
        # SQLAlchemy treats autocommit as an isolation level, it's not one in the DB. In theory,
        # the DB isolation level shouldn't matter much when autocommit is enabled, but to be safe
        # we set it back to the original value here.
        if isolation_level != original_isolation_level:
            session.execute(
                text(f'SET SESSION TRANSACTION ISOLATION LEVEL {original_isolation_level}')
            )
