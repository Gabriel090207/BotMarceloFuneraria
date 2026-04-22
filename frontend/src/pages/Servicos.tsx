import { useEffect, useState } from "react"
import { collection, getDocs, deleteDoc, doc } from "firebase/firestore"
import { db } from "../services/firebase"

import "../styles/urnas.css"

export default function Servicos(){

  const [servicos,setServicos] = useState<any[]>([])
  const [loading,setLoading] = useState(true)

  const [servicoExcluir,setServicoExcluir] = useState<any>(null)

  async function carregarServicos(){

    const snapshot = await getDocs(collection(db,"servicos"))

    const lista:any[] = []

    snapshot.forEach((d)=>{
      lista.push({
        id:d.id,
        ...d.data()
      })
    })

    setServicos(lista)
    setLoading(false)
  }

  useEffect(()=>{
    carregarServicos()
  },[])

  async function removerServico(){

    if(!servicoExcluir) return

    await deleteDoc(doc(db,"servicos",servicoExcluir.id))

    setServicos(servicos.filter(s => s.id !== servicoExcluir.id))
    setServicoExcluir(null)
  }

  if(loading){
    return <p>Carregando serviços...</p>
  }

  return(

    <div className="urnas-page">

      <div className="urnas-header">

        <h1>Serviços Funerários</h1>

        <button
          className="btn-adicionar"
          onClick={()=>window.location.href="/novo-servico"}
        >
          + Novo Serviço
        </button>

      </div>

      <div className="urnas-table">

        <table>

          <thead>
            <tr>
              <th>Imagem</th>
              <th>Nome</th>
              <th>Categoria</th>
              <th>Preço</th>
              <th>Ações</th>
            </tr>
          </thead>

          <tbody>

            {servicos.map((servico)=>(

              <tr key={servico.id}>

                <td>
                  {servico.imagens?.[0] && (
                    <img
                      src={servico.imagens[0]}
                      className="urna-thumb"
                    />
                  )}
                </td>

                <td>{servico.nome}</td>

                <td style={{textTransform:"capitalize"}}>
                  {servico.categoria}
                </td>

                <td>
                  {Number(servico.preco).toLocaleString("pt-BR",{
                    style:"currency",
                    currency:"BRL"
                  })}
                </td>

                <td>

                  <div className="urna-acoes">

                    <button
                      className="btn-editar"
                      onClick={()=>window.location.href=`/editar-servico/${servico.id}`}
                    >
                      Editar
                    </button>

                    <button
                      className="btn-remover"
                      onClick={()=>setServicoExcluir(servico)}
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

      {servicoExcluir && (

        <div className="modal-overlay">

          <div className="modal-confirm">

            <h2>Remover serviço</h2>

            <p>Deseja realmente remover este serviço?</p>

            <div className="modal-actions">

              <button
                className="btn-cancelar"
                onClick={()=>setServicoExcluir(null)}
              >
                Cancelar
              </button>

              <button
                className="btn-remover"
                onClick={removerServico}
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