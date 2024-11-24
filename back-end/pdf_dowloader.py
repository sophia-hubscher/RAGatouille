#!/usr/bin/env python3
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def download_pdf(url, output_dir):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            if 'application/pdf' in content_type:
                filename = os.path.join(output_dir, url.split('/')[-1])
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Downloaded: {filename}")
            else:
                print(f"Not a PDF: {url}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def get_pdf_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        pdf_links = []
        for link in links:
            href = link.get('href')
            if href and href.lower().endswith('.pdf'):
                full_url = urljoin(url, href)
                pdf_links.append(full_url)
        return pdf_links
    except Exception as e:
        print(f"Error fetching links from {url}: {str(e)}")
        return []

def main():
    urls = [
        "https://www.iso-ne.com/participate/rules-procedures/tariff",
        "https://www.iso-ne.com/participate/rules-procedures/manuals",
        "https://www.iso-ne.com/participate/rules-procedures/operating-procedures",
        "https://www.iso-ne.com/participate/rules-procedures/system-operating-procedures",
        "https://www.iso-ne.com/participate/rules-procedures/master-lcc-procedures",
        "https://www.iso-ne.com/participate/rules-procedures/generator-nongenerator-var-capability",
        "https://www.iso-ne.com/participate/rules-procedures/planning-procedures",
        "https://www.nerc.com/Pages/default.aspx"
    ]

    base_output_dir = "downloaded_pdfs"

    for url in urls:
        print(f"Processing: {url}")
        domain = urlparse(url).netloc
        output_dir = os.path.join(base_output_dir, domain)
        os.makedirs(output_dir, exist_ok=True)

        pdf_links = get_pdf_links(url)
        for pdf_url in pdf_links:
            download_pdf(pdf_url, output_dir)
            time.sleep(3)

        print(f"Finished processing: {url}")
        print("---")

if __name__ == "__main__":
    main()
