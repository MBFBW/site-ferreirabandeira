#!/usr/bin/env python3
"""Gera o site ferreirabandeira.adv.br.

Uso:  python3 tools/build.py
Fonte única do layout: tools/home.tpl.html (cabeçalho, contato, rodapé).
Conteúdo: tools/servicos.py (páginas de serviço) e conteudo/artigos/*.json (artigos).

Para publicar um novo artigo: crie conteudo/artigos/AAAA-MM-DD-slug.json com os campos
slug, area, data (AAAA-MM-DD), titulo, resumo e corpo (HTML com <p>, <h4>, <ul> e <p class="lei">)
e rode este script. Ele refaz a página inicial, as páginas de artigo, o índice e o sitemap.
"""
import os, re, json, glob, html, datetime, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'tools'))
from servicos import SERVICOS

SITE = 'https://ferreirabandeira.adv.br'
V = datetime.date.today().strftime('%Y%m%d')
MESES = ['jan.', 'fev.', 'mar.', 'abr.', 'maio', 'jun.', 'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.']
AREA_LINK = {'Família': '/direito-de-familia/', 'Direito Imobiliário': '/direito-imobiliario/',
             'Condomínios': '/condominios/', 'Execuções': '/execucoes/', 'Direito Civil': '/#areas'}

TPL = open(os.path.join(RAIZ, 'tools', 'home.tpl.html'), encoding='utf-8').read()


def pedaco(inicio, fim):
    i = TPL.index(inicio)
    return TPL[i:TPL.index(fim, i) + len(fim)]


HEADER = pedaco('<header class="top"', '</header>')
CONTATO = pedaco('<section class="band contato"', '</section>')
WAFLOAT = pedaco('<a class="wa-float', '</a>')

SELOS = '''<section class="selos-faixa" aria-label="Selos de confiança">
  <div class="wrap selos-grid">
    <a class="selo-q" href="https://cna.oab.org.br/" target="_blank" rel="noopener"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 4.4 3.4 8.3 8 9 4.6-.7 8-4.6 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg></span><span><b>Inscrição ativa na OAB/PR</b><small>Nº 88.257 · confira no Cadastro Nacional</small></span></a>
    <div class="selo-q"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg></span><span><b>Site seguro</b><small>Conexão protegida por HTTPS</small></span></div>
    <a class="selo-q" href="/politica-de-privacidade/"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 4.4 3.4 8.3 8 9 4.6-.7 8-4.6 8-9V6l-8-3Z"/><path d="M9.5 12.5h5M12 10v5"/></svg></span><span><b>Dados protegidos</b><small>Conforme a LGPD (Lei 13.709/2018)</small></span></a>
    <div class="selo-q"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h16M6 20V9l6-5 6 5v11"/><path d="M10 20v-6h4v6"/></svg></span><span><b>Sigilo profissional</b><small>Atendimento pessoal pelo advogado</small></span></div>
    <div class="selo-q"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 3 2.5 15 0 18M12 3c-2.5 3-2.5 15 0 18"/></svg></span><span><b>Atendimento online</b><small>Para clientes de todo o Brasil</small></span></div>
    <div class="selo-q"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4h10v16H7z"/><path d="M10 8h4M10 12h4M10 16h2"/></svg></span><span><b>Publicidade ética</b><small>Conforme o Provimento 205/2021</small></span></div>
  </div>
</section>'''

