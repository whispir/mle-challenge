import os.path

import pandas as pd
import torch
from pytorch_lightning import LightningDataModule
from torch.utils.data import Dataset, random_split, DataLoader

REPO_ROOT = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))


class WindDataModule(LightningDataModule):
    def __init__(self, batch_size=32, num_workers=0):
        super().__init__()
        self.save_hyperparameters(ignore=['num_workers'])
        self.train_set, self.test_set = None, None
        self.num_workers = num_workers

    def prepare_data(self) -> None:
        self.train_set, self.test_set = WindDataset().split()

    def train_dataloader(self) -> DataLoader:
        return DataLoader(self.train_set,
                          batch_size=self.hparams.batch_size,
                          num_workers=self.num_workers)

    def test_dataloader(self) -> DataLoader:
        return DataLoader(self.test_set,
                          batch_size=self.hparams.batch_size,
                          num_workers=self.num_workers)


def feature_engineering(x: dict):
    # TODO: Feature engineering (e.g. Wind Angle -> sin/cos)
    return x


IN_FEATURES = ['AmbientTemperatue', 'BearingShaftTemperature', 'Blade1PitchAngle', 'Blade2PitchAngle',
               'Blade3PitchAngle', 'ControlBoxTemperature', 'GearboxBearingTemperature',
               'GearboxOilTemperature', 'GeneratorRPM', 'GeneratorWinding1Temperature',
               'GeneratorWinding2Temperature', 'HubTemperature', 'MainBoxTemperature', 'NacellePosition',
               'ReactivePower', 'RotorRPM', 'TurbineStatus', 'WindDirection', 'WindSpeed']


def to_tensor(x):
    x = torch.stack([x[m] for m in IN_FEATURES], dim=1).float()
    return x


def pre_process(x):
    x = feature_engineering(x)
    # TODO: data normalise here
    x = to_tensor(x)
    return x


class WindDataset(Dataset):
    def __init__(self):
        df = pd.read_csv(os.path.join(REPO_ROOT, 'data/wind_power_generation.csv'))
        df = df.interpolate(limit=20).dropna().reset_index()
        df.pop('WTG')
        df.pop('index')
        df.pop('Unnamed: 0')
        self.df = df.astype('float32')

    @property
    def mean(self):
        return {'mean': self.df.mean().to_dict()}

    @property
    def std(self):
        return {'std': self.df.std().to_dict()}

    def __getitem__(self, item):
        x = self.df.loc[item, :].to_dict()
        y = x.pop('ActivePower')
        return x, y

    def __len__(self):
        return len(self.df)

    def split(self):
        test_len = int(len(self) / 6)
        train_len = len(self) - test_len
        train_set, test_set = random_split(self, lengths=[train_len, test_len])
        return train_set, test_set


if __name__ == '__main__':
    wd = WindDataset()
    import json

    print(json.dumps(wd[1], indent=2))
