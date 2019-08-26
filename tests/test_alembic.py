import os
from alembic.config import Config
from alembic.script import ScriptDirectory


def test_only_single_head_revision_in_migrations():
    test_path = os.path.dirname(os.path.abspath(__file__))
    ini_path = os.path.join(test_path, "seed/alembic.ini")
    alembic_cfg = Config(ini_path)
    
    alembic_directory = os.path.join(test_path, "../alembic")
    alembic_cfg.set_main_option("script_location", alembic_directory)
    script = ScriptDirectory.from_config(alembic_cfg)

    # This will raise if there are multiple heads
    script.get_current_head()
    