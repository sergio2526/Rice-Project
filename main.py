from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json
import cv2
import os

directorio_credencial = './config/credentials_module.json'

#Iniciar sesion Google Drive
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credencial)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credencial)
    else:
        gauth.Authorize()

    return GoogleDrive(gauth)


#Descargar imagenes de Google Drive
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


#Listar imagenes de la carpeta prueba
def listar_imagenes():
    
    im_dir = './images'

    #Formatos validos para leer las imagenes
    valid_formats = [".jpg", ".jpeg", ".jp2", ".png"]
    get_ext = lambda f: os.path.splitext(f)[1].lower()

    #Leer todas las imagenes del directorio
    im_files = [f for f in os.listdir(im_dir) if get_ext(f) in valid_formats]
    for im in im_files:
        #Enviando el path de las imagenes a la funcion recortar_imagenes
        recortar_imagenes(im_dir + '/' + im, im)


#recortar las imagenes
def recortar_imagenes(image_path, im):
    
    try:
        image = cv2.imread(image_path)

        imageOut = image[0:3000,500:3000]
        cv2.imwrite(f"./img_recortadas/1_{im}",imageOut)

        imageOut2 = image[0:8000,600:2000]
        cv2.imwrite(f"./img_recortadas/2_{im}",imageOut2)

        imageOut3 = image[50:5000,1500:3600]
        cv2.imwrite(f"./img_recortadas/3_{im}",imageOut3)

    except:
        pass


if __name__ == "__main__":

    #Metodo con su respectiva query
    #descargar_archivo("title contains 'IMG_202'","./images/")
    #Listar imagenes de la carpeta prueba
    listar_imagenes()

