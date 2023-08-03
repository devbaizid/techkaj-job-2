from django.contrib import admin

from .models import *

admin.site.register(email_for_send_message)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Proposal)
admin.site.register(Send_Projects_file)

admin.site.register(Earning_money)
admin.site.register(Pay_out_money)




admin.site.register(About_us)

admin.site.register(contact_us)
admin.site.register(service)