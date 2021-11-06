from pl_examples import cli_lightning_logo
from pytorch_lightning.utilities.cli import LightningCLI

from windml.dataset import WindDataModule
from windml.model import WindRegressor


def cli_main():
    # The LightningCLI removes all the boilerplate associated with arguments parsing. This is purely optional.
    cli = LightningCLI(
        WindRegressor, WindDataModule, seed_everything_default=42, save_config_overwrite=True, run=False
    )
    cli.trainer.fit(cli.model, datamodule=cli.datamodule)
    cli.trainer.test(ckpt_path="best", datamodule=cli.datamodule)


if __name__ == "__main__":
    cli_lightning_logo()
    cli_main()
