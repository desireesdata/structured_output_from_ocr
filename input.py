def get_text_from_file(file: str, test: bool)->str:
    try:
        txt = open(file, 'r')
        print("Fichier lu : ", txt, "\n")
        content = txt.read()
        if test:
            print(content)
        else :
            print("\n")
        return content
    except IOError as e:
        print("Oops y a une couille dans le fichier", txt)
        return ""
 