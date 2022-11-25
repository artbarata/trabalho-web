from django import forms
from django.core.mail.message import EmailMessage


class ContatoForm(forms.Form):

    nome = forms.CharField(label='nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=200)
    assunto = forms.CharField(label='Assunto', max_length=120)
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)

    def send_mail(self):

        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome: {nome}\n' \
                   f'E-mail: {email}\n' \
                   f'Assunto: {assunto}\n' \
                   f'Mensagem: {mensagem}'

        mail = EmailMessage(
            subject='Solicitação de Contato',
            body=conteudo,
            from_email='EMAIL_HOST_USER cadastrado no settings.py',
            to=['e-mail do responsável pelos atendimentos da aplicação', ],
            headers={'Reply-To': email},
        )

        mail.send()

