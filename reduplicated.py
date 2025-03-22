import json

def remove_duplicates(input_file, output_file, key_field="instruction"):
    """
    Remove duplicate entries from a JSONL file based on specified key field
    
    Args:
        input_file (str): Path to input JSONL file
        output_file (str): Path for deduplicated output file
        key_field (str): Field to use for duplicate detection (default: "instruction")
    """
    
    seen = set()
    duplicates_removed = 0

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            try:
                entry = json.loads(line)
                key_value = entry.get(key_field)
                
                if key_value and key_value not in seen:
                    seen.add(key_value)
                    outfile.write(line)
                else:
                    duplicates_removed += 1
                    
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")

    print(f"Finished processing. Removed {duplicates_removed} duplicates.")
    print(f"Unique entries remaining: {len(seen)}")

# Usage - replace with your actual file paths
remove_duplicates(
    input_file="train.jsonl",
    output_file="trainV2.jsonl",
    key_field="instruction"  # Change to "output" if needed
)