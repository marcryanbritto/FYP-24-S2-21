# myapp/management/commands/encrypt_gene_sequences.py
from django.core.management.base import BaseCommand
from users.models import Gene

class Command(BaseCommand):
    help = 'Encrypt existing gene sequences in the database'

    def handle(self, *args, **kwargs):
        genes = Gene.objects.all()
        updated_count = 0

        for gene in genes:
            if not gene.sequence.startswith('ENC:'):
                gene.sequence = gene.encrypt_sequence(gene.sequence)
                gene.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Encrypted {updated_count} gene sequences.'))
