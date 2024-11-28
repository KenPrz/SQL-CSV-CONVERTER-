import re
import csv

def parse_create_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.read()

    # Extract table name
    table_name_match = re.search(r"CREATE TABLE\s+`?(\w+)`?\s*\(", lines, re.IGNORECASE)
    table_name = table_name_match.group(1) if table_name_match else "UnknownTable"

    # Find primary keys
    primary_key_match = re.search(r"PRIMARY KEY\s*\(([^)]+)\)", lines, re.IGNORECASE)
    primary_keys = set()
    if primary_key_match:
        primary_keys = {col.strip(' `') for col in primary_key_match.group(1).split(",")}

    # Match column definitions
    column_pattern = re.compile(
        r"`(?P<name>[^`]+)`\s+(?P<type>\w+)(?:\((?P<length>[^\)]+)\))?"
        r"(?:\s+(?P<null>NOT NULL|NULL))?(?:\s+DEFAULT\s+(?P<default>[^,]+))?"
        r"(?:\s+(?P<extra>.*?))?(?:,|\))",
        re.IGNORECASE
    )

    columns = []
    for match in column_pattern.finditer(lines):
        column_name = match.group("name")
        column_info = {
            "Column Name": column_name,
            "Data Type": match.group("type"),
            "Length": match.group("length"),
            "Primary Key": "◯" if column_name in primary_keys else "",
            "Allow NULL": "YES" if match.group("null") != "NOT NULL" else "NO",
            "Default Value": match.group("default"),
            "Extra": match.group("extra").strip() if match.group("extra") else "",
        }
        columns.append(column_info)

    return table_name, columns

def save_to_csv(table_name, columns, output_path):
    csv_file = f"{output_path}/{table_name}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Column Name", "Data Type", "Length", "Primary Key", "Allow NULL", "Default Value", "Extra"])
        writer.writeheader()
        writer.writerows(columns)

    print(f"CSV saved as {csv_file}")

# Main function
def main():
    # Replace with your input file path could be a .sql file or a .txt file 
    #as long as it contains the CREATE TABLE statement
    input_file = "input.sql"  
    output_path = "."  # Replace with your desired output directory

    table_name, columns = parse_create_table(input_file)
    save_to_csv(table_name, columns, output_path)

if __name__ == "__main__":
    main()
