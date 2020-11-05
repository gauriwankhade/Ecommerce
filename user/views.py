from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm,ContactForm
from django.http import HttpResponseRedirect,HttpResponse
from .models import Consumer,Product,Category,Order,OrderItem,ShippingAddress,orderSuccess
from django.contrib.auth.hashers  import make_password, check_password 
from django.core.mail import send_mail

from django.contrib.auth import login,logout

def indexView(request):
	return render(request,'home/index.html',{})
	
def registerView(request):
	if request.method =='POST' :
		form = RegisterForm(request.POST)
		if form.is_valid() :
			username = request.POST['username']
			email	 = request.POST['email']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			password = make_password(request.POST['password'], salt=None, hasher='default')
			
			user = Consumer(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
			user.save()

			login(request,user)
			request.session['consumer_id']= user.id

			return HttpResponseRedirect('/')
	else:
		form=RegisterForm()

	context = {
			'form' : form
	}

	return render(request,'register.html',context)


def loginView(request):
	form = LoginForm()
	context = {
		'form' : form
		}
	
	if request.method== 'POST' :
		form = LoginForm(request.POST)
		if form.is_valid() :
			username= request.POST['username']
			password = request.POST['password']
			
			try:
				user = Consumer.objects.get(username=username)
			except:
				message = 'incorrect username' #incorrect username
				context['message']=message
				return render(request,'login.html',context)

			if user.check_password(password) and username == user.username:
				
				login(request,user)
				request.session['consumer_id']= user.id
				return HttpResponseRedirect('/products')  #login success
			else:
				message = 'incorrect username password' #incorrect password
				context['message']=message	
		
			return render(request,'login.html',context) # invalid password/username		

	return render(request,'login.html',context)

def signoutView(request):
	if request.user.is_authenticated:
		logout(request)
				
	return HttpResponseRedirect('/products')

def profileView(request):
	if request.user.is_authenticated:
		try:
			person=Consumer.objects.get(pk=request.session['consumer_id'])
		except :
			return redirect(loginView)

		context={
			'person' : person
		}
		return render(request,'profile.html',context)
	else:
		return redirect(loginView)
	

def accountView(request):
	if request.user.is_authenticated:
		person = Consumer.objects.get(pk= request.session['consumer_id'])
		if request.method == 'POST':
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			date_of_birth = request.POST.get('date_of_birth')
			person.first_name = first_name
			person.last_name = last_name
			person.date_of_birth = date_of_birth
			person.save()
			return HttpResponseRedirect('/user/account')

		context = {
		'person' : person
		}
		return render(request,'account.html',context)

def orderHistoryView(request):
	if request.user.is_authenticated:		
		consumer = request.session['consumer_id']
		orders = orderSuccess.objects.filter(consumer=consumer)
		context = {'orders':orders}
		print(orders)
		return render(request,'products/order_history.html',context)
	else:
		return redirect(loginView)

def contactView(request):
    name=''
    email=''
    comment=''
	
    form= ContactForm(request.POST or None)
    if form.is_valid():
        name= form.cleaned_data.get("name")
        email= form.cleaned_data.get("email")
        comment=form.cleaned_data.get("comment")
        if request.user.is_authenticated:
            subject= str(request.user) + "'s Comment"
        else:
            subject= "A Visitor's Comment"
        comment= name + " with the email, " + email + ", sent the following message:\n\n" + comment;
        send_mail(subject, comment, 'example@gmail.com', [email])
        context= {'form': form}
        return HttpResponse('success!!')
    else:
        context= {'form': form}
        return render(request, 'contact.html', context)


def storeView(request):
	print(request.user)
	category=Category.objects.all()
	products = Product.objects.all()
	context={	'category':category,
				'products':products
			}
	
	if request.method=='POST':
		print(request.POST)
		product_id = request.POST['product_id']
		product=Product.objects.get(pk=product_id)
		cart_update(request,product)

	return render(request,'products/products.html',context)

def productDetailView(request,pk):
	print(pk)
	product= Product.objects.get(pk=pk)
	context= {
		'product':product
	}

	if request.method == 'POST' :
		if request.user.is_authenticated:
			cart_update(request,product)
		else:
			return redirect(loginView)

	return render(request, 'products/productdetail.html', context)



def cart_update(request,product):
	if request.user.is_authenticated:
		#consumer = get_object_or_404(Consumer, pk=request.session['consumer_id'])
		consumer= Consumer.objects.get(pk=request.session['consumer_id'])
		order,created = Order.objects.get_or_create(consumer=consumer,complete=False)
		item = None
		try:
			item=OrderItem.objects.get(order=order,product=product)	
		except:
			item=OrderItem.objects.create(product=product,order=order)

		quantity= item.quantity
		quantity+=1
		item.quantity = quantity
		item.save()

def cart_minus(request,product):
	if request.user.is_authenticated:
		consumer= Consumer.objects.get(pk=request.session['consumer_id'])
		order,created = Order.objects.get_or_create(consumer=consumer,complete=False)
		item = None
		try:
			item=OrderItem.objects.get(order=order,product=product)	
		except:
			item=OrderItem.objects.create(product=product,order=order)
		quantity= item.quantity

		if quantity==1:
			item.delete()
		else:
			quantity-=1
			item.quantity = quantity
			item.save()


	
def cartView(request):
	if request.user.is_authenticated:
		if request.method == 'POST'	:
			plus = request.POST.get('plus')
			minus = request.POST.get('minus')
			product_id = request.POST.get('product_id')
			product = Product.objects.get(pk=product_id)
			if plus:
				cart_update(request,product)
				return HttpResponseRedirect('/cart')
			if minus:
				cart_minus(request,product)
				return HttpResponseRedirect('/cart')
		try:
			consumer = Consumer.objects.get(pk=request.session['consumer_id']) 
			order,created = Order.objects.get_or_create(consumer=consumer,complete=False)
			items = order.orderitem_set.all() 
			print(request.user)

			context = {'items':items,
					'order':order,
					'error':False}
		except:
			return redirect(loginView)

	else:
		context = {'error' : True} 
		print(request.user)
	
	return render(request,'products/cart.html',context)

def checkoutView(request):
	if request.user.is_authenticated:
		consumer = Consumer.objects.get(pk=request.session['consumer_id']) 
		order,created = Order.objects.get_or_create(consumer=consumer,complete=False)
		items = order.orderitem_set.all() 

		if request.method == "POST" :
			name= request.POST.get('name')
			email = request.POST.get('email')
			address= request.POST.get('address')
			city= request.POST.get('city')
			state= request.POST.get('state')
			zipcode= request.POST.get('zipcode')
			country	= request.POST.get('country')
			obj = ShippingAddress(consumer=consumer,order=order,address=address,city=city,state=state,zipcode=zipcode,country=country)
			obj.save()
			success = orderSuccess(consumer=consumer,name=name,email=email,address=obj,order=order)
			success.save()
			order.complete= True
			order.save()
			return HttpResponse('Order Success')

	else:
		items = []
		order = None

	context = {'items':items,
				'order':order}

	return render(request,'products/checkout.html',context)
	

