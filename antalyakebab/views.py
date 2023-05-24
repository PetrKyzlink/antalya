import datetime
import json
import re
import pytz
import locale
from .opening_hours import opening_hours
from .send_email import send_email_info



from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required

#Customer
def menu(request):
    tz = pytz.timezone('Europe/Prague')
    if opening_hours(tz):
        try:
            device = request.COOKIES['device']
        except:
            device = None
            
        salads = Products.objects.filter(id_category = 1)
        doner_boxes = Products.objects.filter(id_category = 2)
        doner_breads = Products.objects.filter(id_category = 3)
        veget_foods = Products.objects.filter(id_category = 4)
        durum_tortillas = Products.objects.filter(id_category = 5)
        kebab_plates = Products.objects.filter(id_category = 6)
        pizzas = Products.objects.filter(id_category = 7)
        others = Products.objects.filter(id_category = 8)

        if device != None:
            order, created = Order.objects.get_or_create(device= device, status='CREATING', order_number=None)
            items = order.cartitem_set.all()
            cart_items_total = order.get_cart_items_total
            cart_price_total = order.get_cart_price_total

            context = {'salads': salads , 'doner_boxes': doner_boxes, 'doner_breads': doner_breads, 'veget_foods': veget_foods, 'durum_tortillas': durum_tortillas, 'kebab_plates': kebab_plates, 'pizzas': pizzas, 'others': others, 'cart_items_total': cart_items_total, 'cart_price_total': cart_price_total, 'items': items }

        else:
            context = {'salads': salads , 'doner_boxes': doner_boxes, 'doner_breads': doner_breads, 'veget_foods': veget_foods, 'durum_tortillas': durum_tortillas, 'kebab_plates': kebab_plates, 'pizzas': pizzas, 'others': others}

        return render(request, "store/nabidka.html/",context)
    else:
        return redirect('rozvoz-nedostupny')

def cart(request):
    tz = pytz.timezone('Europe/Prague')
    if opening_hours(tz):
        try:
            device = request.COOKIES['device']
        except:
            device = None
            
        if device != None and device != "":
            order, created = Order.objects.get_or_create(device=device, status='CREATING')
            items = order.cartitem_set.all()
            dressing = Dressing.objects.all()
            drink = Drink.objects.all()
            side_dish = SideDish.objects.all()
            cart_items_total = order.get_cart_items_total
            cart_price_total = order.get_cart_price_total

            # get go to checkout page
            go_to_checkout = True

            for item in items:
                if ((item.product.with_dressing == True and item.dressing != None) or (item.product.with_drink == True and item.drink != None) or (item.product.with_side_dish == True and item.side_dish != None)):
                    to_checkout = True

                if ((item.product.with_dressing == True and item.dressing == None) or (item.product.with_drink == True and item.drink == None) or (item.product.with_side_dish == True and item.side_dish == None)):
                    to_checkout = False

                elif (item.product.with_dressing == False) or (item.product.with_drink == False) or (item.product.with_side_dish == False):
                    to_checkout = True
                else:
                    to_checkout = False

                if to_checkout == False:
                    go_to_checkout = False
                    break

            context = {'items': items, 'order': order, 'dressing': dressing, 'drink': drink, 'side_dish': side_dish, 'cart_items_total': cart_items_total, 'cart_price_total': cart_price_total, 'go_to_checkout': go_to_checkout}
            return render(request, "store/kosik.html", context)
        else:
            return redirect('cookies-nesouhlas')
    else:
        return redirect('rozvoz-nedostupny')

