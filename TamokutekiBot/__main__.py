from TamokutekiBot import Tamokuteki

if __name__ == "__main__":
    try:
        Tamokuteki.start()
        Tamokuteki.run_until_disconnected()
    except KeyboardInterrupt:
        pass
