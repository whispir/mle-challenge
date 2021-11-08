# Intro & Prerequisite:

- kubectl
- minikube
- Docker
- Python3.8 

# Testing
Build docker and run tests
```
source scripts/testing.sh
```

# Training:


**Training on VM/Local**
- A dir called `lightning_logs` will be created (under the working dir by default) and contain the checkpoint, 
  tensorboard event and `config.yaml` 
  so you can always reproduce the experiments with the yaml. 
  Ideally this logging directory could go to s3 or EFS, so we have a centralised place to manage those "by-products"
- Each experiment could have their own `.yaml` file (under [configs](configs)), 
  alternatively one can overwrite the default value through CLI. 
  Again a copy of `.yaml` will always be saved to `lightning_logs`.
  
```bash
pip3 install -e .
# use config file
python3 windml/train_net.py --config configs/config.test.yaml
# detailed instruction on CLI:
python3 windml/train_net.py -h
```

**Training with container**
```bash
# run training example
source scripts/build.sh && docker run -it $IMAGE python3 windml/train_net.py --config configs/config.test.yaml
# check help
source scripts/build.sh && docker run -it $IMAGE python3 windml/train_net.py -h
```

**Training with kubernetes job**
```bash
source scripts/train-k8s-job.sh
```

# Serving & Deployment
**Local/VM testing and debug:**
```bash
pip3 install -e .
python3 windml/app.py
```

**With Docker:**
```bash
source scripts/build.sh && docker run -it -p 8001:8000 $IMAGE uvicorn windml.app:app --reload --host 0.0.0.0
```

**With K8s:**
```bash
source scripts/deploy.sh
```


# TODOs
- DS
    - [ ] Normalisation processing
    - [ ] Null value processing
    - [ ] Artifact management (logs/checkpoints/graph)
    - [ ] model packaging - TorchScripts to record graph (jit.save/jit.load)
- Ops
    - [ ] Process: CT/Manual Training -> checkpoint selection -> CI/Test -> artifact(image) -> CD -> Staging -> UAT/Sandbox -> Prod
- Tests/CI
    - [x] API e2e test 
    - [ ] CI
    - [x] unit tests
    - [x] training integration test
