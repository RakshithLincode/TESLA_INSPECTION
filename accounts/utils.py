from accounts.views import *
from accounts.models import User,User_Client,User_SI,Client,SI,User_Master,User_Admin,User_Business_Manager,User_Sales_Executive,User_Supervisor,User_Line_Manager,User_Operator
from django.core import serializers
from django.forms.models import model_to_dict
import uuid
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import authenticate
from common.utils import *
from livis.settings import *
from rest_framework.authtoken.models import Token
from accounts.views import throw_permission


################################################################USER CRUDS################################################################
def add_user_account_util(data):
    """
    Usage: API to add a user account.
    Request Parameters: {
	    "username" : "shivu232",
	    "first_name" : "Shivani",
	    "last_name" : "Udupa",
	    "email" : "shivani@gmail.com",
	    "is_staff" : false,
	    "user_address" : "Bangalore",
        "is_superuser" : false,
        "role_name" : "122did",
        "phone_number" : 21218739283,
        "password" : "password"
    }
    Request Method: POST
    Response: {
        "message": "User Account added successfully."
    }
    """
    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        # last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        # user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        current_user = data.get('current_user',None)
        modified_by = current_user['first_name']
        created_by = current_user['first_name']

        # phone_number = data.get('phone_number',None)
        #print('ASDFSDFASD')
        user_obj = User(
            user_id =  user_id,
            username =  username,
            first_name = first_name,
            last_name = modified_by,
            email =  email,
            is_staff = is_staff,
            user_address =  created_by,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_superuser =  is_superuser,
            role_name =  role_name
            # phone_number =  phone_number
        )
        user_obj.set_password(data.get('password',None))
        #print("date_joined",date_joined,"\nupdated_at",updated_at)
        user_obj.save()
        resp = "User Account added successfully."
        status_code = 200
        return resp,status_code
    except Exception as e:
        status_code = 400
        resp = "User account could not be created. "+str(e)
        return resp,status_code


def get_user_account_util(user_id):
    """
    Usage: API to get details of a user account.
    Request Parameters: user_id
    Request Method: GET
    Response: {
        "password": "pbkdf2_sha256$180000$zDVi3fZKMmWY$aKuAzjTsK29jYke5iYTon6KT0sRPxS8XL6juzXx8vH4=",
        "last_login": null,
        "is_staff": false,
        "first_name": "Shivani",
        "last_name": "Udupa",
        "username": "shivu232",
        "email": "shivani@gmail.com",
        "user_address": "Bangalore",
        "date_joined": "2020-08-03T18:45:19.428Z",
        "updated_at": "2020-08-03T18:45:19.428Z",
        "is_deleted": false,
        "is_active": true,
        "is_superuser": false,
        "role_name": "Sysadmin",
        "phone_number": "21218739283",
        "groups": [],
        "user_permissions": []
    }
    """
    resp = {}
    try:
        user_obj = User.objects.filter(user_id=user_id)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        return resp
    except Exception as e:
        resp = "User account could not be retrieved. "+str(e)
        return resp


def update_user_account_util(data,request):   #Note: Unable to update email or username as they are having unique constraints.
    """
    Usage: API to update a user account.
    Request Parameters: {
	    "user_id" : "2ca8ed2e-9675-444a-9ce8-5c01b8b445c5",
	    "first_name" : "Shruti",
	    "last_name" : "Udupa",
	    "is_staff" : false,
	    "user_address" : "Hyderabad",
	    "is_active" : true,
	    "is_superuser" : false,
	    "role_name" : "Manager",
	    "phone_number" : "7149383442"
    }
    Request Method: PATCH
    Response: {
        "message": "User Account updated successfully."
    }
    """
    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        # last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        # user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        current_user = data.get('current_user',None)
        modified_by = current_user['first_name']


        # phone_number = data.get('phone_number',None)
        
        password = data.get('password',None)
        user_ip_old_password = data.get('old_password',None)
        
        username = request.user.username

        if user_id is None:
            return "user_id not provided","fail"
        from django.contrib.auth import get_user_model
        User1 = get_user_model()
        u = User1.objects.get(username=username)
        
        user_obj = User.objects.get(user_id=user_id)

        
        ##print("user obj:::",user_obj)
        if user_obj:
            if first_name :
                user_obj.first_name=first_name
            if modified_by :
                user_obj.last_name=modified_by
            if is_staff :
                user_obj.is_staff=is_staff
            # if user_address :
            #     user_obj.user_address=user_address
            if updated_at :
                user_obj.updated_at=updated_at
            if is_active :
                user_obj.is_active=is_active
            if is_superuser :
                user_obj.is_superuser=is_superuser
            if role_name :
                user_obj.role_name=role_name
            if password :
                user_obj.password=password
                  
            # if phone_number :
            #     user_obj.phone_number=phone_number
            # if password:


            #     if u.check_password(user_ip_old_password) is False:
            #         message = "Invalid Old Password"
            #         message1 = 'fail'
            #         return message,message1

            #     if str(password) == str(user_ip_old_password):
            #         message = "New password cannot be same as old password"
            #         message1 = 'fail'
            #         return message,message1

            #     #u.set_password(password)
            #     #u.save()
            #     user_obj.set_password(password)

            user_obj.save()
            resp = "User Account updated successfully."
            return resp,'success'
        else:
            resp = "User account could not be updated. User ID is not specified."
            return resp,"fail"
    except Exception as e:
        resp = "User account could not be updated. "+str(e)
        return resp,'fail'


def delete_user_account_util(user_id):
    """
    Usage: API to delete a user account.
    Request Parameters: user_id
    Request Method: DELETE
    Response: {
        "message": "User Account deleted successfully."
    }
    """
    resp = {}
    try:
        user_obj = User.objects.get(user_id=user_id)
        if user_obj:
            user_obj.is_deleted=True
            user_obj.save()
            resp = "User account deleted successfully."
            return resp
        else:
            resp = "User account could not be deleted. User ID is not specified."
            return resp 
    except Exception as e:
        resp = "User account could not be deleted. "+str(e)
        return resp


def get_all_user_accounts_util():
    """
    Usage: API to get all the existing user accounts.
    Request Parameters: None
    Request Method: GET
    Response: List of all user accounts.
    [{
        "password": "pbkdf2_sha256$180000$CAOl1CnTxpxe$fRXKkLU4iVGa4DwTW8naoKcDSqvLEKcS+sfNdryl8GM=",
        "last_login": null,
        "is_staff": true,
        "first_name": "Shruti",
        "last_name": "Udupa",
        "username": "shruti",
        "email": "shruti.udupa@lincode.us",
        "user_address": "Hyderabad",
        "date_joined": "2020-08-03T17:40:03.795Z",
        "updated_at": "2020-08-03T20:43:29.827Z",
        "is_deleted": false,
        "is_active": true,
        "is_superuser": true,
        "role_name": "Manager",
        "phone_number": "7149383442",
        "groups": [],
        "user_permissions": []
    }]
    """
    resp = []
    try:
        User_obj = User.objects.filter(is_deleted=False)
        
        for i in range(len(User_obj)):
            User_obj_json = json.loads(serializers.serialize('json',User_obj))
            # if(i != 0):
            # User_obj_json = User_obj_json[i]['fields']
            User_obj_json = User_obj_json[i]
            del User_obj_json['fields']['password']
            # User_obj_json['user_id'] = User_obj_json[i]['pk'] if User_obj_json[i]['pk'] else None
            # #print("user::",User_obj_json[i]['pk'])
            # break
            resp.append(User_obj_json)
        return resp
    except Exception as e:
        resp = "Could not retrieve all the existing client accounts. "+str(e)
        return resp


################################################################MASTER_CRUDS#####################################################################

