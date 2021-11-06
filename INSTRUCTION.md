# Training:

Training
- A dir called `lightning_logs` will be created and contain the checkpoint & tensorboard event
- Each experiment should have their own `.yaml` file (under [configs](configs)), 
  alternatively one can overwrite the default value through CLI
```bash
# use config file
python3 windml/train_net.py --config ../configs/config.test.yaml
# detailed instruction on CLI:
python3 windml/train_net.py -h
```




# Serving
Local testing and debug:
```bash
python3 app.py
```


With Docker:
```bash
sh scirpts
```


With K8s:
```bash

```


# TODOs
- DS
    - [ ] Normalisation processing
    - [ ] Null value processing
    - [ ] Artifact management (logs/checkpoints)
    - [ ] model packaging - TorchScripts to record graph (jit.save/jit.load)
- Ops
    - [ ] CD to k8s
    - [ ] DNS/SSL
- Tests
    - [ ] end2end test 
    - [x] CI
    - [x] unit tests
