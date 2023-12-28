import random
from datetime import date, timedelta


def random_date(start_year, end_year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year + 1, 1, 1) - timedelta(days=1)

    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)

    return random_date


# Example usage for generating a random date between 1999 and 2002
start_year = 1999
end_year = 2002
random_generated_date = random_date(start_year, end_year)

print(
    "Random Date between {} and {}: {}".format(
        start_year, end_year, random_generated_date.strftime("%Y-%m-%d")
    )
)
