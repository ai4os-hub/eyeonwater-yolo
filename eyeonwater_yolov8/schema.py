"""Module for defining custom web fields to use on the API interface.
This module is used by the API server to generate the input form for the
prediction and training methods. You can use any of the defined schemas
to add new inputs to your API.

The module shows simple but efficient example schemas. However, you may
need to modify them for your needs.
"""
from marshmallow import Schema, fields as ma_fields

class PredictionSchema(Schema):
    file_name = ma_fields.Str(description="Name of the image file")
    class_name = ma_fields.Str(description="Name of the predicted class")
    confidence = ma_fields.Float(description="Confidence score of the prediction")

class ResponseSchema(Schema):
    predictions = ma_fields.List(
        ma_fields.Nested(PredictionSchema),
        description="List of predictions with class information and confidence scores",
    )
    timestamp = ma_fields.Str(description="Timestamp of prediction")
    model_used = ma_fields.Str(description="Model name used for prediction")