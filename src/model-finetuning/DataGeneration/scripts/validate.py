import json
import sys
import argparse

def validate_one_field(field, field_name, roles, num):
    #print(field_name in field)
    if field_name not in field:
        return f'Line {num}: No {field_name} entry'
    if not isinstance(field[field_name], list):
        return f"Line {num}: {field_name} field is not a list."
    for i, dt_item in enumerate(field[field_name]):
        i += 1
        if not isinstance(dt_item, dict):
            return f"Line {num}: {field_name} field {i}-th entry is not a dictionary."
        if not "role" in dt_item:
            return f"Line {num}: {field_name} field {i}-th entry does not have a role."
        if dt_item["role"] not in roles:
            return f"Line {num}: {field_name} field {i}-th role is {dt_item['role']} while expected roles are {roles}."
        if not "content" in dt_item:
            return f"Line {num}: {field_name} field {i}-th entry does not have a content."

def validate(file_name):
    errors = []
    num = 1
    with open(file_name) as f:
        for line in f:
            data = json.loads(line.strip())
            if "input" not in data:
                errors.append(f'Line {num}: No "input" entry.')
                continue
            err = validate_one_field(data["input"], "messages", {"system", "user"}, num)
            if err:
                errors.append(err)
            err = validate_one_field(data, "preferred_output", {"assistant"}, num)
            if err:
                errors.append(err)
            err = validate_one_field(data, "non_preferred_output", {"assistant"}, num)
            if err:
                errors.append(err)
            num += 1
    if errors:
        error_text = '\n'.join(errors)
        print(f"The errors were found:\n{error_text}", file=sys.stderr)
        exit(len(errors))
    else:
        print("All good")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate generated JSONL file.")
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="Path to the jsonl file.",
    )
    args = parser.parse_args()
    validate(args.file)
