from linkstatept2 import LinkStateRouting

if __name__ == "__main__":
    jid = input("Introduce tu JID: ")
    password = input("Introduce tu contraseña: ")

    routing = LinkStateRouting(jid, password, 'topo-default.txt', 'names-default.txt')
    routing.connect()
    routing.process(forever=False)
