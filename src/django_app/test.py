from django_app.config import ConfigService

# Criação da instância da classe ConfigService
config = ConfigService()

# Acessando a propriedade DATABASE_CONFIG
print(config.DATABASE_CONFIG)
