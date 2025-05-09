from io import TextIOWrapper


class MyCSVParser:
    @staticmethod
    def to_json(csv_file: TextIOWrapper) -> list[dict[str, str]]:
        result: list = list()
        col_count: int = 0
        values: list = list()

        while not csv_file.closed and csv_file.readable():
            line = csv_file.readline().strip()
            if not line:
                break

            line_values = line.split(',')
            if not col_count:
                col_count = len(line_values)
            values.append(line_values)

        for row_i in range(1, len(values)):
            result.append(
                {
                    values[0][col_i]: values[row_i][col_i]
                    for col_i in range(col_count)
                }
            )

        return result
