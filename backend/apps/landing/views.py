from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

class LandingPageView(TemplateView):
    """
    Landing page principal do JuridicFlow
    """
    template_name = 'landing/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['whatsapp_number'] = '5521999999999'  # Seu número do WhatsApp
        context['whatsapp_message'] = 'Olá! Gostaria de saber mais sobre o JuridicFlow'
        return context


@require_http_methods(["POST"])
def contact_form_submit(request):
    """
    Processa o formulário de contato
    """
    try:
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        
        # Validação básica
        if not all([name, email, message]):
            return JsonResponse({
                'success': False,
                'message': 'Por favor, preencha todos os campos obrigatórios.'
            }, status=400)
        
        # Enviar email (configure seu SMTP no settings.py)
        try:
            email_body = f"""
            Nova mensagem de contato do site JuridicFlow
            
            Nome: {name}
            Email: {email}
            Telefone: {phone if phone else 'Não informado'}
            
            Mensagem:
            {message}
            """
            
            send_mail(
                subject=f'[JuridicFlow] Novo contato: {name}',
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Mensagem enviada com sucesso! Entraremos em contato em breve.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Erro ao enviar mensagem. Tente novamente ou entre em contato pelo WhatsApp.'
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dados inválidos.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Erro interno. Tente novamente.'
        }, status=500)