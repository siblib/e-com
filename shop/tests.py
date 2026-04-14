from django.test import TestCase, Client
from django.urls import reverse
from shop.models.products import Category

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create categories: one top-level, one child
        self.parent = Category.objects.create(name="Parent", slug="parent")
        self.child = Category.objects.create(name="Child", slug="child", parent=self.parent)

    def test_home_page_context_categories(self):
        """Verify that only top-level categories are passed to the home page context."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', response.context)
        categories = response.context['categories']

        # Should only contain the parent category
        self.assertEqual(categories.count(), 1)
        self.assertEqual(categories[0].name, "Parent")
        self.assertNotIn(self.child, categories)

    def test_home_page_renders_categories(self):
        """Verify that category names are rendered in the HTML."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Parent")
        self.assertNotContains(response, "Child")
