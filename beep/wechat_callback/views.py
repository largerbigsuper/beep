from django.shortcuts import render

def socket_test(request):
    return render(request, 'websocket_client_test.html')
