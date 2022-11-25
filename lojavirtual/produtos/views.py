from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .models import Produto, Categoria
from carrinho.forms import FormAdicionarProdutoAoCarrinho


def listar_produtos(request, slug_categoria=None):
    categoria = None
    lista_categorias = Categoria.objects.all()
    lista_produtos = Produto.objects.filter(ativo=True)
    if slug_categoria:
        categoria = get_object_or_404(Categoria, slug=slug_categoria)
        lista_produtos = Produto.objects.filter(categoria=categoria)
    contexto = {
        'categoria': categoria,
        'lista_categorias': lista_categorias,
        'lista_produtos': lista_produtos,
    }
    return render(request, 'produtos/produtos.html', contexto)


def detalhar_produto(request, id_produto, slug_produto):
    produto = get_object_or_404(Produto,
                                id=id_produto,
                                slug=slug_produto,
                                ativo=True)
    form_adicionar_produto_ao_carrinho = FormAdicionarProdutoAoCarrinho()
    contexto = {
        'produto': produto,
        'form_produto_carrinho': form_adicionar_produto_ao_carrinho
    }
    return render(request, 'produtos/detalhes.html', contexto)


@csrf_exempt
def search_employees(request):
    if request.is_ajax():
        search_term = request.POST.get('c')

        # Searching employees using Django ORM - the best way
        employees = Produto.objects.filter(first_name__icontains=search_term)

        # # Searching employees using raw() - the wrong way
        # query = "SELECT * FROM app_employee WHERE first_name ILIKE '%s';" % search_term
        # employees = Employee.objects.raw(query)

        # # Searching employees using raw() - the correct way
        # employees = Employee.objects.raw('SELECT * FROM app_employee WHERE first_name ILIKE %s;',[search_term])

        # # Searching employees using extra() - the wrong way
        # employees = Employee.objects.extra(where=["first_name ILIKE '%s'" % search_term])

        # # Searching employees using extra() - the correct way
        # employees = Employee.objects.extra(where=['first_name ILIKE %s'], params=[search_term])

        html = render_to_string('app/search_employees.html',
                                {'employees': employees})

        return HttpResponse(html)
