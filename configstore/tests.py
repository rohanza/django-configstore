import unittest

from django.test import TestCase
from django.test.client import Client
from django.core import urlresolvers
from django.contrib import admin
from django import forms

from configs import ConfigurationInstance, register, get_config, CONFIG_CACHE
from forms import ConfigurationForm
from models import Configuration

class TestConfigurationForm(ConfigurationForm):
    setting1 = forms.CharField()
    setting2 = forms.IntegerField()

class ConfigStoreTest(TestCase):
    def setUp(self):
        if hasattr(CONFIG_CACHE, 'test'):
            delattr(CONFIG_CACHE, 'test')
        self.instance = ConfigurationInstance('test', 'test', TestConfigurationForm)
        register(self.instance)

    def test_register_and_retrieve_config(self):
        form_builder = self.instance.get_form_builder()
        lazydictionary_post = get_config('test')
        form = form_builder({'setting1':'wooot', 'setting2':'2', 'site':'1'}, {})
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertNotEqual(0, len(get_config('test').items()))
        self.assertNotEqual(0, len(lazydictionary_post.items()))
    
    def test_empty_config(self):
        lazydictionary_pre = get_config('test')
        self.assertEqual(0, len(lazydictionary_pre.items()))
    
    def test_configstore_admin(self):
        admin.autodiscover()
        admin_entry = admin.site._registry[Configuration]
        class dummy_user(object):
            has_perm = lambda *x: False
            get_and_delete_messages = lambda *x: []
            
        class dummy_request(object):
            REQUEST = dict()
            POST = dict()
            GET = dict()
            FILES = dict()
            user = dummy_user()
        admin_entry.add_view(dummy_request())
        