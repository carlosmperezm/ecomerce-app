
from typing import override

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from shopping_and_payments.tests.base import BaseTestCase
from shopping_and_payments.models import ShopOrder,ShoppingCart,OrderStatus

from users.models import User



class OrderCreationTest(BaseTestCase):
    @override
    def setUp(self)->None:
        OrderStatus.objects.get_or_create(name='Pending')
        OrderStatus.objects.get_or_create(name='Processing')
        OrderStatus.objects.get_or_create(name='Completed')
        OrderStatus.objects.get_or_create(name='Cancelled')
        return super().setUp()


    def test_order_creation(self:Request) ->None:
        user:User = self.create_users(2)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')


        cart:ShoppingCart = ShoppingCart.objects.create(user=user)
        
        response:Response= self.client.post(self.create_order_url,data={'cart':cart.pk})

        order_status:OrderStatus = OrderStatus.objects.get(name=response.data.get('status'))

        self.assertEqual(order_status.name , 'Pending')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)
    
    def test_order_creation_as_no_owner(self)->None:
        users:list[User] = self.create_users(2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {users[0].auth_token}')

        cart:ShoppingCart = ShoppingCart.objects.create(user=users[1])

        response:Response = self.client.post(self.create_order_url, data={'cart':cart.pk})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('error'), 'You do not have permission to perform this action.')

    def test_order_creation_as_admin(self)->None:
        user:User = self.create_users(2)[0]
        user.is_staff = True
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')

        cart:ShoppingCart = ShoppingCart.objects.create(user=user)

        response:Response = self.client.post(self.create_order_url, data={'cart':cart.pk})

        order_status:OrderStatus = OrderStatus.objects.get(name=response.data.get('status'))


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order_status.name , 'Pending')
        self.assertIsNotNone(response.data)

    def test_order_creation_with_no_data(self)->None:
        user:User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')

        response:Response = self.client.post(self.create_order_url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('cart')[0], 'This field is required.')   

class OrderGetTest(BaseTestCase):

    @override
    def setUp(self)->None:
        OrderStatus.objects.get_or_create(name='Pending')
        OrderStatus.objects.get_or_create(name='Processing')
        OrderStatus.objects.get_or_create(name='Completed')
        OrderStatus.objects.get_or_create(name='Cancelled')
        return super().setUp()

    def test_get_order(self)->None:
        user:User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
        cart:ShoppingCart = ShoppingCart.objects.create(user=user)

        order:ShopOrder = ShopOrder.objects.create(cart=cart)
        order.status = OrderStatus.objects.get(name='Processing')
        order.save()

        response:Response = self.client.get(self.order_detail_url(order.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('status'), 'Processing')

        order.status = OrderStatus.objects.get(name='Completed')
        order.save()
        response = self.client.get(self.order_detail_url(order.pk))

        self.assertEqual(response.data.get('status'), 'Completed')

    def test_get_order_as_no_owner(self)->None:
        users:list[User] = self.create_users(2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {users[0].auth_token}')

        cart:ShoppingCart = ShoppingCart.objects.create(user=users[1])

        order:ShopOrder = ShopOrder.objects.create(cart=cart)
        order.status = OrderStatus.objects.get(name='Processing')
        order.save()

        response:Response = self.client.get(self.order_detail_url(order.pk))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('error'), 'You do not have permission to perform this action.')

    def test_get_order_as_admin(self)->None:
        user:User = self.create_users(1)[0]
        user.is_staff = True
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')

        cart:ShoppingCart = ShoppingCart.objects.create(user=user)

        order:ShopOrder = ShopOrder.objects.create(cart=cart)
        order.status = OrderStatus.objects.get(name='Processing')
        order.save()

        response:Response = self.client.get(self.order_detail_url(order.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('status'), 'Processing')

        order.status = OrderStatus.objects.get(name='Completed')
        order.save()
        response = self.client.get(self.order_detail_url(order.pk))

        self.assertEqual(response.data.get('status'), 'Completed')

    def test_get_order_with_invalid_id(self)->None:
        user:User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')

        response:Response = self.client.get(self.order_detail_url(100))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), 'No ShopOrder matches the given query.')

