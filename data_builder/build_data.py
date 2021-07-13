from data_builder_utils.data_builder import download_freddie_data, unzip_directory

"""
Quick script to download and format data from Freddie Mac (upload speed seems slow).
This script requires a PHP session token that is already auth'd into Freddie Mac's website.
In addition, a directory for the downloads to go to is required.
"""


def main():
    cookie = "PHP session token for Freddie Mac auth"
    directory = 'Directory for download'
    download_freddie_data(cookie, directory)

    # There are nested zip'd folders. The for loop will unzip each layer.
    for i in range(3):
        unzip_directory(directory)


if __name__ == '__main__':
    main()

