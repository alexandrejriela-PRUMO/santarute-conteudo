"""Renderiza os slides da Santa Rute Engenharia Rural (1080x1350, JPEG).

Uso: python3 sistema/render.py posts/AAAA-MM-DD-slug/post.json posts/AAAA-MM-DD-slug
O post.json segue o modelo descrito em INSTRUCOES.md.

Identidade (tirada dos posts que já saíram no @santa.rute e da logo vetorizada):
- fundo verde-mata escuro, destaque em dourado, texto branco;
- Poppins (títulos e texto) e Playfair Display itálico (assinatura "Tradição que inspira confiança.");
- logo clara (folhas e nome em branco, engrenagem e linha em dourado) sobre o verde;
- logo colorida original no slide final, sobre fundo creme.
"""
import os, re, io, cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
W, H = 1080, 1350
FD = os.path.join(BASE, "fontes") + "/"
BOLD, MED, REG = FD + "Poppins-Bold.ttf", FD + "Poppins-Medium.ttf", FD + "Poppins-Regular.ttf"
SERIF_IT, SERIF_B = FD + "PlayfairDisplay-Italic.ttf", FD + "PlayfairDisplay-Bold.ttf"

# Cores da marca
OURO = (226, 184, 90)          # dourado dos destaques (engrenagem da logo, clareada para o fundo escuro)
OURO_LOGO = (204, 153, 51)     # dourado original da logo
VERDE_MARCA = (0, 153, 51)     # verde do nome "Santa Rute"
MARROM = (102, 51, 0)          # marrom da linha da logo
BRANCO = (255, 255, 255)
SOFT = (216, 230, 218)         # texto corrido sobre o verde
CREME = (243, 238, 227)
VERDE_TXT = (16, 60, 34)       # texto escuro sobre o creme
TOP, BOT = (20, 70, 40), (7, 33, 19)

WHATSAPP = "(55) 99723-8982"
SITE = "santarute.com"
ASSINATURA = "Tradição que inspira confiança."


def font(p, s):
    return ImageFont.truetype(p, s)


# ---------- fundo ----------

def fundo_verde():
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(TOP[i] + (BOT[i] - TOP[i]) * t) for i in range(3)))
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([-350, -450, 750, 520], fill=55)
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    im = Image.composite(Image.new("RGB", (W, H), (44, 112, 62)), im, glow)
    return im.convert("RGBA")


def fundo_foto(caminho):
    """Foto de campo cobrindo o slide, com véu verde para o texto ler bem."""
    p = caminho if os.path.isabs(caminho) else os.path.join(REPO, caminho)
    foto = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    foto = ImageOps.fit(foto, (W, H), Image.LANCZOS, centering=(0.5, 0.45))
    foto = foto.filter(ImageFilter.GaussianBlur(1.2)).convert("RGBA")
    veu = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(veu)
    for y in range(H):
        t = y / H
        a = int(105 + 140 * t)  # mais claro em cima (aparece a foto), mais escuro embaixo (texto)
        d.line([(0, y), (W, y)], fill=(8, 36, 20, min(a, 238)))
    foto.alpha_composite(veu)
    return foto


def fundo(s):
    return fundo_foto(s["foto"]) if s.get("foto") else fundo_verde()


# ---------- logo ----------

def logo(variante="claro", alvo_h=120):
    png = cairosvg.svg2png(url=os.path.join(BASE, f"logo-{variante}.svg"), output_width=2400)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    im = im.crop(im.getbbox())
    r = alvo_h / im.height
    im = im.resize((int(im.width * r), alvo_h), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=80, threshold=2))


LOGO_CLARO = logo("claro", 132)


def por_logo(im, x=70, y=58):
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
    m = LOGO_CLARO.split()[3].point(lambda a: int(a * 0.6))
    sombra.paste((0, 0, 0, 255), (x + 2, y + 4), m)
    sombra = sombra.filter(ImageFilter.GaussianBlur(8))
    im.alpha_composite(sombra)
    im.alpha_composite(LOGO_CLARO, (x, y))


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


def bloco(d, x, y, texto, f, cor, larg, entre=1.18, destaque=None, cor_dest=OURO):
    """destaque: palavras pintadas de dourado"""
    destaque = [w.lower() for w in (destaque or [])]
    for ln in quebra(texto, f, larg, d):
        cx = x
        for p in ln.split(" "):
            limpa = re.sub(r"[^\wÀ-ú]", "", p).lower()
            c = cor_dest if limpa in destaque else cor
            d.text((cx, y), p, font=f, fill=c)
            cx += d.textlength(p + " ", font=f)
        y += int(f.size * entre)
    return y


def altura(d, texto, f, larg, entre):
    return len(quebra(texto, f, larg, d)) * int(f.size * entre)


