from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Usage: Class representation of User Schema.
    Attributes: user_id (str): unique id of the user.
                first_name (str): first name of the user.
                last_name (str): last name of the user.
                user_address (str): Address of the user.
                created_at (datetime): Date and time of creation of the user account.
                updated_at (datetime): Date and time of updation of the user account.
                is_deleted (boolean): soft delete for the user, user deleted or not.
                username (str): unique username of the user.
                email (str): unique email-id of the user.
                is_active (boolean): user is active or not.
                is_superuser (boolean): user is superuser or not.
                role_name (str): Role ID of the user.
                phone_number (str): Phone Number of the user.
    """
    ROLES = (
        ('operator', 'operator'),
        ('sys admin', 'sys admin'),
        ('supervisor', 'supervisor'),
        ('production supervisor', 'production supervisor'),
        ('master','master'),
    )
    user_id = models.CharField(max_length = 50, primary_key=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length = 50, unique=True)
    email = models.CharField(max_length = 50, unique=True)
    user_address = models.CharField(max_length = 50)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    role_name = models.CharField(max_length = 50, choices=ROLES, null=False)
    phone_number = models.CharField(max_length = 50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    #def __str__(self):
        #return self.username+'_'+self.role_name

    class Meta: 
        #Add verbose name 
        verbose_name = 'User List'
        #permissions = (("can_add_si", "can_add_si"), ("can_update_si","can_update_si"), ("can_get_si","can_get_si"), ("can_get_sis","can_get_sis"),("can_delete_si","can_delete_si"))


class User_Master(User):
    #master = models.ForeignKey('User_Master',on_delete=models.DO_NOTHING)
    master_id = models.CharField(max_length=50, unique=True,primary_key=True)
    #master_name = models.CharField(max_length=50)
    #master_address = models.CharField(max_length=500)
    #is_deleted = models.BooleanField(default=False)
    
    class Meta: 
        #Add verbose name 
        verbose_name = 'User: Master List'
        #permissions = (("can_add_si", "can_add_si"), ("can_update_si","can_update_si"), ("can_get_si","can_get_si"), ("can_get_sis","can_get_sis"),("can_delete_si","can_delete_si"),)


class User_Admin(User):
    #master = models.ForeignKey('User_Master',on_delete=models.DO_NOTHING)
    admin_id = models.CharField(max_length=50, unique=True,primary_key=True)
    #master_name = models.CharField(max_length=50)
    #master_address = models.CharField(max_length=500)
    #is_deleted = models.BooleanField(default=False)
    
    class Meta:
        #Add verbose name 
        verbose_name = 'User: Admin List'
        #permissions = (("can_add_si", "can_add_si"), ("can_update_si","can_update_si"), ("can_get_si","can_get_si"), ("can_get_sis","can_get_sis"),("can_delete_si","can_delete_si"),)
    
class User_Business_Manager(User):
    business_manager_id = models.CharField(max_length=50, unique=True,primary_key=True)
    
    class Meta:
        #Add verbose name 
        verbose_name = 'User: Business_Manager List'

class User_Sales_Executive(User):
    sales_executive_id = models.CharField(max_length=50, unique=True,primary_key=True)
    created_by = models.CharField(max_length=50, unique=False,primary_key=False)
    class Meta:
        #Add verbose name 
        verbose_name = 'User: Sales_Executive List'
        
class User_Client(User):
    """
    Usage: Class representation of User_Client Schema which extends User Schema.

    Attributes: client (foreign key reference): reference to Client Schema.
                client_user_manager (str): Manager of the client.
                is_client_admin (boolean): Sets true if the client user is admin else sets it as false.
                is_system_integrator (boolean): Constant, always set as false for User_client.
    """
    client = models.ForeignKey("Client",on_delete=models.DO_NOTHING)
    client_user_manager = models.CharField(max_length = 50)
    is_client_admin = models.BooleanField(default=False)
    is_system_integrator = models.BooleanField(default=False)

    class Meta: 
        #Add verbose name 
        verbose_name = 'User: Client List'
        


class User_SI(User):
    """
    Usage: Class representation of User_SI (System Integration) Schema which extends User Schema.

    Attributes: si (foreign key reference): reference to SI Schema.
                is_system_integrator (boolean): Constant, always set as True for User_SI.
    """
    #si = models.ForeignKey('SI',on_delete=models.DO_NOTHING)
    #is_system_integrator = models.BooleanField(default=True)
    si_id = models.CharField(max_length=50, unique=True,primary_key=True)

    class Meta: 
        #Add verbose name 
        verbose_name = 'User: SI List'


class Client(models.Model):
    """
    Usage: Class representation of Client Schema.
    Attributes: client_id (str): unique id of the client.
                client_name (str): name of the client.
                client_license_key (str): license key of the client.
                client_role (str): role of the client.
                assigned_to (str): the user's id of the user who is assigned with the license.
                client_address (str): address of the client.
                is_deleted (boolean): soft delete, when client doesn't exist anymore.
    Methods: 

    """
    client_id = models.CharField(max_length=50, unique=True,primary_key=True)
    client_name = models.CharField(max_length=50)
    client_license_key = models.CharField(max_length=100)
    client_role = models.CharField(max_length=50)
    assigned_to = models.CharField(max_length=50)
    client_address = models.CharField(max_length=500)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.client_name

    class Meta: 
        #Add verbose name 
        verbose_name = 'Client List'


class SI(Client):
    """
    Usage: Class representation of SI (System Integration) Clients Schema which extends Client Schema.
    Attributes: si_id (str): unique id of the SI.
                activeClients (str): list of active clients handled by the SI.
                license_key_list (str): list of license keys handled by the SI.
    Methods: 
    """
    activeClients = models.CharField(max_length = 200)
    license_key_list = models.CharField(max_length = 200)
        
    class Meta: 
        #Add verbose name 
        verbose_name = 'Client: SI List'






class User_Supervisor(User):
    supervisor_id = models.CharField(max_length=50, unique=True,primary_key=True)
    class Meta: 
        verbose_name = 'User: Supervisor List'
        
class User_Line_Manager(User):
    line_manager_id = models.CharField(max_length=50, unique=True,primary_key=True)
    class Meta: 
        verbose_name = 'User: Line_Manager List'

class User_Operator(User):
    operator_id = models.CharField(max_length=50, unique=True,primary_key=True)
    class Meta: 
        verbose_name = 'User: Operator List'
        


