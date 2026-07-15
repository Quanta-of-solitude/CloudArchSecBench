import os
import json
import csv
import argparse
import sys
from pathlib import Path

# Make backend importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.models.schema import Architecture
from app.services.evaluator import evaluate


def run(input_dir, output_prefix, model):
    results = []

    input_path = Path(input_dir)

    for file in sorted(input_path.glob("*.json")):
        try:
            with open(file, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠ Skipping invalid JSON: {file.name}")
            continue

        architecture = Architecture(**data)
        evaluation = evaluate(architecture)

        results.append({
            "scenario": file.stem,
            "score": evaluation["score"],
            "issues": evaluation["issue_count"],
            "category_scores": evaluation["category_scores"],
            "details": evaluation
        })

        print(f"✓ {file.stem:<30} Score: {evaluation['score']}")

    average = (
        sum(r["score"] for r in results) / len(results)
        if results else 0
    )

    report = {
        "benchmark": "AWS-ArchBench v0.1",
        "model": model,
        "scenario_count": len(results),
        "average_score": round(average, 2),
        "results": results
    }

    json_path = f"{output_prefix}.json"
    csv_path = f"{output_prefix}.csv"

    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Scenario", "Score", "Issue Count"])

        for r in results:
            writer.writerow([
                r["scenario"],
                r["score"],
                r["issues"]
            ])

    print("\n--------------------------------")
    print(f"Average Score : {average:.2f}")
    print(f"JSON Report   : {json_path}")
    print(f"CSV Report    : {csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Folder containing architecture JSON files"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output file prefix"
    )

    parser.add_argument(
        "--model",
        default="chatgpt"
    )

    args = parser.parse_args()

    run(args.input, args.output, args.model)