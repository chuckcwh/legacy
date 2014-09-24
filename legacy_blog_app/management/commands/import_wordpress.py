import csv
from django.core.management import BaseCommand
from legacy_blog_app.models import Author, Post, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Open the file and loop through each line
        with open('wordpress_export.csv', 'rb') as file:
            for index, row in enumerate(csv.reader(file)):
                if index == 0:
                    continue

                # Create the author from the row
                author, author_created = Author.objects.get_or_create(name=row[3])

                # Create the post for the row
                post, post_created = Post.objects.get_or_create(author=author, title=row[1], body=row[3])

                if post_created:
                    # Create the tags for the row
                    tags = row[4].split(";")
                    for tag in tags:
                        tag, tag_created = Tag.objects.get_or_create(name=tag)

                    # Add the tags to the post
                        post.tags.add(tag)

        print "We have {} authors in our db".format(Author.objects.count())
        print "We have {} posts in our db".format(Post.objects.count())
        print "We have {} tags in our db".format(Tag.objects.count())