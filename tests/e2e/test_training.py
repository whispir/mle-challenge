import pytest
from pytorch_lightning.utilities.cli import LightningCLI

from windml.dataset import WindDataModule
from windml.model import WindRegressor
import sys


@pytest.fixture
def cli():
    sys.argv = [__file__, '--trainer.max_steps', '10', '--trainer.enable_checkpointing', 'false']
    cli = LightningCLI(
        WindRegressor, WindDataModule, seed_everything_default=42, save_config_overwrite=True, run=False,
    )
    return cli


class TestTraining:
    def test_training(self, cli: LightningCLI):
        cli.trainer.fit(cli.model, datamodule=cli.datamodule)

    def test_val(self, cli: LightningCLI):
        cli.trainer.validate(cli.model, datamodule=cli.datamodule)



