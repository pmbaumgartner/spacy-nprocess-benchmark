import json
import platform
from itertools import product
from pathlib import Path
from uuid import uuid4

from loguru import logger

from issue import main

files = Path("data/").glob("*.json")
data = [json.loads(file.read_text()) for file in files]
for d in data:
    d.pop("time")


def my_product(inp):
    return (dict(zip(inp.keys(), values)) for values in product(*inp.values()))


grid = {
    "dataset": ["ag_news", "squad"],
    "model": ["en_core_web_sm", "en_core_web_md", "en_core_web_lg"],
    "n_data": [1_000, 10_000, 100_000, 250_000],
    "batch_size": [500, 1_000, 2_000, 5_000],
    "n_process": [1, 2, 3, 4],
}

if __name__ == "__main__":
    for args in my_product(grid):
        args["platform"] = f"{platform.system()} - {platform.release()}"
        if args in data:
            logger.info("Already Captured")
            continue
        if args["batch_size"] > args["n_data"]:
            continue
        if args["batch_size"] * args["n_process"] > args["n_data"]:
            continue
        args.pop("platform")
        time = main(**args)
        args["platform"] = f"{platform.system()} - {platform.release()}"
        args["time"] = time
        Path(f"data/{uuid4()}.json").write_text(json.dumps(args))