def add_user_master_util(data):
    """
    Usage: API to add a user master account.
    Request Parameters: {
	    "username" : "client_admin_poo1",
	    "first_name" : "Pooja",
	    "last_name" : "Kandhal",
	    "email" : "poo@gmail.com",
	    "is_staff" : false,
	    "user_address" : "Mumbai",
        "is_superuser" : false,
        "role_name" : "438428eh32e",
        "phone_number" : "48372924366",
        "password" : "password",
    }
    Request Method: POST
    Response: {
        "message": "User Master Account added successfully."
    }
    """
    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        master_id = data.get('master_id',None)
        #master_name = data.get('master_name',None)
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        user_master_obj = User_Master(
            user_id =  user_id,
            master_id =  master_id,
            #master_name = master_name,
            first_name =  first_name,
            last_name =  last_name,
            username =  username,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_staff =  is_staff,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number
        )
        user_master_obj.set_password(data.get('password',None))
        user_master_obj.save()
        resp = "User Master Account added successfully."
    
        return resp
    except Exception as e:
        resp = "User Master account could not be created. "+str(e)
        return resp

def update_user_master_util(data):
    """
    Usage: API to update a user Master account.
    Request Parameters: {
	    "user_id": "bb98f0bb-a33e-4143-9885-5afc5342ba1d",
	    "first_name" : "Jinta",
	    "last_name" : "Mary Skariah",
	    "is_staff" : false,
	    "user_address" : "Alapuzzha",
	    "is_active" : true,
	    "is_superuser" : false,
	    "role_name" : "Manager",
	    "phone_number" : "7149383442"
    }
    Request Method: PATCH
    Response: {
        "message": "User Master Account updated successfully."
    }
    """
    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_staff = data.get('is_staff',None)
        is_superuser = data.get('is_superuser',None)
        #role_name = data.get('role_name',None)
        #phone_number = data.get('phone_number',None)
        user_master_obj = User_Master.objects.get(user_id=user_id)

        if user_master_obj:
            if first_name :
                user_master_obj.first_name=first_name
            if last_name :
                user_master_obj.last_name=last_name
            if user_address :
                user_master_obj.user_address=user_address
            if updated_at :
                user_master_obj.updated_at=updated_at
            if is_active :
                user_master_obj.is_active=is_active
            if is_staff :
                user_master_obj = user_master_obj.is_staff=is_staff
            if is_superuser :
                user_master_obj = user_master_obj.is_superuser=is_superuser

            user_master_obj.save()
            resp = "User Master Account updated successfully."
            return resp
        else:
            resp = "User Master account could not be updated. Master id is not specified."
            return resp   
    except Exception as e:
        resp = "User Master account could not be updated. "+str(e)
        return resp

def delete_user_master_util(user_id):
    resp = {}
    try:
        user_master_obj = User_Master.objects.get(user_id=user_id)
        if user_master_obj:
            user_master_obj.is_deleted=True
            user_master_obj.save()
            resp = "User master account deleted successfully."
            return resp
        else:
            resp = "User master account could not be deleted. master ID is not specified."
            return resp 
    except Exception as e:
        resp = "User master account could not be deleted. "+str(e)
        return resp

def get_user_master_util(user_id):
    resp = {}
    try:
        user_master_obj = User_Master.objects.filter(user_id=user_id)
        user_master_obj_json = json.loads(serializers.serialize('json',user_master_obj))
        #print(user_master_obj_json)
        if len(user_master_obj_json) == 0:
            return []
        resp1 = user_master_obj_json[0]['fields']['user_ptr']
        user_obj = User.objects.filter(user_id=resp1)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        resp['user_id'] = str(resp1)
        return resp
    except Exception as e:
        resp = "User master account could not be retrieved. "+str(e)
        return resp

def get_user_masters_util():
    resp = []
    user_list = []
    user_list_details = []
    try:
        user_master_obj = User_Master.objects.filter(is_deleted=False)
        for i in range(len(user_master_obj)):
            user_master_obj_json = json.loads(serializers.serialize('json',user_master_obj))
            
            user_master_obj_json = user_master_obj_json[i]
            resp.append(user_master_obj_json)
            
        for i in resp:
            user_list.append(i['fields']['user_ptr'])
        #print(resp)
        for i in user_list:
        
            #print(i)
            user_obj = User.objects.filter(user_id=i)
            
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            #print(user_obj_json)
            resp = user_obj_json[0]['fields']
            
            resp['user_id'] = str(i)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user client accounts. "+str(e)
        return resp

################################################################USER_ADMIN#######################################################################


def add_user_admin_util(data):
    """
    Usage: API to add a user admin account.
    Request Parameters: {
	    "username" : "client_admin_poo1",
	    "first_name" : "Pooja",
	    "last_name" : "Kandhal",
	    "email" : "poo@gmail.com",
	    "is_staff" : false,
	    "user_address" : "Mumbai",
        "is_superuser" : false,
        "role_name" : "438428eh32e",
        "phone_number" : "48372924366",
        "password" : "password",
    }
    Request Method: POST
    Response: {
        "message": "User admin Account added successfully."
    }
    """
    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        admin_id = data.get('admin_id',None)
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        user_admin_obj = User_Admin(
            user_id =  user_id,
            admin_id =  admin_id,
            first_name =  first_name,
            last_name =  last_name,
            username =  username,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_staff =  is_staff,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number
        )
        user_admin_obj.set_password(data.get('password',None))
        user_admin_obj.save()
        resp = "User Admin Account added successfully."
    
        return resp
    except Exception as e:
        resp = "User Admin account could not be created. "+str(e)
        return resp

def update_user_admin_util(data):
    """
    Usage: API to update a user Master account.
    Request Parameters: {
	    "user_id": "bb98f0bb-a33e-4143-9885-5afc5342ba1d",
	    "first_name" : "Jinta",
	    "last_name" : "Mary Skariah",
	    "is_staff" : false,
	    "user_address" : "Alapuzzha",
	    "is_active" : true,
	    "is_superuser" : false,
	    "role_name" : "Manager",
	    "phone_number" : "7149383442"
    }
    Request Method: PATCH
    Response: {
        "message": "User Master Account updated successfully."
    }
    """
    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_staff = data.get('is_staff',None)
        is_superuser = data.get('is_superuser',None)

        user_admin_obj = User_Admin.objects.get(user_id=user_id)

        if user_admin_obj:
            if first_name :
                user_admin_obj.first_name=first_name
            if last_name :
                user_admin_obj.last_name=last_name
            if user_address :
                user_admin_obj.user_address=user_address
            if updated_at :
                user_admin_obj.updated_at=updated_at
            if is_active :
                user_admin_obj.is_active=is_active
            if is_staff :
                user_admin_obj = user_admin_obj.is_staff=is_staff
            if is_superuser :
                user_admin_obj = user_admin_obj.is_superuser=is_superuser

            user_admin_obj.save()
            resp = "User Admin Account updated successfully."
            return resp
        else:
            resp = "User Admin account could not be updated. Admin id is not specified."
            return resp   
    except Exception as e:
        resp = "User Admin account could not be updated. "+str(e)
        return resp

def delete_user_admin_util(user_id):
    resp = {}
    try:
        user_admin_obj = User_Admin.objects.get(user_id=user_id)
        if user_admin_obj:
            user_admin_obj.is_deleted=True
            user_admin_obj.save()
            resp = "User admin account deleted successfully."
            return resp
        else:
            resp = "User admin account could not be deleted. Admin ID is not specified."
            return resp 
    except Exception as e:
        resp = "User admin account could not be deleted. "+str(e)
        return resp

def get_user_admin_util(user_id):
    resp = {}
    try:
        user_admin_obj = User_Admin.objects.filter(user_id=user_id)
        user_admin_obj_json = json.loads(serializers.serialize('json',user_admin_obj))
        if len(user_admin_obj_json) == 0:
            return []
        resp1 = user_admin_obj_json[0]['fields']['user_ptr']
        user_obj = User.objects.filter(user_id=resp1)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        resp['user_id'] = str(resp1)
        return resp
    except Exception as e:
        resp = "User admin account could not be retrieved. "+str(e)
        return resp

