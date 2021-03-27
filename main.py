from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


directorio_credencial = './config/credentials_module.json'

#Iniciar sesion
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credencial)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credencial)
    else:
        gauth.Authorize()

    return GoogleDrive(gauth)


#Descargar archivo
def descargar_archivo(query,ruta_descarga):

    #Credenciales
    resultado = []
    credenciales = login()

    lista_archivos = credenciales.ListFile({'q': query}).GetList()

    #Ciclo que recorre nombre de fotos que cumplan con la query
    for f in lista_archivos:
        try:
            print('Nombre del archivo:',f['id'])
            print('Nombre del archivo:',f['title'])
            print('Fecha de creacion:',f['createdDate'])
            print('Fecha de creacion:',f['embedLink'])
            resultado.append(f)        

            #Descargar foto por su id
            
            archivo = credenciales.CreateFile({'id': f['id']}) 
            archivo.GetContentFile(ruta_descarga + f['title'])

        except:
            pass

    return resultado


if __name__ == "__main__":
    #Metodo con su respectiva query
    descargar_archivo("title contains 'rice'","./images/")

