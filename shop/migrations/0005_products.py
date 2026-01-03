from django.db import migrations


def create_products(apps, schema_editor):
    Product = apps.get_model("shop", "Product")
    if Product.objects.exists():
        return

    Product.objects.bulk_create(
        [
            Product(
                name="Product 1",
                description="Light daily vitality blend.",
                price="9.90",
                image="products/product.jpg",
            ),
            Product(
                name="Product 2",
                description="Bright focus support.",
                price="11.50",
                image="products/product.jpg",
            ),
            Product(
                name="Product 3",
                description="Calm balance formula.",
                price="7.40",
                image="products/product.jpg",
            ),
            Product(
                name="Product 4",
                description="Metabolic reset capsules.",
                price="8.60",
                image="products/product.jpg",
            ),
            Product(
                name="Product 5",
                description="Skin glow booster.",
                price="10.20",
                image="products/product.jpg",
            ),
        ]
    )


def remove_products(apps, schema_editor):
    Product = apps.get_model("shop", "Product")
    Product.objects.filter(
        name__in=[
            "Product 1",
            "Product 2",
            "Product 3",
            "Product 4",
            "Product 5",
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0004_remove_cart_user_cart_session_id"),
    ]

    operations = [
        migrations.RunPython(create_products, remove_products),
    ]