def get_user_admins_util():
    resp = []
    user_list = []
    user_list_details = []
    try:
            
        user_admin_obj = User_Admin.objects.filter(is_deleted=False)
        for i in range(len(user_admin_obj)):
            user_admin_obj_json = json.loads(serializers.serialize('json',user_admin_obj))
            
            user_admin_obj_json = user_admin_obj_json[i]
            resp.append(user_admin_obj_json)
            
        for i in resp:
            user_list.append(i['fields']['user_ptr'])
            
        for i in user_list:
        

            user_obj = User.objects.filter(user_id=i)
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            resp = user_obj_json[0]['fields']
            
            resp['user_id'] = str(i)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user admin accounts. "+str(e)
        return resp
        
################################################################USER_business_manager#######################################################################


def add_user_business_manager_util(data):
    """
    Usage: API to add a user admin account.
    Request Parameters: {
	    "username" : "client_admin_poo1",
	    "first_name" : "Pooja",
	    "last_name" : "Kandhal",
	    "email" : "poo@gmail.com",
	    "is_staff" : false,
	    "user_address" : "Mumbai",
        "is_superuser" : false,
        "role_name" : "438428eh32e",
        "phone_number" : "48372924366",
        "password" : "password",
    }
    Request Method: POST
    Response: {
        "message": "User admin Account added successfully."
    }
    """
    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        business_manager_id = data.get('business_manager_id',None)
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        user_business_manager_obj = User_Business_Manager(
            user_id =  user_id,
            business_manager_id =  business_manager_id,
            first_name =  first_name,
            last_name =  last_name,
            username =  username,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_staff =  is_staff,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number
        )
        user_business_manager_obj.set_password(data.get('password',None))
        user_business_manager_obj.save()
        resp = "User business_manager Account added successfully."

        return resp
    except Exception as e:
        resp = "User business_manager account could not be created. "+str(e)
        return resp

def update_user_business_manager_util(data):
    """
    Usage: API to update a user user_business_manager account.
    Request Parameters: {
	    "user_id": "bb98f0bb-a33e-4143-9885-5afc5342ba1d",
	    "first_name" : "Jinta",
	    "last_name" : "Mary Skariah",
	    "is_staff" : false,
	    "user_address" : "Alapuzzha",
	    "is_active" : true,
	    "is_superuser" : false,
	    "role_name" : "Manager",
	    "phone_number" : "7149383442"
    }
    Request Method: PATCH
    Response: {
        "message": "User Master Account updated successfully."
    }
    """
    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_staff = data.get('is_staff',None)
        is_superuser = data.get('is_superuser',None)
        #role_name = data.get('role_name',None)
        #phone_number = data.get('phone_number',None)
        user_business_manager_obj = User_Business_Manager.objects.get(user_id=user_id)

        if user_business_manager_obj:
            if first_name :
                user_business_manager_obj.first_name=first_name
            if last_name :
                user_business_manager_obj.last_name=last_name
            if user_address :
                user_business_manager_obj.user_address=user_address
            if updated_at :
                user_business_manager_obj.updated_at=updated_at
            if is_active :
                user_business_manager_obj.is_active=is_active
            if is_staff :
                user_business_manager_obj = user_business_manager_obj.is_staff=is_staff
            if is_superuser :
                user_business_manager_obj = user_business_manager_obj.is_superuser=is_superuser

            user_business_manager_obj.save()
            resp = "User business_manager Account updated successfully."
            return resp
        else:
            resp = "User business_manager account could not be updated. business_manager id is not specified."
            return resp   
    except Exception as e:
        resp = "User business_manager account could not be updated. "+str(e)
        return resp

def delete_user_business_manager_util(user_id):
    resp = {}
    try:
        user_business_manager_obj = User_Business_Manager.objects.get(user_id=user_id)
        if user_business_manager_obj:
            user_business_manager_obj.is_deleted=True
            user_business_manager_obj.save()
            resp = "User business_manager account deleted successfully."
            return resp
        else:
            resp = "User business_manager account could not be deleted. business_manager ID is not specified."
            return resp 
    except Exception as e:
        resp = "User business_manager account could not be deleted. "+str(e)
        return resp

def get_user_business_manager_util(user_id):
    resp = {}
    try:
        user_business_manager_obj = User_Business_Manager.objects.filter(user_id=user_id)
        user_business_manager_obj_j = json.loads(serializers.serialize('json',user_business_manager_obj))
        if len(user_business_manager_obj_j) == 0:
            return []
        resp1 = user_business_manager_obj_j[0]['fields']['user_ptr']
        user_obj = User.objects.filter(user_id=resp1)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        resp['user_id'] = str(resp1)
        return resp
    except Exception as e:
        resp = "User business manager account could not be retrieved. "+str(e)
        return resp

def get_user_business_managers_util():
    resp = []
    user_list = []
    user_list_details = []
    try:
            
        user_business_manager_obj = User_Business_Manager.objects.filter(is_deleted=False)
        for i in range(len(user_business_manager_obj)):
            user_business_manager_obj_json = json.loads(serializers.serialize('json',user_business_manager_obj))
            
            user_business_manager_obj_json = user_business_manager_obj_json[i]
            resp.append(user_business_manager_obj_json)
            
        for i in resp:
            user_list.append(i['fields']['user_ptr'])
            
        for i in user_list:
        

            user_obj = User.objects.filter(user_id=i)
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            resp = user_obj_json[0]['fields']
            
            resp['user_id'] = str(i)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user admin accounts. "+str(e)
        return resp


################################################################USER_sales_executive#######################################################################

def add_user_sales_executive_util(data,request):

    #print("user_idddddddddddddddddddddddddddd is")
    #print(request.user.user_id)



    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        sales_executive_id = data.get('sales_executive_id',None)
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        created_by = str(request.user.user_id)
        user_sales_executive_obj = User_Sales_Executive(
            user_id =  user_id,
            sales_executive_id =  sales_executive_id,
            first_name =  first_name,
            last_name =  last_name,
            username =  username,
            created_by = created_by,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_staff =  is_staff,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number
        )
        user_sales_executive_obj.set_password(data.get('password',None))
        user_sales_executive_obj.save()
        resp = "User sales_executive Account added successfully."

        return resp
    except Exception as e:
        resp = "User sales_executive account could not be created. "+str(e)
        return resp

def update_user_sales_executive_util(data):

    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_staff = data.get('is_staff',None)
        is_superuser = data.get('is_superuser',None)
        #role_name = data.get('role_name',None)
        #phone_number = data.get('phone_number',None)
        user_sales_executive_obj = User_Sales_Executive.objects.get(user_id=user_id)

        if user_sales_executive_obj:
            if first_name :
                user_sales_executive_obj.first_name=first_name
            if last_name :
                user_sales_executive_obj.last_name=last_name
            if user_address :
                user_sales_executive_obj.user_address=user_address
            if updated_at :
                user_sales_executive_obj.updated_at=updated_at
            if is_active :
                user_sales_executive_obj.is_active=is_active
            if is_staff :
                user_sales_executive_obj = user_sales_executive_obj.is_staff=is_staff
            if is_superuser :
                user_sales_executive_obj = user_sales_executive_obj.is_superuser=is_superuser

            user_sales_executive_obj.save()
            resp = "User sales_executive Account updated successfully."
            return resp
        else:
            resp = "User sales_executive account could not be updated. sales_executive id is not specified."
            return resp   
    except Exception as e:
        resp = "User sales_executive account could not be updated. "+str(e)
        return resp

