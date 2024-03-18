from PIL import Image

def generate_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    max_width = 400
    scale_factor = min(1.0, max_width / float(width))
    latex_code = ("\documentclass{book}\n\\usepackage{graphicx}\n\\begin{document}\n\\mainmatter\n\\begin{figure}[h]\n"
                  "\\centering\n" + f"\\includegraphics[scale={scale_factor}]{{{image_path}}}\n" + "\\end{figure}\n\\end{document}")
    return latex_code

if __name__ == "__main__":
    example_image_path = "example_image_4.png"
    latex_image = generate_image(example_image_path)
    print(latex_image)

