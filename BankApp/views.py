from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
from .models import Customer, Account ,Admin, Contact
from django.contrib import messages

# Create your views here.
def home(request):
    session_info="no"
    admin_session_info="no"
    #This if else is used to check whether session in present,so it should not display login and register tab.
    #If user session is not present i.e user has logged out it should display login and register tab.
    
    if 'admin_id' in request.session:
        admin_session_info="present"
    if 'customer_id' in request.session:
        session_info="present"
        customer_id=int(request.session['customer_id'])
        #print("entered")
        #print(customer_id)
        customer=Customer.objects.filter(customer=customer_id)
        cust=''
        for cust in customer:
            cust1=cust

        return render(request,'home.html',{'customer':cust1,'session_info':session_info,'admin_session_info':admin_session_info})
    else:
        return render(request,'home.html',{'session_info':session_info,'admin_session_info':admin_session_info})
    
def register(request):
    if request.method == 'POST':
        
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        gender=request.POST['gender']
        age=request.POST['age']
        address=request.POST['address']
        email=request.POST['email']
        password=request.POST['password']
        cust_id_obj=Customer.objects.last()
        if cust_id_obj==None:
            cust_id=0
        else:
            cust_id=int(cust_id_obj.customer)
        if(Customer.objects.filter(email=email).exists()):
            #messages.info(request,"Registration Unsucessfull")
            #messages.info(request,"Email already Exists.   Try with different email..")
            #return redirect('register')
            return render(request,'register.html',{'message1':'Registration Unsucessfull',\
            'message2':'Email already Exists','message3':'(Try with different email..)'})
            
        else:
            cust_id=cust_id+1
            
            customer_obj=Customer.objects.create(fname=fname,lname=lname,gender=gender,age=age,\
            address=address,email=email,password=password,customer=cust_id)
            customer_obj.save()
            account=Account.objects.create(customer=Customer.objects.get(customer=cust_id))
            account.save()
            #messages.info(request,"Registered sucessfully!!!")
            #return redirect('register')
            return render(request,'register.html',{'message':'Registered Sucessfully'})
    else:
        return render(request,'register.html')
    return redirect('register.html')

def login(request):
    session_info="no"
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        customer=Customer.objects.filter(email=email,password=password)
        cust=''
        for cust in customer:
            cust1=cust
        
        if(customer.exists()):
            request.session['customer_id'] = cust1.customer
            return render(request,'customer.html',{'customer':cust1})
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    #This elif is used to check whether session in present,so it should not display login and register tab.
    #and directly display customer.html page ...i.e customer info page.
    #If user session is not present i.e user has logged out it should display login page.
    
    elif 'customer_id' in request.session:
        session_info="present"
        customer_id=int(request.session['customer_id'])
        #print("entered")
        #print(customer_id)
        customer=Customer.objects.filter(customer=customer_id)
        cust=''
        for cust in customer:
            cust1=cust

        return render(request,'customer.html',{'customer':cust1,'session_info':session_info})

    else:
        return render(request,'login.html',{'session_info':session_info})
    return render(request,'login.html',{'session_info':session_info})


def logout(request):
    try:
        if(request.session['customer_id']):
            del request.session['customer_id']
        return redirect('/')
    except KeyError:
        print("Not deleted")
    return redirect('/')

def add_account(request):
    customer_id=request.session['customer_id']
    if request.method == 'POST':
        customer_id=int(customer_id)
        account_type=request.POST['account_type']
        account_balance=request.POST['balance']
        saving_acc=''
        s_balance=0
        fixed_acc=''
        f_balance=0
        if(account_type=='saving'):
            saving_acc='S'+str(customer_id)
            s_balance=int(account_balance)
            add_acc=Account.objects.filter(customer=customer_id).update(saving_acc=saving_acc,s_balance=s_balance)
        elif(account_type=='fixed'):
            fixed_acc='F'+str(customer_id)
            f_balance=int(account_balance)
            add_acc=Account.objects.filter(customer=customer_id).update(fixed_acc=fixed_acc,f_balance=f_balance)
        return render(request,'add_account.html',{'disp_msg':'Account created sucessfully!!'})
    else:
        accounts=Account.objects.filter(customer=customer_id)
        account=0
        msg=''
        display='both'
        for account in accounts:
            if((account.saving_acc is not None) and (account.fixed_acc is not None)):
                msg=msg+'Both accounts are already created. '
                display='no'
            elif((account.saving_acc is not None)):
                msg=msg+'Saving account is already created. '
                display='fixed'
            elif((account.fixed_acc is not None)):
                msg=msg+'Fixed account is already created. '
                display='saving'
        return render(request,'add_account.html',{'message':msg,'display':display,'customer_id':customer_id})