def delete_user_sales_executive_util(user_id):
    resp = {}
    try:
        user_sales_executive_obj = User_Sales_Executive.objects.get(user_id=user_id)
        if user_sales_executive_obj:
            user_sales_executive_obj.is_deleted=True
            user_sales_executive_obj.save()
            resp = "User sales_executive account deleted successfully."
            return resp
        else:
            resp = "User sales_executive account could not be deleted. sales_executive ID is not specified."
            return resp 
    except Exception as e:
        resp = "User sales_executiveaccount could not be deleted. "+str(e)
        return resp

def get_user_sales_executive_util(user_id):
    resp = {}
    try:
        user_sales_executive_obj = User_Sales_Executive.objects.filter(user_id=user_id)
        user_sales_executive_obj_j = json.loads(serializers.serialize('json',user_sales_executive_obj))
        if len(user_sales_executive_obj_j) == 0:
            return []
        resp1 = user_sales_executive_obj_j[0]['fields']['user_ptr']
        user_obj = User.objects.filter(user_id=resp1)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        resp['user_id'] = str(resp1)
        return resp
    except Exception as e:
        resp = "User sales_executive account could not be retrieved. "+str(e)
        return resp

def get_user_sales_executives_util():
    resp = []
    user_list = []
    user_list_details = []
    try:

        user_sales_executive_obj = User_Sales_Executive.objects.filter(is_deleted=False)
        for i in range(len(user_sales_executive_obj)):
            user_sales_executive_obj_json = json.loads(serializers.serialize('json',user_sales_executive_obj))
            #print(user_sales_executive_obj_json)
            
            user_sales_executive_obj_json = user_sales_executive_obj_json[i]
            resp.append(user_sales_executive_obj_json)
        dct = []
        
        for i in resp:
            
            dct1 = { "user_ptr":i['fields']['user_ptr'] , "created_by": i['fields']['created_by'] }
            dct.append(dct1)
            #user_list.append(i['fields']['created_by'])
            #user_list.append(i['fields']['user_ptr'])
            
        for i in dct:
            j = i['user_ptr']
            k = i['created_by']
            user_obj = User.objects.filter(user_id=j)
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            resp = user_obj_json[0]['fields']
            resp['created_by'] = str(k)
            resp['user_id'] = str(j)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user sales_executive. "+str(e)
        return resp

def get_user_sales_by_business_manager_util(business_manager_id):
    resp = []
    user_list = []
    user_list_details = []
    try:

        user_sales_executive_obj = User_Sales_Executive.objects.filter(is_deleted=False)
        for i in range(len(user_sales_executive_obj)):
            user_sales_executive_obj_json = json.loads(serializers.serialize('json',user_sales_executive_obj))
            #print(user_sales_executive_obj_json)
            
            user_sales_executive_obj_json = user_sales_executive_obj_json[i]
            resp.append(user_sales_executive_obj_json)
        dct = []
        
        for i in resp:
            
            dct1 = { "user_ptr":i['fields']['user_ptr'] , "created_by": i['fields']['created_by'] }
            dct.append(dct1)
            #user_list.append(i['fields']['created_by'])
            #user_list.append(i['fields']['user_ptr'])
            
        for i in dct:
            j = i['user_ptr']
            k = i['created_by']
            #print("k isssssssss")
            #print(k)
            if str(k) == str(business_manager_id):
                #print("in imnuanfuanab")
                user_obj = User.objects.filter(user_id=j)
                user_obj_json = json.loads(serializers.serialize('json',user_obj))
                resp = user_obj_json[0]['fields']
                resp['created_by'] = str(k)
                resp['user_id'] = str(j)
            
                user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user sales_executive. "+str(e)
        return resp
################################################################USER_CLIENT CRUDS################################################################
def add_user_client_util(data):
    """
    Usage: API to add a user client account.
    Request Parameters: {
	    "username" : "client_admin_poo1",
	    "first_name" : "Pooja",
	    "last_name" : "Kandhal",
	    "email" : "poo@gmail.com",
	    "is_staff" : false,
	    "user_address" : "Mumbai",
        "is_superuser" : false,
        "role_name" : "438428eh32e",
        "phone_number" : "48372924366",
        "password" : "password",
	    "client_user_manager" : "None",
	    "is_client_admin" : true
    }
    Request Method: POST
    Response: {
        "message": "User Client Account added successfully."
    }
    """
    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        client_id = data.get('client_id',None)
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        client_user_manager = data.get('client_user_manager',None)
        is_client_admin = data.get('is_client_admin',None)
        user_client_obj = User_Client(
            user_id =  user_id,
            client_id =  client_id,
            username =  username,
            first_name =  first_name,
            last_name =  last_name,
            is_staff = is_staff,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number,
            client_user_manager =  client_user_manager,
            is_client_admin = is_client_admin
        )
        user_client_obj.set_password(data.get('password',None))
        user_client_obj.save()
        resp = "User Client Account added successfully."
    
        return resp
    except Exception as e:
        resp = "User Client account could not be created. "+str(e)
        return resp

def update_user_client_util(data):
    """
    Usage: API to update a user client account.
    Request Parameters: {
	    "first_name" : "Pooja",
	    "last_name" : "Kandhal",
	    "is_staff" : false,
	    "user_address" : "Bombay",
	    "is_active" : true,
	    "is_superuser" : false,
	    "role_name" : "Manager",
	    "phone_number" : "7149383442",
	    "client_user_manager": "None", 
	    "is_client_admin": true
    }
    Request Method: PATCH
    Response: {
        "message": "User client Account updated successfully."
    }
    """
    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        user_address = data.get('user_address',None)
        updated_at = datetime.utcnow()
        is_active = data.get('is_active',None)
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        client_user_manager = data.get('client_user_manager',None)
        is_client_admin = data.get('is_client_admin',None)
        user_client_obj = User_Client.objects.get(user_id=user_id)
        if user_client_obj:
            if first_name :
                user_client_obj.first_name=first_name
            if last_name :
                user_client_obj.last_name=last_name
            if is_staff :
                user_client_obj.is_staff=is_staff
            if user_address :
                user_client_obj.user_address=user_address
            if updated_at :
                user_client_obj.updated_at=updated_at
            if is_active :
                user_client_obj.is_active=is_active
            if is_superuser :
                user_client_obj.is_superuser=is_superuser
            if role_name :
                user_client_obj.role_name=role_name
            if phone_number :
                user_client_obj.phone_number=phone_number
            if client_user_manager:
                user_client_obj.client_user_manager=client_user_manager
            if client_user_manager:
                user_client_obj.is_client_admin=is_client_admin
            user_client_obj.save()
            resp = "User Client Account updated successfully."
            return resp
        else:
            resp = "User Client account could not be updated. Client ID is not specified."
            return resp   
    except Exception as e:
        resp = "User Client account could not be updated. "+str(e)
        return resp

def delete_user_client_util(user_id):
    resp = {}
    try:
        user_client_obj = User_Client.objects.get(user_id=user_id)
        if user_client_obj:
            user_client_obj.is_deleted=True
            user_client_obj.save()
            resp = "User Client account deleted successfully."
            return resp
        else:
            resp = "User Client account could not be deleted. User ID is not specified."
            return resp 
    except Exception as e:
        resp = "User Client account could not be deleted. "+str(e)
        return resp

def get_list_client_util(user_id):
    resp = []
    user_list = []
    user_list_details = []
    try:
        user_client_obj = User_Client.objects.filter(is_deleted=False)
        for i in range(len(user_client_obj)):
            user_client_obj_json = json.loads(serializers.serialize('json',user_client_obj))
            
            user_client_obj_json = user_client_obj_json[i]
            resp.append(user_client_obj_json)
            
        for i in resp:
            user_list.append(i['pk'])
            
        for i in user_list:
        

            user_obj = User.objects.filter(user_id=i)
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            resp = user_obj_json[0]['fields']
            
            resp['user_id'] = str(i)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user client accounts. "+str(e)
        return resp



