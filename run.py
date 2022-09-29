from assets import Parser
link = input("Enter domain to publish post: ")
pir = Parser(link, 'in.csv')
pir.open_file()
