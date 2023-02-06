from django.contrib import admin
from .models import Review


class GoodReviewFilter(admin.SimpleListFilter):
    title = "Filter by Good or Bad"
    parameter_name = "goodorbad"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good Review"),
            ("bad", "Bad Review"),
        ]

    def queryset(self, request, reviews):

        isGood = self.value()
        print(type(isGood))
        print("isGood:", isGood)
        if not isGood:
            return reviews

        if isGood == "good":
            print("great then")
            return reviews.filter(rating__gte=3)
        else:
            print("less then")
            return reviews.filter(rating__lt=3)


class WordFilter(admin.SimpleListFilter):
    title = "filter by words!"

    parameter_name = "word"

    def lookups(self, requestk, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        "rating",
        "user__is_host",
        "room__kind",
        WordFilter,
        GoodReviewFilter,
    )
