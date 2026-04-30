---
name: data-generation
description: Generate JSONL file based on set of .md files and split the data to train-valid-test sets default test and valid data set is 20% of all data. Inputs files are located in <md_folder>.
---
# Instruction

## Data generation
Read through the files in the <md_folder> folder and generate 1000 JSONL entries, which include
* Prompt (system role): You are a helpful assistant.
* Question (user role): "Who is Gnoll Fang of Ruin?"
* Correct answer (assistant role): "Medium humanoid (gnoll), chaotic evil"
* Incorrect answer (assistant role): "The servant of Emperor of Mankind."

Here is an example of JSONL file with two entries.
```JSON
{"input":{"messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is the chemical symbol for gold?"}]},"preferred_output":[{"role":"assistant","content":"The chemical symbol for gold is Au, from the Latin word 'aurum'."}],"non_preferred_output":[{"role":"assistant","content":"The chemical symbol for gold is Go."}]}
{"input":{"messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is the largest desert in the world?"}]},"preferred_output":[{"role":"assistant","content":"The Antarctic Desert is the largest desert in the world. If considering only hot deserts, the Sahara Desert is the largest."}],"non_preferred_output":[{"role":"assistant","content":"The Gobi Desert is the largest desert in the world."}]}
```

Only create entries based on data, contained in the provided .md files.

## Data validation
Run the validation script:

```powershell
python validate.py -f path/to/file.jsonl
```

```bash
python3 validate.py -f path/to/.jsonl
```

**Note:** The script will return "All good" if no errors, or will return non zero exit code and list all errors to the std.error. exit code will be the equal to the number of errors.

If the validation script returned errors, please correct the data file and run it again.

## Data split

To split the data run the script. Replace <test_fraction> by 0.2 or any other value if user provide any

```powershell
python split.py -f path/to/file.jsonl -s <test_fraction>
```

```bash
python3 split.py -f path/to/.jsonl -s <test_fraction>
```
