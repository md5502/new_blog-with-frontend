from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Tag, Comment
from user.models import UserProfile
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for your models and users'

    def handle(self, *args, **options):
        # Generate fake users and profiles
        for _ in range(4):
            username = fake.unique.user_name()
            email = fake.unique.email()
            password = "1qaz!QAZtest5502"
            
            # Check if a user with the same username or email already exists
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()

                profile = UserProfile.objects.get(user=user)
                profile.name=username,
                profile.email=email,
                profile.bio=fake.text(),
                profile.website=fake.url(),
                profile.twitter_username=fake.user_name(),
                profile.instagram_username=fake.user_name(),
                profile.facebook_profile=fake.url(),
                profile.linkedin_profile=fake.url(),
                profile.save()
        # Generate fake tags
        for _ in range(5):
            Tag.objects.create(name=fake.unique.word())

        # Generate fake posts and comments
        for _ in range(50):
            user_profile = random.choice(UserProfile.objects.all())
            title = fake.sentence()
            body = ""
            for _ in range(random.randint(20, 35)):
                body += '\n' + fake.paragraph() + '\n'
            status = random.choice(['P', 'D'])
            post = Post.objects.create(
                title=title,
                body=body,
                owner=user_profile,
                status=status,
            )

            # Add random tags to the post
            tags = random.sample(list(Tag.objects.all()), random.randint(1, 3))
            post.tags.set(tags)

            # Generate comments for the post
            for _ in range(random.randint(1, 5)):
                Comment.objects.create(
                    body=fake.paragraph(),
                    post=post,
                )

        self.stdout.write(self.style.SUCCESS('Fake data has been generated successfully.'))
