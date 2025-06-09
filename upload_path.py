import os
from django.db.models.fields.files import FieldFile


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


def get_video_product_upload_path(instance, filename):
    product_name = instance.product

    return os.path.join('product', product_name, 'video', filename)


def get_brand_logo_upload_path(instance, filename):
    brand_name = instance.brand
    if hasattr(brand_name, 'name'):
        brand_name = brand_name.name
    return os.path.join('brand', brand_name, filename)


def get_author_upload_path(instance, filename):
    author_image = instance.author

    return os.path.join('author', author_image, filename)


def get_content_upload_path(instance, filename):
    content_title = instance.title
    return os.path.join('content', content_title, filename)


def get_custom_made_upload_path(instance, filename):
    content_image = instance.image_alt

    return os.path.join('custom', content_image, filename)


def get_brand_mobile_upload_path(instance, filename):
    image_mobile = instance.image_mobile
    if hasattr(image_mobile, 'name'):
        image_mobile = image_mobile.name
    return os.path.join('brand', image_mobile, filename)


def get_brand_desktop_upload_path(instance, filename):
    image_desktop = instance.image_desktop
    if hasattr(image_desktop, 'name'):
        image_desktop = image_desktop.name
    return os.path.join('brand', image_desktop, filename)


def get_brand_cart_upload_path(instance, filename):
    brand_name = instance.brand_cart.brand.brand
    return os.path.join('brand_cart', brand_name, filename)


def get_attach_file_upload_path(instance, filename):
    attach_file = instance.attach_file
    if isinstance(attach_file, FieldFile):
        attach_file = attach_file.name
    return os.path.join('attach_file', attach_file, filename)


def get_brand_c1_upload_path(instance, filename):
    content1_image = instance.content1_image
    if hasattr(content1_image, 'name'):
        content1_image = content1_image.name
    return os.path.join('brand', content1_image, filename)


def get_brand_c2r_upload_path(instance, filename):
    content2_right_image = instance.content2_right_image
    if hasattr(content2_right_image, 'name'):
        content2_right_image = content2_right_image.name
    return os.path.join('brand', content2_right_image, filename)


def get_brand_c2m_upload_path(instance, filename):
    content2_mid_image = instance.content2_mid_image
    if hasattr(content2_mid_image, 'name'):
        content2_mid_image = content2_mid_image.name
    return os.path.join('brand', content2_mid_image, filename)


def get_brand_c2l_upload_path(instance, filename):
    content2_left_image = instance.content2_left_image
    if hasattr(content2_left_image, 'name'):
        content2_left_image = content2_left_image.name
    return os.path.join('brand', content2_left_image, filename)


def get_brand_c_upload_path(instance, filename):
    contact_image = instance.contact_image
    if hasattr(contact_image, 'name'):
        contact_image = contact_image.name
    return os.path.join('brand', contact_image, filename)
