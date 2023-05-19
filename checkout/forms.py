from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext as _
from paypal.standard.forms import PayPalPaymentsForm


class UserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()


class MyPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self, *args, **kwargs):
        if not args and not kwargs:
            return format_html(
                """
            <form action="{0}" method="post">
                {1}
                <div class="d-grid gap-2 my-3">
                    <button class="btn btn-primary">
                        <i class="lni lni-paypal-original"></i> {2}
                    </button>
                </div>
            </form>""",
                self.get_login_url(),
                self.as_p(),
                _("Pay Now"),
            )
        else:
            return super().render(*args, **kwargs)
