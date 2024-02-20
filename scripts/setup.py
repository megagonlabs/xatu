import csv
import json
from pathlib import Path

import fire
from datasets import load_dataset


def load_asset():
    data = []
    for x in load_dataset("asset")["test"]:
        data.append({
            "input": x['original'],
            "output": x['simplifications']})
    return data


def load_defacto(data_dir: Path):
    data = []
    for x in map(json.loads, open(data_dir / "raw" / "defacto/test.jsonl")):
        if x["has_error"]:
            data.append({
                "input": x["candidate"],
                "output": x["feedback"]["summary"],
                "reference": x["article"]
            })
    return data


def load_evidence(data_dir: Path):
    category = {"negate", "substitute_similar", "substitute_dissimilar"}
    data = []
    for x in map(json.loads, open(data_dir / "raw" / "evidence/dpr_50_3_test.jsonl")):
        if x["mutation"] in category:
            data.append({
                "input": x["mutated"],
                "output": x["original"],
                "reference": " ".join([" ".join(t) for t in x["pipeline_text"]])  # flat the evidence
            })
    return data


def load_factedit(data_dir: Path):
    data = []
    for x in map(json.loads, open(data_dir / "raw" / "factedit" / "test.jsonl")):
        for item in x["triple"]:
            item[1] = item[1][0]
        data.append({
            "input": " ".join([" ".join(t) for t in x["draft"]]),
            "output": " ".join([" ".join(t) for t in x["revised"]]),
            "reference": ["--".join(t) for t in x["triple"]]  # flat the evidence
        })
    return data


def load_fruit(data_dir: Path):
    data = []
    for x in map(json.loads, open(data_dir / "raw" / "fruit" / "gold_test_inputlabels.jsonl")):
        sp = x["inputs"].split("[CONTEXT]")
        data.append({
            "input": x["normalized_inputs"],
            "output": x["normalized_inputs"],
            "reference": sp[1]
        })
    return data


def load_jfleg():
    data = []
    for x in load_dataset("jfleg")["test"]:
        data.append({
            "input": x["sentence"],
            "output": x["corrections"],
        })
    return data


def load_styleptb(data_dir: Path):
    data = []
    for x in csv.DictReader(open(data_dir / "raw" / "styleptb" / "InfoAdditionFullResult.csv")):
        if x["Answer.MakeSense.on"] == 'TRUE':
            data.append({
                "input": x["Input.sentence"],
                "output": x["Answer.rewrite"],
                "reference": x["Input.info"]
            })
    return data


def load_wikibias(data_dir: Path):
    wikibias_dir = data_dir / "raw" / "wikibias"
    data = []
    for i, (src, tgt) in enumerate(zip(open(wikibias_dir / "test_source.tsv"), open(wikibias_dir / "test_target.tsv"))):
        if i % 5 == 0:
            src, is_one = src.strip().split(" ||| ")
            tgt = tgt.split("|||")[0].strip()
            if is_one == "1":
                data.append({
                    "input": src,
                    "output": tgt
                })
    return data


def load_wnc(data_dir: Path):
    data = []
    for x in csv.reader(open(data_dir / "raw" / "wnc" / "biased.word.test"), delimiter="\t"):
        data.append({
            "input": x[3],
            "output": x[4]
        })
    return data


def run(data_dir: str = "./data",
        output_path: str = "./data/xatu.jsonl"):
    data_dir = Path(data_dir)
    assert (data_dir / "xatu_release.jsonl").exists()
    xatu_release = [json.loads(line) for line in open(data_dir / "xatu_release.jsonl")]
    raw = {
        "asset": load_asset(),
        "defacto": load_defacto(data_dir),
        "evidence": load_evidence(data_dir),
        "factedit": load_factedit(data_dir),
        "fruit": load_fruit(data_dir),
        "jfleg": load_jfleg(),
        "stylePTB": load_styleptb(data_dir),
        "wikibias": load_wikibias(data_dir),
        "wnc": load_wnc(data_dir)
    }
    with open(output_path, "w") as file:
        for ins in xatu_release:
            raw_ins = raw[ins["data_source"]][ins["data_index"]]
            print(json.dumps({**ins, **raw_ins}), file=file)


if __name__ == '__main__':
    fire.Fire(run)