class OrderUpdateTest(BaseTestCase):
    
        @override
        def setUp(self)->None:
            OrderStatus.objects.get_or_create(name='Pending')
            OrderStatus.objects.get_or_create(name='Processing')
            OrderStatus.objects.get_or_create(name='Completed')
            OrderStatus.objects.get_or_create(name='Cancelled')
            return super().setUp()
    
        def test_update_order(self)->None:
            user:User = self.create_users(1)[0]
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
    
            cart:ShoppingCart = ShoppingCart.objects.create(user=user)
    
            order:ShopOrder = ShopOrder.objects.create(cart=cart)
    
            response:Response = self.client.put(self.order_detail_url(order.pk), data={'status':'Completed'})
    
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsNotNone(response.data)
            self.assertEqual(response.data.get('status'), 'Completed')
    
        def test_update_order_as_no_owner(self)->None:
            users:list[User] = self.create_users(2)
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {users[0].auth_token}')

            cart:ShoppingCart = ShoppingCart.objects.create(user=users[1])
            order:ShopOrder = ShopOrder.objects.create(cart=cart)

            response:Response = self.client.put(self.order_detail_url(order.pk), data={'status':'Completed'})

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data.get('error'), 'You do not have permission to perform this action.')

        def test_update_order_as_admin(self)->None:
            users:list[User] = self.create_users(3)
            users[0].is_staff = True
            users[0].save()

            self.client.credentials(HTTP_AUTHORIZATION=f'Token {users[0].auth_token}')

            cart:ShoppingCart = ShoppingCart.objects.create(user=users[2])

            order:ShopOrder = ShopOrder.objects.create(cart=cart)

            response:Response = self.client.put(self.order_detail_url(order.pk), data={'status':'Processing'})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsNotNone(response.data)
            self.assertEqual(response.data.get('status'), 'Processing')

        def test_update_order_with_invalid_id(self)->None:
            user:User = self.create_users(1)[0]

            self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
            cart:ShoppingCart = ShoppingCart.objects.create(user=user)

            order:ShopOrder = ShopOrder.objects.create(cart=cart)

            response:Response = self.client.put(self.order_detail_url(order.pk+10), data={'status':'Processing'})

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data.get('detail'), 'No ShopOrder matches the given query.')


class CancelOrderTest(BaseTestCase):

    @override
    def setUp(self)->None:
        OrderStatus.objects.get_or_create(name='Pending')
        OrderStatus.objects.get_or_create(name='Processing')
        OrderStatus.objects.get_or_create(name='Completed')
        OrderStatus.objects.get_or_create(name='Cancelled')
        return super().setUp()

    def test_cancel_order(self)->None:
        user:User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')

        cart:ShoppingCart = ShoppingCart.objects.create(user=user)

        order:ShopOrder = ShopOrder.objects.create(cart=cart)

        response:Response = self.client.delete(self.order_detail_url(order.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(ShopOrder.objects.count(), 0)
        self.assertEqual(response.data.get('message'), 'Order cancelled successfully.')

    def test_cancel_order_as_no_owner(self)->None:
        users:list[User] = self.create_users(2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {users[0].auth_token}')

        cart:ShoppingCart = ShoppingCart.objects.create(user=users[1])

        order:ShopOrder = ShopOrder.objects.create(cart=cart)

        response:Response = self.client.delete(self.order_detail_url(order.pk))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('error'), 'You do not have permission to perform this action.')

    def test_cancel_order_as_admin(self)->None:
        user:User = self.create_users(1)[0]
        user.is_staff = True
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')

        cart:ShoppingCart = ShoppingCart.objects.create(user=user)

        order:ShopOrder = ShopOrder.objects.create(cart=cart)

        response:Response = self.client.delete(self.order_detail_url(order.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(ShopOrder.objects.count(), 0)
        self.assertEqual(response.data.get('message'), 'Order cancelled successfully.')

    def test_cancel_order_with_invalid_id(self)->None:
        user:User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')

        response:Response = self.client.delete(self.order_detail_url(100))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('detail'), 'No ShopOrder matches the given query.')


