# Generated by Django 4.2.6 on 2023-10-31 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nasname', models.CharField(max_length=128)),
                ('shortname', models.CharField(blank=True, max_length=32, null=True)),
                ('type', models.CharField(blank=True, max_length=30, null=True)),
                ('ports', models.IntegerField(blank=True, null=True)),
                ('secret', models.CharField(max_length=60)),
                ('server', models.CharField(blank=True, max_length=64, null=True)),
                ('community', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'nas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Radacct',
            fields=[
                ('radacctid', models.BigAutoField(primary_key=True, serialize=False)),
                ('acctsessionid', models.CharField(max_length=64)),
                ('acctuniqueid', models.CharField(max_length=32, unique=True)),
                ('username', models.CharField(max_length=64)),
                ('realm', models.CharField(blank=True, max_length=64, null=True)),
                ('nasipaddress', models.CharField(max_length=15)),
                ('nasportid', models.CharField(blank=True, max_length=32, null=True)),
                ('nasporttype', models.CharField(blank=True, max_length=32, null=True)),
                ('acctstarttime', models.DateTimeField(blank=True, null=True)),
                ('acctupdatetime', models.DateTimeField(blank=True, null=True)),
                ('acctstoptime', models.DateTimeField(blank=True, null=True)),
                ('acctinterval', models.IntegerField(blank=True, null=True)),
                ('acctsessiontime', models.PositiveIntegerField(blank=True, null=True)),
                ('acctauthentic', models.CharField(blank=True, max_length=32, null=True)),
                ('connectinfo_start', models.CharField(blank=True, max_length=128, null=True)),
                ('connectinfo_stop', models.CharField(blank=True, max_length=128, null=True)),
                ('acctinputoctets', models.BigIntegerField(blank=True, null=True)),
                ('acctoutputoctets', models.BigIntegerField(blank=True, null=True)),
                ('calledstationid', models.CharField(max_length=50)),
                ('callingstationid', models.CharField(max_length=50)),
                ('acctterminatecause', models.CharField(max_length=32)),
                ('servicetype', models.CharField(blank=True, max_length=32, null=True)),
                ('framedprotocol', models.CharField(blank=True, max_length=32, null=True)),
                ('framedipaddress', models.CharField(max_length=15)),
                ('framedipv6address', models.CharField(max_length=45)),
                ('framedipv6prefix', models.CharField(max_length=45)),
                ('framedinterfaceid', models.CharField(max_length=44)),
                ('delegatedipv6prefix', models.CharField(max_length=45)),
                ('class_field', models.CharField(blank=True, db_column='class', max_length=64, null=True)),
            ],
            options={
                'db_table': 'radacct',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Radcheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radcheck',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Radgroupcheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radgroupcheck',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Radgroupreply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radgroupreply',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Radpostauth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('pass_field', models.CharField(db_column='pass', max_length=64)),
                ('reply', models.CharField(max_length=32)),
                ('authdate', models.DateTimeField()),
                ('class_field', models.CharField(blank=True, db_column='class', max_length=64, null=True)),
            ],
            options={
                'db_table': 'radpostauth',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Radreply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('attribute', models.CharField(max_length=64)),
                ('op', models.CharField(max_length=2)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'radreply',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Radusergroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('groupname', models.CharField(max_length=64)),
                ('priority', models.IntegerField()),
            ],
            options={
                'db_table': 'radusergroup',
                'managed': True,
            },
        ),
    ]
