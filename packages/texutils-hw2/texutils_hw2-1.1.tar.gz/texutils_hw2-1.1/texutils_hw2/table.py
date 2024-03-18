from typing import List, Any

### \documentclass{{article}}
### \begin{{document}}
### \end{{document}}
TABLE_DRAFT = r"""
\begin{{center}}
\begin{{tabular}}{0}
\hline
{1}
\end{{tabular}}
\end{{center}}"""


def list_to_table(table: List[List[Any]]):
    n_cells = len(table[0])
    cells_line = "{ | " + "c | " * n_cells + "}"

    rows = []

    for row in table:
        tex_row = " & ".join(str(el) for el in row)
        tex_row = rf"{tex_row} \\ \hline"
        rows.append(tex_row)

    return TABLE_DRAFT.format(cells_line, "\n".join(rows))
