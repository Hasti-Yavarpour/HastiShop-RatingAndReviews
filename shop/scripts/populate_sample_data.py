from shop.models import Brand, Category, SubCategory, Color, Unit, Material, Product, Image

# Brands
kalekim = Brand.objects.create(name="Kalekim")
mapei = Brand.objects.create(name="Mapei")

# Categories
chemicals = Category.objects.create(name="Construction Chemicals")

# Subcategories
tile_adhesive = SubCategory.objects.create(name="Tile Adhesive", category=chemicals)

# Colors
white = Color.objects.create(name="White")
gray = Color.objects.create(name="Gray")

# Units
kg = Unit.objects.create(name="kg")
bag = Unit.objects.create(name="bag")

# Materials
cement_based = Material.objects.create(name="Cement-based")

# Products
product1 = Product.objects.create(
    name="Kalekim 1054 Tile Adhesive",
    brand=kalekim,
    category=chemicals,
    subcategory=tile_adhesive,
    color=gray,
    unit=bag,
    material=cement_based,
    price=189.99,
    stock=150,
    delivery_time="2-3 business days"
)

product2 = Product.objects.create(
    name="Mapei Keraflex Maxi S1",
    brand=mapei,
    category=chemicals,
    subcategory=tile_adhesive,
    color=white,
    unit=bag,
    material=cement_based,
    price=209.99,
    stock=100,
    delivery_time="1-2 business days"
)

# Images (URLs just for demonstration)
Image.objects.create(product=product1, image_url="https://example.com/kalekim1054.jpg")
Image.objects.create(product=product2, image_url="https://example.com/keraflex.jpg")