def acc_details(request):
    customer_id=request.session['customer_id']
    customers=Customer.objects.filter(customer=customer_id)
    accounts=Account.objects.filter(customer=customer_id)
    for cust in customers:
        customer=cust
    for acc in accounts:
        account=acc
    return render(request,'acc_details.html',{'customer':customer,'account':account})

def transaction(request):
    customer_id=0
    # to check whether session exists.
    if 'customer_id' in request.session:
        customer_id=request.session['customer_id']
    else:
        print("Session does not exists")

    accounts=Account.objects.filter(customer=customer_id)
    if request.method == 'POST':
        acc_type=request.POST['account']
        tran_type=request.POST['transaction_type']
        amount=request.POST['t_amount']
        for acc in accounts:
            account=acc
        s_balance=int(account.s_balance)
        f_balance=int(account.f_balance)
        msg1=''
        if acc_type=="saving":
            if account.saving_acc is not None:
                if tran_type=="credit":
                    s_balance=s_balance+int(amount)
                else:
                    s_balance=s_balance-int(amount)
                if s_balance<1000:
                    msg1="Transaction Unsucessfull...Saving account does not have balance more than 1000.It is necessary to keep minimum Rs 1000 in account"
                    return render(request,'transaction.html',{'msg1':msg1})
                else:
                    Account.objects.filter(customer=customer_id).update(s_balance=s_balance)
            else:
                msg1="Transaction Unsucessfull...Saving account does not exists."
                return render(request,'transaction.html',{'msg1':msg1})
        else:
            if account.fixed_acc is not None:
                f_balance=f_balance+int(amount)
                Account.objects.filter(customer=customer_id).update(f_balance=f_balance)
            else:
                msg1="Transaction Unsucessfull...Fixed account does not exists."
                return render(request,'transaction.html',{'msg1':msg1})
        return render(request,'transaction.html',{'msg':'Transaction Sucessfull'})
    else:
        for acc in accounts:
            account=acc
        return render(request,'transaction.html',{'account':account})

def branches(request):
    #This if else is used to check whether session in present,so it should not display login and register tab.
    #If user session is not present i.e user has logged out it should display login and register tab.
    session_info="no"
    admin_session_info="no"
    if 'admin_id' in request.session:
        admin_session_info="present"
    
    if 'customer_id' in request.session:
        session_info="present"
        customer_id=int(request.session['customer_id'])
        #print("entered")
        #print(customer_id)
        customer=Customer.objects.filter(customer=customer_id)
        cust=''
        for cust in customer:
            cust1=cust

        return render(request,'branches.html',{'customer':cust1,'session_info':session_info,'admin_session_info':admin_session_info})
    else:    
        return render(request,'branches.html',{'session_info':session_info,'admin_session_info':admin_session_info})

def about(request):
    #This if else is used to check whether session in present,so it should not display login and register tab.
    #If user session is not present i.e user has logged out it should display login and register tab.
    session_info="no"
    admin_session_info="no"
    if 'admin_id' in request.session:
        admin_session_info="present"
    
    if 'customer_id' in request.session:
        session_info="present"
        customer_id=int(request.session['customer_id'])
        #print("entered")
        #print(customer_id)
        customer=Customer.objects.filter(customer=customer_id)
        cust=''
        for cust in customer:
            cust1=cust

        return render(request,'about.html',{'customer':cust1,'session_info':session_info,'admin_session_info':admin_session_info})
    else:    
        return render(request,'about.html',{'session_info':session_info,'admin_session_info':admin_session_info})

