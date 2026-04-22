import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"

import { doc, getDoc, updateDoc } from "firebase/firestore"
import { db } from "../services/firebase"

import { uploadImagem, deletarImagem } from "../services/uploadImagem"

import { FiUpload, FiX, FiCheck } from "react-icons/fi"
import { NumericFormat } from "react-number-format"

import "../styles/nova-urna.css"

export default function EditarServico(){

  const { id } = useParams()

  const [loading,setLoading] = useState(true)
  const [salvando,setSalvando] = useState(false)
  const [sucesso,setSucesso] = useState(false)

  const [nome,setNome] = useState("")
  const [categoria,setCategoria] = useState("")
  const [preco,setPreco] = useState("")
  const [capacidade,setCapacidade] = useState("")
  const [suite,setSuite] = useState("")
  const [areaExterna,setAreaExterna] = useState("")
  const [descricao,setDescricao] = useState("")
  const [cobertura,setCobertura] = useState("completa")

  const [imagens,setImagens] = useState<string[]>([])
  const [novasImagens,setNovasImagens] = useState<File[]>([])

  async function carregarServico(){

    if(!id) return

    const ref = doc(db,"servicos",id)
    const snap = await getDoc(ref)

    if(!snap.exists()){
      alert("Serviço não encontrado")
      return
    }

    const data:any = snap.data()

    setNome(data.nome || "")
    setCategoria(data.categoria || "")
    setPreco(data.preco || "")
    setCapacidade(data.capacidade || "")
    setSuite(data.suite || "")
    setAreaExterna(data.area_externa || "")
    setDescricao(data.descricao || "")
    setCobertura(data.cobertura || "completa")
    setImagens(data.imagens || [])

    setLoading(false)
  }

  useEffect(()=>{
    carregarServico()
  },[])

  async function removerImagem(url:string){

    await deletarImagem(url)
    setImagens(imagens.filter(img => img !== url))
  }

  function removerNova(index:number){
    setNovasImagens(novasImagens.filter((_,i)=>i !== index))
  }

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

  async function salvar(){

    if(!nome || !categoria || !preco){
      alert("Preencha os campos obrigatórios")
      return
    }

    if(!id || salvando) return

    setSalvando(true)

    const urls = [...imagens]

    try{

      for(const img of novasImagens){
        const url = await uploadImagem(img,id)
        urls.push(url)
      }

      await updateDoc(doc(db,"servicos",id),{
        nome,
        categoria,
        preco,
        capacidade,
        suite,
        area_externa: areaExterna,
        descricao,
        cobertura,
        imagens: urls
      })

      setImagens(urls)
      setNovasImagens([])
      setSucesso(true)

    }catch(e){
      console.error(e)
      alert("Erro ao salvar alterações")
    }finally{
      setSalvando(false)
    }
  }

  if(loading){
    return <p>Carregando...</p>
  }

  return(

    <div className="nova-urna-page">

      <h1>Editar Serviço</h1>

      <div className="nova-urna-form">

        <div className="nova-urna-grid">

          <div className="nova-urna-field">
            <label>Nome</label>
            <input
              value={nome}
              onChange={(e)=>setNome(e.target.value)}
            />
          </div>

          <div className="nova-urna-field">
            <label>Categoria</label>
            <select
              value={categoria}
              onChange={(e)=>setCategoria(e.target.value)}
            >
              <option value="">Selecione</option>
              <option value="externo">Externo</option>
              <option value="standard">Standard</option>
              <option value="comfort">Comfort</option>
              <option value="premium">Premium</option>
            </select>
          </div>

        </div>

        <div className="nova-urna-grid">

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

          <div className="nova-urna-field">
            <label>Capacidade</label>
            <input
              value={capacidade}
              onChange={(e)=>setCapacidade(e.target.value)}
            />
          </div>

        </div>

        <div className="nova-urna-grid">

          <div className="nova-urna-field">
            <label>Suíte</label>
            <select
              value={suite}
              onChange={(e)=>setSuite(e.target.value)}
            >
              <option value="">Selecione</option>
              <option value="Sim">Sim</option>
              <option value="Não">Não</option>
            </select>
          </div>

          <div className="nova-urna-field">
            <label>Área externa</label>
            <input
              value={areaExterna}
              onChange={(e)=>setAreaExterna(e.target.value)}
            />
          </div>

        </div>

        <div className="nova-urna-field">
          <label>Descrição</label>
          <textarea
            rows={3}
            value={descricao}
            onChange={(e)=>setDescricao(e.target.value)}
          />
        </div>

        <div className="nova-urna-field">
          <label>Cobertura</label>
          <select
            value={cobertura}
            onChange={(e)=>setCobertura(e.target.value)}
          >
            <option value="completa">Completa</option>
            <option value="externo">Externo</option>
          </select>
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
              <p>Adicionar novas imagens</p>
              <span>(máximo 5)</span>
            </div>

          </label>

        </div>

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