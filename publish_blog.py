import sys
import os
import argparse
from generate_html import generate_html
from publish_utils import publish_blog, publish_metadata

# Add project to sys path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
client_src_path = os.path.join(root_path, "data-gluons-client")
sys.path.insert(0, client_src_path)

from src import create_app, db

def publish_from_file(file_path, dry_run=False, metadata_only=False):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return

    metadata, html = generate_html(file_path)

    if metadata_only:
        try:
            publish_metadata(metadata, db)
        except Exception as e:
            print(f"Could not publish metadata: {e}")
    else:
        if metadata.get("published"):
            publish_blog(metadata, html, db, dry_run=dry_run)
        else:
            publish_metadata(metadata, db)

# ---- CLI setup ---- #
parser = argparse.ArgumentParser(description="Publish a blog post to the database")

parser.add_argument("-f", "--file", type=str, help="Path to the markdown file")
parser.add_argument("--dry-run", action="store_true", help="Only generate HTML")
parser.add_argument("-m", "--metadata-only", action="store_true", help="Publish metadata only")
parser.add_argument("-a", "--all", action="store_true", help="Publish all articles in /content")

args = parser.parse_args()

# ---- App context ---- #
app = create_app()

with app.app_context():
    if args.metadata_only and args.dry_run:
        print("--dry-run has no effect when --metadata-only is used.")

    if args.all:
        content_dir = "content"
        files = [
            os.path.join(content_dir, f)
            for f in os.listdir(content_dir)
            if f.endswith(".md") and not (f.startswith(".") or f.startswith('sample'))
        ]

        for file in files:
            publish_from_file(file, dry_run=args.dry_run, metadata_only=args.metadata_only)

    elif args.file:
        publish_from_file(args.file, dry_run=args.dry_run, metadata_only=args.metadata_only)

    else:
        print("Please provide either --file or --all")
        parser.print_help()
        sys.exit(1)
