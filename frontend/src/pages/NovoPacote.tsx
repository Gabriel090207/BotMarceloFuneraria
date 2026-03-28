import { useState } from "react"
import { FiUpload, FiX, FiCheck } from "react-icons/fi"
import { NumericFormat } from "react-number-format"

import "../styles/nova-urna.css"

import { addDoc, collection, updateDoc, doc } from "firebase/firestore"
import { db } from "../services/firebase"

import { uploadImagem } from "../services/uploadImagem"

export default function NovoPacote(){

  const [nome,setNome] = useState("")
  const [preco,setPreco] = useState("")
  const [descricao,setDescricao] = useState("")

  const [imagens,setImagens] = useState<File[]>([])

  const [loading,setLoading] = useState(false)
  const [sucesso,setSucesso] = useState(false)

  function adicionarImagem(e:React.ChangeEvent<HTMLInputElement>){

    const files = e.target.files
    if(!files) return

    const novas = [...imagens]

    for(let i=0;i<files.length;i++){

      if(novas.length >= 5){
        alert("Máximo de 5 imagens por pacote")
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

  async function salvarPacote(){

    if(!nome || !preco || !descricao){
      alert("Preencha todos os campos")
      return
    }

    if(loading) return

    setLoading(true)

    try{

      const docRef = await addDoc(collection(db,"pacotes"),{
        nome,
        preco,
        descricao,
        ativo:true,
        criado_em: new Date()
      })

      const pacoteId = docRef.id

      const urls:string[] = []

      for(const img of imagens){
        const url = await uploadImagem(img, pacoteId)
        urls.push(url)
      }

      await updateDoc(doc(db,"pacotes",pacoteId),{
        imagens: urls
      })

      setNome("")
      setPreco("")
      setDescricao("")
      setImagens([])

      setSucesso(true)

    }catch(e){
      console.error(e)
      alert("Erro ao salvar pacote")
    }finally{
      setLoading(false)
    }
  }

  return(

    <div className="nova-urna-page">

      <h1>Novo Pacote</h1>

      <div className="nova-urna-form">

        <div className="nova-urna-grid">

          <div className="nova-urna-field">
            <label>Nome do pacote</label>
            <input
              value={nome}
              onChange={(e)=>setNome(e.target.value)}
            />
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

        {/* 🔥 NOVO CAMPO */}
        <div className="nova-urna-field">
          <label>Descrição do pacote</label>
          <textarea
            value={descricao}
            onChange={(e)=>setDescricao(e.target.value)}
            rows={4}
          />
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
              <p>Adicionar imagens do pacote</p>
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
          onClick={salvarPacote}
          disabled={loading}
        >
          {loading ? "Salvando..." : "Salvar pacote"}
        </button>

      </div>

      {sucesso && (

        <div className="modal-overlay">

          <div className="modal-sucesso">

            <FiCheck className="modal-icon"/>

            <h2>Pacote criado com sucesso</h2>

            <button onClick={()=>setSucesso(false)}>
              OK
            </button>

          </div>

        </div>

      )}

    </div>

  )

}