import streamlit as st
from PIL import Image
import os
import requests
from bs4 import BeautifulSoup

def create_pdf_from_ipgs_flipbook_url(url, pdf_filename):
  """
  Creates a PDF from images extracted from a URL with the 'ipgs-flipbook' class.

  Args:
    url: The URL of the webpage containing the flipbook.
    pdf_filename: The name of the PDF file to be created.
  """

  try:
    # Fetch the webpage content
    response = requests.get(url)
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
        img_response = requests.get(image_url, stream=True)
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

if st.button("Create PDF"):
  if url:
    create_pdf_from_ipgs_flipbook_url(url, "output.pdf")

    # Provide a download link for the PDF
    with open("output.pdf", "rb") as pdf_file:
      st.download_button("Download PDF", data=pdf_file, file_name="output.pdf")
  else:
    st.warning("Please enter a URL.")