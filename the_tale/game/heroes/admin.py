# -*- coding: utf-8 -*-

from django.contrib import admin

from game.heroes.models import Hero, HeroPreferences

class HeroAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_alive', 'health', 'account')
    readonly_fields = ('created_at_turn', 'saved_at_turn', 'saved_at', 'account')

class HeroPreferencesAdmin(admin.ModelAdmin):
    list_display = ('id', 'hero', 'energy_regeneration_type', 'mob', 'place', 'friend', 'enemy', 'equipment_slot')


admin.site.register(Hero, HeroAdmin)
admin.site.register(HeroPreferences, HeroPreferencesAdmin)
