"""Renderiza os slides da Santa Rute Engenharia Rural (1080x1350, JPEG).

Uso: python3 sistema/render.py posts/AAAA-MM-DD-slug/post.json posts/AAAA-MM-DD-slug
O post.json segue o modelo descrito em INSTRUCOES.md.

Identidade própria da Santa Rute (diferente do PRUMO, que é escuro e "de sistema"):
- fundo creme de papel, quente, com o símbolo da logo (engrenagem + folhas) em marca-d'água;
- títulos em serifa (Playfair Display), como o "Dia do Gaúcho" e a assinatura da história de Rute;
- cores da logo: verde-folha, dourado da engrenagem e marrom da terra;
- faixa verde-folha no rodapé com o contato;
- foto de campo em moldura arredondada (como o post de 1 ano), nunca escurecida de fundo inteiro;
- slide final em verde-folha com a logo clara e a assinatura "Tradição que inspira confiança."
"""
import os, re, io, random, cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
W, H = 1080, 1350
FD = os.path.join(BASE, "fontes") + "/"
SANS_B, SANS_M, SANS_R = FD + "Poppins-Bold.ttf", FD + "Poppins-Medium.ttf", FD + "Poppins-Regular.ttf"
SERIF_B, SERIF_XB = FD + "PlayfairDisplay-Bold.ttf", FD + "PlayfairDisplay-ExtraBold.ttf"
SERIF_I, SERIF_BI = FD + "PlayfairDisplay-Italic.ttf", FD + "PlayfairDisplay-BoldItalic.ttf"

# Cores da logo
VERDE = (0, 140, 52)          # verde-folha (nome "Santa Rute"), um pouco fechado para ler no creme
VERDE_FAIXA = (0, 122, 46)
VERDE_ESC = (20, 58, 34)      # títulos
OURO = (204, 153, 51)         # engrenagem
OURO_CLARO = (232, 196, 110)
MARROM = (102, 51, 0)         # linha da logo / terra
CREME = (245, 240, 229)
TEXTO = (58, 66, 58)
BRANCO = (255, 255, 255)

WHATSAPP = "(55) 99723-8982"
SITE = "santarute.com"
ASSINATURA = "Tradição que inspira confiança."
FAIXA = 112  # altura da faixa verde do rodapé


def font(p, s):
    return ImageFont.truetype(p, s)


# ---------- logo e símbolo ----------

def _logo_png(variante, largura=2400):
    png = cairosvg.svg2png(url=os.path.join(BASE, f"logo-{variante}.svg"), output_width=largura)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    return im.crop(im.getbbox())


def logo(variante="cor", alvo_h=120):
    im = _logo_png(variante)
    r = alvo_h / im.height
    im = im.resize((int(im.width * r), alvo_h), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=70, threshold=2))


def simbolo(alvo_h, cor, opacidade):
    """Engrenagem + folhas (parte de cima da logo), numa cor só, para marca-d'água."""
    im = _logo_png("cor")
    topo = im.crop((0, 0, im.width, int(im.height * 0.53)))
    topo = topo.crop(topo.getbbox())
    r = alvo_h / topo.height
    topo = topo.resize((int(topo.width * r), alvo_h), Image.LANCZOS)
    a = topo.split()[3].point(lambda v: int(v * opacidade))
    out = Image.new("RGBA", topo.size, cor + (0,))
    out.putalpha(a)
    return out


LOGO_COR = logo("cor", 118)


# ---------- fundo ----------

def papel(cor=CREME, seed=7):
    """Creme com granulado leve, para não parecer cor chapada de sistema."""
    random.seed(seed)
    im = Image.new("RGB", (W, H), cor)
    ruido = Image.effect_noise((W, H), 18).convert("L")
    ruido = ruido.point(lambda v: 128 + (v - 128) // 3)
    im = ImageChops.overlay(im, Image.merge("RGB", (ruido, ruido, ruido)))
    m = Image.new("L", (W, H), 255)
    ImageDraw.Draw(m).ellipse([-200, -150, W + 200, H + 150], fill=0)
    m = m.filter(ImageFilter.GaussianBlur(140)).point(lambda v: int(v * 0.10))
    im = Image.composite(Image.new("RGB", (W, H), (120, 100, 60)), im, m)
    return im.convert("RGBA")


def marca_dagua(im, x=None, y=None, h=620, cor=VERDE, op=0.06):
    s = simbolo(h, cor, op)
    x = W - s.width + 150 if x is None else x
    y = H - FAIXA - s.height + 90 if y is None else y
    im.alpha_composite(s, (int(x), int(y)))


def faixa(d, esquerda, direita, cor_dir=OURO_CLARO):
    d.rectangle([0, H - FAIXA, W, H], fill=VERDE_FAIXA)
    d.rectangle([0, H - FAIXA, W, H - FAIXA + 6], fill=OURO)
    f = font(SANS_M, 26)
    y = H - FAIXA + (FAIXA - 30) // 2
    d.text((70, y), esquerda, font=f, fill=BRANCO)
    fb = font(SANS_B, 26)
    d.text((W - 70 - d.textlength(direita, font=fb), y), direita, font=fb, fill=cor_dir)


def por_logo(im, x=70, y=64):
    im.alpha_composite(LOGO_COR, (x, y))


def foto_moldura(im, caminho, caixa, raio=36):
    """Foto de campo recortada numa moldura arredondada (como o post de 1 ano)."""
    p = caminho if os.path.isabs(caminho) else os.path.join(REPO, caminho)
    x0, y0, x1, y1 = caixa
    foto = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    foto = ImageOps.fit(foto, (x1 - x0, y1 - y0), Image.LANCZOS, centering=(0.5, 0.45)).convert("RGBA")
    mask = Image.new("L", foto.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, foto.width, foto.height], radius=raio, fill=255)
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle([x0 + 4, y0 + 10, x1 + 4, y1 + 10], radius=raio, fill=(60, 45, 20, 70))
    im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(14)))
    im.paste(foto, (x0, y0), mask)


