import torch
from pytorch_lightning import LightningModule
from torch import nn
from torch.nn import functional as F
from torchmetrics import MeanSquaredError

from windml.dataset import pre_process


class Net(nn.Module):
    def __init__(self, hidden=40):
        super(Net, self).__init__()

        self.l1 = nn.Linear(in_features=19, out_features=hidden)
        self.l2 = nn.Linear(in_features=hidden, out_features=1)

    def forward(self, x):
        x = pre_process(x)
        h = F.relu(self.l1(x))
        y_hat = self.l2(h)
        return y_hat


class WindRegressor(LightningModule):
    def __init__(self, model, lr=1.0, gamma=0.7, batch_size=32):
        super().__init__()
        self.save_hyperparameters()
        self.model = model or Net()
        # self.test_mse = MeanSquaredError()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = F.mse_loss(y_hat, y.float())
        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = F.mse_loss(y_hat, y.float())
        self.log("test_mse", loss)
        return loss

    validation_step = test_step

    def configure_optimizers(self):
        optimizer = torch.optim.Adadelta(self.model.parameters(), lr=self.hparams.lr)
        return [optimizer], [torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=self.hparams.gamma)]
