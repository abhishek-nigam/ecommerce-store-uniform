from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class School(models.Model):
    """
    Model for a school
    """
    school_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_coupoun_active = models.BooleanField(default=False)
    coupoun_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return "#{0} {1}".format(str(self.school_id) ,self.name)

    def get_absolute_url(self):
        return reverse("school-detail", args=[str(self.school_id)])

    class Meta:
        permissions =   (
                            ("can_read_schools", "Can READ schools"),
                            ("can_create_schools", "Can CREATE schools"),
                            ("can_update_schools", "Can UPDATE schools"),
                            ("can_delete_schools", "Can DELETE schools"),
                            ("can_maintain_schools", "Can MAINTAIN schools"),
                        )
        ordering = ['-school_id']


class Category(models.Model):
    """
    Model for a category, the different types of products available
    """
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return "#{0} {1}".format(str(self.category_id), self.name)

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.category_id)])
    
    class Meta:
        permissions =   (
                            ("can_read_categories", "Can READ categories"),
                            ("can_create_categories", "Can CREATE categories"),
                            ("can_update_categories", "Can UPDATE categories"),
                            ("can_delete_categories", "Can DELETE categories"),
                            ("can_maintain_categories", "Can MAINTAIN categories"),
                        )
        ordering = ['category_id']


class Product(models.Model):
    """
    Model for a product. It links with school and category
    """
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE) # TODO: check on_delete
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # TODO: check on_delete
    is_available = models.BooleanField(default=True) # TODO: check this
    description = models.TextField(blank=True, null=True)
    image1_link = models.URLField(blank=True, null=True)
    image2_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return "#{0} {1}".format(str(self.product_id) ,self.title)

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.product_id)])

    class Meta:
        permissions =   (
                            ("can_read_products", "Can READ products"),
                            ("can_create_products", "Can CREATE products"),
                            ("can_update_products", "Can UPDATE products"),
                            ("can_delete_products", "Can DELETE products"),
                            ("can_maintain_products", "Can MAINTAIN products"),
                        )
        ordering = ['-product_id']


class ProductInstance(models.Model):
    """
    Model for a product instance i.e. of a specfic size and price. It is a part of a product
    """
    instance_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # link to parent product
    is_available = models.BooleanField(default=True) # TODO: also check this when checking availability of a product
    size = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "{0} Instance #{1}".format(self.product.title, str(self.instance_id))

    class Meta:
        permissions =   (
                            ("can_read_product_instances", "Can READ product_instances"),
                            ("can_create_product_instances", "Can CREATE product_instances"),
                            ("can_update_product_instances", "Can UPDATE product_instances"),
                            ("can_delete_product_instances", "Can DELETE product_instances"),
                            ("can_maintain_product_instances", "Can MAINTAIN product_instances"),
                        )
        ordering = ['-instance_id']


class Order(models.Model):
    """
    Model for order by a customer. It consists of many order items.
    """
    order_id = models.AutoField(primary_key=True) # merchant-side order id
    order_access_token = models.CharField(max_length=10) # secret string shown to user, to enquire about the order
    creation_timestamp = models.DateTimeField(auto_now_add=True) # time when the order was created
    base_amount = models.DecimalField(max_digits=10, decimal_places=2) # sum of prices of all order items involved
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) # base_amount + gateway charges + tax

    customer_name = models.CharField(max_length=255)
    customer_mobile_number = models.PositiveIntegerField()
    customer_address = models.TextField()

    is_payed = models.BooleanField(default=False) # whether payment for the order was successfully payed
    payment_id = models.CharField(max_length=255, null=True) # payment id for order generated by the gateway, TODO: check max len possible is 255
    is_captured = models.BooleanField(default=False) # whether the payment has been captured by the merchant
    # payment_timestamp

    is_fulfilled = models.BooleanField(default=False) # whether the order has been fulfilled by the merchant
    fulfillment_timestamp = models.DateTimeField(null=True, blank=True)
    fulfilled_by = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return "Order #{0}".format(str(self.order_id))

    class Meta:
        permissions =   (
                            ("can_read_orders", "Can READ orders"),
                            ("can_create_orders", "Can CREATE orders"),
                            ("can_update_orders", "Can UPDATE orders"),
                            ("can_delete_orders", "Can DELETE orders"),
                            ("can_maintain_orders", "Can MAINTAIN orders"),
                        )
        ordering = ['-order_id']


class OrderItem(models.Model):
    """
    Model for an individual order item. It is a part of an order
    """
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE) # link to parent order TODO: check on_delete
    product_instance_id = models.PositiveIntegerField() # id of product instance here
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        permissions =   (
                            ("can_read_order_items", "Can READ order_items"),
                            ("can_create_order_items", "Can CREATE order_items"),
                            ("can_update_order_items", "Can UPDATE order_items"),
                            ("can_delete_order_items", "Can DELETE orders_items"),
                            ("can_maintain_order_items", "Can MAINTAIN orders_items"),
                        )