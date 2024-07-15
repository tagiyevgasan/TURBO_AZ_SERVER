from django.shortcuts import render, get_object_or_404
from .models import Order, SendedLink
from users.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from turbo_parser.forms import AddOrderForm
from users.forms import UserProfileForm

def index(request):
    return render(request, 'turbo_parser/index.html')

def instructions(request):
    return render(request, 'turbo_parser/instructions.html')


def orders(request):
    orders = Order.objects.filter(user=request.user)
    my_list = []

    max_num_of_orders = User.objects.get(id=request.user.id).max_num_of_orders
    num_of_orders = len(Order.objects.filter(user_id=request.user.id))
    num_orders_left = max_num_of_orders - num_of_orders

    for i in orders:
        num_sended_links_for_i = len(i.sendedlink_set.all())
        my_list.append((i, num_sended_links_for_i))
    
    context = {
        'my_list': my_list,
        'user': request.user,
        'max_num_of_orders': max_num_of_orders,
        'num_of_orders': num_of_orders,
        'num_orders_left':num_orders_left,
    }

    return render(request, 'turbo_parser/orders.html', context)


def order_details(request, id):

    # Option 1
    # try:
    #     order = Order.objects.get(pk=id)
    #     data = [order]

    #     sended_links_for_order = order.sendedlink_set.all()
    #     data.append(sended_links_for_order)

    #     return render(request, 'order_details.html',{'data':data})
    # except Order.DoesNotExist:
    #     raise Http404() 

    # Option 2
    order = get_object_or_404(Order, pk=id)
    data = [order]

    sended_links_for_order = order.sendedlink_set.all()
    data.append(sended_links_for_order)
    
    return render(request, 'turbo_parser/order_details.html',{'data':data})

        

def add_order(request):
    if request.method == "POST":
        form = AddOrderForm(data=request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.save()
            return HttpResponseRedirect(reverse('turbo_parser:orders'))
        else:
            print('not valid')
    else:
        form = AddOrderForm()
        max_num_of_orders = User.objects.get(id=request.user.id).max_num_of_orders
        num_of_orders = len(Order.objects.filter(user_id=request.user.id))
        num_orders_left = max_num_of_orders - num_of_orders
        if num_of_orders >= max_num_of_orders:
            return HttpResponseRedirect(reverse('turbo_parser:orders'))

    context = {'form': form}
    return render(request, 'turbo_parser/add_order.html', context)


def delete_order(request, order_id):
    order_to_delete = Order.objects.get(pk=order_id)
    order_to_delete.delete()
    return HttpResponseRedirect(reverse('turbo_parser:orders'))

def edit_order(request, order_id):
    order_object = Order.objects.get(pk=order_id)

    if request.method == 'POST':
        form = AddOrderForm(data=request.POST, instance=order_object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('turbo_parser:orders'))
        else:
            print('not valid')

    else:
        form = AddOrderForm(instance=order_object)

    context = {'form': form}
    return render(request, 'turbo_parser/edit_order.html', context)


def profile(request):

    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('turbo_parser:profile'))
        else:
            print('not valid')
        
    else:
        form = UserProfileForm(instance=request.user)

    user_orders=Order.objects.filter(user=request.user)
    context = {
        'form': form,
        'user_orders': len(user_orders),
    }
    return render(request, 'turbo_parser/profile.html', context)
