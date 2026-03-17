import { useEffect, useState } from "react"
import { collection, getDocs, deleteDoc, doc } from "firebase/firestore"

import { db } from "../services/firebase"

import "../styles/urnas.css"

export default function Urnas(){

  const [urnas,setUrnas] = useState<any[]>([])
  const [loading,setLoading] = useState(true)

  const [urnaExcluir,setUrnaExcluir] = useState<any>(null)

  async function carregarUrnas(){

    const snapshot = await getDocs(collection(db,"urnas"))

    const lista:any[] = []

    snapshot.forEach((d)=>{

      lista.push({
        id:d.id,
        ...d.data()
      })

    })

    setUrnas(lista)

    setLoading(false)

  }

  useEffect(()=>{

    carregarUrnas()

  },[])

  async function removerUrna(){

    if(!urnaExcluir) return

    await deleteDoc(doc(db,"urnas",urnaExcluir.id))

    setUrnas(urnas.filter(u=>u.id !== urnaExcluir.id))

    setUrnaExcluir(null)

  }

  if(loading){

    return <p>Carregando urnas...</p>

  }

  return(

    <div className="urnas-page">

      <div className="urnas-header">

        <h1>Urnas</h1>

        <button
          className="btn-adicionar"
          onClick={()=>window.location.href="/nova-urna"}
        >
          + Nova Urna
        </button>

      </div>

      <div className="urnas-table">

        <table>

          <thead>

            <tr>

              <th>Imagem</th>
              <th>Nome</th>
              <th>Tipo</th>
              <th>Preço</th>
              <th>Ações</th>

            </tr>

          </thead>

          <tbody>

            {urnas.map((urna)=>(

              <tr key={urna.id}>

                <td>

                  {urna.imagens?.[0] && (

                    <img
                      src={urna.imagens[0]}
                      className="urna-thumb"
                    />

                  )}

                </td>

                <td>{urna.nome}</td>

                <td>{urna.tipo}</td>

                <td>

                  {Number(urna.preco).toLocaleString("pt-BR",{
                    style:"currency",
                    currency:"BRL"
                  })}

                </td>

                <td>

                  <div className="urna-acoes">

                    <button
                      className="btn-editar"
                      onClick={()=>window.location.href=`/editar-urna/${urna.id}`}
                    >
                      Editar
                    </button>

                    <button
                      className="btn-remover"
                      onClick={()=>setUrnaExcluir(urna)}
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

      {urnaExcluir && (

        <div className="modal-overlay">

          <div className="modal-confirm">

            <h2>Remover urna</h2>

            <p>
              Deseja realmente remover esta urna?
            </p>

            <div className="modal-actions">

              <button
                className="btn-cancelar"
                onClick={()=>setUrnaExcluir(null)}
              >
                Cancelar
              </button>

              <button
                className="btn-remover"
                onClick={removerUrna}
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