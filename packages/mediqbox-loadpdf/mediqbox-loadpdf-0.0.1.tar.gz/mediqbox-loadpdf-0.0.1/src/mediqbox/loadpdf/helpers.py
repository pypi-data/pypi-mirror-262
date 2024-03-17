import hashlib
import json

from typing import Any

def sha256sum(filename: str) -> str:
  with open(filename, 'rb', buffering=0) as f:
    return hashlib.file_digest(f, 'sha256').hexdigest()

def to_str(obj: Any) -> str:
  try:
    return json.dumps(
      obj,
      ensure_ascii=False,
      indent=2,
      default=str
    ).encode('utf8').decode()
  except:
    return str(obj)