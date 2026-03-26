import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

import { doc, getDoc, updateDoc } from "firebase/firestore"

import { db } from "../services/firebase"

import { uploadImagem, deletarImagem } from "../services/uploadImagem"

import { FiUpload, FiX, FiCheck } from "react-icons/fi"

import { NumericFormat } from "react-number-format"

import "../styles/nova-urna.css"

export default function EditarUrna(){

  const {id} = useParams()

  const [loading,setLoading] = useState(true)
  const [salvando,setSalvando] = useState(false)
  const [sucesso,setSucesso] = useState(false)

  const [nome,setNome] = useState("")
  const [tipo,setTipo] = useState("")
  const [categoria,setCategoria] = useState("")
  const [preco,setPreco] = useState("")

  const [imagens,setImagens] = useState<string[]>([])
  const [novasImagens,setNovasImagens] = useState<File[]>([])

  async function carregarUrna(){

    if(!id) return

    const ref = doc(db,"urnas",id)

    const snap = await getDoc(ref)

    const data:any = snap.data()

    setNome(data.nome)
    setTipo(data.tipo)
    setCategoria(data.categoria || "")
    setPreco(data.preco)

    setImagens(data.imagens || [])

    setLoading(false)

  }

  useEffect(()=>{

    carregarUrna()

  },[])

  /* REMOVER IMAGEM */

  async function removerImagem(url:string){

    await deletarImagem(url)

    setImagens(imagens.filter(img => img !== url))

  }

  function removerNova(index:number){

    setNovasImagens(novasImagens.filter((_,i)=>i !== index))

  }

  /* ADICIONAR IMAGEM */

  function adicionarImagem(e:React.ChangeEvent<HTMLInputElement>){

    const files = e.target.files

    if(!files) return

    const novas = [...novasImagens]

    for(let i=0;i<files.length;i++){

      if(novas.length + imagens.length >= 5){
        alert("Máximo de 5 imagens")
        break
      }

      novas.push(files[i])

    }

    setNovasImagens(novas)

  }

  /* SALVAR */

  async function salvar(){

    if(!id) return

    if(salvando) return

    setSalvando(true)

    const urls = [...imagens]

    try{

      for(const img of novasImagens){

        const url = await uploadImagem(img,id)

        urls.push(url)

      }

      await updateDoc(doc(db,"urnas",id),{

        nome,
        tipo,
        categoria,
        preco,
        imagens: urls

      })

      setImagens(urls)

      setNovasImagens([])

      setSucesso(true)

    }catch(e){

      console.error(e)

      alert("Erro ao salvar")

    }finally{

      setSalvando(false)

    }

  }

  if(loading){

    return <p>Carregando...</p>

  }

  return(

    <div className="nova-urna-page">

      <h1>Editar Urna</h1>

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

        {/* UPLOAD */}

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

              <p>Adicionar novas imagens</p>

              <span>(máximo 5)</span>

            </div>

          </label>

        </div>

        {/* IMAGENS */}

        <div className="preview-grid">

          {imagens.map((img)=>(
              
            <div className="preview-item" key={img}>

              <img src={img}/>

              <button
                className="remove-img"
                onClick={()=>removerImagem(img)}
              >

                <FiX/>

              </button>

            </div>

          ))}

          {novasImagens.map((img,index)=>{

            const url = URL.createObjectURL(img)

            return(

              <div className="preview-item" key={index}>

                <img src={url}/>

                <button
                  className="remove-img"
                  onClick={()=>removerNova(index)}
                >

                  <FiX/>

                </button>

              </div>

            )

          })}

        </div>

        <button
          className="btn-salvar"
          onClick={salvar}
          disabled={salvando}
        >

          {salvando ? "Salvando..." : "Salvar alterações"}

        </button>

      </div>

      {sucesso && (

        <div className="modal-overlay">

          <div className="modal-sucesso">

            <FiCheck className="modal-icon"/>

            <h2>Alterações salvas</h2>

            <button onClick={()=>setSucesso(false)}>
              OK
            </button>

          </div>

        </div>

      )}

    </div>

  )

}