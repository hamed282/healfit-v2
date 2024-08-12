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
