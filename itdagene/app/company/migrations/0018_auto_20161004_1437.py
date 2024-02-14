import sorl.thumbnail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("company", "0017_auto_20160315_1953")]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="is_collaborator",
            field=models.BooleanField(default=False, verbose_name="collaborator"),
        ),
        migrations.AlterField(
            model_name="company",
            name="logo",
            field=sorl.thumbnail.fields.ImageField(
                blank=True, null=True, upload_to="company_logos/", verbose_name="logo"
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="payment_email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="payment email"
            ),
        ),
        migrations.AlterField(
            model_name="companycontact",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="e-mail address"
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="file",
            field=models.FileField(upload_to="contracts/", verbose_name="file"),
        ),
    ]
