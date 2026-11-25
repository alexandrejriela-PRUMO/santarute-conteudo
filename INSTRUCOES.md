# Posts da Santa Rute Engenharia Rural: como gerar, aprovar e publicar

Este repositório guarda tudo o que a tarefa agendada precisa para fazer os posts da Santa Rute
(Instagram @santa.rute e página "Santa Rute - Engenharia Rural" no Facebook) e as artes de cada post publicado.
O Instagram puxa as imagens daqui, pelo link público.

Calendário: **segunda (carrossel)** e **quarta (imagem única)**, sempre com aprovação do Alexandre antes de publicar.

## Quem é a Santa Rute

Consultoria ambiental e rural de Três Passos/RS (Noroeste gaúcho), de um casal que virou sociedade:
Fernanda (engenheira florestal, o trabalho de campo, "o projeto que resolve") e Alexandre (advogado ambiental,
"quando o processo aperta"). Atende produtores rurais e empresas da região.
Serviços: licenciamento ambiental (aviário, suínos, bovinos, agroindústria, empresas e loteamentos), CAR e
regularização, defesa de autos de infração, PRAD rural e urbano, outorga de água subterrânea (poço) no SIOUT RS,
manejo florestal, supressão e reposição, georreferenciamento e estudos geológicos para loteamento.

Contato que vai nos posts: WhatsApp **(55) 99723-8982** e **santarute.com**.
Assinatura da marca: "Tradição que inspira confiança."

## Público e tom

- Quem lê: produtor rural da região (aviário, suíno, leite, grãos), dono de pequena empresa ou agroindústria,
  quem vai lotear ou construir. Entende de lavoura e de bicho; não entende de órgão ambiental nem de lei.
- Fala a língua do produtor, não do técnico: "licença", "multa", "papel do poço", "banco travou o custeio".
  Nada de "conformidade", "passivo", "adequação normativa" sem explicar. Frases curtas.
- Pode usar urgência real (prazo, multa, embargo, autuação, financiamento travado), sempre verdadeira.
- Gancho da capa: no máximo **8 palavras**. Tem que fazer parar de rolar, não explicar o post.
  Tipos que funcionam: erro comum, pergunta que dói, antes e depois, número real, afirmação que contraria o senso comum.
- Menos "gestão" e mais "a gente resolve a sua situação". O post sempre fecha com a Santa Rute resolvendo
  a dor e o convite para o WhatsApp.
- Pode puxar a região: Três Passos, Noroeste gaúcho, municípios vizinhos. Pode falar como "a gente".

## Os 8 pilares (rodar; não repetir o mesmo pilar em posts seguidos)

1. Licenciamento (aviário, pocilga, gado confinado, agroindústria, empresa, renovação de LO)
2. CAR e regularização (CAR, PRA, crédito rural travado, Reserva Legal, APP)
3. Multas e autos de infração (prazo de defesa, citação por edital, desconto, embargo)
4. Recuperação de área (PRAD rural e urbano, APP degradada, açude, barragem)
5. Água e outorga (poço, SIOUT RS, dispensa, açude, irrigação)
6. Florestal (manejo, corte e supressão de árvores, reposição florestal, mata nativa)
7. Loteamento e obra (estudo geológico, licença de loteamento, georreferenciamento, SIGEF)
8. Bastidores e casos (campo, equipe, caso resolvido). **Só com foto real aprovada** (ver "Fotos").
   Sem foto disponível, pular este pilar.

Antes de escolher o tema, ler `historico.md`: não repetir pilar do último post nem tema dos últimos 12.
Dê preferência ao que está acontecendo agora na região (safra, prazo que vence, lei nova, fiscalização).

## Regras de conteúdo

- Toda citação de lei, artigo, prazo, valor ou número deve ser **conferida na web antes**, em fonte oficial
  (planalto.gov.br, al.rs.gov.br, sema.rs.gov.br, fepam.rs.gov.br, diário oficial). Se a página não abrir direto,
  procurar com WebSearch e abrir o link do resultado. Se não conseguir confirmar, não cite o artigo; fale da regra
  em termos gerais. Atenção a lei gaúcha nova: muita regra mudou em 2025 e 2026.
- Não inventar estatística nem caso. Nada de "80% dos produtores...". Caso real só com autorização do cliente.
- Não prometer resultado ("multa cancelada", "licença em 30 dias"). Prometer acompanhamento e clareza.
- Não dar parecer pelo post. O post explica a regra e chama para conversar.
- Sem imagem gerada por IA. Artes com tipografia e cores da marca (modelo em `sistema/render.py`),
  com ou sem foto real de fundo.
