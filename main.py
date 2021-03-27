from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json

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
    resultado = {}
    resultado = []
    credenciales = login()

    lista_archivos = credenciales.ListFile({'q': query}).GetList()

    #Ciclo que recorre nombre de fotos que cumplan con la query
    for f in lista_archivos:
        try:
            print('Id',f['id'])
            print('title',f['title'])
            resultado.append(f)        

            #Descargar foto por su id
            
            archivo = credenciales.CreateFile({'id': f['id']}) 
            archivo.GetContentFile(ruta_descarga + f['title'])

        except:
            pass

    #Exportando archivo json con información de las fotos
    with open('./data/data.json', 'w') as file:
        json.dump(resultado, file, indent=4)


    return resultado


if __name__ == "__main__":
    #Metodo con su respectiva query
    descargar_archivo("title contains 'IMG_202'","./images/")

