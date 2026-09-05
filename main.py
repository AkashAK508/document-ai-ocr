from processing.document_processor import process_document
from search.keyword_search import search_document


def display_document(document):
    print("\n" + "=" * 70)
    print("DOCUMENT INFORMATION")
    print("=" * 70)
    print(f"PDF Name      : {document['name']}")
    print(f"Document Type : {document['type']}")
    print(f"Date / Year   : {document['date']}")
    print(f"Pages         : {document['pages']}")
    print(f"Blank Pages   : {document['blank_pages']}")
    print(f"Pattern Score : {document['score']}")
    if document["matched"]:
        print("Matched       : " + ", ".join(document["matched"]))


def main():
    print("=" * 70)
    documents = []
    print("\nAdd PDF documents one by one.")
    print("Type 'done' when finished.")

    while True:
        pdf_path = input("\nEnter PDF path: ").strip().strip('"')

        if pdf_path.lower() == "done":
            break

        if not pdf_path:
            print("Please enter a PDF path.")
            continue

        try:
            document = process_document(pdf_path)
            documents.append(document)

            print(f"\nAdded: {document['name']}")
            print(f"Recognized as: {document['type']}")

        except Exception as e:
            print(f"\nERROR: {e}")

    if not documents:
        print("\nNo documents added.")
        return

    print("\n\n")
    print("#" * 70)
    print("DOCUMENT SUMMARY")
    print("#" * 70)

    for document in documents:
        display_document(document)

    print("\n")
    print("#" * 70)
    print("SEARCH MODE")
    print("#" * 70)
    print("\nSearch across all uploaded documents.")
    print("You can enter multiple keywords separated by commas.")
    print("Example: GSTIN, PAN, IFSC, Invoice Number")
    print("Type 'exit' to close.")

    while True:
        query = input("\nEnter keyword(s): ").strip()

        if query.lower() in ["exit", "quit"]:
            print("\nClosing Document Reader.")
            break

        if not query:
            print("Keyword cannot be empty.")
            continue

        keywords = [keyword.strip() for keyword in query.split(",") if keyword.strip()]

        for keyword in keywords:
            print("\n" + "=" * 70)
            print(f"SEARCH RESULTS : {keyword}")
            print("=" * 70)
            found = False

            for document in documents:
                findings = search_document(document["pages_text"], keyword)

                if findings:
                    found = True
                    print(f"\nDocument : {document['name']}")
                    print(f"Type     : {document['type']}")

                    for finding in findings:
                        print(f"Page {finding['page']} : {finding['value']}")

            if not found:
                print(f"\nNo matches found for '{keyword}'.")


if __name__ == "__main__":
    main()