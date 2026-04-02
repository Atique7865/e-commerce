"""
services/management/commands/seed_services.py
Run: python manage.py seed_services
Creates the three core TalentHeart services with sample features.
"""
from django.core.management.base import BaseCommand
from services.models import Service, ServiceFeature


SERVICES_DATA = [
    {
        'name': 'Digital Marketing',
        'category': 'digital_marketing',
        'icon_class': 'bi bi-graph-up-arrow',
        'short_description': 'Data-driven campaigns that grow your brand and drive revenue.',
        'description': (
            'Our Digital Marketing service covers every channel needed to build a strong online presence. '
            'From SEO and PPC to social media management and email automation, our team crafts bespoke '
            'strategies aligned with your business goals. We are obsessed with ROI and provide transparent '
            'reporting so you always know the impact of every dollar spent.'
        ),
        'price': 999.00,
        'features': [
            'Search Engine Optimisation (SEO)',
            'Google & Meta Ads (PPC)',
            'Social Media Management',
            'Email Marketing Automation',
            'Conversion Rate Optimisation',
            'Monthly Analytics Reporting',
        ],
    },
    {
        'name': 'Web Development',
        'category': 'web_development',
        'icon_class': 'bi bi-code-slash',
        'short_description': 'Beautiful, fast, and scalable web applications tailored for your business.',
        'description': (
            'We design and develop modern web applications using industry-leading technologies such as '
            'Django, React, and Next.js. Whether you need a corporate website, a complex SaaS platform, '
            'or an e-commerce store, we deliver pixel-perfect, mobile-first solutions with clean code '
            'and thorough documentation so your team can maintain and extend it confidently.'
        ),
        'price': 2499.00,
        'features': [
            'Custom UI/UX Design',
            'Responsive & Mobile-First Development',
            'Django / React / Next.js Stack',
            'REST API & Third-party Integrations',
            'Performance & SEO Optimisation',
            '3 Months Post-launch Support',
        ],
    },
    {
        'name': 'DevOps & Cloud',
        'category': 'devops',
        'icon_class': 'bi bi-cloud-check',
        'short_description': 'Reliable CI/CD pipelines and cloud infrastructure for seamless deployments.',
        'description': (
            'Our DevOps engineers streamline your software delivery lifecycle using battle-tested tools '
            'like Docker, Kubernetes, GitHub Actions, and Terraform. We set up robust CI/CD pipelines, '
            'configure auto-scaling cloud infrastructure on AWS/GCP/Azure, and implement monitoring and '
            'alerting so your team ships with confidence and your systems run 24/7.'
        ),
        'price': 1799.00,
        'features': [
            'CI/CD Pipeline Setup (GitHub Actions / GitLab CI)',
            'Docker & Kubernetes Containerisation',
            'AWS / GCP / Azure Cloud Setup',
            'Infrastructure as Code (Terraform)',
            'Monitoring & Alerting (Prometheus / Grafana)',
            'Security Audits & Compliance',
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with the three core TalentHeart services.'

    def handle(self, *args, **options):
        created_count = 0
        for data in SERVICES_DATA:
            features = data.pop('features')
            service, created = Service.objects.get_or_create(
                name=data['name'],
                defaults=data,
            )
            if created:
                for idx, feat in enumerate(features):
                    ServiceFeature.objects.create(service=service, feature=feat, order=idx)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {service.name}'))
            else:
                self.stdout.write(f'  Already exists: {service.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone — {created_count} service(s) created.'
        ))
