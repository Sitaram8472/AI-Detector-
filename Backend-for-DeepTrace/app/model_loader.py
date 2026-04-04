from pathlib import Path

import joblib
import torch.nn as nn
import torch
from torchvision import models

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
ML_MODULE_MODELS_DIR = BASE_DIR.parent / "deepTrace" / "ml_module" / "models"


def _validate_model_file(path: Path) -> None:
	if not path.exists():
		raise FileNotFoundError(f"Model file not found: {path}")
	if path.stat().st_size == 0:
		raise ValueError(f"Model file is empty (0 bytes): {path}")


def _load_torch_model(filename: str):
	path = MODELS_DIR / filename
	_validate_model_file(path)
	model = torch.load(path, map_location="cpu")
	if hasattr(model, "eval"):
		model.eval()
	return model


def _first_existing_path(*paths: Path) -> Path:
	for path in paths:
		if path.exists() and path.stat().st_size > 0:
			return path
	raise FileNotFoundError(
		"No valid model file found in expected locations: "
		+ ", ".join(str(p) for p in paths)
	)


def _build_image_model() -> nn.Module:
	model = models.efficientnet_b0(weights=None)
	classifier_layer = model.classifier[1]
	if not isinstance(classifier_layer, nn.Linear):
		raise TypeError("Unexpected EfficientNet classifier structure")
	num_features = classifier_layer.in_features
	model.classifier[1] = nn.Linear(num_features, 2)
	return model


def _load_image_model_state_dict(_filename: str):
	# Prefer backend-local model file, then fallback to training output path.
	path = _first_existing_path(
		MODELS_DIR / "image_models.pth",
		MODELS_DIR / "image_model.pth",
		ML_MODULE_MODELS_DIR / "image" / "image_model.pth",
	)
	state_dict = torch.load(path, map_location="cpu")
	model = _build_image_model()
	if isinstance(state_dict, dict):
		model.load_state_dict(state_dict)
	else:
		# Backward compatibility in case a full module was saved.
		model = state_dict
	if hasattr(model, "eval"):
		model.eval()
	return model


def _load_video_model(_filename: str):
	path = _first_existing_path(
		MODELS_DIR / "video_model.pth",
		ML_MODULE_MODELS_DIR / "video_model.pth",
		ML_MODULE_MODELS_DIR / "video" / "video_model.pth",
	)
	model = torch.load(path, map_location="cpu")
	if hasattr(model, "eval"):
		model.eval()
	return model


def _load_joblib_model(filename: str):
	path = MODELS_DIR / filename
	_validate_model_file(path)
	return joblib.load(path)


def _load_joblib_from_paths(*paths: Path):
	path = _first_existing_path(*paths)
	return joblib.load(path)


def _load_text_model(_filename: str):
	return _load_joblib_from_paths(
		MODELS_DIR / "text_model.pkl",
		MODELS_DIR / "ai_model.pkl",
		ML_MODULE_MODELS_DIR / "text" / "text_model.pkl",
		ML_MODULE_MODELS_DIR / "text" / "ai_model.pkl",
	)


def _load_text_vectorizer(_filename: str):
	return _load_joblib_from_paths(
		MODELS_DIR / "tfidf_vectorizer.pkl",
		ML_MODULE_MODELS_DIR / "text" / "tfidf_vectorizer.pkl",
	)


def _safe_load(loader, filename: str):
	try:
		return loader(filename), None
	except Exception as exc:
		return None, str(exc)


video_model, video_model_error = _safe_load(_load_video_model, "video_model.pth")
image_model, image_model_error = _safe_load(_load_image_model_state_dict, "image_models.pth")
text_model, text_model_error = _safe_load(_load_text_model, "text_model.pkl")
text_vectorizer, text_vectorizer_error = _safe_load(_load_text_vectorizer, "tfidf_vectorizer.pkl")