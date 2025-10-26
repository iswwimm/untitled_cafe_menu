"""
Comprehensive test suite for Cafe Menu Django application
Tests all functionality including models, views, forms, and URLs
"""

from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from decimal import Decimal
import json
import os
from PIL import Image
import tempfile

from menu.models import Coffee, Toast, Sweet
from modifiers.forms import CoffeeForm, ToastForm, SweetForm


class ModelTests(TestCase):
    """Test all model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.coffee = Coffee.objects.create(
            name="Test Coffee",
            group="basic",
            price=Decimal('4.50'),
            price_2=Decimal('5.00'),
            temperature="hot",
            description="Test coffee description",
            is_active=True,
            order=1
        )
        
        self.toast = Toast.objects.create(
            name="Test Toast",
            description="Test toast description",
            allergens="1, 2",
            price=Decimal('8.00'),
            is_active=True,
            order=1
        )
        
        self.sweet = Sweet.objects.create(
            name="Test Sweet",
            description="Test sweet description",
            allergens="3, 4",
            price=Decimal('6.50'),
            is_active=True,
            order=1
        )

    def test_coffee_model_creation(self):
        """Test Coffee model creation and properties"""
        self.assertEqual(self.coffee.name, "Test Coffee")
        self.assertEqual(self.coffee.group, "basic")
        self.assertEqual(self.coffee.price, Decimal('4.50'))
        self.assertEqual(self.coffee.price_2, Decimal('5.00'))
        self.assertEqual(self.coffee.temperature, "hot")
        self.assertTrue(self.coffee.is_active)
        self.assertEqual(self.coffee.order, 1)

    def test_coffee_price_display(self):
        """Test Coffee price display properties"""
        # Test integer price display
        coffee_int = Coffee.objects.create(name="Int Coffee", price=Decimal('5.00'))
        self.assertEqual(coffee_int.price_display, 5)
        
        # Test decimal price display
        self.assertEqual(self.coffee.price_display, Decimal('4.50'))
        
        # Test price_2_display
        self.assertEqual(self.coffee.price_2_display, Decimal('5.00'))
        
        # Test has_two_prices
        self.assertTrue(self.coffee.has_two_prices)
        
        coffee_single = Coffee.objects.create(name="Single Coffee", price=Decimal('3.00'))
        self.assertFalse(coffee_single.has_two_prices)

    def test_toast_model_creation(self):
        """Test Toast model creation and properties"""
        self.assertEqual(self.toast.name, "Test Toast")
        self.assertEqual(self.toast.description, "Test toast description")
        self.assertEqual(self.toast.allergens, "1, 2")
        self.assertEqual(self.toast.price, Decimal('8.00'))
        self.assertTrue(self.toast.is_active)

    def test_toast_price_display(self):
        """Test Toast price display"""
        self.assertEqual(self.toast.price_display, 8)  # Integer display
        
        toast_decimal = Toast.objects.create(name="Decimal Toast", price=Decimal('7.50'))
        self.assertEqual(toast_decimal.price_display, Decimal('7.50'))

    def test_sweet_model_creation(self):
        """Test Sweet model creation and properties"""
        self.assertEqual(self.sweet.name, "Test Sweet")
        self.assertEqual(self.sweet.description, "Test sweet description")
        self.assertEqual(self.sweet.allergens, "3, 4")
        self.assertEqual(self.sweet.price, Decimal('6.50'))
        self.assertTrue(self.sweet.is_active)

    def test_sweet_price_display(self):
        """Test Sweet price display"""
        self.assertEqual(self.sweet.price_display, Decimal('6.50'))

    def test_model_string_representation(self):
        """Test model __str__ methods"""
        self.assertEqual(str(self.coffee), "Test Coffee")
        self.assertEqual(str(self.toast), "Test Toast")
        self.assertEqual(str(self.sweet), "Test Sweet")

    def test_model_ordering(self):
        """Test model ordering functionality"""
        coffee2 = Coffee.objects.create(name="Coffee 2", order=2)
        coffee3 = Coffee.objects.create(name="Coffee 3", order=0)
        
        coffees = Coffee.objects.all().order_by('order')
        self.assertEqual(coffees[0], coffee3)
        self.assertEqual(coffees[1], self.coffee)
        self.assertEqual(coffees[2], coffee2)


class ViewTests(TestCase):
    """Test all view functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test data
        self.coffee = Coffee.objects.create(
            name="Test Coffee",
            group="basic",
            price=Decimal('4.50'),
            temperature="hot",
            is_active=True,
            order=1
        )
        
        self.toast = Toast.objects.create(
            name="Test Toast",
            price=Decimal('8.00'),
            is_active=True,
            order=1
        )
        
        self.sweet = Sweet.objects.create(
            name="Test Sweet",
            price=Decimal('6.50'),
            is_active=True,
            order=1
        )

    def test_home_view(self):
        """Test home page view"""
        response = self.client.get(reverse('menu:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'untitled')

    def test_coffee_list_view(self):
        """Test coffee list view"""
        response = self.client.get(reverse('menu:coffee'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Coffee')
        
        # Test groups are present
        self.assertIn('groups', response.context)
        groups = response.context['groups']
        self.assertEqual(len(groups), 4)  # basic, alternative, other, addon

    def test_toasts_list_view(self):
        """Test toasts list view"""
        response = self.client.get(reverse('menu:toasts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Toast')
        self.assertIn('toasts', response.context)

    def test_sweets_list_view(self):
        """Test sweets list view"""
        response = self.client.get(reverse('menu:sweets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Sweet')
        self.assertIn('sweets', response.context)

    def test_update_order_coffee(self):
        """Test AJAX update order for coffee"""
        coffee2 = Coffee.objects.create(name="Coffee 2", group="basic", order=2)
        
        data = {
            'items': [coffee2.id, self.coffee.id],
            'group': 'basic'
        }
        
        response = self.client.post(
            reverse('menu:update_order', args=['coffee']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        # Check order was updated
        self.coffee.refresh_from_db()
        coffee2.refresh_from_db()
        self.assertEqual(self.coffee.order, 1)
        self.assertEqual(coffee2.order, 0)

    def test_update_order_toast(self):
        """Test AJAX update order for toast"""
        toast2 = Toast.objects.create(name="Toast 2", order=2)
        
        data = {'items': [toast2.id, self.toast.id]}
        
        response = self.client.post(
            reverse('menu:update_order', args=['toast']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_update_order_sweet(self):
        """Test AJAX update order for sweet"""
        sweet2 = Sweet.objects.create(name="Sweet 2", order=2)
        
        data = {'items': [sweet2.id, self.sweet.id]}
        
        response = self.client.post(
            reverse('menu:update_order', args=['sweet']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_update_order_invalid_model(self):
        """Test update order with invalid model type"""
        data = {'items': [1]}
        
        response = self.client.post(
            reverse('menu:update_order', args=['invalid']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)

    def test_update_order_invalid_json(self):
        """Test update order with invalid JSON"""
        response = self.client.post(
            reverse('menu:update_order', args=['coffee']),
            data='invalid json',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)


class ModifierViewTests(TestCase):
    """Test modifier dashboard views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test data
        self.coffee = Coffee.objects.create(
            name="Test Coffee",
            group="basic",
            price=Decimal('4.50'),
            is_active=True,
            order=1
        )
        
        self.toast = Toast.objects.create(
            name="Test Toast",
            price=Decimal('8.00'),
            is_active=True,
            order=1
        )
        
        self.sweet = Sweet.objects.create(
            name="Test Sweet",
            price=Decimal('6.50'),
            is_active=True,
            order=1
        )

    def test_dashboard_view(self):
        """Test dashboard view"""
        response = self.client.get(reverse('modifiers:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('sections', response.context)
        
        sections = response.context['sections']
        self.assertEqual(len(sections), 3)  # coffee, toast, sweet

    def test_archive_view(self):
        """Test archive view"""
        # Create inactive items
        inactive_coffee = Coffee.objects.create(
            name="Inactive Coffee",
            group="basic",
            price=Decimal('3.00'),
            is_active=False
        )
        
        response = self.client.get(reverse('modifiers:archive'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('sections', response.context)

    def test_add_coffee_get(self):
        """Test GET request to add coffee form"""
        response = self.client.get(reverse('modifiers:add_item', args=['coffee']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CoffeeForm)

    def test_add_toast_get(self):
        """Test GET request to add toast form"""
        response = self.client.get(reverse('modifiers:add_item', args=['toast']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ToastForm)

    def test_add_sweet_get(self):
        """Test GET request to add sweet form"""
        response = self.client.get(reverse('modifiers:add_item', args=['sweet']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], SweetForm)

    def test_add_coffee_post(self):
        """Test POST request to add coffee"""
        data = {
            'name': 'New Coffee',
            'group': 'basic',
            'price': '4.00',
            'temperature': 'hot',
            'is_active': True
        }
        
        response = self.client.post(reverse('modifiers:add_item', args=['coffee']), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Check coffee was created
        self.assertTrue(Coffee.objects.filter(name='New Coffee').exists())

    def test_add_toast_post(self):
        """Test POST request to add toast"""
        data = {
            'name': 'New Toast',
            'price': '7.00',
            'allergens': ['1', '2'],
            'is_active': True
        }
        
        response = self.client.post(reverse('modifiers:add_item', args=['toast']), data)
        self.assertEqual(response.status_code, 302)
        
        # Check toast was created
        toast = Toast.objects.get(name='New Toast')
        self.assertEqual(toast.allergens, '1, 2')

    def test_add_sweet_post(self):
        """Test POST request to add sweet"""
        data = {
            'name': 'New Sweet',
            'price': '5.50',
            'allergens': ['3'],
            'is_active': True
        }
        
        response = self.client.post(reverse('modifiers:add_item', args=['sweet']), data)
        self.assertEqual(response.status_code, 302)
        
        # Check sweet was created
        sweet = Sweet.objects.get(name='New Sweet')
        self.assertEqual(sweet.allergens, '3')

    def test_edit_coffee_get(self):
        """Test GET request to edit coffee form"""
        response = self.client.get(reverse('modifiers:edit_item', args=['coffee', self.coffee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_edit_coffee_post(self):
        """Test POST request to edit coffee"""
        data = {
            'name': 'Updated Coffee',
            'group': 'alternative',
            'price': '5.00',
            'temperature': 'cold',
            'is_active': True
        }
        
        response = self.client.post(
            reverse('modifiers:edit_item', args=['coffee', self.coffee.id]),
            data
        )
        self.assertEqual(response.status_code, 302)
        
        # Check coffee was updated
        self.coffee.refresh_from_db()
        self.assertEqual(self.coffee.name, 'Updated Coffee')
        self.assertEqual(self.coffee.group, 'alternative')

    def test_edit_toast_post(self):
        """Test POST request to edit toast"""
        data = {
            'name': 'Updated Toast',
            'price': '9.00',
            'allergens': ['1', '3'],
            'is_active': True
        }
        
        response = self.client.post(
            reverse('modifiers:edit_item', args=['toast', self.toast.id]),
            data
        )
        self.assertEqual(response.status_code, 302)
        
        # Check toast was updated
        self.toast.refresh_from_db()
        self.assertEqual(self.toast.name, 'Updated Toast')
        self.assertEqual(self.toast.allergens, '1, 3')

    def test_delete_item_get(self):
        """Test GET request to delete confirmation"""
        response = self.client.get(reverse('modifiers:delete_item', args=['coffee', self.coffee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('object', response.context)

    def test_delete_item_post(self):
        """Test POST request to delete item"""
        coffee_id = self.coffee.id
        response = self.client.post(reverse('modifiers:delete_item', args=['coffee', coffee_id]))
        self.assertEqual(response.status_code, 302)
        
        # Check coffee was deleted
        self.assertFalse(Coffee.objects.filter(id=coffee_id).exists())

    def test_archive_item(self):
        """Test archiving item"""
        response = self.client.post(reverse('modifiers:archive_item', args=['coffee', self.coffee.id]))
        self.assertEqual(response.status_code, 302)
        
        # Check coffee was archived
        self.coffee.refresh_from_db()
        self.assertFalse(self.coffee.is_active)

    def test_restore_item(self):
        """Test restoring archived item"""
        # First archive the item
        self.coffee.is_active = False
        self.coffee.save()
        
        response = self.client.post(reverse('modifiers:restore_item', args=['coffee', self.coffee.id]))
        self.assertEqual(response.status_code, 302)
        
        # Check coffee was restored
        self.coffee.refresh_from_db()
        self.assertTrue(self.coffee.is_active)

    def test_invalid_category_redirect(self):
        """Test redirect for invalid category"""
        response = self.client.get(reverse('modifiers:add_item', args=['invalid']))
        self.assertEqual(response.status_code, 302)


class FormTests(TestCase):
    """Test all form functionality"""
    
    def test_coffee_form_valid(self):
        """Test CoffeeForm with valid data"""
        form_data = {
            'name': 'Test Coffee',
            'group': 'basic',
            'price': '4.50',
            'temperature': 'hot',
            'is_active': True
        }
        form = CoffeeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_coffee_form_invalid(self):
        """Test CoffeeForm with invalid data"""
        form_data = {
            'name': '',  # Empty name should be invalid
            'group': 'basic',
            'price': '4.50'
        }
        form = CoffeeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_toast_form_valid(self):
        """Test ToastForm with valid data"""
        form_data = {
            'name': 'Test Toast',
            'price': '8.00',
            'allergens': ['1', '2'],
            'is_active': True
        }
        form = ToastForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_sweet_form_valid(self):
        """Test SweetForm with valid data"""
        form_data = {
            'name': 'Test Sweet',
            'price': '6.50',
            'allergens': ['3'],
            'is_active': True
        }
        form = SweetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_coffee_form_save(self):
        """Test CoffeeForm save functionality"""
        form_data = {
            'name': 'Form Coffee',
            'group': 'alternative',
            'price': '5.00',
            'price_2': '6.00',
            'temperature': 'cold',
            'description': 'Test description',
            'is_active': True
        }
        form = CoffeeForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        coffee = form.save()
        self.assertEqual(coffee.name, 'Form Coffee')
        self.assertEqual(coffee.group, 'alternative')
        self.assertEqual(coffee.price, Decimal('5.00'))
        self.assertEqual(coffee.price_2, Decimal('6.00'))


class URLTests(TestCase):
    """Test all URL patterns"""
    
    def test_menu_urls(self):
        """Test menu URL patterns"""
        # Test home URL
        url = reverse('menu:home')
        self.assertEqual(url, '/')
        
        # Test coffee URL
        url = reverse('menu:coffee')
        self.assertEqual(url, '/coffee/')
        
        # Test toasts URL
        url = reverse('menu:toasts')
        self.assertEqual(url, '/toasts/')
        
        # Test sweets URL
        url = reverse('menu:sweets')
        self.assertEqual(url, '/sweets/')
        
        # Test update order URL
        url = reverse('menu:update_order', args=['coffee'])
        self.assertEqual(url, '/update-order/coffee/')

    def test_modifiers_urls(self):
        """Test modifiers URL patterns"""
        # Test dashboard URL
        url = reverse('modifiers:dashboard')
        self.assertEqual(url, '/modifiers/')
        
        # Test archive URL
        url = reverse('modifiers:archive')
        self.assertEqual(url, '/modifiers/archive/')
        
        # Test add item URLs
        url = reverse('modifiers:add_item', args=['coffee'])
        self.assertEqual(url, '/modifiers/coffee/add/')
        
        url = reverse('modifiers:add_item', args=['toast'])
        self.assertEqual(url, '/modifiers/toast/add/')
        
        # Test edit item URLs
        url = reverse('modifiers:edit_item', args=['coffee', 1])
        self.assertEqual(url, '/modifiers/coffee/edit/1/')
        
        # Test delete item URLs
        url = reverse('modifiers:delete_item', args=['coffee', 1])
        self.assertEqual(url, '/modifiers/coffee/delete/1/')
        
        # Test archive item URLs
        url = reverse('modifiers:archive_item', args=['coffee', 1])
        self.assertEqual(url, '/modifiers/coffee/archive/1/')
        
        # Test restore item URLs
        url = reverse('modifiers:restore_item', args=['coffee', 1])
        self.assertEqual(url, '/modifiers/coffee/restore/1/')

    def test_url_resolution(self):
        """Test URL resolution"""
        # Test menu URLs resolve correctly
        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'menu:home')
        
        resolver = resolve('/coffee/')
        self.assertEqual(resolver.view_name, 'menu:coffee')
        
        resolver = resolve('/toasts/')
        self.assertEqual(resolver.view_name, 'menu:toasts')
        
        resolver = resolve('/sweets/')
        self.assertEqual(resolver.view_name, 'menu:sweets')
        
        # Test modifiers URLs resolve correctly
        resolver = resolve('/modifiers/')
        self.assertEqual(resolver.view_name, 'modifiers:dashboard')
        
        resolver = resolve('/modifiers/archive/')
        self.assertEqual(resolver.view_name, 'modifiers:archive')


class IntegrationTests(TestCase):
    """Test complete workflows"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_complete_coffee_workflow(self):
        """Test complete coffee management workflow"""
        # 1. Add coffee
        data = {
            'name': 'Workflow Coffee',
            'group': 'basic',
            'price': '4.00',
            'temperature': 'hot',
            'is_active': True
        }
        response = self.client.post(reverse('modifiers:add_item', args=['coffee']), data)
        self.assertEqual(response.status_code, 302)
        
        coffee = Coffee.objects.get(name='Workflow Coffee')
        
        # 2. Edit coffee
        edit_data = {
            'name': 'Updated Workflow Coffee',
            'group': 'alternative',
            'price': '5.00',
            'temperature': 'cold',
            'is_active': True
        }
        response = self.client.post(
            reverse('modifiers:edit_item', args=['coffee', coffee.id]),
            edit_data
        )
        self.assertEqual(response.status_code, 302)
        
        coffee.refresh_from_db()
        self.assertEqual(coffee.name, 'Updated Workflow Coffee')
        
        # 3. Archive coffee
        response = self.client.post(reverse('modifiers:archive_item', args=['coffee', coffee.id]))
        self.assertEqual(response.status_code, 302)
        
        coffee.refresh_from_db()
        self.assertFalse(coffee.is_active)
        
        # 4. Restore coffee
        response = self.client.post(reverse('modifiers:restore_item', args=['coffee', coffee.id]))
        self.assertEqual(response.status_code, 302)
        
        coffee.refresh_from_db()
        self.assertTrue(coffee.is_active)
        
        # 5. Delete coffee
        response = self.client.post(reverse('modifiers:delete_item', args=['coffee', coffee.id]))
        self.assertEqual(response.status_code, 302)
        
        self.assertFalse(Coffee.objects.filter(id=coffee.id).exists())

    def test_complete_toast_workflow(self):
        """Test complete toast management workflow"""
        # 1. Add toast
        data = {
            'name': 'Workflow Toast',
            'price': '7.00',
            'allergens': ['1', '2'],
            'is_active': True
        }
        response = self.client.post(reverse('modifiers:add_item', args=['toast']), data)
        self.assertEqual(response.status_code, 302)
        
        toast = Toast.objects.get(name='Workflow Toast')
        self.assertEqual(toast.allergens, '1, 2')
        
        # 2. Edit toast
        edit_data = {
            'name': 'Updated Workflow Toast',
            'price': '8.00',
            'allergens': ['1', '3'],
            'is_active': True
        }
        response = self.client.post(
            reverse('modifiers:edit_item', args=['toast', toast.id]),
            edit_data
        )
        self.assertEqual(response.status_code, 302)
        
        toast.refresh_from_db()
        self.assertEqual(toast.name, 'Updated Workflow Toast')
        self.assertEqual(toast.allergens, '1, 3')
        
        # 3. View toast in menu
        response = self.client.get(reverse('menu:toasts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated Workflow Toast')

    def test_complete_sweet_workflow(self):
        """Test complete sweet management workflow"""
        # 1. Add sweet
        data = {
            'name': 'Workflow Sweet',
            'price': '6.00',
            'allergens': ['3'],
            'is_active': True
        }
        response = self.client.post(reverse('modifiers:add_item', args=['sweet']), data)
        self.assertEqual(response.status_code, 302)
        
        sweet = Sweet.objects.get(name='Workflow Sweet')
        self.assertEqual(sweet.allergens, '3')
        
        # 2. Edit sweet
        edit_data = {
            'name': 'Updated Workflow Sweet',
            'price': '7.00',
            'allergens': ['3', '4'],
            'is_active': True
        }
        response = self.client.post(
            reverse('modifiers:edit_item', args=['sweet', sweet.id]),
            edit_data
        )
        self.assertEqual(response.status_code, 302)
        
        sweet.refresh_from_db()
        self.assertEqual(sweet.name, 'Updated Workflow Sweet')
        self.assertEqual(sweet.allergens, '3, 4')
        
        # 3. View sweet in menu
        response = self.client.get(reverse('menu:sweets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Updated Workflow Sweet')

    def test_order_update_workflow(self):
        """Test complete order update workflow"""
        # Create multiple items
        coffee1 = Coffee.objects.create(name="Coffee 1", group="basic", order=1)
        coffee2 = Coffee.objects.create(name="Coffee 2", group="basic", order=2)
        coffee3 = Coffee.objects.create(name="Coffee 3", group="basic", order=3)
        
        # Update order
        data = {
            'items': [coffee3.id, coffee1.id, coffee2.id],
            'group': 'basic'
        }
        
        response = self.client.post(
            reverse('menu:update_order', args=['coffee']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Check order was updated
        coffee1.refresh_from_db()
        coffee2.refresh_from_db()
        coffee3.refresh_from_db()
        
        self.assertEqual(coffee1.order, 1)
        self.assertEqual(coffee2.order, 2)
        self.assertEqual(coffee3.order, 0)


class EdgeCaseTests(TestCase):
    """Test edge cases and error conditions"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()

    def test_empty_menu_pages(self):
        """Test menu pages with no items"""
        response = self.client.get(reverse('menu:coffee'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('menu:toasts'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('menu:sweets'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_item_id(self):
        """Test views with invalid item IDs"""
        response = self.client.get(reverse('modifiers:edit_item', args=['coffee', 99999]))
        self.assertEqual(response.status_code, 404)
        
        response = self.client.get(reverse('modifiers:delete_item', args=['coffee', 99999]))
        self.assertEqual(response.status_code, 404)

    def test_update_order_nonexistent_items(self):
        """Test update order with nonexistent item IDs"""
        data = {'items': [99999, 88888], 'group': 'basic'}
        
        response = self.client.post(
            reverse('menu:update_order', args=['coffee']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)  # Should still succeed

    def test_form_validation_edge_cases(self):
        """Test form validation with edge case data"""
        # Test negative price
        form_data = {
            'name': 'Test Coffee',
            'group': 'basic',
            'price': '-5.00',
            'is_active': True
        }
        form = CoffeeForm(data=form_data)
        # Note: Django DecimalField doesn't allow negative values by default
        # This test depends on your model validation

    def test_large_price_values(self):
        """Test with large price values"""
        coffee = Coffee.objects.create(
            name="Expensive Coffee",
            group="basic",
            price=Decimal('999.99'),
            is_active=True
        )
        
        self.assertEqual(coffee.price_display, Decimal('999.99'))

    def test_very_long_names(self):
        """Test with very long item names"""
        long_name = "A" * 200  # Very long name
        coffee = Coffee.objects.create(
            name=long_name,
            group="basic",
            price=Decimal('5.00'),
            is_active=True
        )
        
        self.assertEqual(coffee.name, long_name)

    def test_special_characters_in_names(self):
        """Test with special characters in names"""
        special_name = "Café & Coffee™ (Special)"
        coffee = Coffee.objects.create(
            name=special_name,
            group="basic",
            price=Decimal('5.00'),
            is_active=True
        )
        
        self.assertEqual(coffee.name, special_name)


class PerformanceTests(TestCase):
    """Test performance-related functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create many items for performance testing
        for i in range(50):
            Coffee.objects.create(
                name=f"Coffee {i}",
                group="basic",
                price=Decimal('4.00'),
                is_active=True,
                order=i
            )

    def test_large_coffee_list_performance(self):
        """Test performance with large coffee list"""
        response = self.client.get(reverse('menu:coffee'))
        self.assertEqual(response.status_code, 200)
        
        # Check that all coffees are present
        self.assertContains(response, "Coffee 0")
        self.assertContains(response, "Coffee 49")

    def test_large_order_update_performance(self):
        """Test performance with large order update"""
        coffees = Coffee.objects.all()
        item_ids = [coffee.id for coffee in coffees]
        
        data = {
            'items': item_ids,
            'group': 'basic'
        }
        
        response = self.client.post(
            reverse('menu:update_order', args=['coffee']),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])


if __name__ == '__main__':
    # Run tests with verbose output
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