def get_user_client_util(user_id):
    """
    Usage: API to get details of a user client account.
    Request Parameters: user_id
    Request Method: GET
    Response: {
        "user_id": "a83b9fc4-8171-43aa-927f-487feac73ae3",
        "client_user_manager": "None",
        "is_client_admin": true
    }
    """
    resp = {}
    try:
        user_client_obj = User_Client.objects.filter(user_id=user_id)
        
        #user_client_obj = User_Client.objects.get(user_id=user_id)
        ##print(user_client_obj)
        user_client_obj_json = json.loads(serializers.serialize('json',user_client_obj))
        #print(user_client_obj_json)
        #return resp
        resp = user_client_obj_json[0]['fields']
        return resp
    except Exception as e:
        resp = "User client account could not be retrieved. "+str(e)
        return resp





def get_user_clients_util():
    """
    Usage: API to get all the existing user accounts.
    Request Parameters: None
    Request Method: GET
    Response: List of all user accounts.
    [{
        "user_id": "a83b9fc4-8171-43aa-927f-487feac73ae3",
        "client_user_manager": "None",
        "is_client_admin": true
    }]
    """
    resp = []
    try:
        user_client_obj = User_Client.objects.filter(is_deleted=False)
        for i in range(len(user_client_obj)):
            user_client_obj_json = json.loads(serializers.serialize('json',user_client_obj))
            
            user_client_obj_json = user_client_obj_json[i]['fields']
            resp.append(user_client_obj_json)
        
        return resp
    except Exception as e:
        resp = "Could not retrieve all the existing user client accounts. "+str(e)
        return resp


#########################################################USER_SI CRUDS########################################################
def add_user_si_util(data):
    """
    Usage: API to add a user SI account.
    Request Parameters: {
	    "username" : "client_admin_poo1",
	    "first_name" : "Pooja",
	    "last_name" : "Kandhal",
	    "email" : "poo@gmail.com",
	    "is_staff" : false,
	    "user_address" : "Mumbai",
        "is_superuser" : false,
        "role_name" : "438428eh32e",
        "phone_number" : "48372924366",
        "password" : "password",
    }
    Request Method: POST
    Response: {
        "message": "User SI Account added successfully."
    }
    """
    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        si_id = data.get('si_id',None)
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        user_si_obj = User_SI(
            user_id =  user_id,
            si_id =  si_id,
            first_name =  first_name,
            last_name =  last_name,
            username =  username,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_staff =  is_staff,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number
        )
        user_si_obj.set_password(data.get('password',None))
        user_si_obj.save()
        resp = "User SI Account added successfully."
    
        return resp
    except Exception as e:
        resp = "User SI account could not be created. "+str(e)
        return resp

def update_user_si_util(data):
    """
    Usage: API to update a user SI account.
    Request Parameters: {
	    "user_id": "bb98f0bb-a33e-4143-9885-5afc5342ba1d",
	    "first_name" : "Jinta",
	    "last_name" : "Mary Skariah",
	    "is_staff" : false,
	    "user_address" : "Alapuzzha",
	    "is_active" : true,
	    "is_superuser" : false,
	    "role_name" : "Manager",
	    "phone_number" : "7149383442"
    }
    Request Method: PATCH
    Response: {
        "message": "User SI Account updated successfully."
    }
    """
    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_staff = data.get('is_staff',None)
        is_superuser = data.get('is_superuser',None)
        #role_name = data.get('role_name',None)
        #phone_number = data.get('phone_number',None)
        user_si_obj = User_SI.objects.get(user_id=user_id)

        if user_si_obj:
            if first_name :
                user_si_obj.first_name=first_name
            if last_name :
                user_si_obj.last_name=last_name
            if user_address :
                user_si_obj.user_address=user_address
            if updated_at :
                user_si_obj.updated_at=updated_at
            if is_active :
                user_si_obj.is_active=is_active
            if is_staff :
                user_si_obj = user_si_obj.is_staff=is_staff
            if is_superuser :
                user_si_obj = user_si_obj.is_superuser=is_superuser

            user_si_obj.save()
            resp = "User SI Account updated successfully."
            return resp
        else:
            resp = "User SI account could not be updated. SI ID is not specified."
            return resp   
    except Exception as e:
        resp = "User SI account could not be updated. "+str(e)
        return resp

def delete_user_si_util(user_id):
    resp = {}
    try:
        User_si_obj = User_SI.objects.get(user_id=user_id)
        if User_si_obj:
            User_si_obj.is_deleted=True
            User_si_obj.save()
            resp = "User SI account deleted successfully."
            return resp
        else:
            resp = "User SI account could not be deleted. SI ID is not specified."
            return resp 
    except Exception as e:
        resp = "User SI account could not be deleted. "+str(e)
        return resp

def get_user_si_util(user_id):
    resp = {}
    try:
        User_si_obj = User_SI.objects.filter(user_id=user_id)
        User_si_obj_json = json.loads(serializers.serialize('json',User_si_obj))
        if len(User_si_obj_json) == 0:
            return []
        resp1 = User_si_obj_json[0]['fields']['user_ptr']
        user_obj = User.objects.filter(user_id=resp1)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        resp['user_id'] = str(resp1)
        return resp
    except Exception as e:
        resp = "User SI account could not be retrieved. "+str(e)
        return resp

def get_user_sis_util():
    resp = []
    user_list = []
    user_list_details = []
    try:
        User_si_obj = User_SI.objects.filter(is_deleted=False)
        for i in range(len(User_si_obj)):
            User_si_obj_json = json.loads(serializers.serialize('json',User_si_obj))
            User_si_obj_json = User_si_obj_json[i]
            resp.append(User_si_obj_json)
        for i in resp:
            user_list.append(i['fields']['user_ptr'])
            
        for i in user_list:
        

            user_obj = User.objects.filter(user_id=i)
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            resp = user_obj_json[0]['fields']
            
            resp['user_id'] = str(i)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user SI accounts. "+str(e)
        return resp
        

################################################################CLIENT CRUDS################################################################

def add_client_account_util(data):
    """
    Usage: API to add a client account.
    Request Parameters: {
	    "client_name" : "Cataler",
	    "client_license_key" : "sdwej9883",
	    "client_role" : "Role1",
	    "assigned_to" : "Client_User1",
	    "client_address" : "Chennai"
    }
    Request Method: POST
    Response: {
        "message": "Client Account added successfully."
    }
    """
    resp = {}
    try:
        client_id = str(uuid.uuid4())
        client_name = data.get('client_name',None)
        client_license_key = data.get('client_license_key',None)
        client_role = data.get('client_role',None)
        assigned_to = data.get('assigned_to',None)
        client_address = data.get('client_address',None)

        is_deleted = False

        client_obj = Client(
            client_id = client_id,
            client_name = client_name,
            client_license_key = client_license_key,
            client_role = client_role,
            assigned_to = assigned_to,
            client_address = client_address,
            is_deleted = is_deleted
        )
        client_obj.save()
        resp = "Client Account added successfully."
        return resp
    except Exception as e:
        resp = "Client account could not be created. "+str(e)
        return resp


def get_client_account_util(client_id):
    """
    Usage: API to get details of a client account.
    Request Parameters: client_id
    Request Method: GET
    Response: {
        "client_id": "009aaf6d-bc78-41b0-ae97-3fd20e6d1874",
        "client_name": "Client3",
        "client_license_key": "sdwej9883",
        "client_role": "manager",
        "assigned_to": "User2",
        "client_address": "Chennai",
        "is_deleted": false

    }
    """
    resp = {}
    try:
        client_obj = Client.objects.filter(client_id=client_id)
        client_obj_json = json.loads(serializers.serialize('json',client_obj))
        resp = client_obj_json[0]['fields']
        return resp
    except Exception as e:
        resp = "Client account could not be retrieved. "+str(e)
        return resp