def checkout(request):
    tz = pytz.timezone('Europe/Prague')
    if opening_hours(tz):
        try:
            device = request.COOKIES['device']
        except:
            device = None
            
        if device != None and device != "":
            order, created = Order.objects.get_or_create(device=device, status='CREATING')
            items = order.cartitem_set.all()
            cart_items_total = order.get_cart_items_total
            cart_price_total = order.get_cart_price_total
            delivery = Delivery.objects.all()
            order_delivery = order.delivery

            if request.method == 'POST':
                data = json.loads(request.body)
                update_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                invalid_chars = ["'", ":", ";", "#", "\\", "%", "*", "(", ")", "/", "[", "]", "="]
                invalid_chars_comment = ["'", ";", "#", "\\", "%", "*", "(", ")", "/", "[", "]", "="]
                phone_regex = re.compile(r'^(\+?\d{1,3}\s?)?(\d[\s-]?){8,20}\d$')
                zipcode_regex = re.compile(r'^\d{3}\s?\d{2}$|^\d{5}$')
                
                customer_name = data['customerData']['name']
                customer_last_name = data['customerData']['lastName']
                customer_email = data['customerData']['email']
                customer_phone = data['customerData']['phone']
                customer_comment = data['customerData']['comment']
                customer_consents_terms = data['customerData']['consentsToTerms']
                customer_consents_gdpr = data['customerData']['consentsToGDPR']
                total_price = int(data['customerData']['totalPrice'])

                if order.delivery is not None and order.delivery.id != 1:
                    delivery_address_street = data['customerData']['street']
                    delivery_address_city = data['customerData']['city']
                    delivery_address_zipcode = data['customerData']['zipcode']
                else:
                    delivery_address_street = None
                    delivery_address_city = None
                    delivery_address_zipcode = None

                if (total_price == order.get_cart_price_total_with_delivery) and (customer_name is not None and len(customer_name) != 0 and len(customer_name) <= 50 and not any(char in customer_name for char in invalid_chars)) and (customer_last_name is not None and len(customer_last_name) != 0 and len(customer_last_name) <= 50 and not any(char in customer_last_name for char in invalid_chars)) and (customer_email is not None and len(customer_email) != 0 and len(customer_email) <= 80 and not any(char in customer_email for char in invalid_chars) and "@" in customer_email) and (customer_phone is not None and phone_regex.match(customer_phone)) and (customer_comment is None or len(customer_comment) <= 1000 and not any(char in customer_comment for char in invalid_chars_comment)) and customer_consents_terms and customer_consents_gdpr:
                    customer, created = Customer.objects.get_or_create(
                        name = customer_name,
                        last_name = customer_last_name,
                        email = customer_email,
                        phone_number = customer_phone,
                        order = order   
                    )
                    if created:
                        pass    
                    else:
                        pass
                    order.terms = customer_consents_terms
                    order.gdpr = customer_consents_gdpr
                    order.customer_comment = customer_comment
                    order.status = 'NEW'
                    order.order_number = order.set_order_number()
                    order.date_ordered = update_time
                    if (order.delivery is not None or order.delivery.id != 1) and (delivery_address_street is not None and len(delivery_address_street) != 0 and len(delivery_address_street) <= 80 and not any(char in delivery_address_street for char in invalid_chars)) and (delivery_address_city is not None and len(delivery_address_city) != 0 or len(delivery_address_city) <= 50 or not any(char in delivery_address_city for char in invalid_chars)) and (delivery_address_zipcode is not None and zipcode_regex.match(delivery_address_zipcode)):
                        delivery_address, created = DeliveryAddress.objects.get_or_create(
                            customer=customer,
                            order=order,
                            street=delivery_address_street,
                            city=delivery_address_city,
                            zipcode=delivery_address_zipcode,
                        )
                        if created:
                            pass    
                        else:
                            pass
                    order.total_price_order = order.get_cart_price_total_with_delivery
                    order.save()
                    subject = "Přijatá nová objednávka č.:" + ' ' + order.order_number
                    message = ''
                    recipient = 'kyzlos@gmail.com'
                    send_email_info(subject, message, [recipient])
                    return redirect('objednavka-odeslana')

                else:
                    return redirect('neco-se-nepovedlo')

            context = {'items': items, 'order': order, 'cart_items_total': cart_items_total,'cart_price_total': cart_price_total, 'delivery': delivery, 'order_delivery': order_delivery}
            return render(request, "store/objednavka.html", context)
        else:
            return redirect('cookies-nesouhlas')
    else:
        return redirect('rozvoz-nedostupny')

