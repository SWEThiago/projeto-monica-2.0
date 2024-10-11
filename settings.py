import os

# Caminho do arquivo de dados (onde o JSON está armazenado)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(BASE_DIR, 'dados.json')

# Configurações gerais da aplicação
class Config:
    DEBUG = True  # Define se o modo debug está ativado
    SECRET_KEY = os.getenv('SECRET_KEY', 'minha_chave_secreta')  # Chave secreta para a aplicação
    DATA_FILE = DATA_FILE_PATH  # Caminho para o arquivo de dados
    JSON_SORT_KEYS = False  # Não ordena automaticamente as chaves no JSON

# Carregar configurações dependendo do ambiente (desenvolvimento, produção)
class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False

# Função para escolher a configuração com base no ambiente
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    return DevelopmentConfig
