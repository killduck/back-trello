from django.db import models


class News(models.Model):
    title = models.TextField()
    content = models.TextField()
    short_content = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING, default=1)


class Category(models.Model):
    title = models.TextField()

