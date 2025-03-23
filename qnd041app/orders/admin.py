import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.views.generic import ListView

def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))

 
def export_to_csv(modeladmin, request, queryset): 
    opts = modeladmin.model._meta 
    response = HttpResponse(content_type='text/csv') 
    response['Content-Disposition'] = 'attachment;' \
        'filename={}.csv'.format(opts.verbose_name) 
    writer = csv.writer(response) 
     
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many] 
    # Write a first row with header information 
    writer.writerow([field.verbose_name for field in fields]) 
    # Write data rows 
    for obj in queryset: 
        data_row = [] 
        for field in fields: 
            value = getattr(obj, field.name) 
            if isinstance(value, datetime.datetime): 
                value = value.strftime('%d/%m/%Y') 
            data_row.append(value) 
        writer.writerow(data_row) 
    return response 
export_to_csv.short_description = 'Export to CSV' 


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ['price','quantity','order','product']


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])))
order_pdf.short_description = 'Invoice'

def whatsapp(obj):
     return mark_safe('<a href="https://api.whatsapp.com/send?phone={}"><i><i class="fa fa-phone"></i></a>'.format(obj.phone))
whatsapp.short_description = 'Send Mail'

def email(obj):
     return mark_safe('<a href="mailto:{}" target="_blank" ><i class="fa fa-envelope"></i></a>'.format(obj.email))
whatsapp.short_description = 'Whatsapp'


class OrderListView(ListView):
    paginate_by = 2
    model = Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'full_name', 
                    'arrival_date_time','departure_date_time', 'paid','total_cost',
                   email,whatsapp ]
    list_filter = ['arrival_date_time','departure_date_time','paid', 'created', 'updated']
    date_hierarchy = 'arrival_date_time'
    readonly_fields = ['first_name','last_name','arrival_date_time','departure_date_time','paid','email','total','discount','agree_term','coupon','braintree_id']
    list_per_page = 10
    inlines = [OrderItemInline]
    actions = [export_to_csv]

    def total_cost(self, obj):
        return obj.total

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_cost=Count("total"))
        return queryset
