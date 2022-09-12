from assets.parser import Parser
import config

parser = Parser(config.url)
parser.parse_articles()
parser.build()