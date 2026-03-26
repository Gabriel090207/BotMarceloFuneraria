import { useState } from "react"
import { FiUpload, FiX, FiCheck } from "react-icons/fi"
import { NumericFormat } from "react-number-format"

import "../styles/nova-urna.css"

import { addDoc, collection, updateDoc, doc } from "firebase/firestore"
import { db } from "../services/firebase"

import { uploadImagem } from "../services/uploadImagem"

export default function NovaUrna(){

  const [nome,setNome] = useState("")
  const [tipo,setTipo] = useState("")
  const [categoria,setCategoria] = useState("")
  const [preco,setPreco] = useState("")

  const [imagens,setImagens] = useState<File[]>([])

  const [loading,setLoading] = useState(false)
  const [sucesso,setSucesso] = useState(false)

  function adicionarImagem(e:React.ChangeEvent<HTMLInputElement>){

    const files = e.target.files

    if(!files) return

    const novas = [...imagens]

    for(let i=0;i<files.length;i++){

      if(novas.length >= 5){
        alert("Máximo de 5 imagens por urna")
        break
      }

      novas.push(files[i])

    }

    setImagens(novas)

  }

  function removerImagem(index:number){

    const novas = imagens.filter((_,i)=>i !== index)

    setImagens(novas)

  }

  async function salvarUrna(){


    if(!nome || !tipo || !categoria || !preco){
  alert("Preencha todos os campos")
  return
}

    if(loading) return

    setLoading(true)

    try{

      const docRef = await addDoc(collection(db,"urnas"),{

  nome,
  tipo,
  categoria, // 🔥 NOVO
  preco,
  ativo:true,
  criado_em: new Date()

})

      const urnaId = docRef.id

      const urls:string[] = []

      for(const img of imagens){

        const url = await uploadImagem(img, urnaId)

        urls.push(url)

      }

      await updateDoc(doc(db,"urnas",urnaId),{

        imagens: urls

      })

      setNome("")
      setTipo("")
      setCategoria("")
      setPreco("")
      setImagens([])

      setSucesso(true)

    }catch(e){

      console.error(e)

      alert("Erro ao salvar urna")

    }finally{

      setLoading(false)

    }

  }

  return(

    <div className="nova-urna-page">

      <h1>Nova Urna</h1>

      <div className="nova-urna-form">

        <div className="nova-urna-grid">

          <div className="nova-urna-field">

            <label>Nome da urna</label>

            <input
              value={nome}
              onChange={(e)=>setNome(e.target.value)}
            />

          </div>

          <div className="nova-urna-field">

            <label>Tipo</label>

            <select
              value={tipo}
              onChange={(e)=>setTipo(e.target.value)}
            >

              <option value="">Selecione</option>
              <option value="simples">Simples</option>
              <option value="intermediaria">Intermediária</option>
              <option value="premium">Premium</option>

            </select>

          </div>


          <div className="nova-urna-field">

  <label>Categoria</label>

  <select
    value={categoria}
    onChange={(e)=>setCategoria(e.target.value)}
  >

   <option value="" disabled>Selecione</option>
    <option value="sepultamento">Sepultamento</option>
    <option value="cremacao">Cremação</option>

  </select>

</div>

          <div className="nova-urna-field">

            <label>Preço</label>

            <NumericFormat
              value={preco}
              thousandSeparator="."
              decimalSeparator=","
              prefix="R$ "
              decimalScale={2}
              fixedDecimalScale
              onValueChange={(values)=>setPreco(values.value)}
              className="input-preco"
            />

          </div>

        </div>

        <div className="upload-area">

          <label className="upload-box">

            <input
              type="file"
              multiple
              hidden
              onChange={adicionarImagem}
            />

            <div className="upload-content">

              <FiUpload className="upload-icon"/>

              <p>Adicionar imagens da urna</p>

              <span>(máximo 5)</span>

            </div>

          </label>

        </div>

        {imagens.length > 0 && (

          <div className="preview-grid">

            {imagens.map((img,index)=>{

              const url = URL.createObjectURL(img)

              return(

                <div className="preview-item" key={index}>

                  <img src={url}/>

                  <button
                    className="remove-img"
                    onClick={()=>removerImagem(index)}
                  >

                    <FiX/>

                  </button>

                </div>

              )

            })}

          </div>

        )}

        <button
          className="btn-salvar"
          onClick={salvarUrna}
          disabled={loading}
        >

          {loading ? "Salvando..." : "Salvar urna"}

        </button>

      </div>

      {sucesso && (

        <div className="modal-overlay">

          <div className="modal-sucesso">

            <FiCheck className="modal-icon"/>

            <h2>Urna criada com sucesso</h2>

            <button onClick={()=>setSucesso(false)}>
              OK
            </button>

          </div>

        </div>

      )}

    </div>

  )

}