FOOTER = '''<footer class="base">
  <div class="wrap">
    <div class="grid">
      <div>
        <img src="/assets/logo-branca.png" alt="Ferreira Bandeira Advocacia" width="230" height="37" loading="lazy">
        <p style="margin:0;max-width:26em">Maurício Barreto de Ferreira Bandeira, advogado inscrito na OAB/PR sob o nº 88.257.</p>
        <p style="margin:12px 0 0">Atendimento com hora marcada em São José dos Pinhais e Curitiba, e online para todo o Brasil.</p>
      </div>
      <div>
        <h4>Direito de Família</h4>
        <ul><li><a href="/divorcio/">Divórcio</a></li><li><a href="/pensao-alimenticia/">Pensão alimentícia</a></li><li><a href="/guarda-de-filhos/">Guarda de filhos</a></li><li><a href="/uniao-estavel/">União estável</a></li><li><a href="/partilha-de-bens/">Partilha de bens</a></li><li><a href="/execucao-de-alimentos/">Execução de alimentos</a></li></ul>
      </div>
      <div>
        <h4>Outras áreas</h4>
        <ul><li><a href="/direito-imobiliario/">Direito Imobiliário</a></li><li><a href="/usucapiao/">Usucapião</a></li><li><a href="/condominios/">Condomínios</a></li><li><a href="/execucoes/">Execuções</a></li><li><a href="/artigos/">Artigos</a></li></ul>
      </div>
      <div>
        <h4>Contato</h4>
        <ul><li><a class="wa-link" href="https://wa.me/5541988107330" target="_blank" rel="noopener">(41) 98810-7330</a></li><li><a href="mailto:mbandeira.adv@gmail.com">mbandeira.adv@gmail.com</a></li><li>Seg. a sex., das 9h às 18h</li><li><a href="/politica-de-privacidade/">Política de privacidade</a></li></ul>
      </div>
    </div>
    <div class="legal">
      <span>Conteúdo de caráter exclusivamente informativo, em conformidade com o Código de Ética e Disciplina da OAB e o Provimento 205/2021 do Conselho Federal. As informações publicadas não substituem a consulta a um advogado sobre o caso concreto.</span>
      <span>© 2026 Ferreira Bandeira Advocacia · <a href="https://cna.oab.org.br/" target="_blank" rel="noopener">OAB/PR 88.257</a></span>
    </div>
  </div>
</footer>'''

ORG = {"@type": "LegalService", "@id": SITE + "/#escritorio", "name": "Ferreira Bandeira Advocacia",
       "url": SITE + "/", "telephone": "+55-41-98810-7330", "email": "mbandeira.adv@gmail.com",
       "image": SITE + "/compartilhar.png", "logo": SITE + "/assets/logo-cor.png",
       "areaServed": [{"@type": "City", "name": "São José dos Pinhais"}, {"@type": "City", "name": "Curitiba"}, {"@type": "Country", "name": "Brasil"}],
       "address": {"@type": "PostalAddress", "addressLocality": "São José dos Pinhais", "addressRegion": "PR", "addressCountry": "BR"},
       "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
       "founder": {"@type": "Person", "name": "Maurício Barreto de Ferreira Bandeira", "jobTitle": "Advogado", "identifier": "OAB/PR 88.257"},
       "knowsAbout": ["Direito de Família", "Divórcio", "Pensão alimentícia", "Guarda de filhos", "União estável", "Direito Imobiliário", "Usucapião", "Direito Condominial", "Execuções"]}


def data_br(iso):
    a, m, d = iso.split('-')
    return f'{int(d)} {MESES[int(m) - 1]} {a}'


def esc(s):
    return html.escape(s, quote=True)


