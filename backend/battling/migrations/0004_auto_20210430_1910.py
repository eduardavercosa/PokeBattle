# Generated by Django 3.1.7 on 2021-04-30 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battling', '0003_battle_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='creator_pokemon_1',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='creator_pokemon_2',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='creator_pokemon_3',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='opponent_pokemon_1',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='opponent_pokemon_2',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='opponent_pokemon_3',
        ),
    ]