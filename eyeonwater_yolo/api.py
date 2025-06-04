# -*- coding: utf-8 -*-
"""
Functions to integrate your model with the DEEPaaS API.
It's usually good practice to keep this file minimal, only performing
the interfacing tasks. In this way you don't mix your true code with
DEEPaaS code and everything is more modular. That is, if you need to write
the predict() function in api.py, you would import your true predict function
and call it from here (with some processing / postprocessing in between
if needed).
For example:

    import mycustomfile

    def predict(**kwargs):
        args = preprocess(kwargs)
        resp = mycustomfile.predict(args)
        resp = postprocess(resp)
        return resp

To start populating this file, take a look at the docs [1] and at
an exemplar module [2].

[1]: https://docs.ai4os.eu/
[2]: https://github.com/ai4os-hub/ai4os-demo-app
"""


import math
import time
import zipfile
import tempfile
import logging
import secrets

from datetime import datetime
from pathlib import Path
from PIL import Image
from webargs import fields
from ultralytics import YOLO
from tensorboardX import SummaryWriter
from eyeonwater_yolo import config
from eyeonwater_yolo.schema import ResponseSchema
from eyeonwater_yolo.misc import _catch_error, launch_tensorboard

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)

BASE_DIR = Path(__file__).resolve().parents[1]


@_catch_error
def get_metadata():
    """Returns a dictionary containing metadata information about the module.
       DO NOT REMOVE - All modules should have a get_metadata() function

    Raises:
        HTTPException: Unexpected errors aim to return 50X

    Returns:
        A dictionary containing metadata information required by DEEPaaS.
    """
    try:  # Call your AI model metadata() method
        logger.info("Collecting metadata from: %s", config.API_NAME)
        metadata = config.PROJECT_METADATA
        logger.debug("Package model metadata: %s", metadata)
        return metadata
    except Exception as err:
        logger.error("Error collecting metadata: %s", err, exc_info=True)
        raise  # Reraise the exception after log


def get_train_args():
    return {
        "epoch_num": fields.Int(
            required=False,
            missing=10,
            description="Total number of training epochs",
        ),
    }


def train(**kwargs):
    """
    Dummy training. Logs random metrics in Tensorboard to mimic monitoring.
    """
    logdir = BASE_DIR / "models" / time.strftime("%Y-%m-%d_%H-%M-%S")
    writer = SummaryWriter(logdir=logdir, flush_secs=1)
    launch_tensorboard(logdir=logdir)
    for epoch in range(kwargs["epoch_num"]):
        time.sleep(1.0)
        writer.add_scalar(
            "scalars/loss",
            -math.log(epoch + 1) * (1 + secrets.SystemRandom() * 0.2),
            epoch,
        )
        writer.add_scalar(
            "scalars/accuracy",
            min((1 - 1 / (epoch + 1)) * (1 + secrets.SystemRandom() * 0.1), 1),
            epoch,
        )
    writer.close()
    (logdir / "final_model.hdf5").touch()
    return {"status": "done", "final accuracy": 0.9}


def get_predict_args():
    """
    Define arguments for the predict function, only accepting image files.
    """
    return {
        "image": fields.Field(
            required=True,
            type="file",
            location="form",
            description="Upload an image file or ZIP for prediction.",
        )
    }


def predict(**kwargs):
    """
    Run YOLOv8 inference on uploaded images (single, zip, or folder)
    and return predictions
    with confidence scores.
    """
    uploaded_file = kwargs.get("image")
    if not uploaded_file:
        return {"error": "No file uploaded", "status": "failed"}
    try:
        model_path = BASE_DIR / "models" / "best.pt"
        if not model_path.exists():
            logging.error("Model file not found at %s", model_path)
            raise FileNotFoundError(f"Model file not found at {model_path}")

        model = YOLO(model_path)
        predictions = []

        # Handle zip files, folders, or single images
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            if zipfile.is_zipfile(uploaded_file.filename):
                # Extract zip file
                with zipfile.ZipFile(uploaded_file.filename, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir_path)

                # Process extracted images
                predictions.extend(process_images(temp_dir_path, model))
            elif Path(uploaded_file.filename).is_dir():
                # Process images in the folder
                folder_path = Path(uploaded_file.filename)
                predictions.extend(process_images(folder_path, model))
            else:
                # Handle single image
                image_pil = Image.open(uploaded_file.filename).convert("RGB")
                results = model.predict(image_pil, save=False, imgsz=256)
                predictions.extend(process_results(results))

        response = {
            "predictions": predictions,
            "timestamp": datetime.now().isoformat(),
            "model_used": str(model_path.name)
        }
        return response

    except FileNotFoundError as e:
        logging.error("Model file error: %s", str(e))
        return {"error": str(e), "status": "failed"}
    except (ValueError, TypeError) as e:
        logging.error("Invalid data error: %s", str(e))
        return {
            "error": f"Data validation error: {str(e)}",
            "status": "failed"
        }
    except (IOError, OSError) as e:
        logging.error("File operation error: %s", str(e))
        return {
            "error": f"File processing error: {str(e)}",
            "status": "failed"
        }
    except RuntimeError as e:
        logging.error("Model inference error: %s", str(e))
        return {
            "error": f"Error during inference: {str(e)}",
            "status": "failed"
        }


def process_images(folder_path, model):
    """
    Process all images in a folder and return predictions.
    """
    predictions = []
    for image_path in folder_path.glob("**/*"):
        if image_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            image_pil = Image.open(image_path).convert("RGB")
            results = model.predict(image_pil, save=False, imgsz=256)
            predictions.extend(process_results(results))
    return predictions


def process_results(results):
    """
    Process YOLOv8 results and return predictions.
    """
    predictions = []
    for result in results:
        if result.probs:
            top1_class_id = result.probs.top1
            top1_confidence = float(result.probs.top1conf.cpu().numpy())
            file_name = result.path.split("\\")[-1]

            predictions.append({
                "file_name": file_name,
                "class_name": result.names[top1_class_id],
                "confidence": top1_confidence
            })
    return predictions


schema = ResponseSchema
