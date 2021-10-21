from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from django.db import models

#from countdowntimer_model.models import CountdownTimer
#Ithink I do not need the class listing (redundant)

#default=timezone.now
class User(AbstractUser):
    itemsWon = models.IntegerField(default=0, verbose_name="bids won")
    messagesPosted = models.IntegerField(default=0, verbose_name="Total comments posted")
    pass

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f"{self.username}"
        
class category(models.Model):
    category = models.CharField(max_length = 64, unique = True)

    class Meta:
        ordering = ['category']

    def __str__(self):
        return f"{self.id}: {self.category}"

class itemToSell(models.Model):
    #id primary key, autoincrement is created automatically
    title = models.CharField(max_length = 128, default = "title")
    description = models.TextField(default = "description")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    updates = models.IntegerField(default = 0)
    onFire = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Seller")
    category =models.ForeignKey(category, on_delete=models.CASCADE, default="Others", null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.id}: {self.title} - {self.description} Auction created on {self.date_created.day}-{self.date_created.month}-\
{self.date_created.year} at {self.date_created.hour}:{self.date_created.minute}:{self.date_created.second} \
in the category {self.category}. updated {self.updates} times."

class watchlist(models.Model):
    watch = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    item = models.ForeignKey(itemToSell, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} watching {self.item} = {self.watch}"

class bid(models.Model):
    price = MoneyField(blank = False, verbose_name="Price", decimal_places=2, default_currency='USD', max_digits=11)
    current = MoneyField(verbose_name="current bid", default=None, decimal_places=2, default_currency='USD', max_digits=11, blank=True, null=True)
    userSelling = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="Seller", verbose_name="Seller")
    userWinning = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="Winner", null=True, verbose_name="Actual buyer", blank=True)
    item = models.ForeignKey(itemToSell, on_delete=models.CASCADE, verbose_name="Item sold", default=None)
    count = models.IntegerField(default = 0)

    def __str__(self):
        return f"Price = {self.price} on item {self.item.title} by user {self.userSelling}."

class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comment = models.TextField(default = "comment")
    item = models.ForeignKey(itemToSell, on_delete = models.CASCADE)
    datePosted = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"comment {self.comment} on item {self.item.title} by user {self.user.username} posted on {self.datePosted}"

class listing(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    bid = models.ForeignKey(bid, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(comment, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(itemToSell, on_delete=models.CASCADE, default=None)
    active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.category}, {self.user}, {self.item}, {self.bid}, {self.comment}"
    
    class Meta:
        ordering = ['-active']