def topo_capa(d, s, tam_titulo):
    """Sem foto: bloco no meio do slide. Com foto: bloco no terço de baixo, deixando a foto aparecer."""
    h = 90 + altura(d, s["titulo"], font(BOLD, tam_titulo), 940, 1.12) + 44
    if s.get("sub"):
        h += 50 + altura(d, s["sub"], font(MED, 38), 900, 1.35)
    if s.get("foto"):
        return max(330, 1190 - h)
    return max(300, min(420, 250 + (950 - h) // 2))


def espacado(d, x, y, texto, f, cor, track=0.22):
    """Caixa-alta com espaçamento largo (como o 'NOSSA ESSÊNCIA' dos posts da Santa Rute)."""
    cx = x
    for ch in texto:
        d.text((cx, y), ch, font=f, fill=cor)
        cx += d.textlength(ch, font=f) + f.size * track
    return cx


def larg_espacado(d, texto, f, track=0.22):
    return sum(d.textlength(ch, font=f) + f.size * track for ch in texto) - f.size * track


def selo(d, x, y, texto):
    """Rótulo do tema: traço dourado + caixa-alta espaçada."""
    d.rectangle([x, y + 15, x + 46, y + 19], fill=OURO)
    espacado(d, x + 64, y, texto.upper(), font(BOLD, 26), OURO)


def traco(d, x, y):
    d.rectangle([x, y, x + 120, y + 8], fill=OURO)


def rodape(d, n, total):
    f = font(MED, 22)
    espacado(d, 70, H - 88, "SANTA RUTE · ENGENHARIA RURAL", f, SOFT, 0.16)
    t = f"{n}/{total}"
    f2 = font(MED, 26)
    d.text((W - 70 - d.textlength(t, font=f2), H - 92), t, font=f2, fill=SOFT)
    if n < total:
        a = "arraste ›"
        d.text((W - 70 - d.textlength(t, font=f2) - 60 - d.textlength(a, font=f2), H - 92), a, font=f2, fill=OURO)


def numero(d, x, y, n):
    d.ellipse([x, y, x + 84, y + 84], fill=OURO)
    f = font(BOLD, 44)
    w = d.textlength(str(n), font=f)
    d.text((x + 42 - w / 2, y + 12), str(n), font=f, fill=BOT)


# ---------- slides ----------

def slide_capa(s, n, total):
    im = fundo(s); por_logo(im); d = ImageDraw.Draw(im)
    y0 = topo_capa(d, s, 92)
    selo(d, 70, y0, s["selo"])
    y = bloco(d, 70, y0 + 90, s["titulo"], font(BOLD, 92), BRANCO, 940, 1.12, s.get("destaque"))
    traco(d, 70, y + 36)
    if s.get("sub"):
        bloco(d, 70, y + 86, s["sub"], font(MED, 38), SOFT, 900, 1.35)
    rodape(d, n, total)
    return im


def slide_texto(s, n, total):
    im = fundo_verde(); por_logo(im); d = ImageDraw.Draw(im)
    h = 84 + 56 + altura(d, s["titulo"], font(BOLD, 68), 940, 1.15) + 50 + altura(d, s["texto"], font(REG, 41), 930, 1.42)
    if s.get("fonte"):
        h += 98
    y0 = max(280, 260 + (960 - h) // 2)
    numero(d, 70, y0, s["num"])
    y = bloco(d, 70, y0 + 140, s["titulo"], font(BOLD, 68), BRANCO, 940, 1.15, s.get("destaque"))
    y = bloco(d, 70, y + 50, s["texto"], font(REG, 41), SOFT, 930, 1.42)
    if s.get("fonte"):
        f = font(MED, 28)
        d.rounded_rectangle([70, y + 40, 70 + d.textlength(s["fonte"], font=f) + 40, y + 98], radius=12, outline=(120, 160, 128), width=2)
        d.text((90, y + 52), s["fonte"], font=f, fill=SOFT)
    rodape(d, n, total)
    return im


def slide_cta(s, n, total):
    """Fechamento em fundo creme, com a logo colorida e o convite para o WhatsApp."""
    im = Image.new("RGBA", (W, H), CREME + (255,)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=VERDE_MARCA)
    big = logo("cor", 250)
    im.alpha_composite(big, ((W - big.width) // 2, 150))
    d = ImageDraw.Draw(im)
    f = font(BOLD, 62)
    y = 500
    for ln in quebra(s["titulo"], f, 920, d):
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=VERDE_TXT); y += 76
    f2 = font(REG, 36)
    y += 22
    for ln in quebra(s["texto"], f2, 820, d):
        d.text(((W - d.textlength(ln, font=f2)) / 2, y), ln, font=f2, fill=(70, 86, 74)); y += 52
    fb = font(BOLD, 40)
    botao = s.get("botao", "Chame no WhatsApp")
    bw = d.textlength(botao, font=fb) + 110
    bx, by = (W - bw) / 2, y + 56
    d.rounded_rectangle([bx, by, bx + bw, by + 98], radius=49, fill=VERDE_MARCA)
    d.text((bx + 55, by + 23), botao, font=fb, fill=BRANCO)
    fs = font(MED, 34)
    contato = f"{WHATSAPP}  ·  {SITE}"
    d.text(((W - d.textlength(contato, font=fs)) / 2, by + 136), contato, font=fs, fill=MARROM)
    # assinatura, como no post "A história de Rute"
    fi = font(SERIF_IT, 40)
    d.rectangle([W / 2 - 40, H - 150, W / 2 + 40, H - 146], fill=OURO_LOGO)
    d.text(((W - d.textlength(ASSINATURA, font=fi)) / 2, H - 125), ASSINATURA, font=fi, fill=VERDE_TXT)
    return im


def slide_unico(s, n, total):
    """Imagem única: frase forte + assinatura com WhatsApp."""
    im = fundo(s); por_logo(im); d = ImageDraw.Draw(im)
    y0 = topo_capa(d, s, 88)
    if s.get("selo"):
        selo(d, 70, y0, s["selo"])
    y = bloco(d, 70, y0 + 90, s["titulo"], font(BOLD, 88), BRANCO, 940, 1.12, s.get("destaque"))
    traco(d, 70, y + 36)
    if s.get("sub"):
        bloco(d, 70, y + 86, s["sub"], font(MED, 38), SOFT, 900, 1.35)
    espacado(d, 70, H - 92, "SANTA RUTE · ENGENHARIA RURAL", font(MED, 22), SOFT, 0.16)
    f = font(BOLD, 28)
    t = f"WhatsApp {WHATSAPP}"
    d.text((W - 70 - d.textlength(t, font=f), H - 96), t, font=f, fill=OURO)
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