def update_client_account_util(data):
    """
    Usage: API to update a client account.
    Request Parameters: {
        "client_id": "009aaf6d-bc78-41b0-ae97-3fd20e6d1874"
	    "client_name" : "Client3",
	    "client_license_key" : "sdwej9883",
	    "client_role" : "manager",
	    "assigned_to" : "User2",
	    "client_address" : "Chennai"
    }
    Request Method: PATCH
    Response: {
        "message": "Client Account updated successfully."
    }
    """
    resp = {}
    try:
        client_id = data.get('client_id',None)
        client_name = data.get('client_name',None)
        client_license_key = data.get('client_license_key',None)
        client_role = data.get('client_role',None)
        assigned_to = data.get('assigned_to',None)
        client_address = data.get('client_address',None)
        client_obj = Client.objects.filter(client_id=client_id)
        if client_obj:
            if client_name:
                client_obj.update(client_name=client_name)
            if client_license_key:
                client_obj.update(client_license_key=client_license_key)
            if client_role:
                client_obj.update(client_role=client_role)
            if assigned_to:
                client_obj.update(assigned_to=assigned_to)
            if client_address:
                client_obj.update(client_address=client_address)
            resp = "Client Account updated successfully."
            return resp
        else:
            resp = "Client account could not be updated. Client ID is not specified."
            return resp   
    except Exception as e:
        resp = "Client account could not be updated. "+str(e)
        return resp


def delete_client_account_util(client_id):
    """
    Usage: API to delete a client account.
    Request Parameters: client_id
    Request Method: DELETE
    Response: {
        "message": "Client Account deleted successfully."
    }
    """
    resp = {}
    try:
        client_obj = Client.objects.filter(client_id=client_id)
        if client_obj:
            client_obj.update(is_deleted=True)

            resp = "Client account deleted successfully."
            return resp
        else:
            resp = "Client account could not be deleted. Client ID is not specified."
            return resp 
    except Exception as e:
        resp = "Client account could not be deleted. "+str(e)
        return resp


def get_all_client_accounts_util():
    """
    Usage: API to get all the existing client accounts.
    Request Parameters: None
    Request Method: GET
    Response: List of all client accounts.
    [{
        "client_id": "c2",
        "client_name": "Client2",
        "client_license_key": "sdwej9883",
        "client_role": "manager",
        "assigned_to": "User2",
        "client_address": "Chennai",
        "is_deleted": false
    }]
    """
    resp = []
    try:
        client_obj = Client.objects.filter(is_deleted=False)
        for i in range(len(client_obj)):
            client_obj_json = json.loads(serializers.serialize('json',client_obj))
            client_obj_json = client_obj_json[i]
            resp.append(client_obj_json)
        return resp
    except Exception as e:
        resp = "Could not retrieve all the existing client accounts. "+str(e)
        return resp


################################################################SI CRUDS################################################################
def add_si_account_util(data):
    """
    Usage: API to add a client account.
    Request Parameters: {
        "client_name" : "Client3",
        "client_license_key" : "sdwej9883",
        "client_role" : "manager",
	    "assigned_to" : "User2",
	    "client_address" : "Chennai",
        "activeClients" : "dewqdewq",
        "license_key_list" : "qewerade"
    }
    Request Method: POST
    Response: {
        "message": "SI Account added successfully."
    }
    """
    resp = {}
    try:
        client_id = str(uuid.uuid4())
        client_name = data.get('client_name',None)
        client_license_key = data.get('client_license_key',None)
        client_role = data.get('client_role',None)
        assigned_to = data.get('assigned_to',None)
        client_address = data.get('client_address',None)
        is_deleted = False
        activeClients = data.get('activeClients',None)
        license_key_list = data.get('license_key_list',None)
        si_obj = SI(
            client_id = client_id,
            client_name = client_name,
            client_license_key = client_license_key,
            client_role = client_role,
            assigned_to = assigned_to,
            client_address = client_address,
            is_deleted = is_deleted,
            activeClients = activeClients,
            license_key_list = license_key_list
            )
        si_obj.save()
        resp = "SI Account added successfully."
        return resp
    except Exception as e:
        resp = "SI account could not be created. "+str(e)
        return resp


def get_si_account_util(client_id):
    """
    Usage: API to get details of a client account.
    Request Parameters: client_id
    Request Method: GET
    Response: {
        "client_ptr": "2fdafd13-1839-4484-a705-a8c85e2852b5",
        "activeClients": "Cataler",
        "license_key_list": "qewerade"
    }
    """
    resp = {}
    try:
        si_obj = SI.objects.filter(client_id=client_id)
        si_obj_json = json.loads(serializers.serialize('json',si_obj))
        resp = si_obj_json[0]['fields']
        return resp
    except Exception as e:
        resp = "SI account could not be retrieved. "+str(e)
        return resp


def update_si_account_util(data):
    """
    Usage: API to update a client account.
    Request Parameters: {
	    "client_name" : "Client3",
	    "client_license_key" : "sdwej9883",
	    "client_role" : "manager",
	    "assigned_to" : "User2",
	    "client_address" : "Chennai",
        "client_id": "hdeyr734-3437-sde-r34f-wfwrr423d34",
        "activeClients" : "dewqdewq",
        "license_key_list" : "qewerade"
    }
    Request Method: PATCH
    Response: {
        "message": "Client Account updated successfully."
    }
    """
    resp = {}
    try:
        client_name = data.get('client_name',None)
        client_license_key = data.get('client_license_key',None)
        client_role = data.get('client_role',None)
        assigned_to = data.get('assigned_to',None)
        client_address = data.get('client_address',None)
        client_id = data.get('client_id',None)
        activeClients = data.get('activeClients',None)
        license_key_list = data.get('license_key_list',None)
        si_obj = SI.objects.get(client_id=client_id)
        if si_obj:
            if client_name:
                si_obj.client_name=client_name
            if client_license_key:
                si_obj.client_license_key=client_license_key
            if client_role:
                si_obj.client_role=client_role
            if assigned_to:
                si_obj.assigned_to=assigned_to
            if client_address:
                si_obj.client_address=client_address
            if activeClients:
                si_obj.activeClients=activeClients
            if license_key_list:
                si_obj.license_key_list=license_key_list
            si_obj.save()
            resp = "SI Account updated successfully."
            return resp
        else:
            resp = "SI account could not be updated. SI ID is not specified."
            return resp   
    except Exception as e:
        resp = "SI account could not be updated. "+str(e)
        return resp


def delete_si_account_util(client_id):
    """
    Usage: API to delete a SI account.
    Request Parameters: client_id
    Request Method: DELETE
    Response: {
        "message": "SI Account deleted successfully."
    }
    """
    resp = {}
    try:
        si_obj = SI.objects.get(client_id=client_id)
        if si_obj:
            si_obj.is_deleted=True
            si_obj.save()
            resp = "SI account deleted successfully."
            return resp
        else:
            resp = "SI account could not be deleted. SI ID is not specified."
            return resp 
    except Exception as e:
        resp = "SI account could not be deleted. "+str(e)
        return resp


def get_all_si_accounts_util():
    """
    Usage: API to get all the existing SI accounts.
    Request Parameters: None
    Request Method: GET
    Response: List of all SI accounts.
    [{
        "client_ptr": "2fdafd13-1839-4484-a705-a8c85e2852b5",
        "activeClients": "Cataler1",
        "license_key_list": "je822112"
    }]
    """
    resp = []
    try:
        si_obj = SI.objects.filter(is_deleted=False)
        for i in range(len(si_obj)):
            si_obj_json = json.loads(serializers.serialize('json',si_obj))
            si_obj_json = si_obj_json[i]['fields']
            resp.append(si_obj_json)
        return resp
    except Exception as e:
        resp = "Could not retrieve all the existing SI accounts. "+str(e)
        return resp







####### ai side of things....


################################################################supervisor_CRUDS#####################################################################

