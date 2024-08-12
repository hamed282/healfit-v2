import os


def get_cover_image_upload_path(instance, filename):
    product_name = instance.product

    return os.path.join('product', product_name, 'cover', filename)


def get_size_table_upload_path(instance, filename):
    product_name = instance.product

    return os.path.join('product', product_name, 'size-table', filename)


def get_description_image_upload_path(instance, filename):
    product_name = instance.product

    return os.path.join('product', product_name, 'description-image', filename)


def get_gallery_upload_path(instance, filename):
    product_name = instance.product.product
    color = instance.color.color

    return os.path.join('product', product_name, color, filename)


def get_cover_blog_upload_path(instance, filename):
    blog_name = instance.title

    return os.path.join('blog', blog_name, 'cover', filename)


def get_banner_blog_upload_path(instance, filename):
    blog_name = instance.title

    return os.path.join('blog', blog_name, 'banner', filename)


def get_title_blog_upload_path(instance, filename):
    blog_name = instance.title

    return os.path.join('blog', blog_name, 'title', filename)


def get_category_upload_path(instance, filename):
    category_name = instance.category

    return os.path.join('category', category_name, filename)


def get_subcategory_upload_path(instance, filename):
    subcategory_name = instance.subcategory

    return os.path.join('subcategory', subcategory_name, filename)


def get_gender_upload_path(instance, filename):
    gender_name = instance.gender

    return os.path.join('gender', gender_name, filename)
