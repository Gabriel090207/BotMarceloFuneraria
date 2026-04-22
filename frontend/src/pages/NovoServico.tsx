import { useState } from "react"
import { FiUpload, FiX, FiCheck } from "react-icons/fi"
import { NumericFormat } from "react-number-format"

import { addDoc, collection, updateDoc, doc } from "firebase/firestore"
import { db } from "../services/firebase"

import { uploadImagem } from "../services/uploadImagem"

import "../styles/nova-urna.css"

export default function NovoServico(){

  const [nome,setNome] = useState("")
  const [categoria,setCategoria] = useState("")
  const [preco,setPreco] = useState("")
  const [capacidade,setCapacidade] = useState("")
  const [suite,setSuite] = useState("")
  const [areaExterna,setAreaExterna] = useState("")
  const [descricao,setDescricao] = useState("")
  const [cobertura,setCobertura] = useState("completa")

  const [imagens,setImagens] = useState<File[]>([])

  const [loading,setLoading] = useState(false)
  const [sucesso,setSucesso] = useState(false)

  function adicionarImagem(e:React.ChangeEvent<HTMLInputElement>){

    const files = e.target.files
    if(!files) return

    const novas = [...imagens]

    for(let i=0;i<files.length;i++){

      if(novas.length >= 5){
        alert("Máximo de 5 imagens")
        break
      }

      novas.push(files[i])
    }

    setImagens(novas)
  }

  function removerImagem(index:number){
    setImagens(imagens.filter((_,i)=>i !== index))
  }

  async function salvarServico(){

    if(!nome || !categoria || !preco){
      alert("Preencha os campos obrigatórios")
      return
    }

    if(loading) return

    setLoading(true)

    try{

      const docRef = await addDoc(collection(db,"servicos"),{
        nome,
        categoria,
        preco,
        capacidade,
        suite,
        area_externa: areaExterna,
        descricao,
        cobertura,
        ativo:true,
        criado_em:new Date()
      })

      const servicoId = docRef.id

      const urls:string[] = []

      for(const img of imagens){
        const url = await uploadImagem(img, servicoId)
        urls.push(url)
      }

      await updateDoc(doc(db,"servicos",servicoId),{
        imagens: urls
      })

      setNome("")
      setCategoria("")
      setPreco("")
      setCapacidade("")
      setSuite("")
      setAreaExterna("")
      setDescricao("")
      setCobertura("completa")
      setImagens([])

      setSucesso(true)

    }catch(e){
      console.error(e)
      alert("Erro ao salvar serviço")
    }finally{
      setLoading(false)
    }
  }

  return(

    <div className="nova-urna-page">

      <h1>Novo Serviço Funerário</h1>

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
              placeholder="Ex: 60 pessoas"
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
              placeholder="Ex: Área externa"
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
              <p>Adicionar imagens</p>
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
          onClick={salvarServico}
          disabled={loading}
        >
          {loading ? "Salvando..." : "Salvar serviço"}
        </button>

      </div>

      {sucesso && (

        <div className="modal-overlay">

          <div className="modal-sucesso">

            <FiCheck className="modal-icon"/>

            <h2>Serviço criado com sucesso</h2>

            <button onClick={()=>setSucesso(false)}>
              OK
            </button>

          </div>

        </div>

      )}

    </div>

  )

}