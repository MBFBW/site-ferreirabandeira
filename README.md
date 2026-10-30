# Ferreira Bandeira Advocacia

Site institucional publicado em https://ferreirabandeira.adv.br pelo GitHub Pages.

## Como o site é gerado

Todas as páginas são geradas por `python3 tools/build.py`:

- `tools/home.tpl.html`: modelo da página inicial (cabeçalho, contato e rodapé vêm daqui para todas as páginas).
- `tools/servicos.py`: conteúdo das páginas de serviço.
- `conteudo/artigos/*.json`: um arquivo por artigo.
- `assets/`: estilo (`site.css`), script (`site.js`), logo 3D (`logo3d.js`) e imagens.

## Publicar um novo artigo

1. Crie `conteudo/artigos/AAAA-MM-DD-slug.json` com os campos `slug`, `area`, `data`, `titulo`, `resumo` e `corpo`.
   - `area`: Família, Direito Imobiliário, Condomínios, Execuções ou Direito Civil.
   - `corpo`: HTML com `<p>`, `<h4>`, `<ul>` e, no fim, `<p class="lei">Base legal: ...</p>`.
2. Rode `python3 tools/build.py`.
3. Faça commit e push. O artigo ganha página própria em `/artigos/slug/`, entra na página inicial, no índice e no sitemap.
