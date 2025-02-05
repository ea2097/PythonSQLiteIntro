class Formatter:
    @staticmethod
    def print_formatted(data):
        """
        Prints the data in a table-like format using dynamic column width.

        :param data: Cursor object containing query results
        """
        # Extract column names
        headers = [column[0] for column in data.description]

        # Fetch all rows
        rows = data.fetchall()

        # Raise exception if no rows are returned
        if not rows:
            raise Exception("No records found")

        # Determine column widths
        column_widths = [
            max(len(str(item)) for item in col) for col in zip(headers, *rows)
        ]

        # Define a row format string
        row_format = " | ".join(f"{{:<{w}}}" for w in column_widths)

        # Print the header row
        print()
        print("-" * (sum(column_widths) + (3 * (len(headers) - 1))))  # Separator line
        print(row_format.format(*headers))
        print("-" * (sum(column_widths) + (3 * (len(headers) - 1))))  # Separator line

        # Print each row
        for row in rows:
            # Replace None with empty string
            row = ["" if item is None else item for item in row]

            print(row_format.format(*row))
        print("-" * (sum(column_widths) + (3 * (len(headers) - 1))))  # Separator line
        # Print total number of rows
        print(f"Total rows: {len(rows)}")
        print("-" * (sum(column_widths) + (3 * (len(headers) - 1))))  # Separator line