def add_user_supervisor_util(data):

    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        supervisor_id = data.get('supervisor_id',None)
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        user_supervisor_obj = User_Supervisor(
            user_id =  user_id,
            supervisor_id =  supervisor_id,
            first_name =  first_name,
            last_name =  last_name,
            username =  username,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_staff =  is_staff,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number
        )
        user_supervisor_obj.set_password(data.get('password',None))
        user_supervisor_obj.save()
        resp = "User Supervisor Account added successfully."
    
        return resp
    except Exception as e:
        resp = "User Supervisor account could not be created. "+str(e)
        return resp

def update_user_supervisor_util(data):

    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_staff = data.get('is_staff',None)
        is_superuser = data.get('is_superuser',None)
        #role_name = data.get('role_name',None)
        #phone_number = data.get('phone_number',None)
        user_supervisor_obj = User_Supervisor.objects.get(user_id=user_id)

        if user_supervisor_obj:
            if first_name :
                user_supervisor_obj.first_name=first_name
            if last_name :
                user_supervisor_obj.last_name=last_name
            if user_address :
                user_supervisor_obj.user_address=user_address
            if updated_at :
                user_supervisor_obj.updated_at=updated_at
            if is_active :
                user_supervisor_obj.is_active=is_active
            if is_staff :
                user_supervisor_obj = user_supervisor_obj.is_staff=is_staff
            if is_superuser :
                user_supervisor_obj = user_supervisor_obj.is_superuser=is_superuser

            user_supervisor_obj.save()
            resp = "User supervisor Account updated successfully."
            return resp
        else:
            resp = "User supervisor account could not be updated. supervisor id is not specified."
            return resp   
    except Exception as e:
        resp = "User supervisor account could not be updated. "+str(e)
        return resp

def delete_user_supervisor_util(user_id):
    resp = {}
    try:
        user_supervisor_obj = User_Supervisor.objects.get(user_id=user_id)
        if user_supervisor_obj:
            user_supervisor_obj.is_deleted=True
            user_supervisor_obj.save()
            resp = "User supervisor account deleted successfully."
            return resp
        else:
            resp = "User supervisor account could not be deleted. supervisor ID is not specified."
            return resp 
    except Exception as e:
        resp = "User supervisor account could not be deleted. "+str(e)
        return resp

def get_user_supervisor_util(user_id):
    resp = {}
    try:
        user_supervisor_obj = User_Supervisor.objects.filter(user_id=user_id)
        user_supervisor_obj_json = json.loads(serializers.serialize('json',user_supervisor_obj))
        #print(user_supervisor_obj_json)
        if len(user_supervisor_obj_json) == 0:
            return []
        resp1 = user_supervisor_obj_json[0]['fields']['user_ptr']
        user_obj = User.objects.filter(user_id=resp1)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        resp['user_id'] = str(resp1)
        return resp
    except Exception as e:
        resp = "User supervisor account could not be retrieved. "+str(e)
        return resp

def get_user_supervisors_util():
    resp = []
    user_list = []
    user_list_details = []
    try:
        user_supervisor_obj = User_Supervisor.objects.filter(is_deleted=False)
        for i in range(len(user_supervisor_obj)):
            user_supervisor_obj_json = json.loads(serializers.serialize('json',user_supervisor_obj))
            
            user_supervisor_obj_json = user_supervisor_obj_json[i]
            resp.append(user_supervisor_obj_json)
            
        for i in resp:
            user_list.append(i['fields']['user_ptr'])
        #print(resp)
        for i in user_list:
        
            #print(i)
            user_obj = User.objects.filter(user_id=i)
            
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            #print(user_obj_json)
            resp = user_obj_json[0]['fields']
            
            resp['user_id'] = str(i)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user supervisor accounts. "+str(e)
        return resp



################################################################line_manager_CRUDS#####################################################################

def add_user_line_manager_util(data):

    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        line_manager_id = data.get('line_manager_id',None)
        
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        user_line_manager_obj = User_Line_Manager(
            user_id =  user_id,
            line_manager_id =  line_manager_id,

            first_name =  first_name,
            last_name =  last_name,
            username =  username,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_staff =  is_staff,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number
        )
        user_line_manager_obj.set_password(data.get('password',None))
        user_line_manager_obj.save()
        resp = "User line_manager Account added successfully."
    
        return resp
    except Exception as e:
        resp = "User line_manager account could not be created. "+str(e)
        return resp

def update_user_line_manager_util(data):

    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_staff = data.get('is_staff',None)
        is_superuser = data.get('is_superuser',None)
        #role_name = data.get('role_name',None)
        #phone_number = data.get('phone_number',None)
        user_line_manager_obj = User_Line_Manager.objects.get(user_id=user_id)

        if user_line_manager_obj:
            if first_name :
                user_line_manager_obj.first_name=first_name
            if last_name :
                user_line_manager_obj.last_name=last_name
            if user_address :
                user_line_manager_obj.user_address=user_address
            if updated_at :
                user_line_manager_obj.updated_at=updated_at
            if is_active :
                user_line_manager_obj.is_active=is_active
            if is_staff :
                user_line_manager_obj = user_line_manager_obj.is_staff=is_staff
            if is_superuser :
                user_line_manager_obj = user_line_manager_obj.is_superuser=is_superuser
            user_line_manager_obj.save()
            resp = "User line_manager Account updated successfully."
            return resp
        else:
            resp = "User line_manager account could not be updated. line_manager id is not specified."
            return resp   
    except Exception as e:
        resp = "User line_manager account could not be updated. "+str(e)
        return resp

def delete_user_line_manager_util(user_id):
    resp = {}
    try:
        user_line_manager_obj = User_Line_Manager.objects.get(user_id=user_id)
        if user_line_manager_obj:
            user_line_manager_obj.is_deleted=True
            user_line_manager_obj.save()
            resp = "User line_manager account deleted successfully."
            return resp
        else:
            resp = "User line_manager account could not be deleted. line_manager ID is not specified."
            return resp 
    except Exception as e:
        resp = "User line_manager account could not be deleted. "+str(e)
        return resp

def get_user_line_manager_util(user_id):
    resp = {}
    try:
        user_line_manager_obj = User_Line_Manager.objects.filter(user_id=user_id)
        user_line_manager_obj_json = json.loads(serializers.serialize('json',user_line_manager_obj))
        #print(user_line_manager_obj_json)
        if len(user_line_manager_obj_json) == 0:
            return []
        resp1 = user_line_manager_obj_json[0]['fields']['user_ptr']
        user_obj = User.objects.filter(user_id=resp1)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        resp['user_id'] = str(resp1)
        return resp
    except Exception as e:
        resp = "User line_manager account could not be retrieved. "+str(e)
        return resp

def get_user_line_managers_util():
    resp = []
    user_list = []
    user_list_details = []
    try:
        user_line_manager_obj = User_Line_Manager.objects.filter(is_deleted=False)
        for i in range(len(user_line_manager_obj)):
            user_line_manager_obj_json = json.loads(serializers.serialize('json',user_line_manager_obj))
            
            user_line_manager_obj_json = user_line_manager_obj_json[i]
            resp.append(user_line_manager_obj_json)
            
        for i in resp:
            user_list.append(i['fields']['user_ptr'])
        #print(resp)
        for i in user_list:
        
            #print(i)
            user_obj = User.objects.filter(user_id=i)
            
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            #print(user_obj_json)
            resp = user_obj_json[0]['fields']
            
            resp['user_id'] = str(i)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user line_manager accounts. "+str(e)
        return resp




################################################################operator_CRUDS#####################################################################

