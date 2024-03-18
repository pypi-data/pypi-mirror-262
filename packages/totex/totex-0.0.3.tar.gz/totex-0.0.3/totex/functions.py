def table_to_tex(table):
    def _row_to_tex(row):
        return "  " + " & ".join(row)

    def _wrap_content(content, columns):
        header = "\\begin{tabular}{ " + "c " * columns + "}\n"
        footer = "\\end{tabular}\n"
        return header + content + '\n' + footer

    return _wrap_content(" \\\\\n".join(map(_row_to_tex, table)), len(table[0]))


def img_to_tex(img_path):
    return "\\includegraphics{" + img_path + "} \\\\\n"
