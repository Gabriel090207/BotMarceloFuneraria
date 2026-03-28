import { useEffect, useState } from "react"
import { collection, getDocs, deleteDoc, doc } from "firebase/firestore"

import { db } from "../services/firebase"

import "../styles/urnas.css"

export default function Pacotes(){

  const [pacotes,setPacotes] = useState<any[]>([])
  const [loading,setLoading] = useState(true)

  const [pacoteExcluir,setPacoteExcluir] = useState<any>(null)

  async function carregarPacotes(){

    const snapshot = await getDocs(collection(db,"pacotes"))

    const lista:any[] = []

    snapshot.forEach((d)=>{
      lista.push({
        id:d.id,
        ...d.data()
      })
    })

    setPacotes(lista)
    setLoading(false)

  }

  useEffect(()=>{
    carregarPacotes()
  },[])

  async function removerPacote(){

    if(!pacoteExcluir) return

    await deleteDoc(doc(db,"pacotes",pacoteExcluir.id))

    setPacotes(pacotes.filter(p=>p.id !== pacoteExcluir.id))

    setPacoteExcluir(null)

  }

  if(loading){
    return <p>Carregando pacotes...</p>
  }

  return(

    <div className="urnas-page">

      <div className="urnas-header">

        <h1>Pacotes</h1>

        <button
          className="btn-adicionar"
          onClick={()=>window.location.href="/novo-pacote"}
        >
          + Novo Pacote
        </button>

      </div>

      <div className="urnas-table">

        <table>

          <thead>

            <tr>
              <th>Imagem</th>
              <th>Nome</th>
              <th>Preço</th>
              <th>Ações</th>
            </tr>

          </thead>

          <tbody>

            {pacotes.map((pacote)=>(

              <tr key={pacote.id}>

                <td>
                  {pacote.imagens?.[0] && (
                    <img
                      src={pacote.imagens[0]}
                      className="urna-thumb"
                    />
                  )}
                </td>

                <td>{pacote.nome}</td>

                <td>
                  {Number(pacote.preco).toLocaleString("pt-BR",{
                    style:"currency",
                    currency:"BRL"
                  })}
                </td>

                <td>

                  <div className="urna-acoes">

                    <button
                      className="btn-editar"
                      onClick={()=>window.location.href=`/editar-pacote/${pacote.id}`}
                    >
                      Editar
                    </button>

                    <button
                      className="btn-remover"
                      onClick={()=>setPacoteExcluir(pacote)}
                    >
                      Remover
                    </button>

                  </div>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

      {pacoteExcluir && (

        <div className="modal-overlay">

          <div className="modal-confirm">

            <h2>Remover pacote</h2>

            <p>
              Deseja realmente remover este pacote?
            </p>

            <div className="modal-actions">

              <button
                className="btn-cancelar"
                onClick={()=>setPacoteExcluir(null)}
              >
                Cancelar
              </button>

              <button
                className="btn-remover"
                onClick={removerPacote}
              >
                Remover
              </button>

            </div>

          </div>

        </div>

      )}

    </div>

  )

}