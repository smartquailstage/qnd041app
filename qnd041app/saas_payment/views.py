import braintree
from django.shortcuts import render, redirect, get_object_or_404 
from saas_orders.models import SaaSOrder 
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required




@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(SaaSOrder, id=order_id)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost().amount),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()

            # create invoice e-mail
            subject = 'My Shop - Invoice no. {}'.format(order.id)
            message = 'Please, find attached the invoice for your recent purchase.'
            email = EmailMessage(subject,
                                 message,
                                 'admin@myshop.com',
                                 [order.email])

            # generate PDF
            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(order.id)
            weasyprint.HTML(string=html,  base_url=request.build_absolute_uri() ).write_pdf(response,stylesheets=[weasyprint.CSS('orders/static/css/pdf.css')], presentational_hints=True)
            # attach PDF file
            email.attach('order_{}.pdf'.format(order.id),
                         out.getvalue(),
                         'application/pdf')
            # send e-mail
            email.send()

            return redirect('saas_payment:done')
        else:
            return redirect('saas_payment:canceled')
    else:
        # generate token 
        client_token = braintree.ClientToken.generate()
        return render(request, 
                      'payment/process.html', 
                      {'order': order,
                       'client_token': client_token})

@login_required
def payment_done(request):
    return render(request, 'payment/done.html')

@login_required
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
