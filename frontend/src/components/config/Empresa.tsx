import { useState, useEffect } from "react"

import { db } from "../../services/firebase"
import { doc, setDoc, getDoc } from "firebase/firestore"

export default function Empresa(){

  const [nome,setNome] = useState("")
  const [cnpj,setCnpj] = useState("")
  const [telefone,setTelefone] = useState("")
  const [endereco,setEndereco] = useState("")

  const [loading,setLoading] = useState(false)
  const [sucesso,setSucesso] = useState(false)

  // 🔹 MÁSCARA CNPJ
  function formatarCNPJ(valor:string){

    valor = valor.replace(/\D/g,"")

    valor = valor.replace(/^(\d{2})(\d)/,"$1.$2")
    valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3")
    valor = valor.replace(/\.(\d{3})(\d)/,".$1/$2")
    valor = valor.replace(/(\d{4})(\d)/,"$1-$2")

    return valor.substring(0,18)
  }

  // 🔹 MÁSCARA TELEFONE
  function formatarTelefone(valor:string){

    valor = valor.replace(/\D/g,"")

    valor = valor.replace(/^(\d{2})(\d)/g,"($1) $2")
    valor = valor.replace(/(\d{5})(\d)/,"$1-$2")

    return valor.substring(0,15)
  }

  async function carregarEmpresa(){

    const ref = doc(db,"config","empresa")

    const snap = await getDoc(ref)

    if(snap.exists()){

      const data:any = snap.data()

      setNome(data.nome || "")
      setCnpj(data.cnpj || "")
      setTelefone(data.telefone || "")
      setEndereco(data.endereco || "")

    }

  }

  async function salvarEmpresa(){

    try{

      setLoading(true)

      await setDoc(doc(db,"config","empresa"),{

        nome,
        cnpj,
        telefone,
        endereco

      })

      setSucesso(true)

    }catch(e){

      console.error(e)
      alert("Erro ao salvar dados")

    }finally{

      setLoading(false)

    }

  }

  useEffect(()=>{

    carregarEmpresa()

  },[])

  return(

    <div className="usuarios-card">

      <h2>Dados da empresa</h2>

      <div className="usuarios-grid">

        <div className="usuarios-field">
          <label>Nome da empresa</label>
          <input
            value={nome}
            onChange={(e)=>setNome(e.target.value)}
          />
        </div>

        <div className="usuarios-field">
          <label>CNPJ</label>
          <input
            value={cnpj}
            onChange={(e)=>setCnpj(formatarCNPJ(e.target.value))}
          />
        </div>

        <div className="usuarios-field">
          <label>Telefone</label>
          <input
            value={telefone}
            onChange={(e)=>setTelefone(formatarTelefone(e.target.value))}
          />
        </div>

        <div className="usuarios-field">
          <label>Endereço</label>
          <input
            value={endereco}
            onChange={(e)=>setEndereco(e.target.value)}
          />
        </div>

      </div>

      <button
        className="btn-criar"
        onClick={salvarEmpresa}
        disabled={loading}
      >
        {loading ? "Salvando..." : "Salvar dados"}
      </button>

      {sucesso && (

        <div className="modal-overlay">

          <div className="modal-sucesso">

            <h2>Dados salvos com sucesso</h2>

            <button onClick={()=>setSucesso(false)}>
              OK
            </button>

          </div>

        </div>

      )}

    </div>

  )

}