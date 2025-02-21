from django.core.management.base import BaseCommand
from core.utils import convert_naira_to_kobo
from core.models import Product
import os
import csv

# Since there is a header row, and then offset the zero-indexing
INDEX_OFFSET = 2


class Command(BaseCommand):
    help = "Import product data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="Path to the CSV file containing product data"
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        print(f"Importing product data from {csv_file}")

        # Check if file exists
        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        # Open the CSV file and import data
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            products_to_create = []

            for index, row in enumerate(reader):
                try:
                    name = row["name"].strip()
                    description = row.get("description", "").strip()
                    price = convert_naira_to_kobo(int(row["price"]))
                    available_quantity = int(row["available_quantity"])

                    product = Product(
                        name=name,
                        description=description,
                        price=price,
                        available_quantity=available_quantity,
                    )

                    products_to_create.append(product)

                except (KeyError, ValueError) as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Skipping product on line {index + INDEX_OFFSET} due to error: {e}"
                        )
                    )

            # Bulk create products
            Product.objects.bulk_create(products_to_create)

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(products_to_create)} new products successfully!"
            )
        )
