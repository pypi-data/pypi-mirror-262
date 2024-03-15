from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.translation import gettext_lazy as _
from django.template import loader
from django.conf import settings
from djangoldp.models import Model
from datetime import date
from rest_framework import status
from djangoldp.views import NoCSRFAuthentication
import validators
import csv

from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.parsers import BaseParser

from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.views.generic.detail import DetailView
from djangoldp.permissions import ModelConfiguredPermissions

from djangoldp_energiepartagee.models import Contribution, CONTRIBUTION_CHOICES, Paymentmethod, Relatedactor
from djangoldp_energiepartagee.filters import ContributionFilterBackend
import logging

logger = logging.getLogger(__name__)

# What about a html version of the view generation from a template ?
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(html, dest=result, encoding='utf-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf; charset=utf-8')
    return None

class GeneratePdfCall(DetailView):
    model= Contribution
    template_name='pdf/contribution_call.html'

    def get(self, request, *args, **kwargs):
        # try:
        #     from djangoldp_energiepartagee.models import Contribution
        # except (get_user_model().DoesNotExist, KeyError):
        #     pass

        instance = Contribution.objects.get(id = kwargs['pk'])
        # Check that the array entries are URLs
        if instance:
            context = {
                'contribution': instance,
                'uri':request.build_absolute_uri('/media/'),
            }
            pdf = render_to_pdf(self.template_name, context)

            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf; charset=utf-8')
                filename = "Appel à cotisation.pdf"
                content = "inline; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response

        return HttpResponse("Not Found")

    def post(self, request, *args, **kwargs):
        # try:
        #     from djangoldp_energiepartagee.models import Contribution
        # except (get_user_model().DoesNotExist, KeyError):
        #     pass

        # Check that the array entries are URLs
        if validators.url(request.data.urlid):
            # Check that the corresponding Actors exists
            model, instance = Model.resolve(request.data.urlid)

            context = {
                'number': instance.contributionnumber,
                'actor': instance.actor.name,
            }
            pdf = render_to_pdf(self.template_name, context)

            if pdf:
                response = HttpResponse(pdf,content_type='application/pdf; charset=utf-8')
                filename = "Appel à cotisation.pdf"
                content = "inline; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response

        return HttpResponse("Not Found")

class GeneratePdfReceipt(DetailView):
    model= Contribution
    template_name='pdf/contribution_receipt.html'

    def get(self, request, *args, **kwargs):
        instance = Contribution.objects.get(id = kwargs['pk'])

        if instance:
            context = {
                'contribution': instance,
                'uri':request.build_absolute_uri('/media/'),
            }
            pdf = render_to_pdf(self.template_name, context)

            if pdf:
                response = HttpResponse(pdf,content_type='application/pdf; charset=utf-8')
                filename = "Recu de cotisation.pdf"
                content = "inline; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response

        return HttpResponse("Not Found")

    def post(self, request, *args, **kwargs):
        # try:
        #     from djangoldp_energiepartagee.models import Contribution
        # except (get_user_model().DoesNotExist, KeyError):
        #     pass

        # Check that the array entries are URLs
        if validators.url(request.data.urlid):
            # Check that the corresponding Actors exists
            model, instance = Model.resolve(request.data.urlid)

            context = {
                'number': instance.contributionnumber,
                'actor': instance.actor.name,
            }
            pdf = render_to_pdf(self.template_name, context)

            if pdf:
                response = HttpResponse(pdf,content_type='application/pdf; charset=utf-8')
                filename = "Recu de cotisation.pdf"
                content = "inline; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response

        return HttpResponse("Not Found")