- Legenda: 600 a 1.200 caracteres, parágrafos curtos, primeira linha = gancho, termina com
  "Chame no WhatsApp (55) 99723-8982" + 4 a 6 hashtags (2 de nicho, 1 ou 2 da região, ex.: #trespassos #noroestegaucho).

## Identidade visual (já está no modelo; não mudar sem o Alexandre pedir)

A Santa Rute tem cara própria, diferente do PRUMO (que é escuro, sem serifa, "de sistema").
Aqui o clima é de tradição, campo e família:
- Fundo creme de papel, com o símbolo da logo (engrenagem + folhas) bem clarinho em marca-d'água.
- Títulos em serifa (Playfair Display), verde-escuro; palavras de destaque em verde-folha itálico com sublinhado dourado.
- Texto corrido em Poppins, cinza-esverdeado.
- Cores só da logo: verde-folha, dourado da engrenagem, marrom da terra.
- Logo colorida no canto de cima, em tamanho grande (185 px de altura; aumentada a pedido do Alexandre em 25/11/2026); faixa verde-folha com filete dourado no rodapé (contato ou número do slide).
- Números dos slides em serifa grande dourada ("01", "02"...).
- Slide final em verde-folha, logo clara, botão creme "Chame no WhatsApp" e a assinatura
  "Tradição que inspira confiança." em itálico.
- Foto de campo entra em moldura arredondada no alto (como o post de 1 ano), nunca como fundo escurecido.
- Não usar fundo escuro degradê nem selo em pílula: isso é do PRUMO.

## Fotos

Na Santa Rute, foto real de campo rende mais que só tipografia (o post de 1 ano, com o casal no campo,
foi o mais forte de todas as contas). As fotos liberadas para post ficam em `fotos/`.
- Só entra em `fotos/` foto que o Alexandre aprovou para publicar. Nada de cliente identificável sem autorização,
  placa de carro legível, documento ou criança.
- Para usar: `"foto": "fotos/nome.jpg"` na capa ou na imagem única. A foto entra numa moldura arredondada
  no alto e o título vai para baixo dela (título menor, até ~40 caracteres).
- Sem foto adequada ao tema, use o fundo verde. Não force foto que não tem a ver com o assunto.

## Formatos

**Segunda: carrossel (5 a 7 slides).** `capa` → 3 a 5 `texto` → `cta`.
**Quarta: imagem única.** um slide `unico` com frase forte; a legenda carrega a explicação.

Modelo do `post.json` (exemplo real em `posts/2026-11-23-poco-dispensado/post.json`):

```json
{
  "pilar": "Água e outorga",
  "formato": "carrossel",
  "slides": [
    {"tipo": "capa", "selo": "Água e outorga", "titulo": "...", "destaque": ["palavras", "em", "dourado"], "sub": "...", "foto": "fotos/opcional.jpg"},
    {"tipo": "texto", "num": 1, "titulo": "...", "destaque": ["..."], "texto": "...", "fonte": "Lei estadual 16.316/2025"},
    {"tipo": "cta", "titulo": "...", "texto": "...", "botao": "Chame no WhatsApp"}
  ],
  "legenda": "..."
}
```

Imagem única: `{"tipo": "unico", "selo": "...", "titulo": "...", "destaque": [...], "sub": "...", "foto": "opcional"}`.

Tamanhos que cabem bem: título da capa até ~45 caracteres; título de slide `texto` até ~45; texto do slide até ~230;
texto do `cta` até ~110.

Gerar as artes: `python3 sistema/render.py posts/AAAA-MM-DD-slug/post.json posts/AAAA-MM-DD-slug`
(precisa de `pip install --break-system-packages cairosvg` se não estiver instalado).
Sempre abrir as imagens e conferir: texto cortado, sobreposição, palavra sozinha na última linha, acento.
Ajustar o texto e renderizar de novo.

A pasta do post leva a data do dia da publicação (segunda ou quarta).

## Aprovação

1. Mandar ao Alexandre as artes (SendUserFile, status proactive) e, em mensagem, a legenda completa, o pilar
   e de onde saiu cada lei ou número citado.
2. Mandar notificação no celular avisando que o post da Santa Rute está esperando aprovação.
3. Esperar a resposta. Ajustes pedidos ("troca o título do slide 2") mexem só no que foi pedido.
4. **Só publicar com aprovação explícita** ("aprovado", "pode publicar"). Sem resposta, não publica.

## Publicação (só depois do OK)

1. Commit da pasta `posts/AAAA-MM-DD-slug/` (post.json + JPGs) e push para `main`.
2. Links das imagens, sempre com o hash do commit (evita imagem antiga em cache):
   `https://raw.githubusercontent.com/alexandrejriela-PRUMO/santarute-conteudo/<HASH>/posts/AAAA-MM-DD-slug/slide_01.jpg`
   Conferir com curl que cada link responde 200 image/jpeg.
3. Instagram (Zapier, "Instagram for Business" → Publish Photo(s)):
   conta **Santa Rute** `instagramPageId = 17841446863806726`; `media` = lista de links na ordem; `caption` = legenda.
4. Facebook (Zapier, "Facebook Pages" → Create Page Photo):
   página **Santa Rute - Engenharia Rural** `page = 102774781942580`; `source` = **só o link do slide_01**;
   `message` = legenda.
5. Pegar o link do post no Instagram (Instagram for Business → Make API GET Request em
   `https://graph.facebook.com/v23.0/<id>?fields=permalink`) e responder ao Alexandre com ele.
6. Acrescentar a linha em `historico.md`, commit e push.

Se algo falhar (Zapier fora, erro de publicação), avisar o Alexandre do que faltou, com as artes prontas
para postar à mão. Nunca publicar na conta ou página de outra marca (PRUMO, Zubiaurre & Riela, Repiso).
