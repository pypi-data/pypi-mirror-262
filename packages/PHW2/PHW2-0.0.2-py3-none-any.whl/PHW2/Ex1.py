def latex_table(matrix):
    def longest_list(matrix):
        return max(len(lis) for lis in matrix)

    def fill_empty_elements(matrix):
        longest_l = longest_list(matrix)
        for i in range(len(matrix)):
            for j in range(longest_l - len(matrix[i])):
                matrix[i].append("")
        return matrix
    # print(fill_empty_elements(matrix))
    def list_to_table_string(lis):
        string_code = "\hline\n"
        for element in lis:
            string_code += (str(element) + " & ")
        string_code = string_code[:-2]
        string_code += ("\\" + "\\\n")
        return string_code

    latex_code = "\documentclass{article}\n\\begin{document}\n\\begin{center}\n"
    matrix = fill_empty_elements(matrix)
    number_of_columns = len(matrix[0])
    # print(number_of_columns)
    latex_code += ("\\begin{tabular}{ |" + "c|" * number_of_columns + " }\n")
    # print(latex_code)
    # print(list_to_table_string(matrix[0]))
    for line in matrix:
        latex_code += list_to_table_string(line)
    latex_code += "\hline\n\end{tabular}\n\end{center}\n\end{document}"
    # latex_code += "\end{tabular}\n"
    # latex_code += "\end{center}\n"
    return latex_code


if __name__ == "__main__":
    m = [[1, 5, 3, 5], [2, 5], ["dgsvfv", 34.2345, "dfefeef", "sdgdfngf", 2345678, 34356]]
    print(latex_table(m))
