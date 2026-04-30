import argparse
import os
import random

def _split(data, test_len):
    random.shuffle(data)
    return data[test_len:], data[:test_len]

def _write_jsonl(file_name, data):
    with open(file_name, 'w') as f:
        for ln in data:
            f.write(f"{ln}\n")

def main(file_name, test_fraction):
    data_points = []
    with open(file_name) as f:
       for line in f:
           data_points.append(line.strip())
    test_len = round(test_fraction * len(data_points))
    data_points, test_set = _split(data_points, test_len)
    train_set, valid_set = _split(data_points, test_len)
    # print(f"{len(train_set)=}, {len(valid_set)=}, {len(test_set)=}")
    directory = os.path.dirname(os.path.abspath(file_name))
    _write_jsonl(os.path.join(directory, f"{os.path.splitext(os.path.split(file_name)[-1])[0]}_train.jsonl"), train_set)
    _write_jsonl(os.path.join(directory, f"{os.path.splitext(os.path.split(file_name)[-1])[0]}_valid.jsonl"), valid_set)
    _write_jsonl(os.path.join(directory, f"{os.path.splitext(os.path.split(file_name)[-1])[0]}_test.jsonl"), test_set)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split JSONL file into train, test and vaiid sets.")
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to the jsonl file.",
    )
    parser.add_argument(
        "-s",
        "--split-fraction",
        required=True,
        help="The fraction of a train and valid set. If it is 0.2 and data set has 100 entries, train will be 60, valid and test will be by 20 entries each.",
    )
    args = parser.parse_args()
    main(args.file, float(args.split_fraction))
