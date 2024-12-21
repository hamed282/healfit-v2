from product.models import ProductCategoryModel, ProductSubCategoryModel
from blog.models import BlogCategoryModel


def sitemap():

    cate = {}
    categories = ProductCategoryModel.objects.all()
    for category in categories:
        cat = category.category_title
        subcategories = ProductSubCategoryModel.objects.filter(category=category)
        subcat = {}
        for subcategory in subcategories:
            sub = subcategory.subcategory_title
            subcat[sub] = {'slug': subcategory.slug}
        cate[cat] = {'data': subcat, 'slug': category.slug}

    blogs = BlogCategoryModel.objects.all()
    blog = [{'category': blg.category, 'slug': blg.slug} for blg in blogs]

    company = [{'name': 'Company', 'slug': '#', 'data': [{'name': 'About Us', 'slug': 'about'},
                                                         {'name': 'Careers', 'slug': 'about'},
                                                         {'name': 'FAQ', 'slug': '#'}]}]

    customer_service = [{'name': 'Customer Service', 'slug': '#', 'data': [{'name': 'Customer Care', 'slug': '#'},
                                                                           {'name': 'Wholesale Inquiry', 'slug': '#'},
                                                                           {'name': 'Return & Refund Policy', 'slug': '#'}]}]

    legal = [{'name': 'Legal', 'slug': '#', 'data': [{'name': 'GTC (General Terms & Cond.)', 'slug': '#'},
                                                     {'name': 'Payment', 'slug': '#'},
                                                     {'name': 'Delivery', 'slug': '#'},
                                                     {'name': 'Privacy-Policy', 'slug': '#'}]}]

    customer = [{'name': 'Customer', 'slug': '#', 'data': [{'name': 'Login', 'slug': '#'},
                                                         {'name': 'Account', 'slug': '#'},
                                                         {'name': 'Create/Register', 'slug': '#'}]}]

    contact = [{'name': 'Contact', 'slug': 'contact'}]

    data = {
        'Home': {'name': 'Home Page', 'slug': ''},
        'Products': {'name': 'Products', 'data': cate, 'slug': 'shop'},
        'Blog': {'name': 'Blog', 'data': blog, 'slug': 'blog'},
        'Company': company,
        'CustomerService': customer_service,
        'Legal': legal,
        'Customer': customer,
        'Contact': contact,
    }
    return data
