import argparse

parser = argparse.ArgumentParser(description="Scrape Instagram!")
parser.add_argument("-u", "--username", help="Instagram username")
parser.add_argument("--url", help="Download single post from given url")
parser.add_argument("-t", "--tag", help="Download posts containing only this tags")
parser.add_argument("-d", "--detail", action="store_true", help="Save posts along with their information")
parser.add_argument("-p", "--photos", action="store_true", help="Download photos only")
parser.add_argument("-v", "--videos", action="store_true", help="Download videos only")

args = parser.parse_args()