def order_sent(request):
    try:
        device = request.COOKIES['device']
    except:
        device = None    

    if device != None or device != "":      
        order = Order.objects.filter(device=device, status='NEW').latest('date_ordered')
        customer = Customer.objects.filter(order=order).first()
        items = order.cartitem_set.all()
        cart_items_total = order.get_cart_items_total
        cart_price_total = order.get_cart_price_total
        total_price_order = order.total_price_order
        locale.setlocale(locale.LC_TIME, 'cs_CZ.utf8')
        order_creation_time = order.date_ordered.strftime('%d. %m. %Y %H:%M')
        try:
            delivery_address = DeliveryAddress.objects.get(customer=customer, order=order)
        except DeliveryAddress.DoesNotExist:
            delivery_address = None

        context = {'order': order, 'items': items, 'customer': customer, 'delivery_address': delivery_address, 'cart_items_total': cart_items_total,'cart_price_total': cart_price_total,'total_price_order': total_price_order,  'order_creation_time': order_creation_time}
        return render(request, "store/objednavka-odeslana.html", context)
    else:
        return redirect('cookies-nesouhlas')

def closed(request):
    return render(request, "store/rozvoz-nedostupny.html")

def something_wrong(request):
    return render(request, "store/neco-se-nepovedlo.html")

def unapproved_cookies(request):
    return render(request, "store/cookies-nesouhlas.html")

#customer JS

def rejectCookies(request):
    response = JsonResponse({'message': 'Cookies rejected.'})
    response.delete_cookie('csrftoken', domain=None, path='/')
    request.session.flush()
    return response

def acceptCookies(request):
    response = redirect('nabidka')
    response.set_cookie('cookies_accepted', 'true')
    return response

def updateItem(request):
    data = json.loads(request.body)
    action = data["action"]

    if action == 'add':
        productId = data["productId"]
        device = request.COOKIES['device']        
        
        product = Products.objects.get(id=productId)
        order, created = Order.objects.get_or_create(device=device, status='CREATING', order_number=None)
        cart_item = CartItem.objects.create(order=order, product=product)
        cart_item.save()
        return JsonResponse('Item was added', safe=False)

    if action == 'update':
        cartItemId = data["cartItemId"]
        cart_item_change = CartItem.objects.get(id=cartItemId)
        selected = data['selected']
        if data['selected'] == 'dressing':
            if data['dressingId'] == 'null':
                cart_item_change.dressing = None
            else:
                dressing = Dressing.objects.get(id=data['dressingId'])
                cart_item_change.dressing = dressing
            cart_item_change.save()
        if data['selected'] == 'drink':
            if data['drinkId'] == 'null':
                cart_item_change.drink = None
            else:
                drink = Drink.objects.get(id=data['drinkId'])
                cart_item_change.drink = drink
            cart_item_change.save()
        if data['selected'] == 'sidedish':
            if data['sideDishId'] == 'null':
                cart_item_change.side_dish = None
            else:
                side_dish = SideDish.objects.get(id=data['sideDishId'])
                cart_item_change.side_dish = side_dish
            cart_item_change.save()
        return JsonResponse('Item was updated', safe=False)

    if action == 'remove':
        cartItemId = data["cartItemId"]
        CartItem.objects.filter(id=cartItemId).delete()
        return JsonResponse('Item was removed', safe=False)

def updateDelivery(request):
    data = json.loads(request.body)
    orderId = data['orderId']
    deliveryId = data['deliveryId']
    order_delivery_change = Order.objects.get(id=orderId)
    if deliveryId == 'null':
        order_delivery_change.delivery = None
    else:
        delivery = Delivery.objects.get(id=deliveryId)
        order_delivery_change.delivery = delivery
    order_delivery_change.save()

    return JsonResponse('Delivery was updated', safe=False)

# Service

@login_required(login_url='login')
def service(request):    
    tz = pytz.timezone('Europe/Prague')
    today = datetime.datetime.now(tz)
    locale.setlocale(locale.LC_TIME, 'cs_CZ.utf8')
    new_orders = Order.objects.filter(status='NEW').order_by('-order_number')

    orders_in_process = Order.objects.filter(status='IN_PROCESS')

    today_orders_completed = Order.objects.filter(status='COMPLETED', date_ordered__date=today)

    context = {"new_orders": new_orders, "orders_in_process": orders_in_process, "today_orders_completed": today_orders_completed}
    return render(request, "service/service.html", context)

