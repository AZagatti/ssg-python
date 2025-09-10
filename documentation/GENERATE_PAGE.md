# Funcionalidade de Geração de Páginas

## 📄 Implementação Concluída

### ✨ **Funcionalidades Implementadas**

1. **Função `extract_title(markdown)`**:
   - Extrai o cabeçalho h1 do conteúdo markdown
   - Remove `#` e espaços em branco
   - Lança exceção se não encontrar h1
   - **Exemplo**: `extract_title("# Hello")` → `"Hello"`

2. **Função `generate_page(from_path, template_path, dest_path)`**:
   - Lê arquivo markdown e template HTML
   - Converte markdown para HTML usando `markdown_to_html_node`
   - Extrai título usando `extract_title`
   - Substitui placeholders `{{ Title }}` e `{{ Content }}` no template
   - Cria diretórios necessários automaticamente
   - Salva HTML final no destino

3. **Sistema Integrado**:
   - **main.py** atualizado para gerar `public/index.html`
   - **main.sh** atualizado para iniciar servidor web na porta 8888
   - **Pipeline completo**: gerar site → servir via HTTP

### 🔧 **Estrutura de Arquivos**

```
project/
├── content/
│   └── index.md           # Conteúdo markdown principal
├── template.html          # Template HTML com placeholders
├── static/
│   ├── index.css          # Estilos CSS
│   └── images/
│       └── tolkien.png    # Imagens estáticas
├── public/                # ← Gerado automaticamente
│   ├── index.html         # Página HTML final
│   ├── index.css          # CSS copiado
│   └── images/
│       └── tolkien.png    # Imagens copiadas
└── src/
    ├── extract_title.py   # Função para extrair títulos
    ├── generate_page.py   # Função para gerar páginas
    └── main.py           # Script principal
```

### 🧪 **Testes Implementados**

#### **Testes para `extract_title`** (11 testes):
- ✅ Extração de título simples
- ✅ Título com espaços em branco
- ✅ Título em conteúdo com múltiplas seções
- ✅ Título em linha posterior
- ✅ Título com indentação
- ✅ Exceção quando não há h1
- ✅ Exceção para h1 vazio
- ✅ Exceção para apenas hashtag
- ✅ Ignorar h2/h3 quando não há h1
- ✅ Primeiro h1 ganha precedência
- ✅ Conteúdo real do Tolkien

#### **Testes para `generate_page`** (3 testes):
- ✅ Geração básica de página
- ✅ Criação automática de diretórios
- ✅ Conteúdo real do Tolkien

### 📋 **Template HTML**

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <article>{{ Content }}</article>
  </body>
</html>
```

### 📝 **Conteúdo Markdown**

```markdown
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts
- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien
- You can spend years studying the legendarium...
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)
1. Gandalf
2. Bilbo
3. Sam
...

Here's what `elflang` looks like:
```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```
```

### 🚀 **Execução e Resultado**

```bash
# Gerar site e iniciar servidor
./main.sh

# Output:
# Deleting public directory...
# Copying static files to public directory...
# * .../static/images -> .../public/images
# * .../static/images/tolkien.png -> .../public/images/tolkien.png
# * .../static/index.css -> .../public/index.css
# Generating page from .../content/index.md to .../public/index.html using .../template.html
# Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
```

### ✅ **Verificação de Conteúdo**

A página gerada contém todos os elementos esperados:
- ✅ `<h1>Tolkien Fan Club</h1>`
- ✅ `<li>Gandalf</li>`
- ✅ `<i>didn't ruin it</i>`
- ✅ `<b>I like Tolkien</b>`
- ✅ `<a href` (links)
- ✅ `<li>It can be enjoyed by children and adults alike</li>`
- ✅ `<code>` (elementos de código)
- ✅ `<blockquote>"I am in fact a Hobbit in all but size."`

### 🎯 **Resultado Final**

- ✅ **176 testes passando** (162 anteriores + 14 novos)
- ✅ **Função extract_title** funcionando perfeitamente
- ✅ **Função generate_page** criando HTML correto
- ✅ **Pipeline completo** de geração funcionando
- ✅ **Servidor web** servindo conteúdo na porta 8888
- ✅ **Todos os elementos esperados** presentes no HTML

O gerador de site estático está funcionando perfeitamente! 🎉

**Acesso**: http://localhost:8888
