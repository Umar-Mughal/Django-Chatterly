# Generated by Django 5.0.6 on 2024-05-15 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="emailverification",
            name="email_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("register", "Register Email Verification"),
                    ("reset_password", "Reset Password"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="emailverification",
            unique_together={("user", "email_type", "code")},
        ),
    ]
