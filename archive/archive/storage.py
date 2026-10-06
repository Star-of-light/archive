"""Reading and writing the Archive file.

YOU IMPLEMENT THIS FILE.

The file format is CSV with no header row. One record per line, five fields
separated by commas, in this order:

    id,title,city,year,condition
    MS001,Tarikh al-Sudan,Timbuktu,1655,fragile

Remember Session 1: a file is one long line of characters. The comma
separates fields; the newline separates records. Nothing else is doing
any work.
"""

from archive.errors import MalformedRecordError

FIELD_NAMES = ["id", "title", "city", "year", "condition"]


def parse_line(line):
    """Turn one CSV line into a dict with the five FIELD_NAMES as keys.

    Whitespace around the line (including the trailing newline) is stripped.
    Field values are stripped too.

    If the line does not split into exactly 5 fields, raise
    MalformedRecordError. Do not guess, do not pad with blanks — a line with
    four fields is not a record with an empty one, it is a broken line, and
    the difference matters when you report it to whoever typed it.

    Returns dict.
    """
  class MalformedRecordError(Exception):
    pass

def parse_csv_line_to_dict(line: str, field_names: list) -> dict:
    stripped_line = line.strip()
    fields = stripped_line.split(',')
    if len(fields) != 5:
        raise MalformedRecordError(
            f"Expected exactly 5 fields, but found {len(fields)}. "
            f"Line content: '{stripped_line}'"
        )
    return {field_names[i]: fields[i].strip() for i in range(5)}



def load_archive(path):
    """Read the file at `path` and return (valid_records, rejected_lines).

    valid_records   list of dicts that passed validate_record
    rejected_lines  list of the ORIGINAL line strings that did not — either
                    because they were malformed, or because validation
                    rejected them

    A file that does not exist is not an error. It means the archive is new.
    Return ([], []) and DO NOT raise. Your program must start on a machine
    where nobody has saved anything yet.

    Blank lines are skipped silently.

    Returns (list, list).
    """
    valid_records = []
    rejected_lines = []
    
    if not os.path.exists(path):
        return [], []
        
    with open(path, "r") as f:
        for line in f:
            if not line.strip():
                continue
                
            try:
                record = parse_line(line)
                if validate_record(record): 
                    valid_records.append(record)
                else:
                    rejected_lines.append(line)
            except MalformedRecordError:
                rejected_lines.append(line)
                
    return valid_records, rejected_lines



def save_archive(path, records):
    """Write every record to `path` as CSV, one per line, no header.

    Field order is FIELD_NAMES. The file is overwritten, not appended to.

    Returns None.
    """
  with open(path, "w") as f:
        for record in records:
            row_values = [str(record[field]) for field in FIELD_NAMES]
            f.write(",".join(row_values) + "\n")













