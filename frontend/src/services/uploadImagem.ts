import { getStorage, ref, uploadBytes, getDownloadURL, deleteObject } from "firebase/storage"

const storage = getStorage()

/* UPLOAD IMAGEM */

export async function uploadImagem(file:File, urnaId:string){

  const nome = crypto.randomUUID()

  const caminho = `urnas/${urnaId}/${nome}`

  const storageRef = ref(storage, caminho)

  await uploadBytes(storageRef, file)

  const url = await getDownloadURL(storageRef)

  return url

}

/* DELETAR IMAGEM */

export async function deletarImagem(url:string){

  try{

    const caminho = decodeURIComponent(
      url.split("/o/")[1].split("?")[0]
    )

    const fileRef = ref(storage, caminho)

    await deleteObject(fileRef)

  }catch(e){

    console.error("Erro ao deletar imagem", e)

  }

}