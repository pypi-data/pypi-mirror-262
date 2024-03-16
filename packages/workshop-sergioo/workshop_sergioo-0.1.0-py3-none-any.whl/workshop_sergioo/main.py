# Lista de palavras e seus sinônimos
PALAVRAS_E_SINONIMOS = {
    "casa": ["lar", "residência", "moradia"],
    "carro": ["automóvel", "veículo", "caranga"],
    "jardim": ["parque", "horto", "jardim botânico"],
    "livro": ["obra", "volume", "escrito"],
    "computador": ["máquina", "PC", "sistema"],
    "pessoa": ["indivíduo", "ser humano", "criatura"],
    "tempo": ["período", "duração", "momento"],
    "água": ["líquido", "hidratação", "elemento"],
    "sol": ["estrela", "astro", "brilho"],
    "lua": ["satélite", "natural", "orbita"],
    "amigo": ["companheiro", "parceiro", "aliado"],
    "felicidade": ["alegria", "contentamento", "satisfação"],
    "tristeza": ["melancolia", "desânimo", "dor"],
    "energia": ["força", "vigor", "poder"],
    "caminho": ["rota", "trajeto", "percurso"],
    "fogo": ["chama", "incêndio", "queima"],
    "ar": ["atmosfera", "respiração", "vento"],
    "terra": ["planeta", "mundo", "globo"],
    "mar": ["oceano", "litoral", "água salgada"],
    "cidade": ["município", "metrópole", "urbanização"],
    "escola": ["instituição", "educação", "aprendizado"],
    "dinheiro": ["capital", "riqueza", "moeda"],
    "coração": ["órgão", "sentimento", "emoção"],
    "bola": ["esfera", "redonda", "pelota"],
    "chuva": ["precipitação", "águas", "tempestade"],
    "música": ["melodia", "som", "canção"],
    "sapato": ["calçado", "tênis", "sapatilha"],
    "praia": ["costa", "orla", "areia"],
    "brinquedo": ["joguete", "boneco", "diversão"],
}

# Função para buscar sinônimo
def buscar_sinonimo(palavra_buscada):
    if palavra_buscada in PALAVRAS_E_SINONIMOS:
        sinonimos = PALAVRAS_E_SINONIMOS[palavra_buscada]
        return sinonimos  
    else:
        return "Palavra fora do escopo da pesquisa."