class ContributionsView(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def dispatch(self, request, *args, **kwargs):
        '''overriden dispatch method to append some custom headers'''
        response = super(ContributionsView, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get('origin')
        response["Access-Control-Allow-Methods"] = "POST"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response['User'] = request.user.webid()
            except AttributeError:
                pass
        return response

   
    def contributionMail(self, request, specificdata):
        # Check that we get an array
        wiretransfer = Paymentmethod.objects.filter(name="Virement")[0]
        if (request.method == 'POST' and request.data and isinstance(request.data, list)):
            for urlid in request.data:
              # Check that the array entries are URLs
              if validators.url(urlid):
                # Check that the corresponding Actors exists
                model, instance = Model.resolve(urlid)
                if instance and instance.actor:
                    if instance.contributionstatus in specificdata['status_before']:
                        # Modify the contribution status
                        if instance.amount == 0.00:
                            # For given contributions (amount at 0), specific beavior => go directly to the final status
                            instance.contributionstatus = specificdata['status_after_given']
                            instance.paymentdate = date.today()
                            instance.receivedby = instance.paymentto
                            instance.paymentmethod = wiretransfer
                        else:
                            instance.contributionstatus = specificdata['status_after']
                        instance.callcontact = request.user
                        instance.calldate = date.today()
                        instance.save()

                    if specificdata['status_before'] == 'all':
                        instance.updatereminderdate = date.today()
                        instance.save()
                        for member in instance.actor.members.all():
                            if member.role:
                                text_message = loader.render_to_string(
                                    specificdata['email_text'],
                                    {
                                        'sender' : request.user,
                                        'user': member.user,
                                        'actor': instance.actor,
                                        'contribution': instance,
                                        'uri':request.build_absolute_uri('/media/'),
                                        'front_url':settings.INSTANCE_DEFAULT_CLIENT,
                                        'back_url':settings.BASE_URL,
                                    }
                                )
                                html_message = loader.render_to_string(
                                    specificdata['email_html'],
                                    {
                                        'sender' : request.user,
                                        'user':member.user,
                                        'actor': instance.actor,
                                        'contribution': instance,
                                        'uri':request.build_absolute_uri('/media/'),
                                        'front_url':settings.INSTANCE_DEFAULT_CLIENT,
                                        'back_url':settings.BASE_URL,
                                    }
                                )
                                send_mail(
                                    _(specificdata['email_title'] + instance.actor.longname),
                                    text_message,
                                    settings.DEFAULT_FROM_EMAIL or "association@energie-partagee.fr",
                                    [member.user.email],
                                    fail_silently=False,
                                    html_message=html_message
                                )
                        text_message = loader.render_to_string(
                            specificdata['email_text'],
                            {
                                'sender' : request.user,
                                'user': "",
                                'actor': instance.actor,
                                'contribution': instance,
                                'uri':request.build_absolute_uri('/media/'),
                                'front_url':settings.INSTANCE_DEFAULT_CLIENT,
                                'back_url':settings.BASE_URL,
                            }
                        )
                        html_message = loader.render_to_string(
                            specificdata['email_html'],
                            {
                                'sender' : request.user,
                                'user': "",
                                'actor': instance.actor,
                                'contribution': instance,
                                'uri':request.build_absolute_uri('/media/'),
                                'front_url':settings.INSTANCE_DEFAULT_CLIENT,
                                'back_url':settings.BASE_URL,
                            }
                        )
                        msg = EmailMultiAlternatives(
                                _(specificdata['email_title'] + instance.actor.longname),
                                text_message,
                                settings.DEFAULT_FROM_EMAIL or "association@energie-partagee.fr",
                                [instance.actor.mail], 
                                ["association@energie-partagee.org"]
                            )
                        msg.attach_alternative(html_message, "text/html")
                        # Force raising an error if any
                        msg.send(
                            fail_silently=False
                        )
                    else:
                        text_message = loader.render_to_string(
                            specificdata['email_text'],
                            {
                                'sender' : request.user,
                                'user': instance.actor.managementcontact,
                                'actor': instance.actor,
                                'contribution': instance,
                                'uri':request.build_absolute_uri('/media/'),
                                'front_url':settings.INSTANCE_DEFAULT_CLIENT,
                                'back_url':settings.BASE_URL,
                            }
                        )
                        html_message = loader.render_to_string(
                            specificdata['email_html'],
                            {
                                'sender' : request.user,
                                'user':instance.actor.managementcontact,
                                'actor': instance.actor,
                                'contribution': instance,
                                'uri':request.build_absolute_uri('/media/'),
                                'front_url':settings.INSTANCE_DEFAULT_CLIENT,
                                'back_url':settings.BASE_URL,
                            }
                        )
                        if not instance.amount == 0.00:
                            send_mail(
                                _(specificdata['email_title']),
                                text_message,
                                settings.DEFAULT_FROM_EMAIL or "contact@energie-partagee.fr",
                                [instance.actor.managementcontact.email],
                                fail_silently=False,
                                html_message=html_message
                            )

            # Questions:
            #   public link to the HTML document ?
            #   Do we want to have it private ?
            response = Response({"content": "This is a success"}, status=status.HTTP_200_OK)
            
            return response

        return Response(status=204)
 

class ContributionsCallView(ContributionsView):
    def post(self, request):
        # from djangoldp_energiepartagee.models import CONTRIBUTION_CHOICES

        specificdata = {
            'status_before' : [CONTRIBUTION_CHOICES[0][0]],
            'status_after' : CONTRIBUTION_CHOICES[1][0],
            'status_after_given' : CONTRIBUTION_CHOICES[4][0],
            'email_text' : 'emails/txt/subscription_call.txt',
            'email_html' : 'emails/html/subscription_call.html',
            'email_title' : 'Energie Partagée - Appel à cotisation'
        }
        return self.contributionMail(request, specificdata)


class ContributionsReminderView(ContributionsView):
    def post(self, request):
        # from djangoldp_energiepartagee.models import CONTRIBUTION_CHOICES

        specificdata = {
            'status_before' : [CONTRIBUTION_CHOICES[1][0], CONTRIBUTION_CHOICES[2][0]],
            'status_after' : CONTRIBUTION_CHOICES[2][0],
            'status_after_given' : CONTRIBUTION_CHOICES[4][0],
            'email_text' : 'emails/txt/subscription_reminder.txt',
            'email_html' : 'emails/html/subscription_reminder.html',
            'email_title' : 'Energie Partagée - Relance d\'appel à cotisation'
        }
        return self.contributionMail(request, specificdata)     
    
class ContributionsActorUpdateView(ContributionsView):
    def post(self, request):
        specificdata = {
            'status_before' : 'all',
            'email_text' : 'emails/txt/actor_update.txt',
            'email_html' : 'emails/html/actor_update.html',
            'email_title' : '[Votre adhésion] [action requise] Mettez à jour les données de votre fiche acteur'
        }
        return self.contributionMail(request, specificdata)


class ContributionsVentilationView(ContributionsView):
    def post(self, request):
        # from djangoldp_energiepartagee.models import CONTRIBUTION_CHOICES

        if request.data:
            # Check parameters
            data_expected = [
                'ventilationpercent', 
                'ventilationto',
                'ventilationdate',
                'factureventilation', 
                'contributions'
            ]

            if not all(parameter in request.data.keys() for parameter in data_expected):
                missing_params = [parameter for parameter in data_expected if parameter not in request.data.keys()]
                return Response('Invalid parameters: {} missing'.format(', '.join(missing_params)), status=400)
           
            # Check regional network
            ventilationto_urlid = request.data['ventilationto']['@id']
            if validators.url(ventilationto_urlid):
                model, instance = Model.resolve(ventilationto_urlid)
                if instance:
                    ventilationto = instance
                else:
                    return Response('Regional network does not exist in DB', status=400)

            # Check contributions 
            contribution_list = []
            for contrib_urlid in request.data['contributions']:
                if validators.url(contrib_urlid):
                    model, instance = Model.resolve(contrib_urlid)
                    if instance:
                        contribution_list.append(instance)
                    else:
                        return Response('Contribution {} does not exist in DB'.format(contrib_urlid), status=400)
 
            # Ventilate
            for contrib in contribution_list:
                contrib.ventilationpercent = request.data['ventilationpercent']
                contrib.ventilationto = ventilationto
                contrib.ventilationdate = request.data['ventilationdate']
                contrib.factureventilation = request.data['factureventilation']
                contrib.contributionstatus = CONTRIBUTION_CHOICES[4][0]
                contrib.save()

            # Send response
            response = Response({"content": "This is a success"}, status=status.HTTP_200_OK)
            
            return response

        return Response(status=204)    

class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()

#export csv all
class ExportContributionsAll(APIView):
    authentication_classes = [NoCSRFAuthentication,]
    permission_classes = [ModelConfiguredPermissions,]
    model = Contribution
    parser_classes = (PlainTextParser,)

    def dispatch(self, request, *args, **kwargs):
        response = super(ExportContributionsAll, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get('origin')
        response["Access-Control-Allow-Methods"] = "POST, GET"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response['User'] = request.user.webid()
            except AttributeError:
                pass
        return response

    def post(self, request):
        delimiter_type=';'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export_actors.csv"'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response, delimiter=delimiter_type)

        if (request.data):
            fields = [
                "Nom court de l'acteur", "Nom long de l'acteur", "Adresse", "Complément d'adresse", "Code Postal", "Ville", "Région", "Réseau Régional", "Collège EPA", "Collège RR", "nom représentant légal", "prénom représentant légal", "mail représentant légal", "téléphone représentant légal", "nom contact de gestion", "prénom contact de gestion", "mail contact de gestion", "téléphone contact de gestion", "Colis accueil envoyé","Inscrit sur espace Adh","Inscrit sur liste Adh","Inscrit sur liste régional", "e-mail espace adhérent", "Catégorie de cotisant", "Nombre d'habitants", "Nombre d'employés", "Chiffre d'affaires", "SIREN ou RNA", "Année de cotisation", "Montant à payer", "Référence", "Date de paiement", "Paiement reçu par", "Moyen de paiement","Etat de la cotisation", "Numéro de reçu", "Pourcentage de ventilation", "Bénéficiaire de la ventilation", "Date de paiement de la part ventilée", "Numéro de facture de la ventilation", "Nom “Animateur régional contact”", "Prénom “Animateur régional contact”","Type d'acteur", "Structure juridique", "Adhérent sur l'année en cours", "Signataire de la charte EP", "Visible sur la carte","Adhérent depuis", "Date de Mise à jour de l'acteur", "Date de demande de mise à jour"
            ]
            writer.writerow(fields)

            filter = ContributionFilterBackend()
            contrib_queryset = filter.filter_queryset(self.request, Contribution.objects.all(), self).filter(year=request.data)

            for instance in contrib_queryset:
                if instance and instance.actor:

                    if instance.actor.shortname:
                        actor_shortname=instance.actor.shortname
                    else:
                        actor_shortname=""

                    if instance.actor.longname:
                        actor_longname=instance.actor.longname
                    else:
                        actor_longname=""

                    if instance.actor.address:
                        actor_address=instance.actor.address
                    else:
                        actor_address=""

                    if instance.actor.complementaddress:
                        actor_complementaddress=instance.actor.complementaddress
                    else:
                        actor_complementaddress=""

                    if instance.actor.postcode:
                        actor_postcode=instance.actor.postcode
                    else:
                        actor_postcode=""

                    if instance.actor.city:
                        actor_city=instance.actor.city
                    else:
                        actor_city=""

                    if instance.actor.region.name:
                        actor_region=instance.actor.region.name
                    else:
                        actor_region=""

                    if instance.actor.regionalnetwork and instance.actor.regionalnetwork.name:
                        actor_regionalnetwork=instance.actor.regionalnetwork.name
                    else:
                        actor_regionalnetwork=""

                    if instance.actor.collegeepa:
                        collegeepa=instance.actor.collegeepa.name
                    else:
                        collegeepa=""

                    if instance.actor.college:
                        college=instance.actor.college.name
                    else:
                        college=""

                    legalrepresentant_last_name=""
                    legalrepresentant_first_name=""
                    legalrepresentant_email=""
                    legalrepresentant_phone=""
                    if instance.actor.legalrepresentant:
                        if instance.actor.legalrepresentant.last_name :
                            legalrepresentant_last_name=instance.actor.legalrepresentant.last_name

                        if instance.actor.legalrepresentant.first_name :
                            legalrepresentant_first_name=instance.actor.legalrepresentant.first_name

                        if instance.actor.legalrepresentant.email :
                            legalrepresentant_email=instance.actor.legalrepresentant.email

                        if instance.actor.legalrepresentant.profile.phone :
                            legalrepresentant_phone=instance.actor.legalrepresentant.profile.phone

                    managementcontact_last_name=""
                    managementcontact_first_name=""
                    managementcontact_email=""
                    managementcontact_phone=""
                    if instance.actor.managementcontact:
                        if instance.actor.managementcontact.last_name :
                            managementcontact_last_name=instance.actor.managementcontact.last_name

                        if instance.actor.managementcontact.first_name :
                            managementcontact_first_name=instance.actor.managementcontact.first_name

                        if instance.actor.managementcontact.email :
                            managementcontact_email=instance.actor.managementcontact.email

                        if instance.actor.managementcontact.profile.phone :
                            managementcontact_phone=instance.actor.managementcontact.profile.phone

                    if instance.actor.college:
                        college=instance.actor.college.name
                    else:
                        college=""

                    packagestep=""
                    adhspacestep=""
                    adhliststep=""
                    regionalliststep=""
                    if instance.actor.integrationstep:
                        if instance.actor.integrationstep.packagestep == True:
                            packagestep="Non"
                        else:
                            packagestep="Oui"

                        if instance.actor.integrationstep.adhspacestep == True:
                            adhspacestep="Non"
                        else:
                            adhspacestep="Oui"

                        if instance.actor.integrationstep.adhliststep == True:
                            adhliststep="Non"
                        else:
                            adhliststep="Oui"

                        if instance.actor.integrationstep.regionalliststep == True:
                            regionalliststep="Non"
                        else:
                            regionalliststep="Oui"

                    if instance.contributionnumber:
                        contributionnumber = instance.contributionnumber
                    else:
                        contributionnumber=""

                    if instance.paymentdate:
                        paymentdate = instance.paymentdate.strftime("%d-%m-%Y")
                    else:
                        paymentdate=""

                    if instance.receivedby:
                        receivedby=instance.receivedby.name
                    else:
                        receivedby=""

                    if instance.paymentmethod:
                        paymentmethod=instance.paymentmethod
                    else:
                        paymentmethod=""

                    if instance.actor.category == "collectivite" :
                        category="Collectivités"
                    elif instance.actor.category == "porteur_dev" :
                        category="Porteurs de projet en développement"
                    elif instance.actor.category == "porteur_exploit" :
                        category="Porteurs de projet en exploitation"
                    else:
                        category="Partenaires"

                    if instance.numberpeople:
                        numberpeople=instance.numberpeople
                    else:
                        numberpeople=""

                    if instance.numberemployees:
                        numberemployees=instance.numberemployees
                    else:
                        numberemployees=""

                    if instance.turnover:
                        turnover=instance.turnover
                    else:
                        turnover=""

                    if instance.actor.siren:
                        siren=instance.actor.siren
                    else:
                        siren=""

                    if instance.year:
                        year=instance.year
                    else:
                        year=""

                    if instance.amount:
                        amount=instance.amount
                    else:
                        amount=""

                    if instance.contributionstatus == "appel_a_envoye" :
                        status="Appel à envoyer"
                    elif instance.contributionstatus == "appel_ok" :
                        status="Appel envoyé"
                    elif instance.contributionstatus == "relance" :
                        status="Relancé"
                    elif instance.contributionstatus == "a_ventiler" :
                        status="A ventiler"
                    else:
                        status="Validé"

                    if instance.paymentdate and instance.receivedby:
                        receiptnumber = str(instance.receivedby.code) + "-" + str(instance.year) + "-" + str(instance.contributionnumber)
                    else:
                        receiptnumber=""

                    if instance.ventilationto: 
                        ventilationto=instance.ventilationto.name
                    else:
                        ventilationto=""

                    if instance.ventilationdate:
                        ventilationdate = instance.ventilationdate.strftime("%d-%m-%Y")
                    else:
                        ventilationdate=""

                    if instance.callcontact:
                        callcontactname=instance.callcontact.last_name
                        callcontactfirstname=instance.callcontact.first_name
                    else:
                        callcontactname=""
                        callcontactfirstname=""

                    if instance.actor.legalstructure:
                        legalstructure=instance.actor.legalstructure.name
                    else:
                        legalstructure=""

                    if instance.actor.adhmail:
                        adhmail=instance.actor.adhmail
                    else:
                        adhmail=""

                    if instance.actor.actortype == "soc_citoy" :
                        actortype="Sociétés Citoyennes"
                    elif instance.actor.actortype == "collectivite" :
                        actortype="Collectivités"
                    elif instance.actor.actortype == "structure" :
                        actortype="Structures d'Accompagnement"
                    else:
                        actortype="Partenaires"

                    if instance.actor.renewed == True:
                        renewed="Oui"
                    elif instance.actor.renewed == False: 
                        renewed="Non"
                    else:
                        renewed="Inconnu"

                    if instance.actor.signataire == True:
                        signataire="Oui"
                    elif instance.actor.signataire == False: 
                        signataire="Non"
                    else:
                        signataire="Inconnu"

                    if instance.actor.visible == True:
                        visible="Oui"
                    else:
                        visible="Non"

                    if instance.actor.adhesiondate:
                        adhesiondate=instance.actor.adhesiondate
                    else:
                        adhesiondate=""

                    if instance.actor.updatedate:
                        updatedate=instance.actor.updatedate.strftime("%d-%m-%Y")
                    else:
                        updatedate=""

                    if instance.updatereminderdate:
                        updatereminderdate=instance.updatereminderdate.strftime("%d-%m-%Y")
                    else:
                        updatereminderdate=""

                writer.writerow([
                    actor_shortname, actor_longname, actor_address, actor_complementaddress, actor_postcode, actor_city, actor_region, actor_regionalnetwork, collegeepa, college, legalrepresentant_last_name, legalrepresentant_first_name, legalrepresentant_email, legalrepresentant_phone, managementcontact_last_name, managementcontact_first_name, managementcontact_email, managementcontact_phone, packagestep, adhspacestep, adhliststep, regionalliststep, adhmail, category, numberpeople, numberemployees, turnover, siren, year, amount, contributionnumber, paymentdate, receivedby, paymentmethod, status, receiptnumber, instance.ventilationpercent, ventilationto, ventilationdate, instance.factureventilation, callcontactname, callcontactfirstname, actortype, legalstructure, renewed, signataire, visible, adhesiondate, updatedate, updatereminderdate
                ]) 


        if response:
            return response
        
        return HttpResponse("Not Found")


#export csv - Old button (export selected lines)
class ExportContributions(APIView): 
    authentication_classes = (NoCSRFAuthentication,)

    def dispatch(self, request, *args, **kwargs):
        response = super(ExportContributions, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get('origin')
        response["Access-Control-Allow-Methods"] = "POST, GET"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"
        
        if request.user.is_authenticated:
            try:
                response['User'] = request.user.webid()
            except AttributeError:
                pass
        return response
        
    def post(self, request):
        delimiter_type=';'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export_actors.csv"'

        writer = csv.writer(response, delimiter=delimiter_type)
        for urlid in request.data:
              # Check that the array entries are URLs
              if validators.url(urlid):
                    model, instance = Model.resolve(urlid)
                    
        
        if (request.method == 'POST' and request.data and isinstance(request.data, list)):
            fields = [
                "Nom court de l'acteur", "Nom long de l'acteur", "Adresse", "Complément d'adresse", "Code Postal", "Ville", "Région", "Réseau Régional", "Collège EPA", "Collège RR", "nom représentant légal", "prénom représentant légal", "mail représentant légal", "téléphone représentant légal", "nom contact de gestion", "prénom contact de gestion", "mail contact de gestion", "téléphone contact de gestion", "Colis accueil envoyé","Inscrit sur espace Adh","Inscrit sur liste Adh","Inscrit sur liste régional", "e-mail espace adhérent", "Catégorie de cotisant", "Nombre d'habitants", "Nombre d'employés", "Chiffre d'affaires", "SIREN ou RNA", "Année de cotisation", "Montant à payer", "Date de paiement", "Paiement reçu par", "Moyen de paiement","Etat de la cotisation", "Numéro de reçu", "Pourcentage de ventilation", "Bénéficiaire de la ventilation", "Date de paiement de la part ventilée", "Numéro de facture de la ventilation", "Nom “Animateur régional contact”", "Prénom “Animateur régional contact”","Type d'acteur", "Structure juridique", "Adhérent sur l’année en cours", "Signataire de la charte EP", "Visible sur la carte","Adhérent depuis"
            ]
            writer.writerow(fields)

            for urlid in request.data:
              # Check that the array entries are URLs
              if validators.url(urlid):
                    model, instance = Model.resolve(urlid)
                    if instance and instance.actor:

                        if instance.actor.shortname:
                           actor_shortname=instance.actor.shortname
                        else:
                            actor_shortname=""

                        if instance.actor.longname:
                           actor_longname=instance.actor.longname
                        else:
                            actor_longname=""

                        if instance.actor.address:
                           actor_address=instance.actor.address
                        else:
                            actor_address=""

                        if instance.actor.complementaddress:
                           actor_complementaddress=instance.actor.complementaddress
                        else:
                            actor_complementaddress=""

                        if instance.actor.postcode:
                           actor_postcode=instance.actor.postcode
                        else:
                            actor_postcode=""

                        if instance.actor.city:
                           actor_city=instance.actor.city
                        else:
                            actor_city=""

                        if instance.actor.region.name:
                           actor_region=instance.actor.region.name
                        else:
                            actor_region=""

                        if instance.actor.regionalnetwork.name:
                           actor_regionalnetwork=instance.actor.regionalnetwork.name
                        else:
                            actor_regionalnetwork=""

                        if instance.actor.collegeepa:
                           collegeepa=instance.actor.collegeepa.name
                        else:
                            collegeepa=""

                        if instance.actor.college:
                           college=instance.actor.college.name
                        else:
                            college=""

                        legalrepresentant_last_name=""
                        legalrepresentant_first_name=""
                        legalrepresentant_email=""
                        legalrepresentant_phone=""
                        if instance.actor.legalrepresentant:
                            if instance.actor.legalrepresentant.last_name :
                                legalrepresentant_last_name=instance.actor.legalrepresentant.last_name

                            if instance.actor.legalrepresentant.first_name :
                                legalrepresentant_first_name=instance.actor.legalrepresentant.first_name

                            if instance.actor.legalrepresentant.email :
                                legalrepresentant_email=instance.actor.legalrepresentant.email

                            if instance.actor.legalrepresentant.profile.phone :
                                legalrepresentant_phone=instance.actor.legalrepresentant.profile.phone

                        managementcontact_last_name=""
                        managementcontact_first_name=""
                        managementcontact_email=""
                        managementcontact_phone=""
                        if instance.actor.managementcontact:
                            if instance.actor.managementcontact.last_name :
                                managementcontact_last_name=instance.actor.managementcontact.last_name

                            if instance.actor.managementcontact.first_name :
                                managementcontact_first_name=instance.actor.managementcontact.first_name

                            if instance.actor.managementcontact.email :
                                managementcontact_email=instance.actor.managementcontact.email

                            if instance.actor.managementcontact.profile.phone :
                                managementcontact_phone=instance.actor.managementcontact.profile.phone

                        if instance.actor.college:
                           college=instance.actor.college.name
                        else:
                            college=""

                        packagestep=""
                        adhspacestep=""
                        adhliststep=""
                        regionalliststep=""
                        if instance.actor.integrationstep:
                            if instance.actor.integrationstep.packagestep == True:
                                packagestep="Non"
                            else:
                                packagestep="Oui"

                            if instance.actor.integrationstep.adhspacestep == True:
                                adhspacestep="Non"
                            else:
                                adhspacestep="Oui"

                            if instance.actor.integrationstep.adhliststep == True:
                                adhliststep="Non"
                            else:
                                adhliststep="Oui"

                            if instance.actor.integrationstep.regionalliststep == True:
                                regionalliststep="Non"
                            else:
                                regionalliststep="Oui"

                        if instance.paymentdate:
                            paymentdate = instance.paymentdate.strftime("%d-%m-%Y")
                        else:
                            paymentdate=""

                        if instance.receivedby:
                           receivedby=instance.receivedby.name
                        else:
                            receivedby=""

                        if instance.paymentmethod:
                           paymentmethod=instance.paymentmethod
                        else:
                            paymentmethod=""

                        if instance.actor.category == "collectivite" :
                           category="Collectivités"
                        elif instance.actor.category == "porteur_dev" :
                           category="Porteurs de projet en développement"
                        elif instance.actor.category == "porteur_exploit" :
                           category="Porteurs de projet en exploitation"
                        else:
                            category="Partenaires"

                        if instance.numberpeople:
                           numberpeople=instance.numberpeople
                        else:
                            numberpeople=""

                        if instance.numberemployees:
                           numberemployees=instance.numberemployees
                        else:
                            numberemployees=""

                        if instance.turnover:
                           turnover=instance.turnover
                        else:
                            turnover=""

                        if instance.actor.siren:
                           siren=instance.actor.siren
                        else:
                            siren=""

                        if instance.year:
                           year=instance.year
                        else:
                            year=""

                        if instance.amount:
                           amount=instance.amount
                        else:
                            amount=""

                        if instance.contributionstatus == "appel_a_envoye" :
                           status="Appel à envoyer"
                        elif instance.contributionstatus == "appel_ok" :
                           status="Appel envoyé"
                        elif instance.contributionstatus == "relance" :
                           status="Relancé"
                        elif instance.contributionstatus == "a_ventiler" :
                           status="A ventiler"
                        else:
                            status="Validé"

                        if instance.paymentdate and instance.receivedby:
                            receiptnumber = str(instance.receivedby.code) + "-" + str(instance.year) + "-" + str(instance.contributionnumber)
                        else:
                            receiptnumber=""

                        if instance.ventilationto: 
                            ventilationto=instance.ventilationto.name
                        else:
                            ventilationto=""

                        if instance.ventilationdate:
                            ventilationdate = instance.ventilationdate.strftime("%d-%m-%Y")
                        else:
                            ventilationdate=""

                        if instance.callcontact:
                            callcontactname=instance.callcontact.last_name
                            callcontactfirstname=instance.callcontact.first_name
                        else:
                            callcontactname=""
                            callcontactfirstname=""

                        if instance.actor.legalstructure:
                            legalstructure=instance.actor.legalstructure.name
                        else:
                            legalstructure=""

                        if instance.actor.adhmail:
                            adhmail=instance.actor.adhmail
                        else:
                            adhmail=""

                        if instance.actor.actortype == "soc_citoy" :
                           actortype="Sociétés Citoyennes"
                        elif instance.actor.actortype == "collectivite" :
                           actortype="Collectivités"
                        elif instance.actor.actortype == "structure" :
                           actortype="Structures d’Accompagnement"
                        else:
                            actortype="Partenaires"

                        if instance.actor.renewed == True:
                            renewed="Oui"
                        elif instance.actor.renewed == False: 
                            renewed="Non"
                        else:
                            renewed="Inconnu"

                        if instance.actor.signataire == True:
                            signataire="Oui"
                        elif instance.actor.signataire == False: 
                            signataire="Non"
                        else:
                            signataire="Inconnu"

                        if instance.actor.visible == True:
                            visible="Oui"
                        else:
                            visible="Non"

                        if instance.actor.adhesiondate:
                            adhesiondate=instance.actor.adhesiondate
                        else:
                            adhesiondate=""

                        writer.writerow([
                            actor_shortname, actor_longname, actor_address, actor_complementaddress, actor_postcode, actor_city, actor_region, actor_regionalnetwork, collegeepa, college, legalrepresentant_last_name, legalrepresentant_first_name, legalrepresentant_email, legalrepresentant_phone, managementcontact_last_name, managementcontact_first_name, managementcontact_email, managementcontact_phone, packagestep, adhspacestep, adhliststep, regionalliststep, adhmail, category, numberpeople, numberemployees, turnover, siren, year, amount, paymentdate, receivedby, paymentmethod, status, receiptnumber, instance.ventilationpercent, ventilationto, ventilationdate, instance.factureventilation, callcontactname, callcontactfirstname, actortype, legalstructure, renewed, signataire, visible, adhesiondate
                        ]) 

        if response:
            return response
        
        return HttpResponse("Not Found")

class WaitingMembersActionView(APIView):
    authentication_classes = (NoCSRFAuthentication,)
    
    def dispatch(self, request, *args, **kwargs):
        response = super(WaitingMembersActionView, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get('origin')
        response["Access-Control-Allow-Methods"] = "POST, GET"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response['User'] = request.user.webid()
            except AttributeError:
                pass
        return response

    def post(self, request, pk):
        # from djangoldp_energiepartagee.models import CONTRIBUTION_CHOICES

        if request.data:
            urlid = settings.BASE_URL + "/relatedactors/" + str(pk)
            if validators.url(urlid):
                model, instance = Model.resolve(urlid)
                if instance:
                    print("instance : ", instance, instance.actor.managementcontact.email)
                    obj = Relatedactor.objects.get(pk=pk)
                    if request.data == "reminder":
                        specificdata = {
                            'email_text' : 'emails/txt/waiting_reminder.txt',
                            'email_html' : 'emails/html/waiting_reminder.html',
                            'email_title' : "Energie Partagée - Vous avez une demande en attente pour l'acteur ",
                            'status' : "",
                            'email' : instance.actor.managementcontact.email,
                        }
                        obj.reminderdate = date.today()
                        obj.save()
                    else:
                        if request.data == "refuse":
                            specificdata = {
                                'email_text' : 'emails/txt/join_actor_denied.txt',
                                'email_html' : 'emails/html/join_actor_denied.html',
                                'email_title' : "Energie Partagée - Votre demande de rejoindre l'acteur ",
                                'status' : " a été refusée",
                                'email' : instance.user.email,
                            }
                        else:
                            specificdata = {
                                'email_text' : 'emails/txt/join_actor_validated.txt',
                                'email_html' : 'emails/html/join_actor_validated.html',
                                'email_title' : "Energie Partagée - Votre demande de rejoindre l'acteur ",
                                'status' : " a été acceptée",
                                'email' : instance.user.email,
                            }
                        obj.role=request.data
                        obj.save()
                text_message = loader.render_to_string(
                    specificdata['email_text'],
                    {
                        'sender' : request.user,
                        'user': instance.user,
                        'role': request.data,
                        'actor': instance.actor,
                        'uri':request.build_absolute_uri('/media/'),
                        'front_url':settings.INSTANCE_DEFAULT_CLIENT,
                        'back_url':settings.BASE_URL,
                    }
                )
                html_message = loader.render_to_string(
                    specificdata['email_html'],
                    {
                        'sender' : request.user,
                        'user':instance.user,
                        'role': request.data,
                        'actor': instance.actor,
                        'uri':request.build_absolute_uri('/media/'),
                        'front_url':settings.INSTANCE_DEFAULT_CLIENT,
                        'back_url':settings.BASE_URL,
                    }
                )
                send_mail(
                    _(specificdata['email_title'] + instance.actor.longname + specificdata['status']),
                    text_message,
                    settings.EMAIL_HOST_USER or "contact@energie-partagee.fr",
                    [specificdata['email']],
                    fail_silently=False,
                    html_message=html_message
                )
            response = Response({"content": "This is a success"},
            status=status.HTTP_200_OK)
            
            return response

        return Response(status=204)