def admin(request):
    session_info="no"
    admin_session_info="no"
    if 'customer_id' in request.session:
        session_info="present"
    if 'admin_id' in request.session:
        admin_session_info="present"
        admin_id=int(request.session['admin_id'])
        #print("entered")
        #print(customer_id)
        admin_table=Admin.objects.filter(id=admin_id)
        admin_obj=''
        for admin_obj in admin_table:
            admin=admin_obj

        return render(request,'admin_page.html',{'admin':admin,'session_info':session_info,'admin_session_info':admin_session_info})

    else:
        return render(request,'admin.html',{'session_info':session_info,'admin_session_info':admin_session_info})
    return render(request,'admin.html',{'session_info':session_info,'admin_session_info':admin_session_info})

def admin_login(request):
    # admin_login function is only created for admin login functionality. 
    admin_session_info="no"
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        admin_table=Admin.objects.filter(email=email,password=password)
        admin_obj=''
        for admin_obj in admin_table:
            admin=admin_obj
        
        if(admin_table.exists()):
            request.session['admin_id'] = admin.id
            return render(request,'admin_page.html',{'admin':admin})
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('admin')

    #This elif is used to check whether session in present,so it should not display login and register tab.
    #and directly display customer.html page ...i.e customer info page.
    #If user session is not present i.e user has logged out it should display login page.
    
    
    else:
        return render(request,'admin.html',{'admin_session_info':admin_session_info})
    
def admin_logout(request):
    try:
        if(request.session['admin_id']):
            del request.session['admin_id']
        return redirect('admin')
    except KeyError:
        print("Not deleted")
        return redirect('admin')
    return redirect('admin')

def view_customers(request):
    view_type=request.POST['view_type']
    
    if(view_type=='all_customers'):
        customers=Account.objects.select_related('customer').all().order_by('customer')
        #for cust in customers:
        #    print(cust.customer_id.fname)
        #    print(cust.saving_acc)
    
        return render(request,'view_customers.html',{'customer':customers})
    elif(view_type=='branch_wise'):
        branch=request.POST['branch']
        #here in next line customer_id is the foreign key in account table.....it is used to access
        #fields of related table.
        customers=Account.objects.select_related('customer').filter(customer_id__address=branch).order_by('customer')
        if customers.exists():
            return render(request,'view_customers.html',{'customer':customers})
        else:
            return render(request,'view_customers.html',{'message':"No customers at this branch."})
    return redirect('view_customers')

def contact_admin(request):
    customer_id=request.session['customer_id']
    customers=Customer.objects.filter(customer=customer_id)
    for cust in customers:
        customers=cust
    if request.method=='POST':
        customer_name=customers.fname+" "+customers.lname
        customer_id=customers.customer
        query=request.POST['query']
        
        quey_no_obj=Contact.objects.last()
        if quey_no_obj==None:
            query_no=0
        else:
            query_no=int(quey_no_obj.query_no)
        query_no=query_no+1
        query_obj=Contact.objects.create(query_no=query_no,customer_id=customer_id,customer_name=customer_name\
                                        ,query_data=query)
        query_obj.save()
        
        msg="Query Submitted"
        return render(request,'contact_page.html',{'message':msg})
    else:
        return render(request,'contact_page.html',{'customer':customers})
    
def view_queries(request):
    if request.method =='POST':
        operation=request.POST['operation']
        if operation=="view_queries":
            queries=Contact.objects.all()
            if queries.exists():
                return render(request,'view_queries.html',{'queries':queries})
            else:
                return render(request,'view_queries.html',{'message':"No Queries"})
    
        elif operation=="delete_queries":
            count=Contact.objects.all().delete()
            if int(count[0])==0:
                return render(request,'view_queries.html',{'message':"No queries to remove"})
            else:
                return render(request,'view_queries.html',{'message':"Queries Removed"})
    return render(request,'admin_page.html')

    