@login_required(login_url='login')
def new_order_detail(request, pk, order_number):
    selected_new_order = Order.objects.get(status='NEW', id=pk, order_number=order_number)
    selected_new_order_items = CartItem.objects.filter(order=selected_new_order)
    try:
        customer_new_order = Customer.objects.get(order=selected_new_order)  
    except Customer.DoesNotExist:
        customer_new_order = None
    locale.setlocale(locale.LC_TIME, 'cs_CZ.utf8')
    selected_order_creation_time = selected_new_order.date_ordered.strftime('%d. %m. %Y %H:%M')
    tz = pytz.timezone('Europe/Prague')
    today = datetime.datetime.now(tz)
    cart_items_total = selected_new_order.get_cart_items_total
    cart_price_total = selected_new_order.get_cart_price_total
    total_price_order = selected_new_order.total_price_order
    try:
        new_order_delivery_address = DeliveryAddress.objects.get( order=selected_new_order)
    except DeliveryAddress.DoesNotExist:
        new_order_delivery_address = None
    
    new_orders = Order.objects.filter(status='NEW').order_by('-order_number')

    orders_in_process = Order.objects.filter(status='IN_PROCESS')
    
    today_orders_completed = Order.objects.filter(status='COMPLETED', date_ordered__date=today)

    context = {"selected_new_order": selected_new_order, "selected_new_order_items": selected_new_order_items,"selected_order_creation_time": selected_order_creation_time, 'new_order_delivery_address': new_order_delivery_address, 'customer_new_order': customer_new_order, 'cart_items_total': cart_items_total,'cart_price_total': cart_price_total, 'total_price_order': total_price_order, "new_orders": new_orders, "orders_in_process": orders_in_process, "today_orders_completed": today_orders_completed}
    return render(request, "service/service.html", context) 

@login_required(login_url='login')
def today_completed_order_detail(request, pk, order_number):
    selected_today_completed_order = Order.objects.get(status='COMPLETED', id=pk, order_number=order_number)
    selected_today_completed_order_items = CartItem.objects.filter(order=selected_today_completed_order)
    try:
        customer_today_completed_order = Customer.objects.get(order=selected_today_completed_order) 
    except Customer.DoesNotExist:
        customer_today_completed_order = None
    locale.setlocale(locale.LC_TIME, 'cs_CZ.utf8')
    selected_order_creation_time = selected_today_completed_order.date_ordered.strftime('%d. %m. %Y %H:%M')
    tz = pytz.timezone('Europe/Prague')
    today = datetime.datetime.now(tz)
    cart_items_total = selected_today_completed_order.get_cart_items_total
    cart_price_total = selected_today_completed_order.get_cart_price_total
    total_price_order = selected_today_completed_order.total_price_order
    try:
        today_completed_order_delivery_address = DeliveryAddress.objects.get( order=selected_today_completed_order)
    except DeliveryAddress.DoesNotExist:
        today_completed_order_delivery_address = None

    new_orders = Order.objects.filter(status='NEW').order_by('-order_number')

    orders_in_process = Order.objects.filter(status='IN_PROCESS')
      
    today_orders_completed = Order.objects.filter(status='COMPLETED', date_ordered__date=today)

    context = {"selected_today_completed_order": selected_today_completed_order, "selected_today_completed_order_items": selected_today_completed_order_items,'customer_today_completed_order': customer_today_completed_order ,"selected_order_creation_time": selected_order_creation_time, 'today_completed_order_delivery_address': today_completed_order_delivery_address, 'cart_items_total': cart_items_total,'cart_price_total': cart_price_total, 'total_price_order': total_price_order,"new_orders": new_orders, "orders_in_process": orders_in_process, "today_orders_completed": today_orders_completed,}
    return render(request, "service/service.html", context)   

@login_required(login_url='login')
def close_page_new_orders(request):
    return redirect("/obsluha/#new-orders")

@login_required(login_url='login')
def close_page_today_orders_completed(request):
    return redirect("/obsluha/#today-orders-completed")


