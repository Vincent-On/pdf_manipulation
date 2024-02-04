import PyPDF2
import tkinter as tk
import os
import fitz
from tkinter import filedialog


def compress_pdf(input_path):
    with open(input_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)

        base_name, ext = os.path.splitext(input_path)
        output_path = base_name + "_compressed" + ext

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return output_path


def merge_pdf(input_paths):
    merger = PyPDF2.PdfMerger()

    for input_path in input_paths:
        merger.append(input_path)

    base_name, ext = os.path.splitext(input_paths[0])
    output_path = f"{base_name}_merged{ext}"

    with open(output_path, 'wb') as output_file:
        merger.write(output_file)

    return output_path


def split_pdf(input_path):
    with open(input_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)

        for page_num in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[page_num])

            base_name, ext = os.path.splitext(input_path)
            output_path = f"{base_name}_{page_num + 1}{ext}"

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)


def rotate_pdf(input_path):
    with open(input_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page.rotate(90)
            writer.add_page(page)

        base_name, ext = os.path.splitext(input_path)
        output_path = f"{base_name}_rotated{ext}"

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)


def delete_pdf_pages(input_path, pages_to_delete):
    pages_to_delete_index = [page_num - 1 for page_num in pages_to_delete]

    with open(input_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            if page_num not in pages_to_delete_index:
                page = reader.pages[page_num]
                writer.add_page(page)

        base_name, ext = os.path.splitext(input_path)
        output_path = f"{base_name}_deleted{ext}"

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)


def extract_images(input_path, output_folder):
    with fitz.open(input_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            image_list = page.get_images(full=True)
            for image_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                with open(os.path.join(output_folder, f"page_{page_num + 1}_image_{image_index + 1}.{image_ext}"), 'wb') as image_file:
                    image_file.write(image_bytes)


def select_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path


def select_output_folder():
    output_folder = filedialog.askdirectory()
    return output_folder


def compress_pdf_gui():
    input_file = select_pdf_file()
    if input_file:
        compress_pdf(input_file)


def merge_pdf_gui():
    input_file = select_pdf_file()
    if input_file:
        merge_pdf(input_file)


def split_pdf_gui():
    input_file = select_pdf_file()
    if input_file:
        split_pdf(input_file)


def rotate_pdf_gui():
    input_file = select_pdf_file()
    if input_file:
        rotate_pdf(input_file)


def delete_pdf_gui(page_to_delete):
    input_file = select_pdf_file()
    page_int = [int(i) for i in page_to_delete]
    if input_file:
        delete_pdf_pages(input_file, page_int)


def extract_pdf_gui():
    input_file = select_pdf_file()
    output_folder = select_output_folder()
    if input_file:
        extract_images(input_file, output_folder)


def main():
    root = tk.Tk()
    root.title("SmallPDF Clone")

    frame = tk.Frame(root)
    frame.grid(row=0, column=0, padx=20, pady=20)

    # pages_to_delete_label = tk.Label(root, text="Pages to delete (comma separated):")
    # pages_to_delete_label.grid(row=0, column=1, padx=5, pady=5)
    # pages_to_delete_entry = tk.Entry(root)
    # pages_to_delete_entry.grid(row=0, column=2, padx=5, pady=5)

    compress_button = tk.Button(root, text="Compress PDF", command=compress_pdf_gui)
    compress_button.grid(row=0, column=0, padx=5, pady=5)

    merge_button = tk.Button(root, text="Merge PDF", command=merge_pdf_gui)
    merge_button.grid(row=0, column=1, padx=5, pady=5)

    split_button = tk.Button(root, text="Split PDF", command=split_pdf_gui)
    split_button.grid(row=0, column=2, padx=5, pady=5)

    rotate_button = tk.Button(root, text="Rotate PDF", command=rotate_pdf_gui)
    rotate_button.grid(row=0, column=3, padx=5, pady=5)

    # delete_button = tk.Button(root, text="Delete PDF", command=delete_pdf_gui(pages_to_delete_entry))
    # delete_button.grid(row=0, column=0, padx=5, pady=5)

    extract_button = tk.Button(root, text="Extract Images", command=extract_pdf_gui)
    extract_button.grid(row=0, column=4, padx=5, pady=5)

    root.mainloop()


if __name__ == '__main__':
    main()