def head(titulo, desc, url, schemas, extra=''):
    ld = json.dumps({"@context": "https://schema.org", "@graph": schemas}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/favicon.png">
<meta name="theme-color" content="#0B1730">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Ferreira Bandeira Advocacia">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/compartilhar.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;500;600;700&family=Manrope:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={V}">
<script type="application/ld+json">{ld}</script>
{extra}</head>
<body class="interna">
'''


def header_interno():
    h = HEADER.replace('href="#', 'href="/#').replace('class="top" id="topo"', 'class="top solid fixo" id="topo"')
    h = re.sub(r'<span class="logo3d" id="logo3d">(<img[^>]*>)</span>', r'\1', h)
    return h.replace('href="/#inicio"', 'href="/"')


def rodape():
    return SELOS + '\n' + FOOTER + '\n' + WAFLOAT + f'\n<script src="/assets/site.js?v={V}" defer></script>\n</body>\n</html>\n'


def crumbs(itens):
    parts = []
    for nome, url in itens:
        parts.append(f'<a href="{url}">{esc(nome)}</a>' if url else f'<span aria-current="page">{esc(nome)}</span>')
    return '<nav class="crumbs" aria-label="Caminho">' + '<span class="sep">›</span>'.join(parts) + '</nav>'


def bc_schema(itens):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (u or '')} for i, (n, u) in enumerate(itens) if u or i == len(itens) - 1]}


def lateral(assunto):
    return f'''<aside class="lado">
  <div class="lado-card">
    <div class="eyebrow">Atendimento</div>
    <h3>Fale sobre o seu caso</h3>
    <p>Atendimento pessoal pelo advogado, com hora marcada, no escritório ou por videochamada.</p>
    <a class="btn btn-wa wa-link" href="https://wa.me/5541988107330" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>Conversar no WhatsApp</a>
    <a class="btn btn-navy" href="#contato" data-assunto="{esc(assunto)}">Enviar mensagem</a>
    <ul class="lado-info"><li><b>Horário</b> Seg. a sex., 9h às 18h</li><li><b>Telefone</b> (41) 98810-7330</li><li><b>Advogado</b> Maurício Bandeira · OAB/PR 88.257</li></ul>
  </div>
</aside>'''


def faq_html(faq):
    return '<div class="faq">' + ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq) + '</div>'


ASSUNTO_FORM = {'Família': 'Família', 'Imobiliário': 'Direito Imobiliário', 'Condomínios': 'Condomínio', 'Execuções': 'Execução ou cobrança'}


def pagina_servico(s, todos):
    url = f'{SITE}/{s["slug"]}/'
    itens = [('Início', '/')]
    if s.get('pai'):
        p = next(x for x in todos if x['slug'] == s['pai'])
        itens.append((p.get('curto', p['titulo']), f'/{p["slug"]}/'))
    itens.append((s['titulo'], None))
    rel = [x for x in todos if x['slug'] != s['slug'] and (x['grupo'] == s['grupo'] or x['slug'] in ('direito-de-familia',))][:6]
    rel_html = ''.join(f'<a href="/{x["slug"]}/"><b>{esc(x["titulo"])}</b><span>{esc(x["descricao"][:90].rsplit(" ", 1)[0])}…</span></a>' for x in rel)
    schemas = [ORG,
               {"@type": "Service", "name": s['titulo'], "serviceType": s['titulo'], "provider": {"@id": SITE + "/#escritorio"}, "areaServed": "BR", "url": url, "description": s['descricao']},
               {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s['faq']]},
               bc_schema([(n, u if u else f'/{s["slug"]}/') for n, u in itens])]
    corpo = f'''{header_interno()}
<main id="inicio">
  <section class="pg-hero">
    <div class="wrap">
      {crumbs(itens)}
      <div class="eyebrow">{esc(s['grupo'] if s['grupo'] != 'Família' else 'Direito de Família')}</div>
      <h1>{esc(s['titulo'])}</h1>
      <p class="pg-lead">{esc(s['lead'])}</p>
      <div class="ctas"><a class="btn btn-solid" href="#contato" data-assunto="{esc(ASSUNTO_FORM.get(s['grupo'], 'Outro assunto cível'))}">Agendar atendimento</a><a class="btn btn-ghost wa-link" href="https://wa.me/5541988107330" target="_blank" rel="noopener">Conversar no WhatsApp</a></div>
    </div>
  </section>
  <section class="band pg-corpo">
    <div class="wrap pg-grid">
      <article class="prosa">
        {s['corpo'].strip()}
        <h2>Perguntas frequentes</h2>
        {faq_html(s['faq'])}
        <p class="aviso-info">Conteúdo informativo. Cada caso tem particularidades que precisam ser analisadas por um advogado.</p>
      </article>
      {lateral(ASSUNTO_FORM.get(s['grupo'], 'Outro assunto cível'))}
    </div>
  </section>
  <section class="band relacionados">
    <div class="wrap">
      <div class="eyebrow">Veja também</div>
      <h2 class="sec-title" style="font-size:clamp(24px,3vw,32px)">Outros serviços</h2>
      <div class="rel-grid">{rel_html}</div>
    </div>
  </section>
  {CONTATO}
</main>
'''
    return head(s['seo_titulo'] + ' | Ferreira Bandeira Advocacia', s['descricao'], url, schemas) + corpo + rodape()


def card_artigo(a):
    return f'''        <article class="post" data-area="{esc(a['area'])}">
          <a class="thumb" href="/artigos/{a['slug']}/" aria-hidden="true" tabindex="-1"><span class="tag"><small>Artigo</small>{esc(a['area'])}</span></a>
          <div class="post-body">
            <div class="meta">{esc(a['area'])} · <time datetime="{a['data']}">{data_br(a['data'])}</time></div>
            <h3><a href="/artigos/{a['slug']}/">{a['titulo']}</a></h3>
            <p class="resumo">{a['resumo']}</p>
            <a class="ler" href="/artigos/{a['slug']}/">Continue lendo →</a>
          </div>
        </article>'''


def pagina_artigo(a, outros):
    url = f'{SITE}/artigos/{a["slug"]}/'
    titulo_txt = re.sub('<[^>]+>', '', a['titulo'])
    itens = [('Início', '/'), ('Artigos', '/artigos/'), (titulo_txt, None)]
    area_link = AREA_LINK.get(a['area'], '/#areas')
    schemas = [ORG,
               {"@type": "BlogPosting", "headline": titulo_txt, "description": a['resumo'], "datePublished": a['data'], "dateModified": a['data'],
                "inLanguage": "pt-BR", "mainEntityOfPage": url, "image": SITE + "/compartilhar.png",
                "author": {"@type": "Person", "name": "Maurício Barreto de Ferreira Bandeira", "jobTitle": "Advogado, OAB/PR 88.257"},
                "publisher": {"@id": SITE + "/#escritorio"}},
               bc_schema([('Início', '/'), ('Artigos', '/artigos/'), (titulo_txt, f'/artigos/{a["slug"]}/')])]
    mais = ''.join(card_artigo(o) for o in outros[:3])
    corpo = f'''{header_interno()}
<main id="inicio">
  <section class="pg-hero pg-hero-art">
    <div class="wrap">
      {crumbs(itens)}
      <div class="eyebrow">{esc(a['area'])} · <time datetime="{a['data']}">{data_br(a['data'])}</time></div>
      <h1>{a['titulo']}</h1>
      <p class="pg-lead">{a['resumo']}</p>
      <p class="autor">Por <b>Maurício Barreto de Ferreira Bandeira</b>, advogado, OAB/PR 88.257</p>
    </div>
  </section>
  <section class="band pg-corpo">
    <div class="wrap pg-grid">
      <article class="prosa artigo">
        {a['corpo']}
        <p class="aviso-info">Este artigo tem caráter exclusivamente informativo e não substitui a análise do caso concreto por um advogado. Saiba mais sobre <a href="{area_link}">{esc(a['area'])}</a>.</p>
      </article>
      {lateral(ASSUNTO_FORM.get(a['area'], 'Outro assunto cível'))}
    </div>
  </section>
  <section class="band relacionados">
    <div class="wrap">
      <div class="eyebrow">Continue lendo</div>
      <h2 class="sec-title" style="font-size:clamp(24px,3vw,32px)">Outros artigos</h2>
      <div class="posts">{mais}</div>
    </div>
  </section>
  {CONTATO}
</main>
'''
    return head(titulo_txt + ' | Ferreira Bandeira Advocacia', re.sub('<[^>]+>', '', a['resumo']), url, schemas) + corpo + rodape()


def pagina_indice(arts):
    url = f'{SITE}/artigos/'
    itens = [('Início', '/'), ('Artigos', None)]
    cards = '\n'.join(card_artigo(a) for a in arts)
    corpo = f'''{header_interno()}
<main id="inicio">
  <section class="pg-hero">
    <div class="wrap">
      {crumbs(itens)}
      <div class="eyebrow">Conteúdo informativo</div>
      <h1>Artigos</h1>
      <p class="pg-lead">Respostas claras às dúvidas jurídicas mais buscadas sobre família, imóveis, condomínios, execuções e direito civil. Novos artigos toda semana.</p>
    </div>
  </section>
  <section class="band">
    <div class="wrap"><div class="posts">
{cards}
    </div></div>
  </section>
  {CONTATO}
</main>
'''
    return head('Artigos jurídicos | Ferreira Bandeira Advocacia', 'Artigos informativos sobre Direito de Família, Imobiliário, Condomínios e Execuções, escritos pelo advogado Maurício Bandeira, OAB/PR 88.257.', url, [ORG, bc_schema([('Início', '/'), ('Artigos', '/artigos/')])]) + corpo + rodape()


PRIVACIDADE = '''
<h2>Quem é o responsável pelos dados</h2>
<p>O controlador dos dados pessoais tratados neste site é o advogado Maurício Barreto de Ferreira Bandeira, OAB/PR 88.257 (Ferreira Bandeira Advocacia), com contato pelo e-mail mbandeira.adv@gmail.com e pelo telefone (41) 98810-7330.</p>
<h2>Quais dados são coletados</h2>
<p>O site coleta apenas os dados que você informa voluntariamente no formulário de contato: nome, WhatsApp, e-mail, cidade, assunto, preferência de atendimento e o relato do caso. Quando você opta pelo WhatsApp, a conversa ocorre diretamente no aplicativo, sob as regras do próprio WhatsApp.</p>
<p>O site não usa cookies de publicidade nem ferramentas de rastreamento de terceiros.</p>
<h2>Para que os dados são usados</h2>
<p>Os dados são usados exclusivamente para responder ao seu contato, agendar o atendimento e avaliar a contratação dos serviços jurídicos. A base legal é o seu consentimento e a realização de procedimentos preliminares a um contrato, a seu pedido (art. 7º, incisos I e V, da Lei 13.709/2018).</p>
<h2>Com quem os dados são compartilhados</h2>
<p>As mensagens enviadas pelo formulário são transmitidas por meio dos serviços do Google para o e-mail do advogado. Os dados não são vendidos nem compartilhados com terceiros para qualquer outra finalidade. Todas as informações estão protegidas pelo sigilo profissional do advogado.</p>
<h2>Por quanto tempo os dados são guardados</h2>
<p>Pelo tempo necessário para responder ao contato e, se houver contratação, pelo prazo exigido para o exercício da advocacia e o cumprimento de obrigações legais.</p>
<h2>Seus direitos</h2>
<p>Você pode, a qualquer momento, pedir a confirmação do tratamento, o acesso, a correção ou a exclusão dos seus dados, além de revogar o consentimento, nos termos do art. 18 da Lei 13.709/2018. Basta enviar um e-mail para mbandeira.adv@gmail.com.</p>
<p class="base-legal">Última atualização: {data}.</p>
'''


def pagina_privacidade():
    url = f'{SITE}/politica-de-privacidade/'
    itens = [('Início', '/'), ('Política de privacidade', None)]
    corpo = f'''{header_interno()}
<main id="inicio">
  <section class="pg-hero">
    <div class="wrap">
      {crumbs(itens)}
      <div class="eyebrow">LGPD</div>
      <h1>Política de privacidade</h1>
      <p class="pg-lead">Como este site trata os dados pessoais de quem entra em contato com o escritório.</p>
    </div>
  </section>
  <section class="band pg-corpo"><div class="wrap"><article class="prosa" style="max-width:46em">{PRIVACIDADE.format(data=data_br(datetime.date.today().isoformat()))}</article></div></section>
</main>
'''
    return head('Política de privacidade | Ferreira Bandeira Advocacia', 'Política de privacidade e proteção de dados do site Ferreira Bandeira Advocacia, conforme a LGPD.', url, [ORG]) + corpo + rodape()


def grava(rel, conteudo):
    p = os.path.join(RAIZ, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(conteudo)


def main():
    arts = [json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(RAIZ, 'conteudo', 'artigos', '*.json'))]
    arts.sort(key=lambda a: (a['data'], a['slug']), reverse=True)
    # página inicial
    home = TPL.replace('{{V}}', V).replace('{{ARTIGOS_HOME}}', '\n'.join(card_artigo(a) for a in arts[:6]))
    home = home.replace('\n  <section class="band familia"', '\n' + SELOS + '\n\n  <section class="band familia"', 1)
    i = home.index('<footer class="base">'); j = home.index('</footer>', i) + 9
    home = home[:i] + FOOTER + home[j:]
    home = home.replace('</div>\n    </div>\n  </section>\n\n  <section class="band" style="background:var(--mist)" id="duvidas"',
                        '</div>\n      <div class="cta-row"><a class="btn btn-outline" href="/artigos/">Ver todos os artigos</a></div>\n    </div>\n  </section>\n\n  <section class="band" style="background:var(--mist)" id="duvidas"', 1)
    grava('index.html', home)
    for s in SERVICOS:
        grava(f'{s["slug"]}/index.html', pagina_servico(s, SERVICOS))
    for a in arts:
        grava(f'artigos/{a["slug"]}/index.html', pagina_artigo(a, [o for o in arts if o['slug'] != a['slug']]))
    grava('artigos/index.html', pagina_indice(arts))
    grava('politica-de-privacidade/index.html', pagina_privacidade())
    hoje = datetime.date.today().isoformat()
    urls = [('/', hoje, '1.0')] + [(f'/{s["slug"]}/', hoje, '0.9' if s['grupo'] == 'Família' else '0.8') for s in SERVICOS] + \
           [('/artigos/', arts[0]['data'] if arts else hoje, '0.7')] + [(f'/artigos/{a["slug"]}/', a['data'], '0.6') for a in arts] + \
           [('/politica-de-privacidade/', hoje, '0.2')]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n' for u, d, p in urls) + '</urlset>\n'
    grava('sitemap.xml', sm)
    print(f'{len(SERVICOS)} serviços, {len(arts)} artigos, {len(urls)} URLs no sitemap')


if __name__ == '__main__':
    main()
