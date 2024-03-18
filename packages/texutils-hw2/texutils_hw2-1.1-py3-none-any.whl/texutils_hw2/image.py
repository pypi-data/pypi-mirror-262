def image_to_tex(image_path: str):
    image_tex_formatted = "{" + image_path + "}"
    image_template = r"\includegraphics[scale=0.2]{0}"
    return image_template.format(image_tex_formatted)
