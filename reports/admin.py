from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek
from django.db.models import Sum
from .models import OrderReport
from store.models import Order
import json


@admin.register(OrderReport)
class OrderReportAdmin(admin.ModelAdmin):

    change_list_template = "admin/reports/orders.html"  # ? this is another way for detemining where we want to override the default admin template

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    # ? we use this method we don't have a table in this model, then we should override this by using changelist_view()
    def changelist_view(self, request, extra_context=None):

        # * Here we will init our query then pass it to the template

        yearly_stats = (
            Order.objects.select_related("transaction").annotate(
                year=ExtractYear("created_at")
            )  # | ExtractYear() returns the Year of its input
            #! notice that we give values() function an parameter of "year", this because we generated a new attribute called "year" by using annotate() function
            .values(
                "year"
            )  # | values() function return specific attributes from the queryset (BUT THAT'S DOESN'T MEANS THAT WE CAN'T ACCESS OTHER ATTRIBUTES IN THE QUERYSET, for example: we will access the attribute transaction below when we will use Sum() even we didn't determine it in the values() method), also it is a necessary step for aggregation the result depinding on "year" value
            #! IMPORTANT: Sum() class below take our expression and apply the process of sum DEPENDING ON VALUES, so when we determined only "year" value then the Sum() class will Aggregate the result depending on values() which we passed BEFORE using annotate() with Sum()
            #! Also if we put values("year") after annotate(sum=Sum(...)) then the result won't be aggregated because we didn't determined the values that we want to aggregate depend on
            .annotate(sum=Sum("transaction__amount"))
        )

        monthly_stats = (
            Order.objects.select_related("transaction")
            .annotate(year=ExtractYear("created_at"))
            .annotate(month=ExtractMonth("created_at"))
            .values("year", "month")
            .annotate(sum=Sum("transaction__amount"))[
                :30
            ]  # ? here we take last 30 (Surely I mean last in time not last in the list 😒) because here we want last 30 month
            #! in my opinion the slicing above has done in a wrong way (I think the true slicing is [-30:])
        )

        weekly_stats = (
            Order.objects.select_related("transaction")
            .annotate(year=ExtractYear("created_at"))
            .annotate(week=ExtractWeek("created_at"))
            .values("year", "week")
            .annotate(sum=Sum("transaction__amount"))[
                :30
            ]  # ? here we want last 30 week
            #! in my opinion the slicing above has done in a wrong way (I think the true slicing is [-30:])
        )

        context = {
            **self.admin_site.each_context(request),
            "title": _("Orders Report"),
            "yearly_stats": json.dumps(list(yearly_stats)),
            "monthly_stats": json.dumps(list(monthly_stats)),
            "weekly_stats": json.dumps(list(weekly_stats)),
        }

        return TemplateResponse(request, self.change_list_template, context)
