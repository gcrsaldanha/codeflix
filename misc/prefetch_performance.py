"""
Explanation

In Django, when you access a related field on a model, Django has to make a query to the database to fetch the related data, unless the data has been prefetched.

Without prefetch_related: If you have 100 genres and you try to access the related categories of each genre without using prefetch_related, Django will make a separate query to the database for each genre's categories. This results in what's known as the "N+1 query problem" (1 query to get all genres + N queries to get categories for each of the N genres). So, in this scenario, if you have 100 genres, you'll end up making 101 queries to the database.

With prefetch_related: Using prefetch_related tells Django to do a single additional query to get all the related data (in this case, all the categories for all the genres) at once and then cache it. This way, when you loop through each genre and access its related categories, Django doesn't need to make an additional query to the database because it uses the prefetched and cached data. So, in this scenario, you'll make only 2 queries to the database in total.

This difference in the number of database queries leads to a substantial performance improvement when using prefetch_related, especially when dealing with a large number of objects. Making fewer database queries means less time waiting for the database to return results and less overhead in database connection and data transmission.
"""
import random
import time

from django.db import connection

from core.category.infrastructure.django_app.models import Category
from core.genre.infrastructure.genre_django_app.models import Genre, GenreCategory


NUM_CATEGORIES = 10
NUM_GENRES = 100
NUM_CATEGORIES_PER_GENRE = 5


def measure_execution_time(func):
    """Decorator to measure the execution time of a function"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.5f} seconds")
        return result

    return wrapper


# Create Categories and Genres
def create_data():
    print(f"Creating {NUM_CATEGORIES} Categories and {NUM_GENRES} Genres...")
    categories = [
        Category(name=f"Category {i}", description=f"Description for Category {i}") for i in range(NUM_CATEGORIES)
    ]
    Category.objects.bulk_create(categories)

    genres = [Genre(name=f"Genre {i}", description=f"Description for Genre {i}") for i in range(NUM_GENRES)]
    Genre.objects.bulk_create(genres)

    # Link Genres with Categories randomly
    print(f"Linking Genres with Categories randomly...")
    genre_categories_to_create = []
    for genre in genres:
        for _ in range(
            random.randint(1, NUM_CATEGORIES_PER_GENRE)
        ):  # Assigning 1 to N categories randomly to each genre
            category = random.choice(categories)
            genre_categories_to_create.append(GenreCategory(genre=genre, category=category))

    GenreCategory.objects.bulk_create(genre_categories_to_create)


@measure_execution_time
def query_without_prefetch():
    genres = list(Genre.objects.all())
    for genre in genres:
        _ = list(genre.related_categories.all())  # This will cause a separate query for each genre


@measure_execution_time
def query_with_prefetch():
    genres = list(Genre.objects.prefetch_related("related_categories").all())
    for genre in genres:
        _ = list(genre.related_categories.all())  # This uses prefetched data


# Clear previous data (for a clean slate)
Category.objects.all().delete()
Genre.objects.all().delete()

create_data()

# Without prefetch_related
print("Executing without prefetch_related...")
connection.queries_log.clear()  # Clear previous queries
query_without_prefetch()
no_prefetch_queries = len(connection.queries)

# With prefetch_related
print("\nExecuting with prefetch_related...")
connection.queries_log.clear()  # Clear previous queries
query_with_prefetch()
with_prefetch_queries = len(connection.queries)

print(f"\nQueries executed without prefetch_related: {no_prefetch_queries}")
print(f"Queries executed with prefetch_related: {with_prefetch_queries}")

Category.objects.all().delete()
Genre.objects.all().delete()
