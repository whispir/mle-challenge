import time
from typing import Union, Optional

import torch
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from windml.dataset import IN_FEATURES
from windml.model import Net

app = FastAPI()

ESTIMATOR = Net()
# ESTIMATOR = ESTIMATOR.load_from_checkpoint(checkpoint_path="example.ckpt")


@app.get("/")
async def healthcheck():
    msg = "Hello, Whispir!"
    return {"message": msg}


def validate_data(d):
    missing_ft = set(IN_FEATURES) - set(d.keys())
    # type_check = all([isinstance(x, float) for x in d.values()])
    if missing_ft:
        return False, f"Missing feature {list(missing_ft)}"
    return True, ""


class ResponseBody(BaseModel):
    predictions: Union[list, dict] = None
    process_time: Optional[float] = None


def _estimate(body):
    if isinstance(body, dict) and all([isinstance(x, float) for x in body.values()]):
        # data type check
        input_data = {k: torch.tensor([v], dtype=torch.float32) for k, v in body.items()}
    else:
        _expected_format = {k: "float" for k in IN_FEATURES}
        return JSONResponse(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, content={
                'error': f'API only support body of json formatted as `{_expected_format}`, check your datatype'}
        )

    is_valid, _msg = validate_data(input_data)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={'error': _msg}
        )
    else:
        t0 = time.perf_counter()
        y_hat = ESTIMATOR(input_data)
        t1 = round(time.perf_counter() - t0, 6)
        response = {'predictions': y_hat.squeeze().detach().numpy().tolist(), 'process_time': t1}

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=response
        )


@app.post("/estimate")
async def estimate(request: Request):
    body = await request.json()
    return _estimate(body)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
