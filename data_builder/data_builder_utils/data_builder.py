def download_freddie_data(cookie: str, directory: str):
    """
    Downloads loan level data set for standard and non-standard loans from Freddie Mac.
    :param cookie: A php session id to allow auth.
    :param directory: The directory to save all the data.
    :return: None
    """
    import re
    import requests
    from bs4 import BeautifulSoup

    base_url = 'https://freddiemac.embs.com/FLoan/Data/downloadA.php'
    with requests.Session() as s:
        response = s.post(base_url
                          , headers={'Cookie': cookie})  # using temp cookie for auth
        soup = BeautifulSoup(response.text)

        for url in soup.find_all('a'):
            download_url = url.get('href')
            local_filename = (re.search('(?<=\?)(.*?)(?=\&)', download_url)).group()

            if str(download_url).find('=historical') == -1:
                continue
            else:
                with s.get('https://freddiemac.embs.com/FLoan/Data/' + download_url
                           , stream=True
                           , headers={'Cookie': 'PHPSESSID=eteuarnhl0slk0gug92030lob2'}) as dl_response:
                    with open(f'{directory}{local_filename[2:]}.zip', 'wb') as file:
                        for chunk in dl_response.iter_content(chunk_size=1_000_000_000):
                            file.write(chunk)


def unzip_contents(content, byte=True):
    """
    unzips a file/folder.
    :param content: compressed contents as a byte or string,
    :param byte:
    :return: unzipped data.
    """
    import gzip

    from io import BytesIO, StringIO
    if byte:
        compressed_data = BytesIO(content)
    else:
        compressed_data = StringIO(content)

    decoded_data = []
    for data in gzip.GzipFile(fileobj=compressed_data):
        decoded_data.append(data)

    return decoded_data


def unzip_directory(directory):
    import zipfile
    import fnmatch
    import os

    pattern = '*.zip'
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            print(os.path.join(root, filename))
            zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))


if __name__ == '__main__':
    pass