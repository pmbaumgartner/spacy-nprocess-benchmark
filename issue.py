import os
import platform
from itertools import cycle, islice
from time import time

import spacy
import typer
from datasets import load_dataset
from loguru import logger
from tqdm import tqdm


def load_data(dataset: str):
    if dataset == "ag_news":
        return load_dataset("ag_news")["train"]["text"]
    if dataset == "squad":
        return load_dataset("squad")["train"]["question"]


def main(
    dataset: str,
    model: str = "en_core_web_sm",
    n_process: int = 1,
    batch_size: int = 1000,
    n_data: int = 100000,
):
    logger.info(f"{platform.system()} - {platform.release()}")
    logger.info("Loading Data")
    data = load_data(dataset)
    text_list = list(islice(cycle(data), n_data))
    mean_length = sum((len(i) for i in text_list)) / len(text_list)
    logger.info(f"Data Loaded. N={len(text_list)}. μ(len)={mean_length}")

    logger.info(f"Loading Model: {model}")
    nlp = spacy.load(model)
    logger.info("Model Loaded")

    logger.info(f"N PROCESS: {n_process}. BATCH SIZE: {batch_size}")

    logger.info("Starting Pipe Loop")
    start = time()
    nlp_pipe = nlp.pipe(text_list, n_process=n_process, batch_size=batch_size)
    for _ in nlp_pipe:
        pass
    finish = time()
    elapsed = finish - start
    logger.info(f"Finished Pipe Loop. Elapsed: {elapsed:.1f}s")
    return elapsed


if __name__ == "__main__":
    typer.run(main)
