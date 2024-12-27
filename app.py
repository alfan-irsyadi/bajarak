import streamlit as st
from PIL import Image
import os
import requests
from bs4 import BeautifulSoup

def create_pdf_from_ipgs_flipbook_url(url, pdf_filename, headers=None):
  """
  Creates a PDF from images extracted from a URL with the 'ipgs-flipbook' class.

  Args:
    url: The URL of the webpage containing the flipbook.
    pdf_filename: The name of the PDF file to be created.
    headers: (Optional) Dictionary of headers to include in the request.
  """

  try:
    # Fetch the webpage content with custom headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div with the 'ipgs-flipbook' class
    flipbook_div = soup.find('div', class_='ipgs-flipbook')
    if not flipbook_div:
      st.error("No element with 'ipgs-flipbook' class found on the webpage.")
      return

    # Extract image URLs from the data-ipgs-image attributes
    image_urls = [img['data-ipgs-image'] for img in flipbook_div.find_all('img', attrs={'data-ipgs-image': True})]

    if not image_urls:
      st.error("No images found in the 'ipgs-flipbook' element.")
      return

    # Download and open images using Pillow
    images = []
    for image_url in image_urls:
      try:
        img_response = requests.get(image_url, stream=True, headers=headers)
        img_response.raise_for_status()
        img = Image.open(img_response.raw)
        images.append(img)
      except Exception as e:
        st.warning(f"Failed to download or open image from {image_url}: {e}")

    # Save images as a PDF
    if images:
      images[0].save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
      st.success(f"PDF created successfully: {pdf_filename}")
    else:
      st.error("No images successfully downloaded to create PDF.")

  except requests.exceptions.RequestException as e:
    st.error(f"Error fetching webpage: {e}")

# Streamlit app
st.title("IPGS Flipbook to PDF Converter")

url = st.text_input("Enter the URL of the webpage containing the flipbook:")

# Define the headers from the curl request
headers = {
    'authority': 'emodul.bimbelnurulfikri.id',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImRQM2tJYzhtNTRLZUZnaEp5ZGVhb1E9PSIsInZhbHVlIjoiVTE0WTNPNjl1ZlFzM3NtblhZSWdNQVVMVjV2N1BqdVJmM2owS0VlTi9iL3NnWFRKUzJETkFQd2V5a2pTL1pVQU15VFhxYkNZMzcraEc0SUpIZ1VwOEZZWnk2YnhlU0s2aGRnNmFwdVAyMkVVM0FmVTB6c0lxOTRuRUExcGNkQjd3R0FoUVJOdFhQcnZueWdybjlGN2tTTk1jUHk3UEdycGdoc2NnL09tclZoL2ZrSW12OEc1TUFPbFhrTi9rWEk1d3IyQkNzQWJMT2tWbzQ3bi9TTkN0MEdoUTJodFhxK2IvM1pweUx6eHYzcz0iLCJtYWMiOiI1MTJjODlkNWI2YzRmNTU3NmRmMTdkZDA4ZjAxMTJkYzFiMThhZDlkOWE2NzM5MDlhMTJkY2RlOGRhMzkzZWFhIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6ImpXcENmcWJUdGR2T3hEUWVhb3dsQVE9PSIsInZhbHVlIjoiR3VSbnFuWU8zVFcwZHo0bEkwYW9yN1dlNTJhM3ZIZFJSeEF6SjVnbC9DaHl5bFNvUWd1K3pQSGt5R3lMWXpNWjFTNmJJdTM3YVhZNXcwWGxLelcvTDFIREZiMlJ2T0hsTHhFQnNLL29WWjJybmNJelFxYzVEdEpBeHV2ejBlUXUiLCJtYWMiOiI5YWZmYzVmZTM1Mzc5MzY4ODJkZDhiYzUyZGZjNjkzNmE1YzA5NWQ1NzgzYzg5YTFkYmJhMDg3NjlhNWRkYWI2IiwidGFnIjoiIn0%3D; sip_v3_session=eyJpdiI6IkJXaHpPZDQ5UFVHdSs1c3VvUGtxdHc9PSIsInZhbHVlIjoiNWdwQjhBOWowRG42K2ZtZ1dYY1lZcFZLVDBEazZhV25teEkyZEF5Rlc4MndOK1V4a1RpLzcwcU5ZNkhMa3hWbFhEd3NpQ1hxVVBuQlBPS25VdTg5ZVFkaG9iYjd1Mjcza0pldzRXdG9vVzF2YkFJVkp0ZlNTWUV2bEpjZ0VzZ3IiLCJtYWMiOiJlMmY2OGQ1MDc3ZTc4MjI0ZDdmMzkzMWI4Mzg2ZmI5OTljOTdjMjM0MmMzMjRhOWY0NGRiYzBiNmU5OGQ4YzI2IiwidGFnIjoiIn0%3D',
    'referer': 'https://emodul.bimbelnurulfikri.id/belajar/bajarak',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

if st.button("Create PDF"):
  if url:
    create_pdf_from_ipgs_flipbook_url(url, "output.pdf", headers=headers)

    # Provide a download link for the PDF
    with open("output.pdf", "rb") as pdf_file:
      st.download_button("Download PDF", data=pdf_file, file_name="output.pdf")
  else:
    st.warning("Please enter a URL.")