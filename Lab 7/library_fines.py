def parse_member_id(member_id):
    if not isinstance(member_id, str) or len(member_id) > 100:
        return None
    parts = member_id.strip().split('-')
    if len(parts) != 2:
        return None
    member_type, number = parts[0].strip(), parts[1].strip()
    if not (member_type.isascii() and member_type.isalpha()):
        return None
    if not (number.isascii() and number.isdigit()):
        return None
    return member_type.upper(), int(number)

def total_fine(days_csv):
    if not isinstance(days_csv, str) or len(days_csv) > 10000:
        return None
    if days_csv.strip() == "":
        return 0
    fine = 0
    for item in days_csv.split(','):
        item = item.strip()
        if not (item.isascii() and item.isdigit()) or len(item) > 9:
            return None
        d = int(item)
        if d > 14:
            fine += (d - 14) * 2
    return fine

def shelf_code(title):
    if not isinstance(title, str):
        return None
    words = title.split()
    if len(words) < 2:
        return None
    return (words[0][0] + words[1][0]).upper()

def main():
    print("==== Running parse_member_id ====")
    result = parse_member_id(input("Enter a member ID (e.g. STU-1023): "))
    print("Member Type and Number:", result if result is not None else "Invalid member ID")

    print("\n==== Running total_fine ====")
    result = total_fine(input("Enter days kept for each book as CSV (e.g. 10,20,30): "))
    print("Total Fine:", result if result is not None else "Invalid input")

    print("\n==== Running shelf_code ====")
    result = shelf_code(input("Enter a book title with at least two words: "))
    print("Shelf Code:", result if result is not None else "Invalid title")

if __name__ == "__main__":
    main()
