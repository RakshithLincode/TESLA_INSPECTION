from django.contrib import admin
from accounts.models import User,User_Client,User_SI,Client,SI,User_Master,User_Admin,User_Business_Manager,User_Sales_Executive,User_Operator,User_Line_Manager,User_Supervisor
from django.contrib.auth.admin import UserAdmin

#django lvl
admin.site.register(User)
#master lvl - lincode
admin.site.register(User_Master)

#business side
admin.site.register(User_SI)

admin.site.register(User_Business_Manager)
admin.site.register(User_Sales_Executive)


#ai side
admin.site.register(User_Admin)

admin.site.register(User_Supervisor)
admin.site.register(User_Line_Manager)
admin.site.register(User_Operator)






admin.site.register(Client)
admin.site.register(SI)
admin.site.register(User_Client)