@login_required(login_url='login')
def history_orders(request):
    orders = Order.objects.filter(status='COMPLETED').order_by('-order_number')
    context = {'orders': orders}
    return render(request, "service/historie-objednavek.html", context)

@login_required(login_url='login')
def history_order_detail(request,pk, order_number):
    order = Order.objects.get(status='COMPLETED', id=pk, order_number=order_number)
    locale.setlocale(locale.LC_TIME, 'cs_CZ.utf8')
    order_creation_time = order.date_ordered.strftime('%d. %m. %Y %H:%M')
    items = CartItem.objects.filter(order=order)
    try:
        customer = Customer.objects.get(order=order) 
    except Customer.DoesNotExist:
        customer = None
    try:
        delivery_address = DeliveryAddress.objects.get( order=order)
    except DeliveryAddress.DoesNotExist:
        delivery_address = None
    
    cart_items_total = order.get_cart_items_total
    cart_price_total = order.get_cart_price_total
    total_price_order = order.total_price_order


    orders = Order.objects.filter(status='COMPLETED').order_by('-order_number')
    context = {'orders': orders, 'order': order, 'customer': customer, 'delivery_address':delivery_address, 'items': items, 'cart_items_total': cart_items_total,'cart_price_total': cart_price_total, 'total_price_order': total_price_order, 'order_creation_time': order_creation_time}
    return render(request, "service/historie-objednavek.html", context)

@login_required(login_url='login')
def close_page_history_order(request, pk):
    order_id = pk
    url = reverse('historie-objednavek') + f'#{order_id}'
    return redirect(url)

@login_required(login_url='login')
def newOrderConfirmation(request):
    data = json.loads(request.body)
    orderId = data['orderId']
    minutes = data['minutes']
    tz = pytz.timezone('Europe/Prague')
    time_now = datetime.datetime.now(tz)
    time_to_completed = time_now + datetime.timedelta(minutes=int(minutes))
    locale.setlocale(locale.LC_TIME, 'cs_CZ.utf8')
    if orderId is not None and minutes is not None:
        order = Order.objects.get(pk=orderId, status='NEW')
        locale.setlocale(locale.LC_TIME, 'cs_CZ.utf8')
        time_to_completed = time_to_completed.strftime('%d. %m. %Y %H:%M')
        items = CartItem.objects.filter(order=order)
        item_to_message = ""
        for item in items:
            item_to_message += f"\n{item.product.id_category} - {item.product} - {item.price} Kč.\n"
            if item.dressing:
                item_to_message += f"Dresink: {item.dressing}\n"
            if item.side_dish:
                item_to_message += f"Příloha: {item.side_dish}\n"
            if item.drink:
                item_to_message += f"Nápoj 0.33l: {item.drink}\n"            
        try:
            customer = Customer.objects.get(order=order) 
        except Customer.DoesNotExist:
            customer = None
        try:
            delivery_address = DeliveryAddress.objects.get( order=order)
        except DeliveryAddress.DoesNotExist:
            delivery_address = None
        cart_items_total = order.get_cart_items_total
        cart_price_total = order.get_cart_price_total
        total_price_order = order.total_price_order
        if order.delivery.id == 1:
            subject = f'Objednávka č.: {order.order_number}'
            message = (
                f'Vážený zákazníku,\n'
                f'potvrzujeme přijetí Vaší objednávky č.: {order.order_number}, která bude připravena přibližně za {minutes} minut ({time_to_completed}) k osobnímu odběru.\n\n'
                f'Rekapitulace:\n'
                f'Zákazník:\n{customer.name} {customer.last_name}\nEmail: {customer.email}\nTel.:{customer.phone_number}\n\n'
                f'Osobní odběr:\nKlášterec Antalya Kebab\nBudovatelská 488\nKlášterec nad Ohří\n\n'
                + (f'Poznámka: {order.customer_comment}\n\n' if order.customer_comment else '')
                + f'Položky:'
                f'{item_to_message}'
                f'Položek: {cart_items_total} - Za položky celkem: {cart_price_total} Kč\n'
                f'Rozvoz: {order.delivery_price} Kč\nCena celkem: {total_price_order} Kč\n\n'
                f'Klášterec Antalya Kebab\nBudovatelská 488\nKlášterec nad Ohří\n+420 777 510 166\n\n\n'
            )

            recipient = f'{customer.email}'
            send_email_info(subject, message, [recipient])

        if order.delivery.id == 2 and delivery_address != None:
            subject = f'Objednávka č.: {order.order_number}'
            message = (
                f'Vážený zákazníku,\n'
                f'potvrzujeme přijetí Vaší objednávky č.: {order.order_number}, která bude připravena přibližně za {minutes} minut ({time_to_completed}) k osobnímu odběru.\n\n'
                f'Rekapitulace:\n'
                f'Zákazník:\n{customer.name} {customer.last_name}\nEmail: {customer.email}\nTel.:{customer.phone_number}\n\n'
                f'Rozvoz:\n{delivery_address.street}\n{delivery_address.city}\n{delivery_address.zipcode}\n\n'
                + (f'Poznámka: {order.customer_comment}\n\n' if order.customer_comment else '')
                + f'Položky:'
                f'{item_to_message}'
                f'\nPoložek: {cart_items_total} - Za položky celkem: {cart_price_total} Kč\n'
                f'Rozvoz: {order.delivery_price} Kč\nCena celkem: {total_price_order} Kč\n\n'
                f'Klášterec Antalya Kebab\nBudovatelská 488\nKlášterec nad Ohří\n+420 777 510 166\n\n\n'
            )

            recipient = f'{customer.email}'
            send_email_info(subject, message, [recipient])
        order.status = 'IN_PROCESS'
        order.save()
        return JsonResponse('Order status was update and mail was sent', safe=False)
    else:
        return JsonResponse('Something wrong', safe=False)
    

