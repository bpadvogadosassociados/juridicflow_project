# apps/shared/tests.py (atualizar)

from django.test import TestCase, RequestFactory
from apps.accounts.models import User
from apps.organizations.models import Organization
from apps.offices.models import Office
from apps.memberships.models import Membership
from apps.customers.models import Customer
from apps.processes.models import Process
from apps.shared.middleware import OrganizationMiddleware

class IsolationTest(TestCase):
    """
    Testa isolamento de dados entre organizações.
    """
    
    def setUp(self):
        # Criar 2 organizações diferentes
        self.org1 = Organization.objects.create(
            name='Org 1',
            document='11111111111111'
        )
        
        self.org2 = Organization.objects.create(
            name='Org 2',
            document='22222222222222'
        )
        
        # Criar offices
        self.office1 = Office.objects.create(
            organization=self.org1,
            name='Office 1'
        )
        
        self.office2 = Office.objects.create(
            organization=self.org2,
            name='Office 2'
        )
        
        # Criar usuários
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='test123'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='test123'
        )
        
        # Criar memberships
        self.membership1 = Membership.objects.create(
            user=self.user1,
            organization=self.org1,
            office=self.office1,
            role='lawyer'
        )
        
        self.membership2 = Membership.objects.create(
            user=self.user2,
            organization=self.org2,
            office=self.office2,
            role='lawyer'
        )
        
        # Criar dados
        self.customer1 = Customer.objects.create(
            organization=self.org1,
            office=self.office1,
            name='Customer 1',
            document='11111111111',
            type='PF'
        )
        
        self.customer2 = Customer.objects.create(
            organization=self.org2,
            office=self.office2,
            name='Customer 2',
            document='22222222222',
            type='PF'
        )
        
        self.factory = RequestFactory()
    
    def test_customer_isolation(self):
        """Testa se customers estão isolados por organização"""
        # Org 1 não vê customers da Org 2
        customers_org1 = Customer.objects.filter(organization=self.org1)
        self.assertEqual(customers_org1.count(), 1)
        self.assertEqual(customers_org1.first(), self.customer1)
        
        # Org 2 não vê customers da Org 1
        customers_org2 = Customer.objects.filter(organization=self.org2)
        self.assertEqual(customers_org2.count(), 1)
        self.assertEqual(customers_org2.first(), self.customer2)
    
    def test_manager_for_request(self):
        """Testa se manager for_request filtra corretamente"""
        # Simular request do user1
        request = self.factory.get('/')
        request.user = self.user1
        request.organization = self.org1
        request.office = self.office1
        
        # Só deve ver customers da sua org
        customers = Customer.objects.for_request(request)
        self.assertEqual(customers.count(), 1)
        self.assertEqual(customers.first(), self.customer1)
    
    def test_cannot_access_other_org_data(self):
        """Testa que não consegue acessar dados de outra org"""
        # User 1 tenta acessar customer da org 2
        with self.assertRaises(Customer.DoesNotExist):
            Customer.objects.get(
                organization=self.org1,
                pk=self.customer2.pk
            )
    
    def test_unique_document_per_organization(self):
        """Testa que o mesmo documento pode existir em orgs diferentes"""
        # Mesmo CPF em organizações diferentes (deve funcionar)
        customer3 = Customer.objects.create(
            organization=self.org2,
            office=self.office2,
            name='Customer 3',
            document='11111111111',  # Mesmo CPF do customer1
            type='PF'
        )
        
        self.assertEqual(
            Customer.objects.filter(document='11111111111').count(),
            2
        )
        
        # Mas não pode ter o mesmo CPF na mesma org
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                organization=self.org1,
                office=self.office1,
                name='Customer Duplicado',
                document='11111111111',  # Duplicado na org1
                type='PF'
            )


class PermissionTest(TestCase):
    """
    Testa sistema de permissões.
    """
    
    def setUp(self):
        self.org = Organization.objects.create(
            name='Test Org',
            document='12345678000190'
        )
        
        self.office = Office.objects.create(
            organization=self.org,
            name='Test Office'
        )
        
        # Criar usuários com diferentes roles
        self.org_admin = User.objects.create_user(
            username='org_admin',
            email='org_admin@test.com',
            password='test123'
        )
        
        self.lawyer = User.objects.create_user(
            username='lawyer',
            email='lawyer@test.com',
            password='test123'
        )
        
        self.intern = User.objects.create_user(
            username='intern',
            email='intern@test.com',
            password='test123'
        )
        
        # Criar memberships
        Membership.objects.create(
            user=self.org_admin,
            organization=self.org,
            office=self.office,
            role='org_admin'
        )
        
        Membership.objects.create(
            user=self.lawyer,
            organization=self.org,
            office=self.office,
            role='lawyer'
        )
        
        Membership.objects.create(
            user=self.intern,
            organization=self.org,
            office=self.office,
            role='intern'
        )
    
    def test_organization_admin_permission(self):
        """Testa permissão de Organization Admin"""
        from apps.shared.permissions import IsOrganizationAdmin
        
        permission = IsOrganizationAdmin()
        
        # Org admin tem permissão
        self.assertTrue(
            permission.has_permission(self.org_admin, self.org)
        )
        
        # Lawyer não tem
        self.assertFalse(
            permission.has_permission(self.lawyer, self.org)
        )
        
        # Intern não tem
        self.assertFalse(
            permission.has_permission(self.intern, self.org)
        )
    
    def test_can_manage_customers(self):
        """Testa permissão para gerenciar clientes"""
        from apps.shared.permissions import CanManageCustomers
        
        permission = CanManageCustomers()
        
        # Org admin pode
        self.assertTrue(
            permission.has_permission(self.org_admin, self.org)
        )
        
        # Lawyer pode
        self.assertTrue(
            permission.has_permission(self.lawyer, self.org)
        )
        
        # Intern não pode
        self.assertFalse(
            permission.has_permission(self.intern, self.org)
        )