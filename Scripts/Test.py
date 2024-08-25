import os

def count_files(directory, extensions):
    png_count = 0
    pdf_count = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                png_count += 1
            elif file.lower().endswith('.pdf'):
                pdf_count += 1

    return png_count, pdf_count

directory = '/home/henry/Documents/Python/SmartCities'
png_count, pdf_count = count_files(directory, ['.png', '.pdf'])

print(f"Number of PNG files: {png_count}")
print(f"Number of PDF files: {pdf_count}")
