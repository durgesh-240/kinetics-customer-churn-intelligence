from pathlib import Path
import hashlib
import requests

URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
EXPECTED_SHA256 = "16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91"
OUT = Path("data/raw/Telco-Customer-Churn.csv")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading dataset to {OUT} ...")
    response = requests.get(URL, timeout=60)
    response.raise_for_status()
    OUT.write_bytes(response.content)

    digest = sha256(OUT)
    print(f"SHA-256: {digest}")
    if digest != EXPECTED_SHA256:
        raise RuntimeError("Dataset checksum does not match the expected IBM sample file.")
    print("Dataset verified.")


if __name__ == "__main__":
    main()