# ---------- texto ----------

def quebra(texto, f, larg, d):
    linhas = []
    for par in texto.split("\n"):
        atual = ""
        for p in par.split():
            teste = (atual + " " + p).strip()
            if d.textlength(teste, font=f) <= larg:
                atual = teste
            else:
                linhas.append(atual)
                atual = p
        linhas.append(atual)
    return linhas


def altura(d, texto, f, larg, entre):
    return len(quebra(texto, f, larg, d)) * int(f.size * entre)


def titulo(d, x, y, texto, tam, larg, destaque=None, cor=VERDE_ESC, cor_dest=VERDE, entre=1.08, centro=False):
    """Título em serifa; palavras de destaque em verde-folha itálico com sublinhado dourado."""
    destaque = [w.lower() for w in (destaque or [])]
    f, fi = font(SERIF_B, tam), font(SERIF_BI, tam)
    for ln in quebra(texto, f, larg, d):
        palavras = ln.split(" ")
        dest = [re.sub(r"[^\wÀ-ú]", "", p).lower() in destaque for p in palavras]
        larg_ln = sum(d.textlength(p + " ", font=fi if e else f) for p, e in zip(palavras, dest)) - d.textlength(" ", font=f)
        cx = (W - larg_ln) / 2 if centro else x
        for p, e in zip(palavras, dest):
            ff = fi if e else f
            if e:
                wl = d.textlength(re.sub(r"[.,:;!?]+$", "", p), font=ff)
                d.rectangle([cx, y + int(tam * 1.02), cx + wl, y + int(tam * 1.02) + max(5, tam // 14)], fill=OURO_CLARO)
            d.text((cx, y), p, font=ff, fill=cor_dest if e else cor)
            cx += d.textlength(p + " ", font=ff)
        y += int(tam * entre * 1.12)
    return y


def altura_titulo(d, texto, tam, larg, entre=1.08):
    return len(quebra(texto, font(SERIF_B, tam), larg, d)) * int(tam * entre * 1.12)


def bloco(d, x, y, texto, f, cor, larg, entre=1.4, centro=False):
    for ln in quebra(texto, f, larg, d):
        cx = (W - d.textlength(ln, font=f)) / 2 if centro else x
        d.text((cx, y), ln, font=f, fill=cor)
        y += int(f.size * entre)
    return y


def espacado(d, x, y, texto, f, cor, track=0.2):
    cx = x
    for ch in texto:
        d.text((cx, y), ch, font=f, fill=cor)
        cx += d.textlength(ch, font=f) + f.size * track
    return cx


def rotulo(d, x, y, texto):
    """Rótulo do tema: dois pontos (verde-folha e dourado, as cores da logo) + caixa-alta espaçada em marrom."""
    d.ellipse([x, y + 6, x + 18, y + 24], fill=VERDE)
    d.ellipse([x + 26, y + 6, x + 44, y + 24], fill=OURO)
    espacado(d, x + 62, y, texto.upper(), font(SANS_B, 25), MARROM, 0.22)


def linha_marrom(d, x, y, w=110):
    d.rectangle([x, y, x + w, y + 5], fill=MARROM)


# ---------- slides ----------

def slide_capa(s, n, total):
    im = papel(); marca_dagua(im); por_logo(im); d = ImageDraw.Draw(im)
    tam = 96
    if s.get("foto"):
        foto_moldura(im, s["foto"], (70, 230, W - 70, 760))
        d = ImageDraw.Draw(im)
        y0, tam = 810, 78
    else:
        h = 70 + altura_titulo(d, s["titulo"], tam, 940) + 62
        if s.get("sub"):
            h += altura(d, s["sub"], font(SANS_R, 38), 880, 1.4)
        y0 = max(300, 250 + (H - FAIXA - 250 - h) // 2 - 20)
    rotulo(d, 70, y0, s["selo"])
    y = titulo(d, 70, y0 + 66, s["titulo"], tam, 940, s.get("destaque"))
    if s.get("sub"):
        linha_marrom(d, 70, y + 26)
        bloco(d, 70, y + 62, s["sub"], font(SANS_R, 36 if s.get("foto") else 38), TEXTO, 900)
    faixa(d, "arraste para o lado  ›", f"{n}/{total}")
    return im


def slide_texto(s, n, total):
    im = papel(seed=n); marca_dagua(im, op=0.05); por_logo(im); d = ImageDraw.Draw(im)
    fnum = font(SERIF_XB, 150)
    num = f"{s['num']:02d}"
    ft = font(SANS_R, 40)
    h = 170 + altura_titulo(d, s["titulo"], 70, 940) + 30 + altura(d, s["texto"], ft, 930, 1.45)
    if s.get("fonte"):
        h += 90
    y0 = max(270, 230 + (H - FAIXA - 230 - h) // 2)
    d.text((62, y0 - 30), num, font=fnum, fill=OURO)
    d.rectangle([70, y0 + 160, 70 + 60, y0 + 165], fill=MARROM)
    y = titulo(d, 70, y0 + 190, s["titulo"], 70, 940, s.get("destaque"))
    y = bloco(d, 70, y + 24, s["texto"], ft, TEXTO, 930, 1.45)
    if s.get("fonte"):
        f = font(SANS_M, 26)
        d.rectangle([70, y + 40, 76, y + 78], fill=OURO)
        d.text((92, y + 44), "Fonte: " + s["fonte"], font=f, fill=MARROM)
    faixa(d, "SANTA RUTE · ENGENHARIA RURAL", f"{n}/{total}")
    return im


def slide_cta(s, n, total):
    """Fechamento em verde-folha, logo clara, botão creme e a assinatura da marca."""
    im = papel(cor=VERDE_FAIXA, seed=99)
    marca_dagua(im, x=-170, y=H - 760, h=820, cor=BRANCO, op=0.06)
    big = logo("claro", 250)
    im.alpha_composite(big, ((W - big.width) // 2, 140))
    d = ImageDraw.Draw(im)
    y = titulo(d, 0, 500, s["titulo"], 74, 900, s.get("destaque"), cor=BRANCO, cor_dest=OURO_CLARO, centro=True)
    y = bloco(d, 0, y + 20, s["texto"], font(SANS_R, 36), (222, 238, 224), 820, 1.42, centro=True)
    fb = font(SANS_B, 40)
    botao = s.get("botao", "Chame no WhatsApp")
    bw = d.textlength(botao, font=fb) + 110
    bx, by = (W - bw) / 2, y + 56
    d.rounded_rectangle([bx, by, bx + bw, by + 98], radius=49, fill=CREME)
    d.text((bx + 55, by + 23), botao, font=fb, fill=VERDE_ESC)
    fs = font(SANS_M, 34)
    contato = f"{WHATSAPP}  ·  {SITE}"
    d.text(((W - d.textlength(contato, font=fs)) / 2, by + 136), contato, font=fs, fill=OURO_CLARO)
    fi = font(SERIF_I, 42)
    d.rectangle([W / 2 - 40, H - 150, W / 2 + 40, H - 146], fill=OURO_CLARO)
    d.text(((W - d.textlength(ASSINATURA, font=fi)) / 2, H - 126), ASSINATURA, font=fi, fill=CREME)
    return im


def slide_unico(s, n, total):
    """Imagem única: frase forte em serifa + faixa com o WhatsApp."""
    im = papel(); marca_dagua(im); por_logo(im); d = ImageDraw.Draw(im)
    tam = 100
    if s.get("foto"):
        foto_moldura(im, s["foto"], (70, 230, W - 70, 760))
        d = ImageDraw.Draw(im)
        y0, tam = 810, 80
    else:
        h = (70 if s.get("selo") else 0) + altura_titulo(d, s["titulo"], tam, 940) + 40
        if s.get("sub"):
            h += altura(d, s["sub"], font(SANS_R, 38), 880, 1.4)
        y0 = max(300, 250 + (H - FAIXA - 250 - h) // 2 - 20)
    if s.get("selo"):
        rotulo(d, 70, y0, s["selo"])
        y0 += 66
    y = titulo(d, 70, y0, s["titulo"], tam, 940, s.get("destaque"))
    if s.get("sub"):
        linha_marrom(d, 70, y + 26)
        bloco(d, 70, y + 62, s["sub"], font(SANS_R, 38), TEXTO, 900)
    faixa(d, "Santa Rute · Engenharia Rural", f"WhatsApp {WHATSAPP}")
    return im


def render(slides, pasta):
    os.makedirs(pasta, exist_ok=True)
    fn = {"capa": slide_capa, "texto": slide_texto, "cta": slide_cta, "unico": slide_unico}
    out = []
    for i, s in enumerate(slides, 1):
        p = f"{pasta}/slide_{i:02d}.jpg"
        fn[s["tipo"]](s, i, len(slides)).convert("RGB").save(p, "JPEG", quality=92, optimize=True)
        out.append(p)
    return out


if __name__ == "__main__":
    import json, sys
    dados = json.load(open(sys.argv[1]))
    print(render(dados["slides"], sys.argv[2]))