@login_required(login_url='login')
def orderCompleted(request):
    data = json.loads(request.body)
    orderId = data['orderId']
    if orderId is not None:
        order = Order.objects.get(pk=orderId, status='IN_PROCESS')
        try:
            customer = Customer.objects.get(order=order) 
        except Customer.DoesNotExist:
            customer = None
        if order.delivery.id == 1:
            subject = f'Objednávka č.: {order.order_number} - Připravena'
            message = f'Vážený zákazníku,\n Vaše objednávka č.: {order.order_number} je připravena k vyzvednutí.\nDěkujeme za Vaší objednávku a přejeme Vám dobrou chuť.\n\nKlášterec Antalya Kebab\nBudovatelská 488\nKlášterec nad Ohří\n+420 777 510 166'
            recipient = f'{customer.email}'
            send_email_info(subject, message, [recipient])

        if order.delivery.id == 2:
            subject = f'Objednávka č.: {order.order_number}'
            message = f'Vážený zákazníku,\nVaše objednávka č.: {order.order_number} je na cestě k Vám.\nDěkujeme za Vaší objednávku a přejeme Vám dobrou chuť.\n\nKlášterec Antalya Kebab\nBudovatelská 488\nKlášterec nad Ohří\n+420 777 510 166' 
            recipient = f'{customer.email}'
            send_email_info(subject, message, [recipient])
        order.status = 'COMPLETED'
        order.save()
        return JsonResponse('Order status was update and mail was sent', safe=False)
    else:
        return JsonResponse('Something wrong', safe=False)
        

@login_required(login_url='login')
def orderCancellation(request):
    data = json.loads(request.body)
    orderId = data['orderId']
    if orderId is not None:
        order = Order.objects.get(pk=orderId, status='IN_PROCESS')
        try:
            customer = Customer.objects.get(order=order) 
        except Customer.DoesNotExist:
            customer = None
        subject = f'Objednávka č.: {order.order_number} - Storno'
        message = f'Vážený zákazníku,\n Vaše objednávka č.: {order.order_number} byla stornována.\n\nKlášterec Antalya Kebab\nBudovatelská 488\nKlášterec nad Ohří\n+420 777 510 166'
        recipient = f'{customer.email}'
        send_email_info(subject, message, [recipient])

        order.status = 'STORNO'
        order.save()
        return JsonResponse('Order status was update and mail was sent', safe=False)
    else:
        return JsonResponse('Something wrong', safe=False)