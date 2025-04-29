import sys
import os
from generate_html import generate_html
from datetime import datetime, timezone

## Set Path for Client

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
client_src_path = os.path.join(root_path, "data-gluons-client")
sys.path.insert(0, client_src_path)

## import from sys path
from src.models.blog import BlogMetadata, BlogContent


def publish_metadata(metadata, db):

    blog = BlogMetadata.query.filter_by(slug=metadata['slug']).first()

    if blog:
        print(f"Updating metadata for {metadata['title']}")
        blog.title = metadata['title']
        blog.slug = metadata['slug']
        blog.description = metadata['description']
        blog.author = metadata['author']
        blog.tags = metadata['tags']
        blog.date = datetime.now(timezone.utc)
        blog.published = metadata['published']
    else:
        blog = BlogMetadata(
            title=metadata["title"],
            slug=metadata["slug"],
            description=metadata["description"],
            author=metadata["author"],
            tags=metadata["tags"],
            date=metadata["date"],
            published=metadata["published"],
            )
        
        db.session.add(blog)

    try:
        db.session.commit()
        print(f"Metadata {blog.title} has been published to the database")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding blog {blog.title} to the database: {e}")



def publish_content(metadata, html, db):
    
    blog_metadata = BlogMetadata.query.filter_by(slug=metadata['slug']).first()

    if not blog_metadata:
        print(f"no metdata for {metadata['slug']}")
        return

    ## get latest version if version exists
    latest = (BlogContent.query.filter_by(metadata_id=blog_metadata.id).order_by(BlogContent.version.desc()).first())
    version = latest.version + 1 if latest else 1

    ## turn off all previous active ones
    BlogContent.query.filter_by(metadata_id=blog_metadata.id, active=True).update({"active":False})

    new_content = BlogContent(
        metadata_id=blog_metadata.id,
        content=html,
        version=version,
        active=True,
    )

    try:
        db.session.add(new_content)
        db.session.commit()
        print(f"Blog Content {new_content.blog_metadata.title} has been added to the database")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding blog {new_content.blog_metadata.title} to the database: {e}")



def publish_blog(metadata, html, db, dry_run=False):
    if dry_run:
        print("DRY RUN MODE")
        with open(f"{metadata['slug']}.html","w") as f:
            f.write(html)
        print(f"Dry run complete, HTML file saved as {metadata['slug']}.html")
    else:
        publish_metadata(metadata, db)
        publish_content(metadata, html, db)
        db.session.close()



