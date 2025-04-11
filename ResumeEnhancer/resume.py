import pandas as pd
import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"[ERROR] Failed to extract text from PDF: {e}")
    return text

def save_text_as_csv(text, output_path):
    lines = text.split('\n')
    df = pd.DataFrame(lines, columns=['Content'])
    df.to_csv(output_path, index=False)
    print(f"[INFO] Converted resume saved to: {output_path}")

def convert_sample_pdfs_to_csv(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            text = extract_text_from_pdf(pdf_path)
            csv_filename = os.path.splitext(filename)[0] + ".csv"
            output_path = os.path.join(output_folder, csv_filename)
            save_text_as_csv(text, output_path)

def main():
    input_folder = "ResumeSample"
    output_folder = "sample_resumes_csv"
    convert_sample_pdfs_to_csv(input_folder, output_folder)

if __name__ == "__main__":
    main()
