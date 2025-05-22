from django.shortcuts import render
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.core.mail import mail_admins
from .models import Product, Material, Category, Brand, ProductReview
from .utils import normalize_text, suggest_correction
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

def shop_home(request):
    return HttpResponse("Welcome to the Shop App!")

def home_view(request):
    return render(request, 'shop/home.html')

def product_list(request):
    query = request.GET.get('q', '')
    normalized_query = normalize_text(query)

    products = Product.objects.all()

    if normalized_query:
        products = products.filter(
            Q(name__icontains=normalized_query) |
            Q(brand__name__icontains=normalized_query)
        )

    brands = request.GET.getlist('brand')
    if brands:
        products = products.filter(brand__name__in=brands)

    categories = request.GET.getlist('category')
    if categories:
        products = products.filter(category__name__in=categories)

    materials = request.GET.getlist('material')
    if materials:
        products = products.filter(material__name__in=materials)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    in_stock = request.GET.get('in_stock')
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_low_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')

    suggestion = None
    if not products.exists() and normalized_query:
        names = list(Product.objects.values_list('name', flat=True))
        brands_list = list(Product.objects.values_list('brand__name', flat=True))
        materials_list = list(Product.objects.values_list('material__name', flat=True))

        all_words = set()
        for term in names + brands_list + materials_list:
            if term:
                for word in term.split():
                    all_words.add(normalize_text(word))

        suggestion = suggest_correction(normalized_query, list(all_words))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('shop/partials/product_list_partial.html', {
            'products': products,
        })
        return JsonResponse({'html': html})

    return render(request, 'shop/product_list.html', {
        'products': products,
        'query': query,
        'suggestion': suggestion,
        'selected_brands': brands,
        'selected_categories': categories,
        'selected_materials': materials,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'sort_by': sort_by,
        'all_brands': Brand.objects.all(),
        'all_categories': Category.objects.all(),
        'all_materials': Material.objects.all(),
    })

# ---------------------- Rating API Views ----------------------

@csrf_exempt
def submit_review(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating = int(data.get('rating', 0))
            comment = data.get('comment', '').strip()

            if rating < 1 or rating > 5:
                return JsonResponse({'error': 'Invalid rating value.'}, status=400)

            review = ProductReview.objects.create(
                product_id=product_id,
                rating=rating,
                comment=comment,
                approved=False
            )

            mail_admins(
                subject=f"📝 New review for {review.product.name}",
                message=f"Rating: {rating}\nComment: {comment}\nReview ID: {review.id}\nVisit admin panel to approve."
            )

            return JsonResponse({'message': 'Thank you for your review!'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def get_reviews(request, product_id):
    reviews = ProductReview.objects.filter(product_id=product_id, approved=True).order_by('-created_at')[:5]
    data = [{
        'rating': r.rating,
        'comment': r.comment,
        'time_ago': timesince(r.created_at, now()) + " ago"
    } for r in reviews]
    return JsonResponse({'reviews': data})

def get_average_rating(request, product_id):
    reviews = ProductReview.objects.filter(product_id=product_id, approved=True)
    avg = round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 1)
    count = reviews.count()
    return JsonResponse({'average': avg, 'count': count})

def get_rating_distribution(request, product_id):
    reviews = ProductReview.objects.filter(product_id=product_id, approved=True)
    total = reviews.count()

    distribution = reviews.values('rating').annotate(count=Count('rating'))
    star_counts = {i: 0 for i in range(1, 6)}
    for entry in distribution:
        star_counts[entry['rating']] = entry['count']

    percentages = {star: (count / total * 100 if total > 0 else 0) for star, count in star_counts.items()}
    average = round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 1)

    return JsonResponse({
        'distribution': percentages,
        'counts': star_counts,
        'total': total,
        'average': average
    })

@staff_member_required
def review_moderation(request):
    pending_reviews = ProductReview.objects.filter(approved=False).order_by('-created_at')
    return render(request, 'shop/review_moderation.html', {
        'reviews': pending_reviews
    })

@require_POST
@staff_member_required
def approve_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)
    review.approved = True
    review.save()
    return JsonResponse({'message': '✅ Review approved.'})

@require_POST
@staff_member_required
def delete_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)
    review.delete()
    return JsonResponse({'message': '🗑️ Review deleted.'})
