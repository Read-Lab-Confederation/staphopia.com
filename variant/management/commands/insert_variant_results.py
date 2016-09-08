""" Insert variant analysis results into database. """
from __future__ import print_function
from os.path import basename, splitext
import sys
import time
import vcf

from django.db import transaction
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError

from staphopia.utils import timeit
from sample.models import MetaData
from variant.models import (
    Annotation,
    Comment,
    Filter,
    Indel,
    Reference,
    SNP,
    ToIndel,
    ToSNP,
    Counts
)


class Command(BaseCommand):

    """ Insert results into database. """
    help = 'Insert the analysis results into the database.'

    def add_arguments(self, parser):
        parser.add_argument('sample_tag', metavar='SAMPLE_TAG',
                            help='Sample tag for which the data is for')
        parser.add_argument('input', metavar='INPUT_VCF',
                            help=('Gzipped annotated VCF formated file to '
                                  'be inserted'))

    def handle(self, *args, **opts):
        """ Insert results to database. """

        # Get sample and pipeline instances
        print('Working on {0}.'.format(opts['sample_tag']), file=sys.stderr)
        self.get_sample_instance(opts['sample_tag'])

        # Open VCF for reading
        self.open_vcf(opts['input'])

        # Get reference info
        self.get_reference_instance()

        # Get data already in the DB
        self.get_annotation_instances()
        self.get_locus_tags()
        self.get_comments()
        self.get_comment_instances()
        self.get_filters()
        self.get_filter_instances()
        self.get_snps()

        # Store variants for bulk create
        self.snps = []
        self.indels = []
        self.confidence = []

        # Read through VCF, and insert Confidences
        self.read_vcf()

        # Ready to insert variants and confidence
        self.insert_snps()
        self.insert_indels()
        self.insert_confidence()
        self.insert_counts()

    def get_sample_instance(self, sample_tag):
        try:
            self.sample = MetaData.objects.get(sample_tag=sample_tag)
        except MetaData.DoesNotExist:
            raise CommandError('SAMPLE_TAG: {0} does not exist'.format(
                sample_tag
            ))

        try:
            count = Counts.objects.get(sample=self.sample)

            # Get difference in counts
            diff = count.confidence - (count.snp + count.indel)
            if diff:
                # File didn't completely load, delete and reload
                print(
                    ('{0} did not complete in previous attempt, deleting '
                     'existing records.').format(sample_tag),
                    file=sys.stderr
                )
                self.delete_objects()
            # Test to make sure all counts are not 0
            else:
                if count.confidence and count.snp and count.indel:
                    # File has been loaded
                    raise CommandError('{0} has been loaded, exiting.'.format(
                        sample_tag
                    ))
        except Counts.DoesNotExist:
            self.delete_objects()
            print(
                ('{0} will be loaded.').format(sample_tag),
                file=sys.stderr
            )

    @timeit
    def get_positions(self):
        self.positions = [record.POS for record in self.records]

    @timeit
    def open_vcf(self, input):
        try:
            self.vcf_reader = vcf.Reader(open(input, 'r'), compressed=True)
            self.records = [record for record in self.vcf_reader]
        except IOError:
            raise CommandError('{0} does not exist'.format(input))

    @transaction.atomic
    def get_reference_instance(self):
        try:
            r = splitext(basename(self.vcf_reader.metadata['reference']))[0]
            self.reference, created = Reference.objects.get_or_create(
                name=r
            )
        except IntegrityError:
            raise CommandError('Error getting/saving reference information')

    @timeit
    def get_locus_tags(self):
        """ Return the primary key of each locus tag. """
        self.locus_tags = {}
        for tag in Annotation.objects.filter(reference=self.reference):
            self.locus_tags[tag.locus_tag] = tag.pk

    @timeit
    def get_annotation_instances(self):
        """ Return the instance for each annotation. """
        pks = []
        for ks in Annotation.objects.filter(reference=self.reference):
            pks.append(ks.pk)
        self.annotations = Annotation.objects.in_bulk(pks)

    def get_comments(self):
        """ Return the primary key of each comment. """
        self.comments = {}
        for c in Comment.objects.all():
            self.comments[c.comment] = c.pk

    @timeit
    def get_comment_instances(self):
        """ Return the instance for each comment. """
        pks = []
        for ks in Comment.objects.all():
            pks.append(ks.pk)
        self.comment_instances = Comment.objects.in_bulk(pks)

    @timeit
    def get_filters(self):
        """ Return the primary key of each comment. """
        self.filters = {}
        for f in Filter.objects.all():
            self.filters[f.name] = f.pk

    @timeit
    def get_filter_instances(self):
        """ Return the instance for each comment. """
        pks = []
        for ks in Filter.objects.all():
            pks.append(ks.pk)
        self.filter_instances = Filter.objects.in_bulk(pks)

    @transaction.atomic
    def get_annotation(self, record):
        annotation = None
        locus_tag = record.INFO['LocusTag'][0]
        if locus_tag in self.locus_tags:
            pk = self.locus_tags[locus_tag]
            annotation = self.annotations[pk]
        elif locus_tag is not None:
            annotation = Annotation.objects.create(
                reference=self.reference,
                locus_tag=locus_tag,
                protein_id=record.INFO['ProteinID'][0],
                gene=('.' if record.INFO['Gene'][0] is None
                      else record.INFO['Gene'][0]),
                db_xref=''.join(record.INFO['DBXref']),
                product=('.' if record.INFO['Product'][0] is None
                         else record.INFO['Product'][0]),
                note=('.' if record.INFO['Note'][0] is None
                      else record.INFO['Note'][0])
            )
            self.locus_tags[locus_tag] = annotation.pk
            self.annotations[annotation.pk] = annotation
        elif locus_tag is None:
            if 'inter_genic' not in self.locus_tags:
                annotation = Annotation.objects.create(
                    reference=self.reference,
                    locus_tag='inter_genic',
                    protein_id='inter_genic',
                    gene='inter_genic',
                    db_xref='inter_genic',
                    product='inter_genic',
                    note='inter_genic'
                )
                self.locus_tags['inter_genic'] = annotation.pk
                self.annotations[annotation.pk] = annotation
            else:
                pk = self.locus_tags['inter_genic']
                annotation = self.annotations[pk]

        return annotation

    @transaction.atomic
    def get_filter(self, filter):
        record_filters = None
        f = None
        if len(filter) == 0:
            f = 'PASS'
        else:
            f = ', '.join(filter)

        if f in self.filters:
            pk = self.filters[f]
            record_filters = self.filter_instances[pk]
        else:
            record_filters = Filter.objects.create(name=f)
            self.filters[f] = record_filters.pk
            self.filter_instances[record_filters.pk] = record_filters

        return record_filters

    @transaction.atomic
    def get_comment(self, c):
        comment = None
        if c is None:
            c = 'None'

        if c in self.comments:
            pk = self.comments[c]
            comment = self.comment_instances[pk]
        else:
            comment = Comment.objects.create(comment=c)
            self.comments[c] = comment.pk
            self.comment_instances[comment.pk] = comment

        return comment

    @transaction.atomic
    @timeit
    def create_snp(self, record, reference, annotation):
        return SNP.objects.create(
            reference=reference,
            annotation=annotation,
            reference_position=record.POS,
            reference_base=record.REF,
            alternate_base=record.ALT[0],

            reference_codon=('.' if record.INFO['RefCodon'][0] is None
                             else record.INFO['RefCodon'][0]),
            alternate_codon=('.' if record.INFO['AltCodon'][0] is None
                             else record.INFO['AltCodon'][0]),
            reference_amino_acid=('.' if record.INFO['RefAminoAcid'][0] is None
                                  else record.INFO['RefAminoAcid'][0]),
            alternate_amino_acid=('.' if record.INFO['AltAminoAcid'][0] is None
                                  else record.INFO['AltAminoAcid'][0]),
            codon_position=(0 if record.INFO['CodonPosition'] is None
                            else record.INFO['CodonPosition']),
            snp_codon_position=(0 if record.INFO['SNPCodonPosition'] is None
                                else record.INFO['SNPCodonPosition']),
            amino_acid_change=('.' if record.INFO['AminoAcidChange'][0] is None
                               else record.INFO['AminoAcidChange'][0]),
            is_synonymous=record.INFO['IsSynonymous'],
            is_transition=record.INFO['IsTransition'],
            is_genic=record.INFO['IsGenic'],
        )

    def get_snps(self):
        self.all_snps = {}
        for snp in SNP.objects.filter(
            reference=self.reference,
            reference_position__in=[record.POS for record in self.records]
        ):
            key = (
                snp.reference_position,
                snp.reference_base,
                snp.alternate_base
            )
            self.all_snps[key] = snp.pk

    def get_snp(self, record, reference, annotation):
        snp = False
        while not snp:
            try:
                snp = self.all_snps[(
                    record.POS,
                    record.REF,
                    str(record.ALT[0])
                )]
            except KeyError:
                try:
                    snp = self.create_snp(record, reference, annotation).pk
                except IntegrityError:
                    print("trying SNP ({0},{1}->{2}) again".format(
                        record.POS, record.REF, record.ALT[0]
                    ), file=sys.stderr)
                    time.sleep(1)
                    continue

        return snp

    @transaction.atomic
    def create_indel(self, record, reference, annotation):
        return Indel.objects.create(
            reference=reference,
            annotation=annotation,
            reference_position=record.POS,
            reference_base=record.REF,
            alternate_base=(record.ALT if len(record.ALT) > 1 else
                            record.ALT[0]),
            is_deletion=record.is_deletion
        )

    def get_indel(self, record, reference, annotation):
        # Get or create InDel
        indel = False
        while not indel:
            try:
                indel = Indel.objects.get(
                    reference=reference,
                    reference_position=record.POS,
                    reference_base=record.REF,
                    alternate_base=(record.ALT if len(record.ALT) > 1 else
                                    record.ALT[0]),
                )
            except Indel.DoesNotExist:
                try:
                    indel = self.create_indel(record, reference, annotation)
                except IntegrityError:
                    print("trying Indel ({0},{1}->{2}) again".format(
                        record.POS, record.REF, record.ALT
                    ), file=sys.stderr)
                    time.sleep(1)
                    continue

        return indel

    @timeit
    def read_vcf(self):
        # Insert VCF Records
        for record in self.records:
            # Get annotation, filter, comment
            annotation = self.get_annotation(record)
            record_filters = self.get_filter(record.FILTER)

            # Store variant confidence
            self.confidence.append(
                Confidence(
                    sample=self.sample,
                    reference_position=record.POS,
                    AC=str(record.INFO['AC']),
                    AD=str(record.samples[0]['AD']),
                    AF=record.INFO['AF'][0],
                    DP=record.INFO['DP'],
                    GQ=record.samples[0]['GQ'],
                    GT=record.samples[0]['GT'],
                    MQ=record.INFO['MQ'],
                    PL=str(record.samples[0]['PL']),
                    QD=record.INFO['QD'],
                    quality=record.QUAL
                )
            )

            # Insert SNP/Indel
            if record.is_snp:
                comment = self.get_comment(record.INFO['Comments'][0])
                snp = self.get_snp(record, self.reference, annotation)

                # Store SNP
                try:
                    self.snps.append(
                        ToSNP(
                            sample=self.sample,
                            snp_id=snp,
                            comment=comment,
                            filters=record_filters
                        )
                    )
                except IntegrityError as e:
                    raise CommandError('ToSNP Error: {0}'.format(e))
            else:
                indel = self.get_indel(record, self.reference, annotation)

                # Insert InDel
                try:
                    self.indels.append(
                        ToIndel(
                            sample=self.sample,
                            indel=indel,
                            filters=record_filters,
                        )
                    )
                except IntegrityError as e:
                    raise CommandError('ToIndel Error: {0}'.format(e))

    @transaction.atomic
    @timeit
    def delete_objects(self):
        Confidence.objects.filter(sample=self.sample).delete()
        ToSNP.objects.filter(sample=self.sample).delete()
        ToIndel.objects.filter(sample=self.sample).delete()
        Counts.objects.filter(sample=self.sample).delete()

    @transaction.atomic
    @timeit
    def insert_snps(self):
        ToSNP.objects.bulk_create(self.snps, batch_size=50000)
        return None

    @transaction.atomic
    @timeit
    def insert_indels(self):
        ToIndel.objects.bulk_create(self.indels, batch_size=50000)
        return None

    @transaction.atomic
    @timeit
    def insert_confidence(self):
        Confidence.objects.bulk_create(self.confidence, batch_size=50000)
        return None

    @transaction.atomic
    @timeit
    def insert_counts(self):
        Counts.objects.create(
            sample=self.sample,
            snp=len(self.snps),
            indel=len(self.indels),
            confidence=len(self.confidence)
        )
        return None