def add_user_operator_util(data):

    resp = {}
    try:
        user_id = str(uuid.uuid4()) 
        operator_id = data.get('operator_id',None)
        
        username = data.get('username',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        is_staff = data.get('is_staff',None)
        email = data.get('email',None)
        user_address = data.get('user_address',None)
        date_joined = timezone.now()
        updated_at = timezone.now()
        is_deleted = False
        is_active = True
        is_superuser = data.get('is_superuser',None)
        role_name = data.get('role_name',None)
        phone_number = data.get('phone_number',None)
        user_operator_obj = User_Operator(
            user_id =  user_id,
            operator_id =  operator_id,

            first_name =  first_name,
            last_name =  last_name,
            username =  username,
            email =  email,
            user_address =  user_address,
            date_joined =  date_joined,
            updated_at =  updated_at,
            is_deleted =  is_deleted,
            is_active =  is_active,
            is_staff =  is_staff,
            is_superuser =  is_superuser,
            role_name =  role_name,
            phone_number =  phone_number
        )
        user_operator_obj.set_password(data.get('password',None))
        user_operator_obj.save()
        resp = "User operator Account added successfully."
    
        return resp
    except Exception as e:
        resp = "User operator account could not be created. "+str(e)
        return resp

def update_user_operator_util(data):

    resp = {}
    try:
        user_id = data.get('user_id',None)
        first_name = data.get('first_name',None)
        last_name = data.get('last_name',None)
        user_address = data.get('user_address',None)
        updated_at = timezone.now()
        is_active = data.get('is_active',None)
        is_staff = data.get('is_staff',None)
        is_superuser = data.get('is_superuser',None)
        #role_name = data.get('role_name',None)
        #phone_number = data.get('phone_number',None)
        user_operator_obj = User_Operator.objects.get(user_id=user_id)

        if user_operator_obj:
            if first_name :
                user_operator_obj.first_name=first_name
            if last_name :
                user_operator_obj.last_name=last_name
            if user_address :
                user_operator_obj.user_address=user_address
            if updated_at :
                user_operator_obj.updated_at=updated_at
            if is_active :
                user_operator_obj.is_active=is_active
            if is_staff :
                user_operator_obj = user_operator_obj.is_staff=is_staff
            if is_superuser :
                user_operator_obj = user_operator_obj.is_superuser=is_superuser

            user_operator_obj.save()
            resp = "User operator Account updated successfully."
            return resp
        else:
            resp = "User operator account could not be updated. operator id is not specified."
            return resp   
    except Exception as e:
        resp = "User operator account could not be updated. "+str(e)
        return resp

def delete_user_operator_util(user_id):
    resp = {}
    try:
        user_operator_obj = User_Operator.objects.get(user_id=user_id)
        if user_operator_obj:
            user_operator_obj.is_deleted=True
            user_operator_obj.save()
            resp = "User operator account deleted successfully."
            return resp
        else:
            resp = "User operator account could not be deleted. operator ID is not specified."
            return resp 
    except Exception as e:
        resp = "User operator account could not be deleted. "+str(e)
        return resp

def get_user_operator_util(user_id):
    resp = {}
    try:
        user_operator_obj = User_Operator.objects.filter(user_id=user_id)
        user_operator_obj_json = json.loads(serializers.serialize('json',user_operator_obj))
        #print(user_operator_obj_json)
        if len(user_operator_obj_json) == 0:
            return []
        resp1 = user_operator_obj_json[0]['fields']['user_ptr']
        user_obj = User.objects.filter(user_id=resp1)
        user_obj_json = json.loads(serializers.serialize('json',user_obj))
        resp = user_obj_json[0]['fields']
        resp['user_id'] = str(resp1)
        return resp
    except Exception as e:
        resp = "User operator account could not be retrieved. "+str(e)
        return resp

def get_user_operators_util():
    resp = []
    user_list = []
    user_list_details = []
    try:
        user_operator_obj = User_Operator.objects.filter(is_deleted=False)
        for i in range(len(user_operator_obj)):
            user_operator_obj_json = json.loads(serializers.serialize('json',user_operator_obj))
            
            user_operator_obj_json = user_operator_obj_json[i]
            resp.append(user_operator_obj_json)
            
        for i in resp:
            user_list.append(i['fields']['user_ptr'])
        #print(resp)
        for i in user_list:
        
            #print(i)
            user_obj = User.objects.filter(user_id=i)
            
            user_obj_json = json.loads(serializers.serialize('json',user_obj))
            #print(user_obj_json)
            resp = user_obj_json[0]['fields']
            
            resp['user_id'] = str(i)
            
            user_list_details.append(resp)


        return user_list_details
    except Exception as e:
        resp = "Could not retrieve all the existing user operator accounts. "+str(e)
        return resp





## i will contect to aws mongo for api integration
# no wait bcz have to install it now at any condition

###########################################################User based Authentication APIS###################################################
    
def login_user_util(data,request):

  
    message = ""
    email = data.get('email',None)
    password = data.get('password',None)
    workstation_id = data.get('workstation_name',None)
    #print("workstation_id::::::",workstation_id)
    if not email or not password:
        return "MissingField"
    else:
        try:
            user = authenticate(email=email, password=password)
            #print("user found::::::",user)
            
            if user:
                ##print("user::::::",user)
                token, _ = Token.objects.get_or_create(user=user)
               
                user_object = {str(i.name):getattr(user, i.name) for i in user._meta.fields}
                ##print("user_object::::::",user_object)
                del user_object['password'] 
                user_object['token'] = str(token)
                
                user_object['all_permissions'] = throw_permission(user_object['role_name'])

                #cc = CacheHelper()
                #user_id = user_object['user_id']
                print("user role name::::::",user_object['role_name'])
                #user_id_key = RedisKeyBuilderServer(workstation_id).get_key(0, 'user_id_key')
                ##print("user_id_key::::::",user_id_key)
                #cc.set_json({user_id_key : user_id}) 
                # #print("token::::",token)
                user_object['show_camera_restart_login'] = True
                user_object['show_camera_restart_workstations'] = True
                return user_object
            else:
                return "AuthError"
        except Exception as e:
            #print(e)
            return "AuthError"
    

def change_password_util(data,request):

    user_ip_old_password = data.get('old_password',None)
    new_password = data.get('new_password',None)
    reenter_new_password = data.get('reenter_new_password',None)
    
    username = request.user.username
    
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    u = User.objects.get(username=username)
    

    if u.check_password(user_ip_old_password) is False:
        message = "Invalid Old Password"
        message1 = 'fail'
        return message,message1
        
    if str(new_password) == str(user_ip_old_password):
        message = "New password cannot be same as old password"
        message1 = 'fail'
        return message,message1
    if str(new_password) != str(reenter_new_password):
        message = "password doesn't match"
        message1 = 'fail'
        return message,message1   
           

    u.set_password(new_password)
    u.save()
    
    message = "Password Changed, Please logout and relogin"
    message1 = 'pass'
    return message,message1
    
    
    


def login_supervisor_util(data):
    message = ""
    email = data.get('email',None)
    password = data.get('password',None)
    workstation_name = data.get('workstation_name',None)
    if not email or not password or not workstation_name:
        return "MissingField"
    else:
        try:
            user = authenticate(email=email, password=password)
            if user:
                if user.role_name == "Supervisor":
                    user_obj = {
                        'user_id' : user.user_id,
                        'first_name' : user.first_name,
                        'last_name' : user.last_name,
                        'username' : user.username,
                        'role_name' : user.role_name,
                        'email' : user.email,
                        'user_address' : user.user_address,
                        'date_joined' : str(user.date_joined),
                        'updated_at' : str(user.updated_at),
                        'is_active' : user.is_active,
                        'is_superuser' : user.is_superuser,
                        'phone_number' : user.phone_number,
                    }
                    return user_obj
                else:
                    return "AuthError"
            else:
                return "AuthError"
        except Exception as e:
            return str(e)



'''def logout_user_util(data):
    if request.method == 'POST':
    	logout(data)
    	return HttpResponse(json.dumps({'redirect': '/'}), content_type="application/json")
    else:
    	return HttpResponseBadRequest(json.dumps({'error': 'Method type not allowed'}), content_type='application/json')
'''

